import json
import random
from typing import List, Dict, Any, Optional
from pathlib import Path
from .schema import RebusPuzzle, ClueElement, ClueType, DifficultyTier

class SentenceCombiner:
    """Provides grammatically natural, semantically meaningful sentence rebuses."""

    def __init__(self, grammar_path: Path):
        with open(grammar_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.sentences = self.data.get("collocation_sentences", [])

    def get_natural_sentence_puzzle(self) -> Optional[RebusPuzzle]:
        """Returns a semantically coherent, natural sentence rebus."""
        if not self.sentences:
            return None
            
        choice = random.choice(self.sentences)
        clues = [
            ClueElement(
                type=ClueType(c["type"]),
                value=c["value"],
                symbol=c.get("symbol"),
                position=c.get("position"),
                modifier=c.get("modifier"),
                cloud_description=c.get("cloud_description", "")
            )
            for c in choice["elements"]
        ]

        return RebusPuzzle(
            id=choice["id"],
            answer=choice["answer"],
            tier=DifficultyTier.TIER_4_SENTENCES,
            difficulty_score=choice["difficulty_score"],
            category=choice.get("category", "natural_sentence"),
            hint=choice["hint"],
            time_limit_sec=choice.get("time_limit_sec", 18),
            alternate_answers=[choice["answer"].replace(" ", "")],
            combinable_part="full_sentence",
            clues=clues
        )
