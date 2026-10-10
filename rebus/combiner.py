import json
import random
from typing import List, Dict, Any, Optional
from pathlib import Path
from .schema import RebusPuzzle, ClueElement, ClueType, DifficultyTier

class SentenceCombiner:
    """Dynamically combines atomic rebus components into full phrases and sentences."""

    def __init__(self, grammar_path: Path):
        with open(grammar_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.subjects = self.data.get("subjects", [])
        self.verbs = self.data.get("verbs", [])
        self.templates = self.data.get("templates", [])

    def generate_sentence_puzzle(self, object_puzzles: List[RebusPuzzle]) -> RebusPuzzle:
        """Combines a Subject + Verb + Object (from tier 1/2) into a cohesive sentence puzzle."""
        subject = random.choice(self.subjects)
        verb = random.choice(self.verbs)
        target_obj = random.choice(object_puzzles)

        sentence_answer = f"{subject['value']} {verb['value']} {target_obj.answer}"
        
        # Build clues sequentially across the sky
        combined_clues: List[ClueElement] = []
        
        # 1. Subject Clue
        combined_clues.append(ClueElement(
            type=ClueType.ICON,
            value=subject["value"],
            symbol=subject["symbol"],
            position="left",
            cloud_description=subject["description"]
        ))
        
        # 2. Verb Clue
        combined_clues.append(ClueElement(
            type=ClueType.ICON,
            value=verb["value"],
            symbol=verb["symbol"],
            position="center_left",
            cloud_description=verb["description"]
        ))
        
        # 3. Object Clues (embed target object clues)
        for clue in target_obj.clues:
            combined_clues.append(ClueElement(
                type=clue.type,
                value=clue.value,
                symbol=clue.symbol,
                position="right",
                cloud_description=clue.cloud_description
            ))

        puzzle_id = f"gen_{random.randint(1000, 9999)}"
        return RebusPuzzle(
            id=puzzle_id,
            answer=sentence_answer,
            tier=DifficultyTier.TIER_4_SENTENCES,
            difficulty_score=target_obj.difficulty_score + 4,
            category="generated_sentence",
            hint=f"Sentence: {subject['value']}... ({target_obj.hint})",
            time_limit_sec=target_obj.time_limit_sec + 8,
            alternate_answers=[sentence_answer.replace(" ", "")],
            combinable_part="full_sentence",
            clues=combined_clues
        )
