from agentsec.agent import run_agent
from agentsec.audit import AuditLog
from agentsec.models.base import ModelResponse
from agentsec.models.fake import ScriptedModelAdapter

def test_three_step_conversation(tmp_path):
    script = [
        ModelResponse("", "fake", {"name": "search_documents", "args": {"query": "q3"}}),
        ModelResponse("", "fake", {"name": "read_document", "args": {"doc_id": "notes"}}),
        ModelResponse("The Q3 notes say nothing secret.", "fake"),
    ]
    audit = AuditLog(tmp_path / "audit.jsonl", clock=lambda: 0.0)

    answer = run_agent(ScriptedModelAdapter(script), "What do the Q3 notes say?", audit, user="alice")

    assert answer == "The Q3 notes say nothing secret."
    events = audit.read_all()
    assert [e["event"] for e in events] == [
        "session_start",
        "user_message",
        "model_response", "tool_call",
        "model_response", "tool_call",
        "model_response",
    ]
    assert all(e.get("ok", True) for e in events)