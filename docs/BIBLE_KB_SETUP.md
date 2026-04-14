# Bible Knowledge Base Setup (Full Bible)

Yes — you can provide the full Bible dataset, and we can wire it into the app.

## 1) Expected input format
You can provide either JSON or CSV.

### JSON rows
```json
[
  {"book":"Kejadian", "chapter":1, "verse":1, "text":"Pada mulanya...", "reference":"Kejadian 1:1"}
]
```

### CSV columns
- `book`
- `chapter`
- `verse`
- `text`
- `reference` (optional)

## 2) Build the local Bible database
From repo root:

```bash
python scripts/build_bible_kb.py --input /path/to/alkitab_tb.json --format json --translation TB
```

or

```bash
python scripts/build_bible_kb.py --input /path/to/alkitab_tb.csv --format csv --translation TB
```

This creates `kb/bible.db` with:
- `verses` table
- full-text search (`verses_fts`) for passage lookup

## 3) Important legal note
Before importing a full Alkitab text, ensure you have the proper rights/license for storage and redistribution.

## 4) Next step for retrieval quality
After the full dataset exists, we can add:
- semantic embeddings for better context retrieval,
- topic mapping (anxiety/work/grief/etc),
- safer response guardrails for high-risk mental-health messages.
