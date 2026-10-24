# GM Web · Sitios web para negocios

Sitio comercial de Gonzalo Martínez, desarrollador web de San Miguel, Buenos Aires.

**[Ver sitio publicado](https://gonza10715.github.io/gonzalo/)** · [Consultar por WhatsApp](https://wa.me/5491132284507)

## Qué incluye

- Presentación de servicios de desarrollo web, catálogos y gestión de inventario.
- Diseño adaptable a celulares, tabletas y escritorio.
- Menú de demostración con filtros por categoría.
- Demo de stock con cambios de cantidad y restablecimiento.
- Formulario que prepara una consulta para revisar y enviar por WhatsApp.

## Tecnologías

HTML5, CSS3 y JavaScript, sin dependencias ni proceso de compilación.

## Ejecutar

Abrí `index.html` en un navegador. También podés ejecutar `python -m http.server 8000` desde esta carpeta y visitar `http://localhost:8000`.

## Estructura

- `index.html`: contenido y estructura semántica.
- `style.css`: identidad visual y estilos adaptables.
- `app.js`: filtros, selección de productos, demo de stock y contacto.

## Demos del portfolio

- [Casa Brava — restaurante con filtros de menú](https://gonza10715.github.io/gonzalo/demos/restaurante/)
- [Norte Studio — tienda con catálogo y carrito simulado](https://gonza10715.github.io/gonzalo/demos/tienda/)
- [ATELIER — arquitectura, galería filtrable y contacto](https://gonza10715.github.io/gonzalo/demos/atelier/)
- [VELOCE Motors — catálogo premium de vehículos ficticios](https://gonza10715.github.io/gonzalo/demos/veloce/)
- [SERENA Casa Hotel — habitaciones y simulador de estadía](https://gonza10715.github.io/gonzalo/demos/serena/)
- [CLARA Dental — especialidades filtrables y turnos simulados](https://gonza10715.github.io/gonzalo/demos/sonrisa/)
- [LOMA Propiedades — búsqueda y filtros de inmuebles ficticios](https://gonza10715.github.io/gonzalo/demos/loma/)
- [AZAHAR Flores — catálogo floral y carrito simulado](https://gonza10715.github.io/gonzalo/demos/azahar/)
- [Portfolio técnico de Gonzalo Martínez](https://gonza10715.github.io/gonzalo/demos/portfolio/)

Estas demos están publicadas mediante GitHub Pages desde la rama `main`. Son ejemplos ficticios de portfolio y no procesan operaciones reales.

### Funciones demostradas

| Proyecto | Interacción principal | Tecnologías de esta demo |
| --- | --- | --- |
| GM Web | Menú filtrable, control de stock y consulta prearmada | HTML, CSS, JavaScript |
| Casa Brava | Filtros de menú | HTML, CSS, JavaScript |
| Norte Studio | Catálogo y carrito de prueba | HTML, CSS, JavaScript |
| ATELIER | Galería de proyectos filtrable | HTML, CSS, JavaScript |
| VELOCE Motors | Catálogo de vehículos con filtros | HTML, CSS, JavaScript |
| SERENA Casa Hotel | Simulación de una estadía | HTML, CSS, JavaScript |
| CLARA Dental | Filtros de especialidades y turnos de prueba | HTML, CSS, JavaScript |
| LOMA Propiedades | Búsqueda combinada de inmuebles | HTML, CSS, JavaScript |
| AZAHAR Flores | Filtros, selección de ramos y cálculo de total | HTML, CSS, JavaScript |

El portfolio técnico enlaza además proyectos independientes del perfil, como el inventario con Flask y SQLite. Esos repositorios tienen su propio código y tecnologías; no forman parte del despliegue estático de GM Web.

### Pruebas manuales recomendadas

1. Abrir el sitio desde un celular y una computadora; revisar que el menú, los textos y las tarjetas no se corten.
2. En GM Web, cambiar categorías del menú y sumar/restar unidades en el stock. Comprobar que ninguna cantidad sea negativa y que «Restablecer» recupere los valores iniciales.
3. Completar el formulario de contacto. Confirmar que prepara un mensaje en WhatsApp y **no** lo envía automáticamente.
4. En los catálogos y buscadores, combinar filtros y probar casos sin resultados.
5. En AZAHAR, agregar productos, cambiar cantidades, vaciar la selección y cerrar el carrito con la tecla Escape. Comprobar que se pueda navegar con Tab.
6. Verificar los enlaces de vuelta al portfolio y la ausencia de operaciones reales de compra, pago o reserva.


## Alcance

Las demos usan datos ficticios. No procesan pagos ni pedidos y no guardan un inventario real. El formulario abre WhatsApp; la persona revisa y envía el mensaje. Una solución de producción requiere definir persistencia, acceso de usuarios y alcance con cada cliente.

## Autor

Gonzalo Martínez · [GitHub](https://github.com/gonza10715)
