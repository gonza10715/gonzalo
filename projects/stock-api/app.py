"""API educativa de inventario con Flask y SQLite. No apta para producción sin autenticación."""
import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request

HERE = Path(__file__).resolve().parent
SCHEMA = (HERE / "schema.sql").read_text(encoding="utf-8")
MAX_QUANTITY = 1_000_000_000
MAX_PRICE_CENTS = 100_000_000_000


def create_app(database=None):
    app = Flask(__name__)
    db_path = str(database or os.environ.get("STOCK_DB", HERE / "stock.sqlite3"))

    def connect():
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    with connect() as con:
        con.executescript(SCHEMA)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/products")
    def list_products():
        term = request.args.get("q", "").strip()[:100]
        # Treat '%' and '_' as text, not LIKE wildcards.
        escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pattern = f"%{escaped}%"
        with connect() as con:
            rows = con.execute(
                "SELECT id, sku, name, quantity, price_cents FROM products "
                "WHERE name LIKE ? ESCAPE '\\' OR sku LIKE ? ESCAPE '\\' "
                "ORDER BY id DESC LIMIT 100",
                (pattern, pattern),
            ).fetchall()
        return jsonify([dict(row) for row in rows])

    @app.post("/api/products")
    def create_product():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Se necesita un objeto JSON."), 400
        raw_sku, raw_name = data.get("sku"), data.get("name")
        if not isinstance(raw_sku, str) or not isinstance(raw_name, str):
            return jsonify(error="SKU y nombre deben ser texto."), 400
        sku, name = raw_sku.strip(), raw_name.strip()
        qty, price = data.get("quantity", 0), data.get("price_cents", 0)
        if not (1 <= len(sku) <= 40 and 1 <= len(name) <= 100):
            return jsonify(error="SKU o nombre inválido."), 400
        if (type(qty) is not int or type(price) is not int or
                not 0 <= qty <= MAX_QUANTITY or not 0 <= price <= MAX_PRICE_CENTS):
            return jsonify(error="Cantidad o precio fuera del rango permitido."), 400
        try:
            with connect() as con:
                cur = con.execute(
                    "INSERT INTO products(sku,name,quantity,price_cents) VALUES(?,?,?,?)",
                    (sku, name, qty, price),
                )
                product_id = cur.lastrowid
        except sqlite3.IntegrityError:
            return jsonify(error="SKU duplicado."), 409
        return jsonify(id=product_id, sku=sku, name=name, quantity=qty, price_cents=price), 201

    @app.patch("/api/products/<int:product_id>/stock")
    def change_stock(product_id):
        data = request.get_json(silent=True)
        delta = data.get("delta") if isinstance(data, dict) else None
        if type(delta) is not int or not -100000 <= delta <= 100000:
            return jsonify(error="Delta debe ser un entero dentro del rango permitido."), 400
        with connect() as con:
            cur = con.execute(
                "UPDATE products SET quantity=quantity+? "
                "WHERE id=? AND quantity+? BETWEEN 0 AND ?",
                (delta, product_id, delta, MAX_QUANTITY),
            )
            if cur.rowcount == 0:
                existing = con.execute(
                    "SELECT quantity FROM products WHERE id=?", (product_id,)
                ).fetchone()
                if not existing:
                    return jsonify(error="Producto no encontrado."), 404
                error = ("Stock insuficiente." if existing["quantity"] + delta < 0
                         else "Stock supera el límite permitido.")
                return jsonify(error=error), 409
            row = con.execute("SELECT id,sku,name,quantity,price_cents FROM products WHERE id=?", (product_id,)).fetchone()
        return jsonify(dict(row))

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
