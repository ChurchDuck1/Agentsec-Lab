import os
import pytest
from agentsec.models import FakeModelAdapter, Message

def test_fake_is_deterministic():
    m = FakeModelAdapter(rules={"weather": "Sunny"})
    msgs = [Message("user", "what's the weather?")]
    assert m.complete(msgs).text == m.complete(msgs).text == "Sunny"

def test_fake_records_calls():
    m = FakeModelAdapter()
    m.complete([Message("user", "hi")])
    assert m.calls[0][0].content == "hi"

@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no API key")
def test_real_anthropic_smoke():
    from agentsec.models.anthropic_adapter import AnthropicAdapter
    r = AnthropicAdapter().complete([Message("user", "Reply with the word pong.")])
    assert "pong" in r.text.lower()