# Cinco tareas iniciales

Este archivo es un backlog preparado para copiar a GitHub Issues; no afirma que ya existan issues o asignaciones en GitHub. Elegir los usuarios reales en la primera reunión. Cada tarea debe tener un responsable y un revisor distintos. Empezar con una tarea activa por persona.

| ID | Responsable propuesto | Revisor propuesto | Rama sugerida |
|---|---|---|---|
| T01 · Reporte de calidad | Integrante 1 | Integrante 2 | feature/reporte-calidad |
| T02 · Retrasos de entregas | Integrante 2 | Integrante 1 | feature/analisis-retrasos |
| T03 · Restablecer filtros | Integrante 3 | Integrante 5 | feature/restablecer-filtros |
| T04 · Publicación y S3 | Integrante 4 | Integrante 3 | docs/evidencias-cloud |
| T05 · Pruebas de aceptación e informe | Integrante 5 | Integrante 4 | test/aceptacion-equipo |

## T01 — Reporte reproducible de calidad

Archivos previstos: nuevo scripts/quality_report.py, su prueba y docs/datos.md. Mantener la validación compartida en cloudtrack/analytics.py como fuente del contrato; no duplicarla.

- [ ] Un comando analiza el CSV demo y muestra número de pedidos, rango de fechas, ciudades, categorías y distribución de estados.
- [ ] Usa load_orders para rechazar archivos inválidos y termina con un error entendible.
- [ ] Los totales de estados suman el total de pedidos; se prueba un archivo válido y uno inválido.
- [ ] README o docs/datos.md explica cómo reproducir el reporte.

## T02 — Profundizar el análisis de retrasos

Archivos previstos: cloudtrack/analytics.py, tests/test_analytics.py y docs/datos.md. Reservar la integración visual en app.py para un PR posterior coordinado con T03.

- [ ] Calcular cantidad de entregados tardíos y promedio de días de retraso entre los tardíos.
- [ ] El denominador y la regla de atraso están documentados; pedidos en tránsito y cancelados quedan excluidos.
- [ ] Sin tardíos, la cantidad es 0 y el promedio no está definido; no inventar 0 días como una medición.
- [ ] Un conjunto pequeño calculado a mano prueba casos puntual, tardío y sin entregas.

## T03 — Restablecer filtros del panel

Archivos previstos: app.py y una prueba propia en tests/test_filters.py. Mantener componentes nativos de Streamlit.

- [ ] Un botón Restablecer filtros devuelve todas las ciudades y categorías y el rango completo del conjunto cargado.
- [ ] Funciona después de dejar una selección vacía y conserva la fuente de datos elegida.
- [ ] Se comprueba con Streamlit AppTest y se adjunta una captura del flujo.
- [ ] No se modifica la fórmula de los KPIs.

## T04 — Publicar y comprobar la arquitectura cloud

Archivos previstos: docs/despliegue.md y evidencias sin secretos en docs/evidencias/. No versionar credenciales ni activar servicios de pago sin acordar los costos con el dueño de la cuenta.

- [ ] Desplegar main/app.py desde SatoJoe762/cloudtrack-analytics en Streamlit Community Cloud con Python 3.12.
- [ ] Registrar URL, commit desplegado y quién puede abrir el panel; probar desde otra computadora.
- [ ] Crear S3 privado y subir raw/orders.csv usando el dataset sintético; configurar GetObject con mínimo privilegio.
- [ ] Comparar los mismos filtros en demo y S3; probar una ruta inválida.
- [ ] Documentar región, supuestos de costos y cómo retirar recursos o credenciales al finalizar.

Dependencias: acceso del propietario a Streamlit y AWS. Se puede publicar la demo antes de conectar S3. El Dockerfile es opcional y no hace falta para Community Cloud.

## T05 — Aceptación e informe con evidencias

Archivos previstos: tests/test_acceptance.py y docs/resultados.md. Coordinar cualquier cambio en tests/test_app.py con T03.

- [ ] Agregar un caso de prueba de un rango de fechas acotado comparando el KPI visible con un cálculo independiente sobre el CSV.
- [ ] Registrar en docs/resultados.md tres preguntas de negocio y sus resultados reproducibles con filtros y denominadores.
- [ ] Describir que los datos son sintéticos y que las conclusiones no representan una empresa real.
- [ ] Recopilar enlaces de los PR de cada integrante y evidencias reales del despliegue cuando T04 termine.
- [ ] Completar el informe siguiendo plan-e-informe.md, con aportes de los cinco.

## Acuerdo de integración

T01 y T02 pueden avanzar en paralelo. T03 concentra al comienzo los cambios de app.py. T04 documenta infraestructura y T05 trabaja pruebas e informe. No reservar archivos para siempre: coordinar en el issue cuando dos cambios coincidan. Una tarea termina con PR revisado, CI aprobado y evidencia del criterio de aceptación, no solo con código subido.
