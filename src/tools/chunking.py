from typing import List
import tiktoken

def token_len(s: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(s))

def chunk_text(text: str, max_tokens: int = 2800) -> List[str]:
    """Split by paragraphs while preserving [Page N] tags."""
    paras = text.split("\n\n")
    chunks, cur, cur_tokens = [], [], 0
    for p in paras:
        t = token_len(p)
        if cur and cur_tokens + t > max_tokens:
            chunks.append("\n\n".join(cur))
            cur, cur_tokens = [p], t
        else:
            cur.append(p); cur_tokens += t
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks