from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = ROOT / "news"
OUTPUT_FILE = ROOT / "news.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def read_existing_dates() -> dict[str, str]:
    """Сохраняет первоначальную дату уже опубликованных изображений."""
    if not OUTPUT_FILE.exists():
        return {}

    try:
        posts = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    dates: dict[str, str] = {}

    if not isinstance(posts, list):
        return dates

    for post in posts:
        if not isinstance(post, dict):
            continue

        post_date = post.get("date")
        images = post.get("images")

        if not isinstance(post_date, str) or not isinstance(images, list):
            continue

        for image in images:
            if isinstance(image, str):
                dates[image] = post_date

    return dates


def load_flat_image(image: Path, existing_dates: dict[str, str]) -> dict[str, Any]:
    """Каждый файл прямо в news/ становится отдельной новостью."""
    relative_path = image.relative_to(ROOT).as_posix()
    publication_date = existing_dates.get(relative_path, date.today().isoformat())

    return {
        "id": f"flat-{image.stem}",
        "date": publication_date,
        "_sort_order": 0,
        "title": "",
        "category": "",
        "description": "",
        "language": "ru",
        "images": [relative_path],
    }


def load_legacy_folder(folder: Path) -> dict[str, Any] | None:
    """Поддержка старых публикаций с post.json, чтобы они не исчезли."""
    post_file = folder / "post.json"

    if not post_file.exists():
        return None

    try:
        post = json.loads(post_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка JSON в {post_file}: {error}")
        return None

    required_fields = {"date", "title", "category"}

    if not required_fields.issubset(post):
        print(f"Пропущено: не заполнены обязательные поля — {folder.name}")
        return None

    if post.get("published") is not True:
        return None

    try:
        publication_date = date.fromisoformat(str(post["date"]))
    except ValueError:
        print(f"Неверная дата в {post_file}")
        return None

    if publication_date > date.today():
        return None

    images = sorted(
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not images:
        return None

    return {
        "id": folder.name,
        "date": post["date"],
        "_sort_order": int(post.get("sort_order", 0)),
        "title": str(post["title"]).strip(),
        "category": str(post["category"]).strip(),
        "description": str(post.get("description", "")).strip(),
        "language": str(post.get("language", "ru")).strip(),
        "images": [image.relative_to(ROOT).as_posix() for image in images],
    }


def main() -> None:
    NEWS_DIR.mkdir(exist_ok=True)
    existing_dates = read_existing_dates()
    posts: list[dict[str, Any]] = []

    # Новый простой режим: изображения лежат непосредственно в news/.
    for image in sorted(NEWS_DIR.iterdir()):
        if image.is_file() and image.suffix.lower() in IMAGE_EXTENSIONS:
            posts.append(load_flat_image(image, existing_dates))

    # Временная совместимость со старой структурой публикаций.
    for folder in sorted(NEWS_DIR.iterdir()):
        if not folder.is_dir():
            continue

        post = load_legacy_folder(folder)
        if post:
            posts.append(post)

    posts.sort(
        key=lambda item: (item["date"], item["_sort_order"], item["id"]),
        reverse=True,
    )

    for post in posts:
        post.pop("_sort_order", None)

    OUTPUT_FILE.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Создан {OUTPUT_FILE.name}. Публикаций: {len(posts)}")


if __name__ == "__main__":
    main()
