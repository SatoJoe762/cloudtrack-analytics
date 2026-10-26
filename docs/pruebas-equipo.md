# Pruebas finales del equipo

Usar la [aplicación publicada](https://cloudtrack-analytics-exmcgfwkcp9hsubskacdnw.streamlit.app/). No se necesitan cuentas Cloudflare ni claves para consultar el panel. El responsable principal coordina; los otros integrantes pueden verificar y documentar sin modificar código.

## Reparto sugerido

| Rol | Responsable por completar | Trabajo |
|---|---|---|
| 1 — Coordinación | SatoJoe762 | Integración, consumo cloud y revisión de resultados |
| 2 — Datos | Pendiente | Comparar demo/R2 y revisar fórmulas |
| 3 — Filtros | Pendiente | Ciudad, categoría, fechas y selección vacía |
| 4 — Archivos | Pendiente | Descargas y carga de CSV válido/inválido |
| 5 — Documentación | Pendiente | Otro dispositivo, capturas e informe |

## Casos de aceptación

Todas las filas siguientes están pendientes de ejecución por el equipo. La integración R2 ya observada se documenta aparte en [validacion.md](validacion.md).

| Caso | Pasos | Resultado esperado | Resultado observado / fecha / persona |
|---|---|---|---|
| 1. Acceso | Abrir el enlace en otro equipo o navegador | Panel accesible, sin error de importación | Pendiente |
| 2. Demo | Elegir Demostración y Restablecer filtros | 100 pedidos, BOB 87.889,84 y 44,8 % puntualidad | Pendiente |
| 3. Lectura R2 | Elegir Almacenamiento cloud y Restablecer filtros | Totales del CSV que esté en R2, iguales al cargar ese mismo archivo por Cargar CSV | Pendiente |
| 4. Filtros | Elegir solo La Paz, manteniendo categorías y fechas completas | 213 pedidos; gráficos y reporte respetan la selección | Pendiente |
| 5. Sin selección | Quitar todas las ciudades; luego Restablecer filtros | Aviso sin error; después recupera todos los pedidos de la fuente elegida | Pendiente |
| 6. Descargas | Filtrar La Paz y descargar CSV/JSON en Datos y metodología | CSV con 213 pedidos; JSON corresponde a esa selección | Pendiente |
| 7. Carga válida | Elegir Cargar CSV y subir data/orders_demo.csv | 100 pedidos; R2 no se modifica | Pendiente |
| 8. Carga inválida | Subir copia del demo sin columna order_id | Mensaje de columna faltante, sin mostrar un análisis exitoso | Pendiente |
| 9. Cambio de fuente | Tras filtrar, cambiar entre Demo y cloud | Se restablece el rango y las selecciones al cambiar la fuente | Pendiente |

En el caso inválido trabajar con una copia local; no reemplazar el archivo de R2 ni editar el demo compartido. Para verificar fechas, elegir un período menor y contrastar el CSV descargado con el rango de Fecha del pedido.

## Registro y revisión

Por cada caso, reemplazar Pendiente con aprobado/fallido, resultado real, fecha, navegador/dispositivo y persona. Adjuntar capturas sin Secrets ni claves en docs/evidencias y enlazarlas desde el registro. Si falla, crear un issue con pasos, resultado esperado y observado. No marcar casos como aprobados por suponer que funcionan.

Se puede enviar el registro mediante una rama y PR, siguiendo [CONTRIBUTING.md](../CONTRIBUTING.md), o entregar los resultados al coordinador para consolidarlos. El cierre requiere revisar fallos y repetir únicamente los casos afectados.
