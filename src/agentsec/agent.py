import json
from agentsec.audit import AuditLog
from agentsec.models.base import Message, ModelAdapter
from agentsec.tools.doccuments import read_doccument, search_doccuments, DoccumentAccessError

def run_agent(model: ModelAdapter, user_msg: str, audit: AuditLog, user: str, max_steps: int = 5):
    tools = {
        "search_documents": lambda query: search_doccuments(query, user=user),
        "read_document": lambda doc_id: read_doccument(doc_id, user=user),
    }
    audit.record("session_start", user=user)
    messages = [Message("user", user_msg)]
    audit.record("user_message", content=user_msg)

    for step in range(max_steps):
        resp = model.complete(messages)
        audit.record("model_response", step=step, text=resp.text, tool_call=resp.tool_call)

        if resp.tool_call is None:
            return resp.text   

        name, args = resp.tool_call["name"], resp.tool_call.get("args", {})
        if name not in tools:
            result = "error: unknown tool"
            audit.record("tool_denied", tool=name, reason="unknown tool")
        else:
            try:
                result = tools[name](**args)
                audit.record("tool_call", tool=name, args=args, ok=True)
            except (DoccumentAccessError, TypeError) as e:
                result = f"error: {e}"
                audit.record("tool_call", tool=name, args=args, ok=False, error=str(e))

        messages.append(Message("assistant", f"[called {name}]"))
        messages.append(Message("user", f"tool result: {json.dumps(result)}"))

    audit.record("max_steps_reached")
    return None