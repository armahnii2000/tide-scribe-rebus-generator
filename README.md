# 🌊 Tide Scribe - Rebus Puzzle Library

A ranked, curated, and combinable Rebus puzzle library designed for word & puzzle games. Built especially for games where **pictorial and typographic riddles form across the sky** and players race against the ocean tide to carve answers into the wet sand.

---

## 🎯 Features

- **Tiered Difficulty Ranking:** 4 distinct tiers ranked from 1 (Gentle Compound Words) to 10 (Full Cryptic Sentences & Proverbs).
- **Phrase & Sentence Combiner:** Dynamically merges atomic subjects, verbs, and objects into cohesive multi-part sentence rebuses.
- **Game-Engine Ready:** Every puzzle includes cloud vapor descriptions, emoji symbols, spatial position tags, and strict/normalized answer checking.
- **Ocean Wave Timers:** Tuned time limits per difficulty level for pressure-based wave mechanics.

---

## 📈 Difficulty Groups

| Group | Tier Name | Difficulty Score | Description | Example |
|---|---|---|---|---|
| **Tier 1** | `tier_1_compound` | 1 – 2 | Concrete, intuitive compound words (no abstract letter math). | ☀️ + 👓 $\rightarrow$ `SUNGLASSES` |
| **Tier 2** | `tier_2_spatial` | 3 – 5 | Typographic and spatial positioning in the sky (over, under, between). | `STAND` over `I` $\rightarrow$ `I UNDERSTAND` |
| **Tier 3** | `tier_3_phrases` | 6 – 7 | Multi-element visual idioms and coastal sayings. | 🍰 + `OF` + 🎂 $\rightarrow$ `PIECE OF CAKE` |
| **Tier 4** | `tier_4_sentences` | 8 – 10 | Composite full sentences and ancient coastal proverbs. | 👁️ + ❤️ + 🏖️ + 🏰 $\rightarrow$ `I LOVE SANDCASTLES` |

---

## 🚀 Quickstart & CLI

### Run the CLI Tool:

```bash
# View library stats across tiers
python3 -m rebus.cli stats

# List all puzzles in order of difficulty
python3 -m rebus.cli list

# Filter by specific tier
python3 -m rebus.cli list --tier tier_1_compound

# Synthesize a dynamic phrase or sentence across the sky
python3 -m rebus.cli combine

# Play an interactive terminal beach round against the incoming tide
python3 -m rebus.cli play --tier tier_2_spatial

# Export unified JSON for Godot or web engines
python3 -m rebus.cli export --output all_puzzles.json
```

---

## 🧩 Schema Example

```json
{
  "id": "t1_03",
  "answer": "SANDCASTLE",
  "tier": "tier_1_compound",
  "difficulty_score": 1,
  "category": "beach",
  "hint": "Sculpture built on the shore",
  "time_limit_sec": 20,
  "alternate_answers": ["SAND CASTLE"],
  "clues": [
    {
      "type": "icon",
      "value": "SAND",
      "symbol": "🏖️",
      "position": "left",
      "cloud_description": "A mound of golden sand grains in cloud silhouette"
    },
    {
      "type": "math",
      "value": "+",
      "symbol": "+",
      "position": "center",
      "cloud_description": "Plus sign in vapor"
    },
    {
      "type": "icon",
      "value": "CASTLE",
      "symbol": "🏰",
      "position": "right",
      "cloud_description": "Fortress with turrets and battlements"
    }
  ]
}
```

---

## 🧪 Testing

```bash
python3 -m unittest discover -s tests
```
