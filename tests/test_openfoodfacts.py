from app import app
import app as app_module


def test_search_without_parameters(client):
    response = client.get("/products/search")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_search_product_by_name(client, monkeypatch):
    # Use a fake product so the test does not need the internet.
    def fake_search(name):
        return {
            "barcode": "3017624010701",
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, cocoa, hazelnuts",
            "categories": "Spreads",
            "image_url": "",
            "nutriscore_grade": "e"
        }

    monkeypatch.setattr(app_module, "search_product_by_name", fake_search)

    response = client.get("/products/search?name=Nutella")
    data = response.get_json()

    assert response.status_code == 200
    assert data["source"] == "Open Food Facts"
    assert data["product"]["product_name"] == "Nutella"


def test_search_product_by_barcode(client, monkeypatch):
    # Pretend the external API found the product by its barcode.
    def fake_lookup(barcode):
        return {
            "barcode": barcode,
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, cocoa, hazelnuts",
            "categories": "Spreads",
            "image_url": "",
            "nutriscore_grade": "e"
        }

    monkeypatch.setattr(app_module, "get_product_by_barcode", fake_lookup)

    response = client.get("/products/search?barcode=3017624010701")
    data = response.get_json()

    assert response.status_code == 200
    assert data["product"]["barcode"] == "3017624010701"


def test_external_product_not_found(client, monkeypatch):
    # Check that the API handles a product that was not found.
    monkeypatch.setattr(
        app_module,
        "search_product_by_name",
        lambda name: None
    )

    response = client.get("/products/search?name=UnknownProduct")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_external_api_failure(client, monkeypatch):
    # Simulate a problem while contacting Open Food Facts.
    def fake_search(name):
        raise RuntimeError("Open Food Facts is unavailable")

    monkeypatch.setattr(app_module, "search_product_by_name", fake_search)

    response = client.get("/products/search?name=Nutella")

    assert response.status_code == 502
    assert "unavailable" in response.get_json()["error"]
