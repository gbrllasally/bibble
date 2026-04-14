#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "kb" / "bible.db"
SCHEMA_PATH = ROOT / "kb" / "schema.sql"


def init_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return conn


def rows_from_json(path: Path, translation: str) -> Iterable[tuple[str, str, int, int, str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for row in payload:
        book = row["book"]
        chapter = int(row["chapter"])
        verse = int(row["verse"])
        text = row["text"].strip()
        reference = row.get("reference") or f"{book} {chapter}:{verse}"
        yield (translation, book, chapter, verse, reference, text)


def rows_from_csv(path: Path, translation: str) -> Iterable[tuple[str, str, int, int, str, str]]:
    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = row["book"]
            chapter = int(row["chapter"])
            verse = int(row["verse"])
            text = row["text"].strip()
            reference = row.get("reference") or f"{book} {chapter}:{verse}"
            yield (translation, book, chapter, verse, reference, text)


def insert_rows(conn: sqlite3.Connection, rows: Iterable[tuple[str, str, int, int, str, str]]) -> int:
    count = 0
    for row in rows:
        conn.execute(
            """
            INSERT INTO verses (translation, book, chapter, verse, reference, text)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(translation, book, chapter, verse)
            DO UPDATE SET reference=excluded.reference, text=excluded.text
            """,
            row,
        )
        count += 1
    conn.commit()
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SQLite Bible knowledge base")
    parser.add_argument("--input", required=True, help="Path to JSON or CSV file")
    parser.add_argument("--format", choices=["json", "csv"], required=True)
    parser.add_argument("--translation", default="TB", help="Translation tag (default: TB)")
    parser.add_argument("--db", default=str(DB_PATH), help="Output db path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = init_db(db_path)

    if args.format == "json":
        rows = rows_from_json(input_path, args.translation)
    else:
        rows = rows_from_csv(input_path, args.translation)

    inserted = insert_rows(conn, rows)
    total = conn.execute("SELECT COUNT(*) FROM verses WHERE translation = ?", (args.translation,)).fetchone()[0]
    print(f"Inserted/updated {inserted} rows for translation={args.translation}")
    print(f"Total verses for translation={args.translation}: {total}")


if __name__ == "__main__":
    main()
