# Tide Scribe — Procedural Rebus Generation Engine

An algorithmic, on-the-fly Rebus puzzle generation engine and CLI written in Python. While it includes a curated seed lexicon, Tide Scribe's core capability is procedurally decomposing arbitrary phrases and sentences into multi-modal pictorial, phonetic, and typographic riddles with automated difficulty ranking and solvability checks.

Originally designed for word and puzzle games where **pictorial and typographic riddles form across the sky** and players race against the ocean tide to carve answers into the wet sand.

---

## Architecture & Generation Pipeline

```
Input Phrase ("I UNDERSTAND")
       │
       ▼
[ Token & Morphological Parser ]
       │
       ├─► 1. Phonetic Decomposition (Homophones & sound-alike tokens)
       ├─► 2. Semantic & Icon Mapping (Concept → visual glyph / emoji)
       ├─► 3. Spatial & Typographic Transform (Layout offsets: over, under, split, inverted)
       └─► 4. Letter Arithmetic (Additive / subtractive glyph operations)
       │
       ▼
[ Heuristic Solvability & Difficulty Scorer ] ──► (Ranks 1–10, calculates solve window)
       │
       ▼
[ Scene Graph & Engine Exporter ] ──► (Emits game-ready JSON for Godot 4 / Canvas / Terminal)
```

1. **Phonetic & Morphological Decomposition:** Breaks words into syllables, homophones, and phonetic fragments (e.g., decomposing "before" into `B` + `4`, or "sea" into 🌊).
2. **Semantic Substitution:** Replaces atomic tokens with corresponding visual symbols, emojis, or pictorial icons from the seed lexicon.
3. **Spatial & Typographic Layouts:** Computes non-linear 2D layout relationships:
   - *Vertical Stacking:* `STAND` placed vertically over `I` $\rightarrow$ `I UNDERSTAND`.
   - *Containment:* `IN` placed inside a word boundary.
   - *Typographic Sizing:* Scaling and positioning to represent words like "high", "low", "growing", or "split".
4. **Letter Arithmetic:** Generates valid addition and subtraction operations on glyphs (e.g., $CLUES - S = CLUE$).
5. **Heuristic Difficulty & Ambiguity Scorer:** Calculates cognitive complexity based on token obscurity, spatial abstraction, and phonetic distance to assign a difficulty score (1–10) and dynamic countdown timer.

---

## Difficulty Tiers

| Group | Tier Name | Difficulty Score | Description | Example |
|---|---|---|---|---|
| **Tier 1** | `tier_1_compound` | 1 – 2 | Concrete, intuitive compound words (direct icon addition). | ☀️ + 👓 $\rightarrow$ `SUNGLASSES` |
| **Tier 2** | `tier_2_spatial` | 3 – 5 | Typographic and spatial positioning (over, under, between, inside). | `STAND` over `I` $\rightarrow$ `I UNDERSTAND` |
| **Tier 3** | `tier_3_phrases` | 6 – 7 | Multi-element visual idioms and common phrases. | 🍰 + `OF` + 🎂 $\rightarrow$ `PIECE OF CAKE` |
| **Tier 4** | `tier_4_sentences` | 8 – 10 | Composite full sentences and abstract riddles with mixed operations. | 👁️ + ❤️ + 🏖️ + 🏰 $\rightarrow$ `I LOVE SANDCASTLES` |

---

## CLI & Quickstart

```bash
# Generate a procedural rebus on the fly from an arbitrary phrase
python3 -m rebus.cli generate "I UNDERSTAND"

# Generate with explicit difficulty constraints
python3 -m rebus.cli generate "ONCE IN A BLUE MOON" --tier tier_3_phrases

# View seed library statistics
python3 -m rebus.cli stats

# List seed puzzles ordered by difficulty
python3 -m rebus.cli list

# Synthesize a composite phrase across spatial layout coordinates
python3 -m rebus.cli combine

# Play an interactive terminal beach round against the incoming tide
python3 -m rebus.cli play --tier tier_2_spatial

# Export generated puzzles to engine-ready JSON (Godot 4 / Web Canvas)
python3 -m rebus.cli export --output all_puzzles.json
```

---

## Puzzle Schema

Generated puzzles emit a clean, engine-agnostic schema with precise spatial and semantic metadata:

```json
{
  "id": "gen_spatial_042",
  "answer": "I UNDERSTAND",
  "tier": "tier_2_spatial",
  "difficulty_score": 4,
  "category": "spatial_typographic",
  "hint": "Comprehension idiom",
  "time_limit_sec": 18,
  "alternate_answers": ["I UNDERSTAND", "UNDERSTAND"],
  "clues": [
    {
      "type": "text",
      "value": "STAND",
      "symbol": "STAND",
      "position": "top",
      "cloud_description": "The word STAND rendered in bold vapor"
    },
    {
      "type": "spatial_relation",
      "value": "OVER",
      "position": "relation",
      "target": "I"
    },
    {
      "type": "text",
      "value": "I",
      "symbol": "I",
      "position": "bottom",
      "cloud_description": "The letter I rendered beneath STAND"
    }
  ]
}
```

---

## Roadmap

- [x] Seed lexicon with 4-tier difficulty curation and baseline validation.
- [x] Interactive terminal player with tide timer emulation.
- [x] Multi-part sentence and collocation combiner.
- [ ] Automated phonetic decomposition using CMU Pronouncing Dictionary phoneme mappings.
- [ ] Dynamic spatial layout solver for rendering composite 2D layout trees into SVG / HTML Canvas.
- [ ] Headless difficulty calibration harness to benchmark puzzle solvability and time-to-solve distributions.

---

## Testing

Run unit tests directly:

```bash
python3 -m unittest discover -s tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).
