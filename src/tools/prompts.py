SYSTEM_POLICY_SUMMARY = """You are an expert policy communicator.
You read legislation/regulations and produce audience-tailored explanations that are faithful to the source.
Do not invent facts not supported by the text. If unclear, say so.
Cite page tags like [Page 3] when referencing specifics. Be concise and concrete."""

TIERED_EXPLANATIONS_PROMPT = """You are given a slice of a policy document.

Slice:
---
{slice_text}
---

Produce explanations for THIS slice only:

## For a high schooler
- 5–7 bullets (plain language, avoid jargon)

## For a small business owner
- 5–7 bullets (compliance, costs, timelines, risks/opportunities)

## For an economist
- 5–12 bullets (mechanism, incidence, incentives, second-order effects)

Rules: Ground every claim in the slice; if not present, write "Not specified in this slice."
Include [Page #] markers when referencing specifics."""

SYNTHESIS_PROMPT = """Combine the per-slice explanations into one cohesive set.
Resolve duplication; if contradictions exist, flag them.

## For a high schooler
- 5–9 bullets

## For a small business owner
- 5–9 bullets

## For an economist
- 5–12 bullets

## Caveats
- List uncertainties and items not specified."""

WHAT_IT_MEANS_PROMPT = """Using the synthesized explanations and the persona, generate a short, concrete note (120–180 words).
Use conditional language ("likely", "may", "could") and ground statements in the synthesis.

Persona:
{persona_block}

Output:
## What this means for you
<one paragraph with 2–3 practical next steps if relevant>"""