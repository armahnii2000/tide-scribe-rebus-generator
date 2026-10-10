from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

class DifficultyTier(str, Enum):
    TIER_1_COMPOUND = "tier_1_compound"        # Single concrete compound words (Sun + Glasses)
    TIER_2_SPATIAL = "tier_2_spatial"          # Spatial & typographic idioms (Head over Heels)
    TIER_3_PHRASES = "tier_3_phrases"          # Multi-element idioms & sayings (Piece of Cake)
    TIER_4_SENTENCES = "tier_4_sentences"      # Full visual sentences & clever cryptograms

class ClueType(str, Enum):
    ICON = "icon"          # Graphic or pictograph (e.g. Sun, Fish, Boots)
    TEXT = "text"          # Literal word or letter in sand/cloud
    SPATIAL = "spatial"    # Relative positioning (over, under, inside, between)
    MATH = "math"          # Combiner (+, -, without)

@dataclass
class ClueElement:
    type: ClueType
    value: str                         # e.g. "SUN", "GLASSES", "OVER"
    symbol: Optional[str] = None       # Emoji or icon key, e.g. "☀️", "👓"
    position: Optional[str] = None     # e.g. "top", "bottom", "inside", "center"
    modifier: Optional[str] = None     # e.g. "-er", "+", "x2"
    cloud_description: str = ""        # Visual guidance for the cloud shader/artist

@dataclass
class RebusPuzzle:
    id: str
    answer: str
    tier: DifficultyTier
    difficulty_score: int              # 1 (easiest) to 10 (hardest)
    clues: List[ClueElement]
    hint: str
    category: str
    time_limit_sec: int = 15
    alternate_answers: List[str] = field(default_factory=list)
    combinable_part: Optional[str] = None # e.g. "subject", "verb", "object", "noun"

    def normalize_string(self, text: str) -> str:
        return "".join(c for c in text.upper() if c.isalnum())

    def check_answer(self, user_input: str) -> bool:
        norm_user = self.normalize_string(user_input)
        if norm_user == self.normalize_string(self.answer):
            return True
        for alt in self.alternate_answers:
            if norm_user == self.normalize_string(alt):
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "answer": self.answer,
            "tier": self.tier.value,
            "difficulty_score": self.difficulty_score,
            "category": self.category,
            "hint": self.hint,
            "time_limit_sec": self.time_limit_sec,
            "alternate_answers": self.alternate_answers,
            "combinable_part": self.combinable_part,
            "clues": [
                {
                    "type": c.type.value,
                    "value": c.value,
                    "symbol": c.symbol,
                    "position": c.position,
                    "modifier": c.modifier,
                    "cloud_description": c.cloud_description
                }
                for c in self.clues
            ]
        }
