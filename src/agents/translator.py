from typing import List
from src.tools.llm import chat
from src.tools.prompts import (
    SYSTEM_POLICY_SUMMARY,
    TIERED_EXPLANATIONS_PROMPT,
    SYNTHESIS_PROMPT,
    WHAT_IT_MEANS_PROMPT,
)
from src.models.persona import Persona

class PolicyTranslatorAgent:
    def explain_chunks(self, chunks: List[str]) -> List[str]:
        outs = []
        for ch in chunks:
            prompt = TIERED_EXPLANATIONS_PROMPT.format(slice_text=ch)
            outs.append(chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.2))
        return outs

    def synthesize(self, per_slice_explanations: List[str]) -> str:
        stitched = "\n\n---\n\n".join(per_slice_explanations)
        prompt = f"The following are tiered explanations for different slices of the same document.\n\n{stitched}\n\n{SYNTHESIS_PROMPT}"
        return chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.2)

    def personalize(self, synthesis: str, persona: Persona) -> str:
        pblock = (
            f"Name: {persona.label}\nContext: {persona.description}\n"
            f"Region: {persona.region}\nSector: {persona.sector}\n"
            f"Org size: {persona.size}\nIncome band: {persona.income_band}"
        )
        prompt = f"Synthesized explanations:\n---\n{synthesis}\n---\n\n" + WHAT_IT_MEANS_PROMPT.format(persona_block=pblock)
        return chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.35)