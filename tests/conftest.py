import pytest

from app import app
from data.inventory import inventory


@pytest.fixture
def client():
    # Save the original inventory before running a test.
    original_inventory = inventory.copy()

    # Use Flask's test client without starting the server.
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    # Restore the original inventory after the test.
    inventory.clear()
    inventory.extend(original_inventory)
