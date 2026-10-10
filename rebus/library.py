import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Any
from .schema import RebusPuzzle, ClueElement, ClueType, DifficultyTier
from .combiner import SentenceCombiner

class RebusLibrary:
    """Core catalog for ranking, filtering, and generating rebus puzzles for games."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # Default to adjacent data/ directory
            data_dir = Path(__file__).resolve().parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.puzzles: List[RebusPuzzle] = []
        self._load_datasets()
        
        grammar_file = self.data_dir / "grammar_templates.json"
        if grammar_file.exists():
            self.combiner = SentenceCombiner(grammar_file)
        else:
            self.combiner = None

    def _load_datasets(self):
        self.puzzles.clear()
        tier_files = [
            ("tier1_compounds.json", DifficultyTier.TIER_1_COMPOUND),
            ("tier2_spatial_idioms.json", DifficultyTier.TIER_2_SPATIAL),
            ("tier3_multi_element.json", DifficultyTier.TIER_3_PHRASES),
            ("tier4_sentences.json", DifficultyTier.TIER_4_SENTENCES),
        ]

        for filename, expected_tier in tier_files:
            file_path = self.data_dir / filename
            if not file_path.exists():
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                for item in raw_list:
                    clues = [
                        ClueElement(
                            type=ClueType(c["type"]),
                            value=c["value"],
                            symbol=c.get("symbol"),
                            position=c.get("position"),
                            modifier=c.get("modifier"),
                            cloud_description=c.get("cloud_description", "")
                        )
                        for c in item.get("clues", [])
                    ]
                    puzzle = RebusPuzzle(
                        id=item["id"],
                        answer=item["answer"],
                        tier=DifficultyTier(item["tier"]),
                        difficulty_score=item["difficulty_score"],
                        category=item.get("category", "general"),
                        hint=item.get("hint", ""),
                        time_limit_sec=item.get("time_limit_sec", 15),
                        alternate_answers=item.get("alternate_answers", []),
                        combinable_part=item.get("combinable_part"),
                        clues=clues
                    )
                    self.puzzles.append(puzzle)

    def count(self) -> int:
        return len(self.puzzles)

    def get_by_id(self, puzzle_id: str) -> Optional[RebusPuzzle]:
        for p in self.puzzles:
            if p.id == puzzle_id:
                return p
        return None

    def get_by_tier(self, tier: DifficultyTier) -> List[RebusPuzzle]:
        return [p for p in self.puzzles if p.tier == tier]

    def get_ranked(self, ascending: bool = True) -> List[RebusPuzzle]:
        """Returns all puzzles sorted strictly by difficulty score (1 to 10)."""
        return sorted(self.puzzles, key=lambda p: (p.difficulty_score, p.id), reverse=not ascending)

    def get_random(self, tier: Optional[DifficultyTier] = None) -> Optional[RebusPuzzle]:
        pool = self.get_by_tier(tier) if tier else self.puzzles
        return random.choice(pool) if pool else None

    def combine_new_sentence(self) -> Optional[RebusPuzzle]:
        """Combines atomic puzzles into a fresh, dynamic multi-part sentence."""
        if not self.combiner:
            return None
        tier1_pool = self.get_by_tier(DifficultyTier.TIER_1_COMPOUND)
        if not tier1_pool:
            return None
        return self.combiner.generate_sentence_puzzle(tier1_pool)

    def get_stats(self) -> Dict[str, Any]:
        stats = {
            "total_puzzles": len(self.puzzles),
            "by_tier": {},
            "by_category": {},
            "difficulty_range": {"min": 10, "max": 1}
        }
        for p in self.puzzles:
            tier_name = p.tier.value
            stats["by_tier"][tier_name] = stats["by_tier"].get(tier_name, 0) + 1
            stats["by_category"][p.category] = stats["by_category"].get(p.category, 0) + 1
            if p.difficulty_score < stats["difficulty_range"]["min"]:
                stats["difficulty_range"]["min"] = p.difficulty_score
            if p.difficulty_score > stats["difficulty_range"]["max"]:
                stats["difficulty_range"]["max"] = p.difficulty_score
        return stats

    def export_json(self, out_path: Path):
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.get_ranked()], f, indent=2)
