from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Alkitab Teman Hati API", version="0.1.0")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "alkitab_tb_sample.json"


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="ID unik pengguna")
    message: str = Field(..., min_length=1, description="Curhat pengguna")


class Verse(BaseModel):
    reference: str
    text: str


class ChatResponse(BaseModel):
    reflection: str
    recommended_verses: list[Verse]
    reading_plan: list[str]
    disclaimer: str


def load_verse_data() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def detect_tags(message: str) -> set[str]:
    text = message.lower()
    mapping = {
        "cemas": ["cemas", "khawatir", "takut", "gelisah"],
        "sedih": ["sedih", "menangis", "kecewa", "hancur"],
        "bingung": ["bingung", "ragu", "keputusan", "pilihan"],
        "lelah": ["lelah", "capek", "beban", "berat"],
    }

    tags: set[str] = set()
    for tag, keywords in mapping.items():
        if any(keyword in text for keyword in keywords):
            tags.add(tag)

    if not tags:
        tags.add("cemas")
    return tags


def retrieve_verses(tags: set[str], limit: int = 2) -> list[Verse]:
    verses = load_verse_data()
    scored: list[tuple[int, dict[str, Any]]] = []

    for verse in verses:
        verse_tags = set(verse.get("tags", []))
        score = len(tags.intersection(verse_tags))
        scored.append((score, verse))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [item[1] for item in scored[:limit]]
    return [Verse(reference=v["reference"], text=v["text"]) for v in selected]


def build_reading_plan(verses: list[Verse]) -> list[str]:
    plan = []
    for index, verse in enumerate(verses, start=1):
        plan.append(f"Hari {index}: Baca {verse.reference} dan tulis 3 kalimat refleksi doa.")
    plan.append("Hari berikutnya: Ulangi ayat yang paling menyentuh dan doakan secara spesifik.")
    return plan


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    tags = detect_tags(payload.message)
    verses = retrieve_verses(tags)
    reflection = (
        "Terima kasih sudah jujur berbagi. Tuhan melihat pergumulanmu hari ini. "
        "Mari melangkah perlahan lewat firman dan doa yang terarah."
    )
    disclaimer = (
        "Layanan ini adalah pendamping refleksi rohani, bukan pengganti terapis/profesional kesehatan mental."
    )
    plan = build_reading_plan(verses)
    return ChatResponse(
        reflection=reflection,
        recommended_verses=verses,
        reading_plan=plan,
        disclaimer=disclaimer,
    )


@app.post("/telegram/webhook")
def telegram_webhook(update: dict[str, Any]) -> dict[str, str]:
    return {"status": "received", "note": "Integrasi Telegram disiapkan pada iterasi berikutnya."}
