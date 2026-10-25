# Revisión del rediseño · 24 de octubre de 2026

Disposición final: **ship**, acotada a las correcciones de la revisión visual.

Se revisaron las seis capturas completas de Ventas, Entregas y Datos y metodología, en escritorio (1440 px) y móvil (390 px). Se resolvieron colisiones entre iconos KPI y ayudas móviles, separación de títulos y captions de gráficos, separación del panel de insights, fechas recortadas, alcance del texto de métricas de entrega y contraste de etiquetas laterales.

Verificación funcional: 57 pruebas pytest aprobadas. Las tres pestañas se recorrieron en 1440, 1366, 1024, 768, 430, 390 y 375 px: 21 combinaciones sin desbordamiento horizontal de página ni errores JavaScript observados. Ver `browser-checks.json`.

En navegador se comprobaron filtros de ciudad, restablecimiento, carga del CSV demo, rechazo de CSV inválido, lectura cloud de 600 pedidos, foco visible y movimiento reducido. Ver `controls-checks.json`.

Las pruebas de filtros de categoría y fecha, cálculo de KPIs, selección vacía, ausencia de entregados, validación y errores R2 están incluidas en pytest. No se modificaron fórmulas de analítica, validación de pedidos, almacenamiento, APIs ni credenciales. No se añadieron dependencias.

Límites: resoluciones emuladas en Brave; no se realizaron pruebas en dispositivos físicos ni con lectores de pantalla. El CSS utiliza selectores internos de Streamlit y debe revisarse al actualizar el framework.
