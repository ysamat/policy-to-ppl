from typing import List
from concurrent.futures import ThreadPoolExecutor
import time

from src.tools.llm import chat
from src.tools.prompts import (
    SYSTEM_POLICY_SUMMARY,
    TIERED_EXPLANATIONS_PROMPT,
    SYNTHESIS_PROMPT,
    WHAT_IT_MEANS_PROMPT,
)
from src.models.persona import Persona


class PolicyTranslatorAgent:
    # ---- internal helper: one chunk with simple retries ----
    def _process_chunk(self, ch: str, *, retries: int = 3, delay: float = 1.5) -> str:
        prompt = TIERED_EXPLANATIONS_PROMPT.format(slice_text=ch)
        for attempt in range(retries):
            try:
                return chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.2)
            except Exception as e:
                # backoff on transient errors; last try re-raises
                if attempt == retries - 1:
                    raise
                time.sleep(delay * (2 ** attempt))

    # ---- parallel version (preserves order) ----
    def explain_chunks(self, chunks: List[str], max_workers: int = 10) -> List[str]:
        """
        Run LLM calls for all chunks in parallel threads.
        - max_workers: tune based on your OpenAI rate limits; 8–12 is a safe start.
        - Returns results in the same order as `chunks`.
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self._process_chunk, chunks))
        return results

    def synthesize(self, per_slice_explanations: List[str]) -> str:
        stitched = "\n\n---\n\n".join(per_slice_explanations)
        prompt = (
            f"The following are tiered explanations for different slices of the same document.\n\n"
            f"{stitched}\n\n{SYNTHESIS_PROMPT}"
        )
        return chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.2)

    def personalize(self, synthesis: str, persona: Persona) -> str:
        pblock = (
            f"Name: {persona.label}\n"
            f"Context: {persona.description}\n"
            f"Region: {persona.region}\n"
            f"Sector: {persona.sector}\n"
            f"Org size: {persona.size}\n"
            f"Income band: {persona.income_band}"
        )
        prompt = (
            f"Synthesized explanations:\n---\n{synthesis}\n---\n\n"
            + WHAT_IT_MEANS_PROMPT.format(persona_block=pblock)
        )
        return chat(SYSTEM_POLICY_SUMMARY, prompt, temperature=0.35)