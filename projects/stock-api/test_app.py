from app import create_app


def test_inventory_flow(tmp_path):
    client = create_app(tmp_path / "test.sqlite3").test_client()
    assert client.get("/api/health").json == {"status": "ok"}
    created = client.post("/api/products", json={
        "sku": "GM-001", "name": "Cuaderno", "quantity": 5, "price_cents": 150000
    })
    assert created.status_code == 201
    pid = created.json["id"]
    assert client.post("/api/products", json={"sku": "GM-001", "name": "Duplicado"}).status_code == 409
    assert len(client.get("/api/products?q=cuaderno").json) == 1
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": -2}).json["quantity"] == 3
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": -10}).status_code == 409
    assert client.patch(f"/api/products/{pid}/stock", json={"delta": 0.5}).status_code == 400
    assert client.post("/api/products", json={"sku": "GM-002", "name": "Malo", "quantity": -1}).status_code == 400
