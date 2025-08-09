import os
import time
import streamlit as st
from dotenv import load_dotenv

from src.tools.pdf_utils import extract_text_from_pdf
from src.tools.chunking import chunk_text, token_len
from src.models.persona import DEFAULT_PERSONAS, Persona
from src.agents.translator import PolicyTranslatorAgent

load_dotenv()

st.set_page_config(page_title="Policy-to-People Translator", page_icon="📜", layout="wide")
st.title("📜 Policy-to-People Translator")
st.caption("Upload a bill/regulation PDF → tiered explanations + a personalized 'What this means for you' section.")

with st.expander("How it works", expanded=False):
    st.markdown("""
**Pipeline:** PDF ➜ text ➜ chunk ➜ per-slice tiered explanations ➜ synthesis ➜ persona-based impact.
**Guardrails:** Outputs grounded in the uploaded text; unspecified items are flagged in Caveats; page tags like [Page 3] retained.
    """)

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
col_controls, col_main = st.columns([1,2])
agent = PolicyTranslatorAgent()

with col_controls:
    max_tokens = st.slider("Chunk size (approx tokens)", 1600, 3600, 2800, step=200)
    persona_key = st.selectbox("Persona", options=list(DEFAULT_PERSONAS.keys()) + ["Custom persona…"])

    custom = None
    if persona_key == "Custom persona…":
        st.markdown("**Custom persona**")
        label = st.text_input("Label", "Community college parent")
        desc = st.text_area("Context (1–2 sentences)", "Parent working two jobs; concerned about take-home pay and prices.")
        region = st.text_input("Region (optional)", "mid-sized city")
        sector = st.text_input("Sector (optional)", "hospitality")
        size = st.text_input("Org size (optional)", "sole proprietor")
        income = st.text_input("Income band (optional)", "low-to-middle")
        custom = Persona(label=label, description=desc, region=region or None, sector=sector or None, size=size or None, income_band=income or None)

with col_main:
    if uploaded:
        raw = uploaded.read()
        with st.spinner("Extracting text…"):
            text = extract_text_from_pdf(raw)
        if not text:
            st.error("No text found. If it's a scanned image PDF, OCR it first.")
        else:
            st.success(f"Extracted ~{token_len(text)} tokens.")
            st.text_area("Preview", value=text[:2000] + ("…" if len(text) > 2000 else ""), height=180)

            chunks = chunk_text(text, max_tokens=max_tokens)
            st.write(f"Created **{len(chunks)}** chunk(s).")
            if st.button("Generate tiered explanations"):
                with st.spinner("Per-slice explanations…"):
                    per_slice = agent.explain_chunks(chunks)
                st.session_state["per_slice"] = per_slice
                st.success("Done.")

    if "per_slice" in st.session_state and st.button("Synthesize"):
        with st.spinner("Synthesizing…"):
            synth = agent.synthesize(st.session_state["per_slice"])
        st.session_state["synth"] = synth
        st.success("Synthesis ready.")

    if "synth" in st.session_state:
        persona = custom if custom else DEFAULT_PERSONAS[persona_key]
        if st.button("Generate 'What this means for you'"):
            with st.spinner("Personalizing…"):
                wimy = agent.personalize(st.session_state["synth"], persona)
            st.session_state["wimy"] = wimy
            st.success("Personalized impact ready.")

st.markdown("---")
if "synth" in st.session_state:
    st.subheader("Tiered Explanations (Synthesized)")
    st.markdown(st.session_state["synth"])
if "wimy" in st.session_state:
    st.subheader("Personalized Impact")
    st.markdown(st.session_state["wimy"])
st.markdown("---")
st.caption("This tool summarizes the uploaded text and is not legal advice.")