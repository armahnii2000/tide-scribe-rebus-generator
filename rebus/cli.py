import argparse
import sys
import time
from pathlib import Path
from .library import RebusLibrary
from .schema import DifficultyTier

def display_puzzle_card(puzzle, hide_answer=False):
    print("=" * 60)
    print(f"☁️  [ID: {puzzle.id}] | Tier: {puzzle.tier.value} | Difficulty: {puzzle.difficulty_score}/10")
    print(f"🌊 Category: {puzzle.category.title()} | Time Limit: {puzzle.time_limit_sec}s")
    print("-" * 60)
    print("SKY CLOUD FORMATION:")
    symbols = "   ".join([c.symbol if c.symbol else f"[{c.value}]" for c in puzzle.clues])
    print(f"   {symbols}")
    print("\nVAPOR DESCRIPTIONS:")
    for i, c in enumerate(puzzle.clues, 1):
        sym = f"({c.symbol}) " if c.symbol else ""
        print(f"   {i}. {sym}{c.value}: {c.cloud_description}")
    
    print(f"\n💡 Hint: {puzzle.hint}")
    if not hide_answer:
        print(f"✅ Answer: {puzzle.answer}")
        if puzzle.alternate_answers:
            print(f"   (Alternates: {', '.join(puzzle.alternate_answers)})")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Tide Scribe - Rebus Puzzle Library CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: list
    list_parser = subparsers.add_parser("list", help="List all puzzles ranked by difficulty")
    list_parser.add_argument("--tier", choices=[t.value for t in DifficultyTier], help="Filter by tier")

    # Command: stats
    subparsers.add_parser("stats", help="Show library statistics")

    # Command: combine
    subparsers.add_parser("combine", help="Synthesize a new sentence or phrase rebus")

    # Command: play
    play_parser = subparsers.add_parser("play", help="Play an interactive terminal beach riddle round")
    play_parser.add_argument("--tier", choices=[t.value for t in DifficultyTier], help="Choose difficulty tier")

    # Command: export
    export_parser = subparsers.add_parser("export", help="Export unified ranked puzzle dataset to JSON")
    export_parser.add_argument("--output", default="all_ranked_puzzles.json", help="Output file path")

    args = parser.parse_args()
    library = RebusLibrary()

    if args.command == "list":
        tier_enum = DifficultyTier(args.tier) if args.tier else None
        puzzles = library.get_by_tier(tier_enum) if tier_enum else library.get_ranked()
        print(f"\n📚 Found {len(puzzles)} puzzles:\n")
        for p in puzzles:
            display_puzzle_card(p)

    elif args.command == "stats":
        stats = library.get_stats()
        print("\n📊 REBUS LIBRARY STATS")
        print(f"Total Curated Puzzles: {stats['total_puzzles']}")
        print(f"Difficulty Scale: {stats['difficulty_range']['min']} to {stats['difficulty_range']['max']}/10")
        print("\nPuzzles by Difficulty Tier:")
        for tier, count in stats["by_tier"].items():
            print(f"  • {tier:<20}: {count} puzzles")
        print("\nPuzzles by Category:")
        for cat, count in stats["by_category"].items():
            print(f"  • {cat:<20}: {count} puzzles")

    elif args.command == "combine":
        print("\n✨ Generating a composite sentence puzzle across the sky...\n")
        combo = library.combine_new_sentence()
        if combo:
            display_puzzle_card(combo)
        else:
            print("Failed to generate combined puzzle.")

    elif args.command == "play":
        tier_enum = DifficultyTier(args.tier) if args.tier else None
        puzzle = library.get_random(tier_enum)
        if not puzzle:
            print("No puzzles found for that tier.")
            return

        print("\n🏖️ THE TIDE IS ROLLING IN... LOOK AT THE HORIZON!")
        display_puzzle_card(puzzle, hide_answer=True)
        print(f"\n🌊 The wave is rushing towards the sand! You have {puzzle.time_limit_sec} seconds!")
        start_time = time.time()
        
        try:
            user_input = input("✍️ Carve your answer into the wet sand: ").strip()
            elapsed = time.time() - start_time
            if elapsed > puzzle.time_limit_sec:
                print(f"\n💦 WHOOSH! The ocean wave washed over the sand before you finished! ({elapsed:.1f}s)")
                print(f"The answer was: {puzzle.answer}")
            elif puzzle.check_answer(user_input):
                bonus = max(100, int((puzzle.time_limit_sec - elapsed) * 50))
                print(f"\n✨ SPLASH! The wave hits your letters and sparkles with golden foam! ({elapsed:.1f}s)")
                print(f"🎉 Correct! Answer: {puzzle.answer} | Speed Bonus: +{bonus} pts!")
            else:
                print(f"\n❌ The sand letters didn't match the sky clouds!")
                print(f"Your answer: '{user_input}' | Expected: '{puzzle.answer}'")
        except (KeyboardInterrupt, EOFError):
            print("\nLeaving the beach...")

    elif args.command == "export":
        out_path = Path(args.output)
        library.export_json(out_path)
        print(f"✅ Exported {library.count()} ranked puzzles to {out_path.resolve()}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
