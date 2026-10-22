# Contrato de datos y métricas

Una fila representa un pedido completo, no un producto o ítem. Los IDs repetidos se rechazan para evitar duplicar ventas. Categoría: una clasificación principal por pedido. Separador coma, codificación UTF-8, decimal con punto, sin separador de miles. El archivo debe incluir encabezados y al menos un pedido. Se ignoran columnas adicionales.

| Columna | Regla |
|---|---|
| order_id | Texto único y no vacío |
| order_date | Fecha YYYY-MM-DD obligatoria |
| city | Texto no vacío |
| category | Texto no vacío |
| amount_bob | Número finito ≥ 0; importe comercial del pedido en BOB, sin envío |
| shipping_cost_bob | Número finito ≥ 0; costo de envío en BOB, informativo |
| status | entregado, en_transito o cancelado; se normaliza a minúsculas |
| promised_date | Fecha prometida obligatoria, no anterior a order_date |
| delivered_date | Fecha real obligatoria solo para entregados, vacía para otros estados; no anterior al pedido |

No se mezclan monedas ni se incluyen nombres, teléfonos, direcciones o correos. La fecha prometida puede preceder a la real: esa diferencia es precisamente el retraso. El generador produce una fotografía ilustrativa, no un historial de eventos ni una distribución estadística realista.

## Fórmulas sobre el conjunto filtrado

- Pedidos registrados = cantidad de filas, incluidos cancelados y en tránsito.
- Ventas entregadas = suma de amount_bob donde status = entregado. No equivale a ingreso contable auditado.
- Ticket medio = ventas entregadas / cantidad de entregados.
- Entregas a tiempo = 100 × entregados con delivered_date ≤ promised_date / cantidad de entregados.
- Tiempo medio = promedio de delivered_date − order_date en días calendario, solo entregados.

Sin entregas, ventas = 0, pero puntualidad, ticket y días medios no están definidos; el panel muestra “Sin entregas”. El filtro temporal y el gráfico de ventas usan fecha del pedido, incluso si se entregó después del rango. Para análisis por fecha de entrega, crear una tarea explícita con una nueva etiqueta de gráfico.


## Análisis de retrasos

`delay_metrics` en cloudtrack/analytics.py recibe datos previamente validados, incluidos subconjuntos filtrados. Mantiene separado el contrato de `metrics`, para conservar los indicadores del dashboard.

- Entregados tardíos: cantidad de entregados con delivered_date > promised_date. Llegar en la fecha prometida cuenta como puntual.
- Retraso medio entre tardíos: promedio de delivered_date − promised_date, en días calendario, solo entre quienes llegaron tarde. No se compensan atrasos con entregas anticipadas.
- Si no hay tardíos, su cantidad es 0 y el promedio no está definido (`null` en JSON). Se excluyen cancelados y pedidos en tránsito.

Ejemplo: tres entregados llegan a tiempo, 2 días tarde y 5 días tarde. Hay 2 tardíos y el promedio de retraso entre tardíos es 3,5 días. El tiempo desde el pedido hasta la entrega es otro indicador.

## Reporte de calidad reproducible

Desde la raíz del repositorio y con el entorno instalado:

```bash
.venv/bin/python -m scripts.quality_report
.venv/bin/python -m scripts.quality_report data/orders_demo.csv --json
```

En Windows usar `.venv\Scripts\python.exe` en lugar de `.venv/bin/python`. El primer comando muestra un resumen legible; el segundo JSON. Se puede reemplazar la ruta por otro CSV compatible. No hacen falta AWS ni conexión a internet.

El reporte usa `load_orders`, la misma validación del panel: muestra cantidad de pedidos, rango de fechas, conteos por ciudad/categoría/estado, KPIs existentes y métricas de retraso. Si el archivo falta o no cumple el contrato, termina con código 2, explica el error en stderr y no produce un reporte de éxito. No modifica el CSV ni elimina pedidos silenciosamente. El rango corresponde a las fechas del pedido, no al período de entrega.

Este control comprueba consistencia interna, no garantiza que los datos sean verdaderos o representativos. No es un reporte de todas las anomalías por fila: ante un archivo inválido devuelve el primer problema detectado. Para la demo se usan datos sintéticos.

Ver [resultados reproducibles del dataset demo](reporte-calidad.md). Los indicadores de retraso ya están integrados en la pestaña Entregas del dashboard.


## Uso del dashboard

- Entregas muestra cantidad de tardíos y retraso medio entre tardíos; ambos respetan la selección de ciudad, categoría y fecha.
- Restablecer filtros recupera todas las ciudades y categorías y el rango completo del CSV, sin cambiar la fuente elegida. También funciona después de dejar una selección vacía.
- Si cambia la fuente o el contenido del CSV, se restablecen filtros para evitar opciones incompatibles o fechas de un archivo anterior.
- Datos y metodología muestra cuántos pedidos del archivo se validaron y cuántos quedan seleccionados. Permite descargar el reporte JSON de esa selección y el CSV filtrado.
- El reporte del panel y el comando usan el mismo resumen en cloudtrack/reporting.py; no mantienen fórmulas separadas. El comando analiza el archivo completo; el panel resume la selección actual.

Pruebas añadidas: restablecimiento desde una selección vacía, preservación de fuente, KPIs con rango de fechas frente a un cálculo independiente, casos sin tardíos y cambio del contenido S3 simulado. La prueba de cambio S3 no sustituye la conexión real con AWS.
