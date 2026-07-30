from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = ROOT / "news"
OUTPUT_FILE = ROOT / "news.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_post(folder: Path) -> dict[str, Any] | None:
    post_file = folder / "post.json"

    if not post_file.exists():
        print(f"Пропущено: нет post.json — {folder.name}")
        return None

    try:
        post = json.loads(post_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"Ошибка JSON в {post_file}: {error}")
        return None

    required_fields = {"date", "title", "category"}

    if not required_fields.issubset(post):
        print(f"Пропущено: не заполнены обязательные поля — {folder.name}")
        return None

    if post.get("published") is not True:
        print(f"Не опубликовано: {folder.name}")
        return None

    try:
        publication_date = date.fromisoformat(post["date"])
    except ValueError:
        print(f"Неверная дата в {post_file}")
        return None

    # Будущие материалы пока не показываем
    if publication_date > date.today():
        print(f"Запланировано на будущее: {folder.name}")
        return None

    images = sorted(
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not images:
        print(f"Пропущено: нет изображений — {folder.name}")
        return None

    return {
        "id": folder.name,
        "date": post["date"],
        "title": str(post["title"]).strip(),
        "category": str(post["category"]).strip(),
        "description": str(post.get("description", "")).strip(),
        "language": str(post.get("language", "ru")).strip(),
        "images": [
            image.relative_to(ROOT).as_posix()
            for image in images
        ],
    }


def main() -> None:
    NEWS_DIR.mkdir(exist_ok=True)

    posts: list[dict[str, Any]] = []

    for folder in NEWS_DIR.iterdir():
        if not folder.is_dir():
            continue

        post = load_post(folder)

        if post:
            posts.append(post)

    posts.sort(
        key=lambda item: (item["date"], item["id"]),
        reverse=True,
    )

    OUTPUT_FILE.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Создан {OUTPUT_FILE.name}. Публикаций: {len(posts)}")


if __name__ == "__main__":
    main()
