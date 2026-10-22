# Validación del proyecto

## Integración real comprobada — 22 de octubre de 2026

- Aplicación: [CloudTrack Analytics](https://cloudtrack-analytics-exmcgfwkcp9hsubskacdnw.streamlit.app/), repositorio `SatoJoe762/cloudtrack-analytics`, rama main, entrada `app.py`.
- Soporte R2 integrado mediante [PR #3](https://github.com/SatoJoe762/cloudtrack-analytics/pull/3), merge `eb7aa5185172c308c2e873187984ecb28d51aaf3`; GitHub mostró 1/1 checks aprobados. El commit identifica la integración en Git, no una inspección del SHA dentro del proceso alojado.
- Bucket `cloudtrack-datos`, clase Standard y acceso público deshabilitado; archivo sintético subido como `raw/orders.csv` (49.728 bytes).
- Credencial `cloudtrack-streamlit-lectura`: Object Read only, alcance exclusivo al bucket. Claves guardadas en Secrets de Streamlit, fuera de Git. Se creó sin vencimiento; revisar o revocar al terminar el curso.
- Tras guardar Secrets y reiniciar, desapareció un error de importación observado en el despliegue. La lectura real se verificó seleccionando Almacenamiento cloud, con todas las ciudades, categorías y fechas.

| Indicador | Demo y lectura real de R2 |
|---|---:|
| Pedidos | 600 |
| Ventas entregadas (BOB) | 535.460,90 |
| Entregados usados como denominador | 507 |
| Puntualidad | 49,7 % |
| Tiempo medio de entrega | 4,5 días |
| Entregas tardías | 255 |
| Retraso medio entre tardías | 2,89 días |

![Lectura real de R2 desde el dashboard publicado](evidencias/r2-streamlit-conectado.jpg)

La selección de fuente y los indicadores se observaron en el navegador. La captura documenta una comprobación puntual; no es una medición de disponibilidad continua ni una prueba de concurrencia. Los datos son sintéticos y los mismos resultados se contrastaron en modo Demostración.

## Pruebas automatizadas e historial

La preparación de R2 pasó 52 pruebas locales: contrato CSV, fórmulas, filtros, reportes, panel y lectura cloud simulada. Las respuestas simuladas verifican el código; la comprobación del navegador anterior valida adicionalmente la conexión con la cuenta real.

La base inicial pasó 28 pruebas en Python 3.12.14 y 3.13 y pip check en Python 3.12. Posteriormente pasó 43 pruebas al integrar filtros y retrasos; esos conteos son históricos. Las versiones del entorno local se registraron en requirements.lock.txt. No se volvió a ejecutar la suite para esta actualización de documentación, que no cambia código.

## Pendientes de cierre

- [ ] Ejecutar y registrar las [pruebas del equipo](pruebas-equipo.md) desde otros dispositivos.
- [ ] Configurar y comprobar una alerta de presupuesto en Cloudflare; una alerta no establece un tope de consumo.
- [ ] Verificar descargas y archivos inválidos en la aplicación publicada con evidencia del equipo.
- [ ] Medir rendimiento o concurrencia solo si lo pide el alcance del curso; no se dispone aún de esas mediciones.
- [ ] Completar informe, contribuciones y ensayo de defensa.

Docker sigue siendo una alternativa incluida: la imagen no se construyó en la validación inicial. No se comprobó una cuenta AWS ni se desplegó EC2. La conexión R2 publicada no configura automáticamente secretos en los equipos locales de los integrantes.
