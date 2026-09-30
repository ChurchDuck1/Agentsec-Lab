from agentsec.models.base import Message, ModelResponse

class FakeModelAdapter:
    #deterministic fake llm

    def __init__(self, rules: dict[str, str] | None = None, default: str = "OK"):
        self.rules = rules or {}   #substring in last user msg -> canned reply
        self.default = default
        self.calls: list[list[Message]] = []   #record what was sent

    def complete(self, messages: list[Message], system: str = "") -> ModelResponse:
        self.calls.append(list(messages))
        last = messages[-1].content if messages else ""
        for trigger, reply in self.rules.items():
            if trigger in last:
                return ModelResponse(text=reply, model="fake")
        return ModelResponse(text=self.default, model="fake")