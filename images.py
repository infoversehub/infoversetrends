import random
import requests

from config import (
    PEXELS_API_KEY,
    PIXABAY_API_KEY,
)

# ==========================================
# CONFIG
# ==========================================

PEXELS_URL = (
    "https://api.pexels.com/v1/search"
)

PIXABAY_URL = (
    "https://pixabay.com/api/"
)

OPENVERSE_URL = (
    "https://api.openverse.org/v1/images/"
)

WIKIMEDIA_URL = (
    "https://commons.wikimedia.org/w/api.php"
)

LOREM_PICSUM = (
    "https://picsum.photos/1200/800"
)

HEADERS = {

    "Authorization": PEXELS_API_KEY

}

TIMEOUT = 20

MAX_IMAGES = 5
# ==========================================
# SEARCH PEXELS
# ==========================================

def search_pexels(query, limit=MAX_IMAGES):

    try:

        response = requests.get(

            PEXELS_URL,

            headers=HEADERS,

            params={

                "query": query,

                "per_page": limit

            },

            timeout=TIMEOUT

        )

        if response.status_code != 200:

            return []

        data = response.json()

        images = []

        for photo in data.get(
            "photos",
            []
        ):

            src = photo.get(
                "src",
                {}
            )

            image = src.get(
                "large2x"
            )

            if image:

                images.append(
                    {
                        "url": image,
                        "alt": query
                    }
           )

                
                    
                

        return images

    except Exception as e:

        print(
            "Pexels Error:",
            e
        )

        return []
      # ==========================================
# SEARCH PIXABAY
# ==========================================

def search_pixabay(query, limit=MAX_IMAGES):

    try:

        response = requests.get(

            PIXABAY_URL,

            params={

                "key": PIXABAY_API_KEY,

                "q": query,

                "image_type": "photo",

                "safesearch": "true",

                "per_page": limit

            },

            timeout=TIMEOUT

        )

        if response.status_code != 200:

            return []

        data = response.json()

        images = []

        for photo in data.get(
            "hits",
            []
        ):

            image = photo.get(
                "largeImageURL"
            )

            if image:

                images.append(
                    image
                )

        return images

    except Exception as e:

        print(
            "Pixabay Error:",
            e
        )

        return []
      # ==========================================
# SEARCH OPENVERSE
# ==========================================

def search_openverse(query, limit=MAX_IMAGES):

    try:

        response = requests.get(

            OPENVERSE_URL,

            params={

                "q": query,

                "page_size": limit

            },

            timeout=TIMEOUT

        )

        if response.status_code != 200:

            return []

        data = response.json()

        images = []

        for photo in data.get(
            "results",
            []
        ):

            image = photo.get(
                "url"
            )

            if image:

                images.append(
                    image
                )

        return images

    except Exception as e:

        print(
            "Openverse Error:",
            e
        )

        return []
      # ==========================================
# SEARCH WIKIMEDIA
# ==========================================

def search_wikimedia(query, limit=MAX_IMAGES):

    try:

        response = requests.get(

            WIKIMEDIA_URL,

            params={

                "action": "query",

                "generator": "search",

                "gsrsearch": query,

                "gsrnamespace": 6,

                "gsrlimit": limit,

                "prop": "imageinfo",

                "iiprop": "url",

                "format": "json"

            },

            timeout=TIMEOUT

        )

        if response.status_code != 200:

            return []

        data = response.json()

        pages = data.get(
            "query",
            {}
        ).get(
            "pages",
            {}
        )

        images = []

        for page in pages.values():

            info = page.get(
                "imageinfo",
                []
            )

            if not info:

                continue

            image = info[0].get(
                "url"
            )

            if image:

                images.append(
                    image
                )

        return images

    except Exception as e:

        print(
            "Wikimedia Error:",
            e
        )

        return []
      # ==========================================
# SEARCH LOREM PICSUM
# ==========================================

def search_picsum(limit=MAX_IMAGES):

    images = []

    for _ in range(limit):

        seed = random.randint(
            1,
            1000000
        )

        images.append(
            f"https://picsum.photos/seed/{seed}/1200/800"
        )

    return images
  # ==========================================
# GET IMAGES
# ==========================================

def get_images(
    keywords,
    limit=MAX_IMAGES
):

    if isinstance(
        keywords,
        str
    ):

        keywords = [
            keywords
        ]

    images = []

    for keyword in keywords:

        results = search_pexels(
            keyword,
            limit
        )

        if not results:

            results = search_pixabay(
                keyword,
                limit
            )

        if not results:

            results = search_openverse(
                keyword,
                limit
            )

        if not results:

            results = search_wikimedia(
                keyword,
                limit
            )

        if not results:

            results = search_picsum(
                limit
            )

        for image in results:

            if image not in images:

                images.append(
                    image
                )

            if len(images) >= limit:

                return images

    return images
