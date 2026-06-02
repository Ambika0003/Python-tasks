"""Resolve movie posters and cast photos from static/images folders."""

import os

from flask import current_app, url_for

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def _images_root():
    return os.path.join(current_app.static_folder, "images")


def _resolve_relative(*candidates):
    """
    Try paths under static/images/ without extension.
    e.g. movies/1/poster -> movies/1/poster.png
    """
    root = _images_root()
    for rel in candidates:
        if not rel:
            continue
        rel_path = rel.replace("\\", "/").lstrip("/")
        base = os.path.join(root, *rel_path.split("/"))
        # Path already includes extension
        if os.path.splitext(base)[1].lower() in IMAGE_EXTENSIONS:
            if os.path.isfile(base):
                return url_for("static", filename=f"images/{rel_path}")
            continue
        for ext in IMAGE_EXTENSIONS:
            full = base + ext
            if os.path.isfile(full):
                return url_for("static", filename=f"images/{rel_path}{ext}")
    return None


def movie_poster_src(movie_id, fallback=None):
    """Local file first, then optional DB URL, then placeholder."""
    mid = str(movie_id)
    local = _resolve_relative(
        f"movies/{mid}/poster",
        f"posters/{mid}",
        f"movies/{mid}/image1",
    )
    if local:
        return local
    if fallback and str(fallback).strip().startswith(("http://", "https://")):
        return fallback
    return url_for("static", filename="images/placeholder-poster.svg")


def cast_photo_src(movie_id, cast_id=None, sort_order=None, fallback=None):
    """Cast image: movies/<id>/cast/<n>/photo.png or cast/<n>.png etc."""
    mid = str(movie_id)
    candidates = []
    if cast_id is not None:
        cid = str(cast_id)
        candidates.extend(
            [
                f"movies/{mid}/cast/{cid}/photo",
                f"movies/{mid}/cast/{cid}",
                f"cast/{cid}",
            ]
        )
    if sort_order is not None:
        so = str(sort_order)
        candidates.extend(
            [
                f"movies/{mid}/cast/{so}/photo",
                f"movies/{mid}/cast/{so}",
            ]
        )
    local = _resolve_relative(*candidates)
    if local:
        return local
    if fallback and str(fallback).strip().startswith(("http://", "https://")):
        return fallback
    return url_for("static", filename="images/placeholder-cast.svg")


def movie_poster_hint(movie_id):
    return f"static/images/movies/{movie_id}/poster.png"


def cast_photo_hint(movie_id, cast_id=None, sort_order=None):
    if cast_id is not None:
        return (
            f"static/images/movies/{movie_id}/cast/{cast_id}/photo.png "
            f"(or …/cast/{cast_id}.png)"
        )
    if sort_order is not None:
        return f"static/images/movies/{movie_id}/cast/{sort_order}/photo.png"
    return f"static/images/movies/{movie_id}/cast/<cast_id>/photo.png"
