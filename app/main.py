from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(title="Alkitab Teman Hati API", version="0.3.0")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "alkitab_tb_sample.json"
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))
RNG = random.SystemRandom()


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="ID unik pengguna")
    message: str = Field(..., min_length=1, description="Keluhan pengguna")
    include_long_passages: bool = Field(
        default=False, description="Jika true, prioritaskan passage yang lebih panjang"
    )


class Verse(BaseModel):
    reference: str
    text: str


class ChatResponse(BaseModel):
    reflection: str
    recommended_verses: list[Verse]
    closing_prayer: str
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
        "kerja": ["kerja", "pekerjaan", "kantor", "karier", "bos", "deadline"],
    }

    tags: set[str] = set()
    for tag, keywords in mapping.items():
        if any(keyword in text for keyword in keywords):
            tags.add(tag)

    if not tags:
        tags.add("cemas")
    return tags


def retrieve_verses(
    tags: set[str],
    include_long_passages: bool,
    limit: int = 3,
) -> list[Verse]:
    verses = load_verse_data()

    scored: list[tuple[int, dict[str, Any]]] = []
    for verse in verses:
        verse_tags = set(verse.get("tags", []))
        score = len(tags.intersection(verse_tags))
        if include_long_passages and verse.get("length") == "long":
            score += 1
        scored.append((score, verse))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_scored = [item[1] for item in scored if item[0] > 0]
    if not top_scored:
        top_scored = [item[1] for item in scored]

    picked = RNG.sample(top_scored, k=min(limit, len(top_scored)))
    return [Verse(reference=v["reference"], text=v["text"]) for v in picked]


def build_reflection(tags: set[str]) -> str:
    if "kerja" in tags:
        return (
            "Terima kasih sudah cerita. Pergumulan kerja itu nyata dan bisa sangat melelahkan. "
            "Semoga firman ini menolongmu melihat bahwa Tuhan tetap menyertai di tengah tekanan."
        )
    if "sedih" in tags:
        return "Terima kasih sudah jujur. Tuhan dekat dengan hati yang terluka, dan kamu tidak berjalan sendiri."
    return (
        "Terima kasih sudah jujur berbagi. Tuhan melihat pergumulanmu hari ini. "
        "Mari melangkah perlahan lewat firman dan doa."
    )


def build_closing_prayer(tags: set[str]) -> str:
    if "kerja" in tags:
        return (
            "Tuhan, berikan aku kekuatan dan hikmat dalam pekerjaanku hari ini. "
            "Tolong aku tetap jujur, tekun, dan tenang saat menghadapi tekanan. Amin."
        )
    if "sedih" in tags:
        return (
            "Tuhan, peluk aku di saat hati ini sedih. Beri penghiburan-Mu dan tuntun langkahku pelan-pelan. "
            "Aku percaya Engkau tidak meninggalkanku. Amin."
        )
    return (
        "Tuhan, terima kasih untuk penyertaan-Mu. Tolong aku menyerahkan kecemasan dan bebanku kepada-Mu, "
        "dan penuhi hatiku dengan damai sejahtera-Mu. Amin."
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    tags = detect_tags(payload.message)
    verses = retrieve_verses(tags, include_long_passages=payload.include_long_passages)
    reflection = build_reflection(tags)
    disclaimer = (
        "Layanan ini adalah pendamping refleksi rohani, bukan pengganti terapis/profesional kesehatan mental."
    )
    prayer = build_closing_prayer(tags)
    return ChatResponse(
        reflection=reflection,
        recommended_verses=verses,
        closing_prayer=prayer,
        disclaimer=disclaimer,
    )


@app.post("/telegram/webhook")
def telegram_webhook(update: dict[str, Any]) -> dict[str, str]:
    return {"status": "received", "note": "Integrasi Telegram disiapkan pada iterasi berikutnya."}
