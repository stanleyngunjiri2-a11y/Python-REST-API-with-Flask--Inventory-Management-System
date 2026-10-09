def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_get_all_inventory(client):
    response = client.get("/inventory")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 3
    assert len(data["inventory"]) == 3


def test_get_one_inventory_item(client):
    response = client.get("/inventory/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["product_name"] == "Nutella"


def test_get_missing_inventory_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Inventory item not found"


def test_create_inventory_item(client):
    product = {
        "product_name": "Test Biscuits",
        "price": 120,
        "quantity": 10
    }

    response = client.post("/inventory", json=product)
    data = response.get_json()

    assert response.status_code == 201
    assert data["item"]["product_name"] == "Test Biscuits"
    assert data["item"]["price"] == 120.0
    assert data["item"]["quantity"] == 10


def test_create_product_without_required_fields(client):
    response = client.post(
        "/inventory",
        json={"product_name": "Test Biscuits"}
    )

    assert response.status_code == 400
    assert "fields" in response.get_json()


def test_create_product_with_negative_price(client):
    product = {
        "product_name": "Test Biscuits",
        "price": -10,
        "quantity": 5
    }

    response = client.post("/inventory", json=product)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Price cannot be negative"


def test_update_inventory_item(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 700}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["item"]["price"] == 700.0


def test_update_missing_inventory_item(client):
    response = client.patch(
        "/inventory/999",
        json={"price": 700}
    )

    assert response.status_code == 404


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 204

    # Confirm that the item was removed.
    check_response = client.get("/inventory/1")
    assert check_response.status_code == 404


def test_delete_missing_inventory_item(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404
