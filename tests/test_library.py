import unittest
from pathlib import Path
from rebus.library import RebusLibrary
from rebus.schema import DifficultyTier

class TestRebusLibrary(unittest.TestCase):

    def setUp(self):
        self.library = RebusLibrary()

    def test_library_loads_all_tiers(self):
        self.assertGreater(self.library.count(), 20)
        stats = self.library.get_stats()
        self.assertIn(DifficultyTier.TIER_1_COMPOUND.value, stats["by_tier"])
        self.assertIn(DifficultyTier.TIER_2_SPATIAL.value, stats["by_tier"])
        self.assertIn(DifficultyTier.TIER_3_PHRASES.value, stats["by_tier"])
        self.assertIn(DifficultyTier.TIER_4_SENTENCES.value, stats["by_tier"])

    def test_ranking_order(self):
        ranked = self.library.get_ranked()
        for i in range(len(ranked) - 1):
            self.assertLessEqual(ranked[i].difficulty_score, ranked[i + 1].difficulty_score)

    def test_check_answer_normalization(self):
        puzzle = self.library.get_by_id("t1_01")
        self.assertIsNotNone(puzzle)
        self.assertTrue(puzzle.check_answer("sunglasses"))
        self.assertTrue(puzzle.check_answer("SUN GLASSES"))
        self.assertTrue(puzzle.check_answer("  sun-glasses! "))
        self.assertFalse(puzzle.check_answer("moon glasses"))

    def test_sentence_combiner(self):
        combo = self.library.combine_new_sentence()
        self.assertIsNotNone(combo)
        self.assertEqual(combo.tier, DifficultyTier.TIER_4_SENTENCES)
        self.assertGreaterEqual(len(combo.clues), 3)
        self.assertTrue(combo.check_answer(combo.answer))

if __name__ == "__main__":
    unittest.main()
