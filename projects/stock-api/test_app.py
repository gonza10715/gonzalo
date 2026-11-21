import pytest

from app import MAX_PRICE_CENTS, MAX_QUANTITY, create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(tmp_path / "stock-test.sqlite3")
    app.config["TESTING"] = True
    return app.test_client()


def product(sku="GM-001", name="Cuaderno", quantity=5, price_cents=150000):
    return {"sku": sku, "name": name, "quantity": quantity, "price_cents": price_cents}


def test_inventory_flow(client):
    assert client.get("/api/health").json == {"status": "ok"}
    assert client.get("/api/products").json == []

    created = client.post("/api/products", json=product())
    assert created.status_code == 201
    pid = created.json["id"]
    assert created.json["quantity"] == 5

    assert len(client.get("/api/products?q=cuaderno").json) == 1
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": -2}).json["quantity"] == 3
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": 4}).json["quantity"] == 7
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": 0}).json["quantity"] == 7


@pytest.mark.parametrize("payload", [
    None,
    [],
    {},
    {"sku": 123, "name": "Producto"},
    {"sku": "ABC", "name": None},
    product(sku=" "),
    product(name=" "),
    product(sku="x" * 41),
    product(name="x" * 101),
    product(quantity=-1),
    product(quantity=True),
    product(quantity=1.5),
    product(quantity=MAX_QUANTITY + 1),
    product(price_cents=-1),
    product(price_cents=False),
    product(price_cents=1.1),
    product(price_cents=MAX_PRICE_CENTS + 1),
    product(quantity=10**100),
])
def test_rejects_invalid_product_payloads(client, payload):
    response = client.post("/api/products", json=payload)
    assert response.status_code == 400
    assert response.json["error"]
    assert client.get("/api/products").json == []


def test_duplicate_sku_and_search(client):
    assert client.post("/api/products", json=product()).status_code == 201
    assert client.post("/api/products", json=product(name="Duplicado")).status_code == 409
    assert client.post("/api/products", json=product(sku="GM-002", name="Lápiz")).status_code == 201
    assert len(client.get("/api/products?q=GM-").json) == 2
    assert [p["sku"] for p in client.get("/api/products?q=lápiz").json] == ["GM-002"]
    assert client.get("/api/products?q=ausente").json == []


def test_stock_limits_and_not_found(client):
    created = client.post("/api/products", json=product(quantity=2))
    pid = created.json["id"]
    assert client.patch("/api/products/999/stock", json={"delta": 1}).status_code == 404
    insufficient = client.patch(f"/api/products/{pid}/stock", json={"delta": -3})
    assert insufficient.status_code == 409
    assert "insuficiente" in insufficient.json["error"].lower()
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": 0.5}).status_code == 400
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": True}).status_code == 400
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": 100001}).status_code == 400
    assert client.patch(f"/api/products/{pid}/stock", json=[]).status_code == 400

    maximum = client.post("/api/products", json=product(
        sku="MAX", quantity=MAX_QUANTITY
    )).json["id"]
    over_limit = client.patch(f"/api/products/{maximum}/stock", json={"delta": 1})
    assert over_limit.status_code == 409
    assert "límite" in over_limit.json["error"].lower()
    assert client.get("/api/products?q=MAX").json[0]["quantity"] == MAX_QUANTITY


def test_limit_results_to_one_hundred(client):
    for i in range(105):
        assert client.post("/api/products", json=product(
            sku=f"SKU-{i:03d}", name=f"Item {i}", quantity=0
        )).status_code == 201
    results = client.get("/api/products").json
    assert len(results) == 100
    assert results[0]["sku"] == "SKU-104"
