import re
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "docs" #4 files back, and then into fixtures/docs
_ID_PATTERN = re.compile(r"^[a-z0-9_-]{1,64}$") #prevents .. and / attacks
ACL: dict[str, set[str]] = {
    "welcome": {"alice", "bob"},
    "notes": {"alice", "bob"},
    "alice_notes": {"alice"},
    "bob_notes": {"bob"},
}

class DoccumentAccessError(Exception):
    pass

def read_doccument(doc_id: str, user: str, base_dir: Path = DOCS_DIR,
                  acl: dict[str, set[str]] = ACL) -> str:
    if not isinstance(doc_id, str) or not _ID_PATTERN.fullmatch(doc_id):
        raise DoccumentAccessError(f"invalid doccument id: {doc_id!r}")
    # if user not in acl.get(doc_id, set()):
    #    raise DoccumentAccessError(f"no such doccument: {doc_id!r}")
    #    introduce a bug to allow users improper access
    base = base_dir.resolve()
    path = (base / f"{doc_id}.txt").resolve()
    
    if not path.is_relative_to(base):
        raise DoccumentAccessError(f"path is outside of doccument directory") #prevents ..
    if not path.is_file():
        raise DoccumentAccessError(f"file not found")
    
    return path.read_text(encoding="utf-8") #all checks pass

def search_doccuments(query: str, user: str, base_dir: Path = DOCS_DIR, limit: int = 5) -> list[dict]:
    if not isinstance(query, str) or not (1 <= len(query) <= 200):
        raise DoccumentAccessError("invalid query")
    q = query.lower()
    hits = []
    for path in sorted(base_dir.resolve().glob("*.txt")):
        doc_id = path.stem
        try:
            text = read_doccument(doc_id, base_dir)  #perform same checks as read_doccument
        except DoccumentAccessError:
            continue   #skip if fails checks
        if q in text.lower() or q in doc_id:
            hits.append({"id": doc_id, "snippet": text[:80]})
        if len(hits) >= limit:
            break
    return hits