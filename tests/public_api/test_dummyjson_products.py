import pytest
from pydantic import BaseModel, HttpUrl


def test_dummyjson_list_products_has_items(dummyjson_client):
    r = dummyjson_client.get("/products")
    assert r.status_code == 200

    body = r.json()
    assert "products" in body
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: str | None = None
    category: str
    thumbnail: HttpUrl
    images: list[HttpUrl]


@pytest.mark.regression
def test_dummyjson_get_product_matches_schema(dummyjson_client):
    r = dummyjson_client.get("/products/1")
    assert r.status_code == 200

    # Run validation using Pydantic model defined above.
    # The validation passes by default even if undefined fields are included in the response.
    product = Product(**r.json())
    
    assert product.id == 1
