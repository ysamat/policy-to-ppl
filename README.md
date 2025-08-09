# 📜 Policy-to-People Translator

**Goal:** Convert dense, technical policy PDFs (bills/regulations) into audience-tiered explanations and a persona-tailored "What this means for you" section.

**Why:** Most people see policy as noise. This tool demonstrates a principled approach to context-aware simplification using generative AI — faithful to source, audience-specific, and transparent about uncertainty.

## ✨ Features

- **PDF ingestion** → Extract text (with page tags like [Page 3])
- **Chunking** → Token-aware splitting to keep the LLM grounded and within limits
- **Tiered explanations** → "High schooler", "Small business owner", "Economist"
- **Synthesis** → Merge per-slice outputs into a cohesive, de-duplicated brief with Caveats
- **Persona impact** → "What this means for you" generated from the synthesized brief
- **Guardrails** → No invention beyond the uploaded text; page-tag citations; explicit "Not specified" when needed
- **Modular architecture** → Clear separation: tools / models / agents / app

## 🏗️ Project Structure

```
policy-to-people/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ main.py
└─ src/
   ├─ tools/
   │  ├─ __init__.py
   │  ├─ pdf_utils.py
   │  ├─ chunking.py
   │  ├─ llm.py
   │  └─ prompts.py
   ├─ models/
   │  ├─ __init__.py
   │  └─ persona.py
   └─ agents/
      ├─ __init__.py
      └─ translator.py
```

## ⚙️ Setup

### 1. Python environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## ▶️ Run

```bash
streamlit run main.py
```

1. Upload a policy/bill/regulation PDF with a text layer
2. Click "Generate tiered explanations" → "Synthesize" → "Generate 'What this means for you'"
3. Optionally create a custom persona

## 🧠 Approach

1. **Problem framing:** Policies are complex; audiences vary → produce tiered outputs
2. **Constraints-first:** Chunking & page tags preserve provenance
3. **Separation of concerns:** Tools, agents, and models are modular
4. **Grounding:** Prompts enforce "no new facts" and page citations
5. **Human-centered:** Personas align summaries with user realities

## 🔧 Configuration

- **Chunk size:** Adjust in UI (default ~2800 tokens)
- **Model:** Change `OPENAI_MODEL` in `.env` or `llm.py`
- **Personas:** Modify in `persona.py`

## 🧪 Testing ideas

- Unit tests for PDF parsing, chunking, and prompt outputs
- Smoke tests with small PDFs to validate end-to-end behavior

## 🩹 Troubleshooting

- **Empty text:** PDF might be image-only; OCR it first
- **Token errors:** Lower chunk size
- **Slow responses:** Use fewer chunks or a faster model
- **Hallucinations:** Strengthen grounding instructions in prompts

## 🔐 Security & Ethics

- Processes only uploaded text; no external lookups
- No legal advice; add disclaimers for public demos
- Don't upload sensitive info

## 🌱 Roadmap

- Export to PDF/Markdown
- Readability scoring
- Evidence view with page highlights
- Multi-document synthesis
- Policy API retrieval mode
- Persona library

## 🙏 Acknowledgements

Built with Streamlit, PyPDF2, tiktoken, and OpenAI Python SDK.
