import pytest
from agentsec.tools.doccuments import read_doccument, DoccumentAccessError

@pytest.mark.parametrize("user, doc_id, allowed", [
    ("alice", "welcome", True),  ("bob", "welcome", True),
    ("alice", "alice_notes", True), ("alice", "bob_notes", False),
    ("bob", "bob_notes", True),  ("bob", "alice_notes", False),
    ("mallory", "welcome", False),
])
def test_acl(user, doc_id, allowed):
    if allowed:
        assert read_doccument(doc_id, user=user)
    else:
        with pytest.raises(DoccumentAccessError):
            read_doccument(doc_id, user=user)