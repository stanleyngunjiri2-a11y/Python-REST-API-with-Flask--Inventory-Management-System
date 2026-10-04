import requests


# Open Food Facts production API
OPENFOODFACTS_BASE_URL = "https://world.openfoodfacts.org"

# Identify our application when making requests
USER_AGENT = "InventoryManagementSystem/1.0"


def get_product_by_barcode(barcode):

    url = f"{OPENFOODFACTS_BASE_URL}/api/v3/product/{barcode}"

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # API v3 returns product data when the product exists.
        if "product" not in data:
            return None

        product = data["product"]

        return {
            "barcode": product.get("code", barcode),
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "categories": product.get("categories", ""),
            "image_url": product.get("image_front_url", ""),
            "nutriscore_grade": product.get("nutriscore_grade", "")
        }

    except requests.RequestException as error:
        raise RuntimeError(
            f"Open Food Facts request failed: {error}"
        )


def search_product_by_name(name):

    url = f"{OPENFOODFACTS_BASE_URL}/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        if not products:
            return None

        product = products[0]

        return {
            "barcode": product.get("code", ""),
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "categories": product.get("categories", ""),
            "image_url": product.get("image_front_url", ""),
            "nutriscore_grade": product.get("nutriscore_grade", "")
        }

    except requests.RequestException as error:
        raise RuntimeError(
            f"Open Food Facts search failed: {error}"
        )
