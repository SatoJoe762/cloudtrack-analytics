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
