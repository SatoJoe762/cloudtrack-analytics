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

## Dónde están los datos y cómo actualizarlos

| Modo del panel | Fuente que lee | Persistencia |
|---|---|---|
| Demostración | `data/orders_demo.csv`, incluido en GitHub y en el despliegue | Cambia al integrar otro CSV en el repositorio y desplegarlo |
| Almacenamiento cloud | Objeto privado `cloudtrack-datos/raw/orders.csv` en Cloudflare R2 | Cambia cuando un miembro autorizado reemplaza ese objeto en R2 |
| Cargar CSV | Archivo elegido desde el equipo del visitante | Se analiza en la sesión; la aplicación no lo escribe en GitHub ni R2 |

El archivo original de R2 tenía 600 pedidos; su referencia sintética está en `data/orders_cloud_reference.csv`. La demostración actual tiene 100 pedidos nuevos de mayo a junio de 2026 en `data/orders_demo.csv`. Son archivos independientes: modificar el CSV local o en GitHub no actualiza R2. El contenido actual de R2 depende del último archivo subido. El panel comienza en Demostración; para consultar R2 hay que elegir Almacenamiento cloud.

## Modificar o agregar pedidos

1. Guarda un respaldo del archivo que vas a editar.
2. Edita las filas o agrega pedidos con IDs únicos, manteniendo los nueve encabezados y las reglas del contrato. Guarda en CSV UTF-8 separado por comas.
3. Valida el archivo con `.venv/bin/python -m scripts.quality_report RUTA_DEL_CSV`. Si hay errores, corrígelos antes de reemplazar la fuente.
4. Para la demo que corre en tu equipo, reemplaza `data/orders_demo.csv`. Para R2, reemplaza el objeto exacto `raw/orders.csv` en el bucket configurado, conservando ese nombre y ruta aunque tu archivo original se llame distinto.
5. Con la sesión abierta, “Actualizar cada 30 segundos” relee la fuente. También puedes usar “Actualizar ahora”. Si cambia el contenido se restablecen ciudades, categorías y fechas para mostrar el conjunto nuevo; si no cambia, se conserva la selección.

La hora de “Última lectura correcta” se expresa en UTC y corresponde a una lectura validada, no a la fecha de modificación del archivo. Si la nueva fuente es inválida o no existe, se muestra un error y la revisión automática permite recuperar la lectura cuando se corrija.

En Streamlit Community Cloud, Demostración lee la copia desplegada desde GitHub: para cambiarla hay que integrar el CSV en `main` y esperar el despliegue. Un archivo editado solo en tu computadora no se envía automáticamente al alojamiento. En modo “Cargar CSV”, vuelve a seleccionar el archivo después de editarlo; la copia de la sesión no sigue los cambios del disco.

El dashboard mantiene permisos de solo lectura en R2. La edición y la carga se hacen fuera del panel; no se añaden credenciales de escritura. Cada revisión cloud genera una lectura por sesión abierta; puedes desactivarla cuando no la necesites. Se usa [`st.fragment`](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment) para programar la revisión dentro de la sesión.

Para actualizar la fuente cloud:

1. Conservar una copia del CSV anterior fuera del repositorio público si contiene información privada.
2. Validar el nuevo archivo con `python -m scripts.quality_report RUTA_DEL_CSV` en el entorno del proyecto. Corregir cualquier error antes de subirlo.
3. Desde la sesión autorizada de Cloudflare, reemplazar `raw/orders.csv` dentro de `cloudtrack-datos`, manteniendo la clase Standard y el acceso público deshabilitado.
4. Abrir el panel, seleccionar Almacenamiento cloud y recargar la página para provocar una lectura nueva. Comparar el total de pedidos y ventas con el reporte local.
5. Registrar fecha, responsable, tamaño y resultado. Si falla, restaurar la copia anterior. No modificar las claves para una actualización del CSV.

Para esta aplicación pública usar únicamente datos sintéticos o un dataset autorizado para publicación: que el bucket sea privado no impide que los visitantes consulten y descarguen datos desde el dashboard. Guardar un CSV en `data/private/` lo excluye de Git, pero no anonimiza sus datos ni elimina archivos ya publicados del historial.

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

Ver [resultados históricos de la referencia cloud original](reporte-calidad.md). Los indicadores de retraso ya están integrados en la pestaña Entregas del dashboard.


## Uso del dashboard

- Entregas muestra cantidad de tardíos y retraso medio entre tardíos; ambos respetan la selección de ciudad, categoría y fecha.
- Restablecer filtros recupera todas las ciudades y categorías y el rango completo del CSV, sin cambiar la fuente elegida. También funciona después de dejar una selección vacía.
- Si cambia la fuente o el contenido del CSV, se restablecen filtros para evitar opciones incompatibles o fechas de un archivo anterior.
- Datos y metodología muestra cuántos pedidos del archivo se validaron y cuántos quedan seleccionados. Permite descargar el reporte JSON de esa selección y el CSV filtrado.
- El reporte del panel y el comando usan el mismo resumen en cloudtrack/reporting.py; no mantienen fórmulas separadas. El comando analiza el archivo completo; el panel resume la selección actual.

Pruebas añadidas: restablecimiento desde una selección vacía, preservación de fuente, KPIs con rango de fechas frente a un cálculo independiente, casos sin tardíos y cambio del contenido S3 simulado. La prueba de cambio S3 no sustituye la conexión real con Cloudflare R2.
