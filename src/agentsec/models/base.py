from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Message:
    role: str   #User or Assistant
    content: str
    
@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    tool_call: dict | None = None
    
class ModelAdapter(Protocol):
        def complete(self, messages: list[Message], system: str = "") -> ModelResponse: ...