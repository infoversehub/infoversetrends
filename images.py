"""
InfoVerse Hub V2
Image Manager
"""

import os
import requests

from config import (
    PEXELS_API_KEY,
    PIXABAY_API_KEY,
)


IMAGE_FOLDER = "images"


def ensure_folder():

    os.makedirs(IMAGE_FOLDER, exist_ok=True)


def download_image(url, filename):

    ensure_folder()

    path = os.path.join(IMAGE_FOLDER, filename)

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        return None

    with open(path, "wb") as file:
        file.write(response.content)

    return path


def search_pexels(query):

    if not PEXELS_API_KEY:
        return None

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = (
        "https://api.pexels.com/v1/search"
        f"?query={query}&per_page=5"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        return None

    data = response.json()

    photos = data.get("photos", [])

    if not photos:
        return None

    return photos[0]["src"]["large"]


def search_pixabay(query):

    if not PIXABAY_API_KEY:
        return None

    url = (
        "https://pixabay.com/api/"
        f"?key={PIXABAY_API_KEY}"
        f"&q={query}"
        "&image_type=photo"
        "&per_page=5"
    )

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        return None

    data = response.json()

    hits = data.get("hits", [])

    if not hits:
        return None

    return hits[0]["largeImageURL"]


def search_image(query):

    image = search_pexels(query)

    if image:
        return image

    image = search_pixabay(query)

    if image:
        return image

    return None


def get_featured_image(title):

    image = search_image(title)

    if not image:
        return None

    return download_image(
        image,
        "featured.jpg"
    )


def get_article_images(title, count=3):

    images = []

    for i in range(count):

        image = search_image(title)

        if not image:
            continue

        path = download_image(
            image,
            f"image_{i+1}.jpg"
        )

        if path:
            images.append(path)

    return images
