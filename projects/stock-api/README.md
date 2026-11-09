# GM Stock API — proyecto de práctica

Backend educativo de inventario desarrollado con **Python, Flask, SQLite y SQL**.

## Qué hace

- `GET /api/health`: estado del servicio.
- `GET /api/products?q=texto`: listado y búsqueda.
- `POST /api/products`: creación de productos con SKU único.
- `PATCH /api/products/<id>/stock`: ajustes de unidades sin permitir stock negativo.
- Validación de datos, consultas parametrizadas, respuestas JSON y pruebas con pytest.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

En Windows, activar el entorno con `.venv\Scripts\activate`.

```bash
python -m pytest -q
```

## Ejemplo

```bash
curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"sku":"GM-001","name":"Cuaderno","quantity":5,"price_cents":150000}'
```

## Alcance y seguridad

**Demostración local.** No incluye autenticación, permisos por usuario, rate limits ni despliegue de producción. No exponer esta API públicamente ni conectar datos reales sin implementar esas medidas, migraciones y monitoreo. Los precios se representan en centavos para evitar errores de coma flotante.
