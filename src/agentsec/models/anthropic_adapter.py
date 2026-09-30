import os
from agentsec.models.base import Message, ModelResponse

class AnthropicAdapter:
    def __init__(self, model: str | None = None):
        import anthropic 
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self.client = anthropic.Anthropic()  #reads the key from the environment
        self.model = model or os.environ.get("AGENTSEC_MODEL_NAME", "claude-haiku-4-5-20251001")

    def complete(self, messages: list[Message], system: str = "") -> ModelResponse:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": m.role, "content": m.content}for m in messages],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return ModelResponse(text=text, model=self.model)