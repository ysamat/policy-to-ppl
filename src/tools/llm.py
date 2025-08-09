import os
from openai import OpenAI

_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def chat(system: str, user: str, temperature: float = 0.3) -> str:
    resp = _client.chat.completions.create(
        model=_MODEL,
        temperature=temperature,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
    )
    return resp.choices[0].message.content.strip()