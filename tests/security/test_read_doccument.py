import pytest
from agentsec.tools.doccuments import read_doccument, DoccumentAccessError

@pytest.mark.parametrize("doc_id", ["welcome","notes"])
def test_allowed_ids(doc_id):
    assert read_doccument(doc_id).strip()
    
@pytest.mark.parametrize("doc_id", [
    "../.env", "../../.env", "/etc/passwd", "welcome/../../.env",
    "..", "", "WELCOME", "welcome.txt", "does_not_exist", "a" * 100,
])

def test_denied_ids(doc_id):
    with pytest.raises(DoccumentAccessError):
        read_doccument(doc_id)