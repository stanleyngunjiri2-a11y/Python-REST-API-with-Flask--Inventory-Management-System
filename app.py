from flask import Flask, jsonify, request
from data.inventory import inventory
from services.openfoodfacts import (
    get_product_by_barcode,
    search_product_by_name
)

app = Flask(__name__)


# finding an item using its ID
def find_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


# creating the next ID for a new product
def get_next_id():
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1


# a simple route to check if the API is working
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Inventory API is running"
    }), 200


# getting all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify({
        "count": len(inventory),
        "inventory": inventory
    }), 200


# getting one inventory item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item), 200


# adding a new inventory item
@app.route("/inventory", methods=["POST"])
def create_inventory_item():

    if not request.is_json:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    data = request.get_json()

    required_fields = [
        "product_name",
        "price",
        "quantity"
    ]

    # checking if required information was provided
    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    # checking price
    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Price must be a number"
        }), 400

    # checking quantity
    try:
        quantity = int(data["quantity"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Quantity must be an integer"
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if quantity < 0:
        return jsonify({
            "error": "Quantity cannot be negative"
        }), 400

    new_item = {
        "id": get_next_id(),
        "barcode": data.get("barcode", ""),
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "categories": data.get("categories", ""),
        "image_url": data.get("image_url", ""),
        "nutriscore_grade": data.get("nutriscore_grade", ""),
        "price": price,
        "quantity": quantity
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Inventory item created successfully",
        "item": new_item
    }), 201


# updating an existing item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):

    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    if not request.is_json:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    data = request.get_json()

    allowed_fields = [
        "barcode",
        "product_name",
        "brands",
        "ingredients_text",
        "categories",
        "image_url",
        "nutriscore_grade",
        "price",
        "quantity"
    ]

    # Stopping users from updating fields we don't allow
    for field in data:
        if field not in allowed_fields:
            return jsonify({
                "error": f"Field '{field}' cannot be updated"
            }), 400

    if "price" in data:
        try:
            price = float(data["price"])

            if price < 0:
                return jsonify({
                    "error": "Price cannot be negative"
                }), 400

            item["price"] = price

        except (TypeError, ValueError):
            return jsonify({
                "error": "Price must be a number"
            }), 400

    if "quantity" in data:
        try:
            quantity = int(data["quantity"])

            if quantity < 0:
                return jsonify({
                    "error": "Quantity cannot be negative"
                }), 400

            item["quantity"] = quantity

        except (TypeError, ValueError):
            return jsonify({
                "error": "Quantity must be an integer"
            }), 400

    # updating the other fields
    for field in allowed_fields:
        if field in data and field not in ["price", "quantity"]:
            item[field] = data[field]

    return jsonify({
        "message": "Inventory item updated successfully",
        "item": item
    }), 200


# deleting an inventory item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):

    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    inventory.remove(item)

    return "", 204


# Search Open Food Facts
@app.route("/products/search", methods=["GET"])
def search_external_product():

    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({
            "error": "Provide either barcode or name"
        }), 400

    try:

        if barcode:
            product = get_product_by_barcode(barcode)

        else:
            product = search_product_by_name(name)

        if product is None:
            return jsonify({
                "error": "Product not found in Open Food Facts"
            }), 404

        return jsonify({
            "source": "Open Food Facts",
            "product": product
        }), 200

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 502

if __name__ == "__main__":
    app.run(debug=True, port=5001)