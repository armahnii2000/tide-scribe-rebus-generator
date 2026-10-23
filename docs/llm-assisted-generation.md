# Design: LLM-Assisted Rebus Generation

Status: design proposal (2026-10-23). Adds an optional LLM stage to the
existing procedural pipeline. The procedural engine stays the default and
stays in charge of acceptance.

## Why

The pipeline's weak point is ideation. The four decomposition modules
(phonetic, semantic/icon, spatial/typographic, letter arithmetic) work from
fixed templates and the seed lexicon, so they are good at forms they already
know and poor at inventing a new reading of a phrase. That is the failure
behind flat output: elements placed in a row that merely spell the phrase
when read plainly, with no operation doing any work — not a real puzzle.

An LLM is good at exactly that ideation step: hearing "before" as B + 4,
seeing that a word can sit *inside*, *over*, *between* or *backwards* in
another, proposing the arrangement. It is bad at being the judge — it will
happily call its own weak idea clever. So the split is:

- **LLM proposes.** It suggests candidate decompositions.
- **The engine disposes.** The existing scorer, plus two new checks,
  decides what survives. Nothing the LLM emits reaches the exporter
  unverified.

## Where it slots in

```
Input Phrase
     |
     v
[ Token & Morphological Parser ]
     |
     +--> 1. Phonetic Decomposition ------+
     +--> 2. Semantic & Icon Mapping -----+--> [ Combiner ]
     +--> 3. Spatial & Typographic -------+        |
     +--> 4. Letter Arithmetic -----------+        v
     +--> 5. LLM Proposer (NEW, optional) -+   [ Solvability & Difficulty Scorer ]
                                                       |  (+ 2 new checks)
                                                       v
                                          [ Scene Graph & Engine Exporter ]
```

The proposer emits candidates in the **existing schema** (`rebus/schema.py`)
— the same structure the procedural modules produce — so the combiner,
scorer and exporter do not change shape.

## The proposer

New module `rebus/llm_proposer.py`:

- Input: the target phrase, the requested tier, and the list of operations
  it may use (the four existing kinds).
- Output: up to *k* candidate decompositions as schema JSON. Each candidate
  must declare, per element: its kind (phonetic / icon / spatial /
  arithmetic), its literal text or lexicon token, the spatial relation if
  any, and the intended reading.
- The prompt constrains icon choices to the seed lexicon
  (`data/tier*.json`); a candidate may *propose* a new icon mapping, which
  is flagged `lexicon_proposal` and never auto-accepted into output until
  the mapping exists in the data files.
- One feedback round: if all candidates are rejected, the rejection reasons
  are appended to the prompt and it retries once.

## The two new scorer checks

1. **Round-trip solvability (deterministic).** Reassemble the reading from
   the candidate's elements and relations using fixed rules. It must
   reproduce the target phrase exactly, and the reading must be the natural
   one (no equally-valid alternative reading of the same layout). A
   candidate whose reading only works because the LLM *says* it does fails
   here.
2. **The arrangement must do the work (the non-triviality test).** If the
   phrase can be recovered by reading the elements plainly, in order, with
   zero operations — no spatial relation, no phonetic substitution, no
   arithmetic — the candidate is rejected as a non-puzzle, however neat it
   looks. This encodes the standing quality bar: if it reads plainly
   top-to-bottom, it isn't a rebus. Counted from the schema's declared
   operations, so it stays rule-based, not vibes.

An optional **judge pass** (same provider, separate prompt, given the
rendered layout and the rubric but asked to *solve* it cold) can run on
borderline candidates: if the judge's solve doesn't match the target
phrase, reject. Off by default; costs an extra call.

## Providers and cost

- Provider-agnostic interface; **default is a local model via Ollama**
  (free, runs on the dev machine, no API bill).
- Optional OpenAI-compatible endpoint via environment variable for
  stronger models when wanted.
- Low temperature (0.2) and a proposal cache keyed by phrase + tier, so
  repeated generation is stable and cheap.

## CLI

```bash
# Procedural only (today's behaviour, unchanged)
python3 -m rebus.cli generate "I UNDERSTAND"

# LLM-assisted
python3 -m rebus.cli generate "I UNDERSTAND" --llm
python3 -m rebus.cli generate "ONCE IN A BLUE MOON" --tier tier_3_phrases --llm --candidates 4
```

## Testing

Tests never call a live model. Recorded proposer responses live in
`tests/fixtures/llm/` and are replayed, so the suite stays deterministic
and offline. Provenance is stored on every scene graph
(`source: procedural | llm`, model name, operations used) so output can be
audited and the two engines compared.

## Evaluation

A small harness generates the same phrase set both ways and reports, per
tier: acceptance rate through the scorer, difficulty spread, and how many
candidates each route needed. The LLM route only earns its place if it
accepts *more real puzzles* (passing both new checks), not just more
output.

## Milestones

1. Schema: provenance + declared-operations fields.
2. Proposer module with the Ollama provider; CLI `--llm` flag.
3. Scorer: round-trip check and non-triviality test.
4. Fixtures + tests; evaluation harness and a first comparison run.
5. Optional judge pass; lexicon-proposal review flow.

## Risks

- **Confident nonsense:** the LLM invents readings that don't reassemble.
  Mitigated by the round-trip check — it is the gate, not a warning.
- **Off-lexicon icons:** constrained by prompt, flagged when proposed.
- **Non-determinism:** fixtures in tests, cache in the CLI, low
  temperature.
- **Cost/latency:** local model by default; the flag is opt-in.
