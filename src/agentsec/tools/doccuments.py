import re
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "docs" #4 files back, and then into fixtures/docs
_ID_PATTERN = re.compile(r"^[a-z0-9_-]{1,64}$") #prevents .. and / attacks

class DoccumentAccessError(Exception):
    pass

def read_doccument(doc_id: str, base_dir: Path = DOCS_DIR) -> str:
    if not isinstance(doc_id, str) or not _ID_PATTERN.fullmatch(doc_id):
        raise DoccumentAccessError(f"invalid id")
    
    base = base_dir.resolve()
    path = (base / f"{doc_id}.txt").resolve()
    
    if not path.is_relative_to(base):
        raise DoccumentAccessError(f"path is outside of doccument directory") #prevents ..
    if not path.is_file():
        raise DoccumentAccessError(f"file not found")
    
    return path.read_text(encoding="utf-8") #all checks pass