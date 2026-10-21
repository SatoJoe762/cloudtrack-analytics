# Validación de la base entregada

- Python 3.12.14: 28 pruebas aprobadas.
- Python 3.13: 28 pruebas aprobadas.
- Dependencias: pip check sin incompatibilidades en Python 3.12.
- Panel: probado mediante Streamlit AppTest (carga demo, filtro, selección vacía, carga pendiente y configuración S3 ausente). No se realizó inspección visual en navegador.
- Analítica: pruebas de fórmulas con resultados calculados a mano y rechazo de entradas inválidas.
- S3: pruebas con respuestas simuladas; no se contactó una cuenta AWS.
- Git: rama main inicializada sin commits ni remoto; secretos y carpeta de datos privados excluidos.
- Docker: archivo incluido, imagen no construida porque el servicio Docker local no estaba en ejecución.
- GitHub Actions, alojamiento cloud y permisos IAM reales: requieren ejecución en las cuentas del equipo; no están verificados externamente.

Las versiones instaladas se registran en requirements.lock.txt. Las pruebas locales no sustituyen una validación de infraestructura desplegada.
