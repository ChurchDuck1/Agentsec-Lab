import os
from agentsec.models.base import ModelAdapter, Message, ModelResponse
from agentsec.models.fake import FakeModelAdapter

def get_model() -> ModelAdapter:
    backend = os.environ.get("AGENTSEC_BACKEND", "fake")
    if backend == "fake":
        return FakeModelAdapter()
    if backend == "anthropic":
        from agentsec.models.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter()
    raise ValueError(f"Unknown backend: {backend}")