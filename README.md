# Inventory Management API

## Summative Lab Project

This project is a Flask-based Inventory Management API developed as part of my Summative Lab. The main goal of the project was to build a REST API that can manage inventory items and also connect to the Open Food Facts API to retrieve product information.

The project uses Python, Flask, and the Requests library.

---

## Features Implemented

### 1. Health Check

I created a health-check endpoint to confirm that the API is running correctly.

**Endpoint:**

`GET /health`

It returns a success message when the server is running.

---

### 2. View All Inventory

The API can return all products currently stored in the inventory.

**Endpoint:**

`GET /inventory`

The response includes the inventory items and the total number of items.

---

### 3. View a Single Inventory Item

A specific inventory item can be retrieved using its ID.

**Endpoint:**

`GET /inventory/<item_id>`

If the requested ID does not exist, the API returns a `404 Not Found` response.

---

### 4. Create Inventory Items

New products can be added to the inventory using a POST request.

**Endpoint:**

`POST /inventory`

The API checks that the required information has been provided.

Required fields include:

* Product name
* Price
* Quantity

Additional product information such as barcode, brand, ingredients, categories, image URL, and Nutri-Score can also be provided.

The API automatically generates a new ID for each product.

A successful creation returns HTTP status `201 Created`.

---

### 5. Update Inventory Items

Existing inventory items can be updated using the PATCH method.

**Endpoint:**

`PATCH /inventory/<item_id>`

The API supports partial updates, meaning that only the fields that need to be changed have to be provided.

The ID of an inventory item cannot be changed.

---

### 6. Delete Inventory Items

Inventory items can be deleted using:

`DELETE /inventory/<item_id>`

A successful deletion returns HTTP status `204 No Content`.

If the item does not exist, the API returns `404 Not Found`.

---

## Input Validation

I added validation to make the API safer and prevent invalid inventory data from being stored.

The API checks for:

* Missing required fields
* Requests without JSON
* Invalid prices
* Invalid quantities
* Negative prices
* Negative quantities
* Invalid fields during updates
* Attempts to update the inventory ID

Invalid requests return appropriate HTTP error responses, mainly `400 Bad Request`.

---

## Open Food Facts API Integration

The project also connects to the **Open Food Facts API** to retrieve real product information.

The integration supports two types of searches.

### Search by Product Name

`GET /products/search?name=Nutella`

This searches Open Food Facts for a product by name.

### Search by Barcode

`GET /products/search?barcode=3017620422003`

This retrieves product information using a barcode.

The API returns information such as:

* Barcode
* Product name
* Brand
* Ingredients
* Categories
* Product image
* Nutri-Score

The external API requests also include error handling so that the application can return an appropriate error if Open Food Facts cannot be reached.

---

## Data Storage

For this lab, inventory data is stored in a Python list inside:

`data/inventory.py`

This acts as a temporary database.

Because the project uses in-memory storage, changes made while the server is running are lost when the Flask server is restarted. This is acceptable for the purpose of this lab.

The project starts with three sample inventory products:

1. Nutella
2. Coca-Cola
3. Oreo Original

---

## Project Structure

```text
inventory-management-api/
│
├── app.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── __init__.py
│   └── inventory.py
│
├── services/
│   ├── __init__.py
│   └── openfoodfacts.py
│
├── tests/
│   └── __init__.py
│
└── venv/
```

The virtual environment and Python cache files are excluded from Git using `.gitignore`.

---

## Technologies Used

* Python 3
* Flask
* Requests
* REST API
* JSON
* Open Food Facts API
* Git and GitHub

---

## API Endpoints

| Method | Endpoint                    | Purpose                           |
| ------ | --------------------------- | --------------------------------- |
| GET    | `/health`                   | Check if API is running           |
| GET    | `/inventory`                | Get all inventory                 |
| GET    | `/inventory/<id>`           | Get one inventory item            |
| POST   | `/inventory`                | Create an inventory item          |
| PATCH  | `/inventory/<id>`           | Update an inventory item          |
| DELETE | `/inventory/<id>`           | Delete an inventory item          |
| GET    | `/products/search?name=`    | Search Open Food Facts by name    |
| GET    | `/products/search?barcode=` | Search Open Food Facts by barcode |

---

## Testing

I tested the API using `curl` requests from the terminal.

The testing covered both successful requests and invalid requests.

Some of the tests performed included:

* Checking the health endpoint
* Retrieving all inventory
* Retrieving individual products
* Testing non-existent inventory IDs
* Creating new inventory items
* Testing missing required fields
* Testing invalid prices
* Testing invalid quantities
* Testing negative values
* Updating inventory items
* Testing partial updates
* Testing attempts to update protected fields
* Deleting inventory items
* Testing deletion of non-existent items
* Searching Open Food Facts by product name
* Searching Open Food Facts by barcode
* Testing requests with missing search parameters

I also checked the Python files using `py_compile` to make sure there were no syntax errors.

---

## HTTP Status Codes Used

The API uses appropriate HTTP status codes depending on the result of each request.

* `200 OK` - Successful request
* `201 Created` - New inventory item created
* `204 No Content` - Inventory item successfully deleted
* `400 Bad Request` - Invalid or missing input
* `404 Not Found` - Requested inventory/product does not exist
* `405 Method Not Allowed` - Unsupported HTTP method
* `502 Bad Gateway` - Problem communicating with the external Open Food Facts API

---

## Running the Project

First, activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python3 app.py
```

The API runs on:

```text
http://127.0.0.1:5001
```

The health endpoint can be tested using:

```bash
curl http://127.0.0.1:5001/health
```

---
