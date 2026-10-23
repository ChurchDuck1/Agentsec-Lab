import pytest
from agentsec.tools.doccuments import read_doccument, DoccumentAccessError
from pathlib import Path

@pytest.mark.parametrize("doc_id", ["welcome","notes"])
def test_allowed_ids(doc_id):
    assert read_doccument(doc_id, user="alice").strip()
    
@pytest.mark.parametrize("doc_id", [
    "../.env", "../../.env", "/etc/passwd", "welcome/../../.env",
    "..", "", "WELCOME", "welcome.txt", "does_not_exist", "a" * 100,
])

def test_denied_ids(doc_id):
    with pytest.raises(DoccumentAccessError):
        read_doccument(doc_id, user="alice")

def _error_for(doc_id, user):
    with pytest.raises(DoccumentAccessError) as exc:
        read_doccument(doc_id, user=user)
    return str(exc.value).replace(repr(doc_id), "<id>")

def test_denied_and_missing_look_identical():
    denied = _error_for("alice_notes", "bob")       #exists, not allowed
    missing = _error_for("no_such_doc", "bob")      #doesn't exist
    assert denied == missing
    
def test_denied_read_never_touches_file(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("file was read for a denied user")
    monkeypatch.setattr(Path, "read_text", boom)

    with pytest.raises(DoccumentAccessError):
        read_doccument("alice_notes", user="bob")