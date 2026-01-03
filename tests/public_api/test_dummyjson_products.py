import json
from pathlib import Path

import pytest
from jsonschema import validate


def test_dummyjson_list_products_has_items(dummyjson_client):
    r = dummyjson_client.get("/products")
    assert r.status_code == 200

    body = r.json()
    assert "products" in body
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0


@pytest.mark.regression
def test_dummyjson_get_product_matches_schema(dummyjson_client):
    r = dummyjson_client.get("/products/1")
    assert r.status_code == 200

    product = r.json()

    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "dummyjson_product.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=product, schema=schema)
