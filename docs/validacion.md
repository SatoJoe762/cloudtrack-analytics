# Validación de la base entregada

- Python 3.12.14: 28 pruebas aprobadas.
- Python 3.13: 28 pruebas aprobadas.
- Dependencias: pip check sin incompatibilidades en Python 3.12.
- Panel: probado mediante Streamlit AppTest (carga demo, filtro, selección vacía, carga pendiente y configuración S3 ausente). La demo remota también se comprobó en navegador; ver publicacion.md.
- Analítica: pruebas de fórmulas con resultados calculados a mano y rechazo de entradas inválidas.
- S3: pruebas con respuestas simuladas; no se contactó una cuenta AWS.
- Git: repositorio conectado a GitHub; documentación en la rama docs/equipo-y-despliegue y PR #1 abierto para revisión; secretos y datos privados excluidos.
- Docker: archivo incluido, imagen no construida porque el servicio Docker local no estaba en ejecución.
- Alojamiento cloud: demostración publicada y comprobada en Streamlit Community Cloud el 21 de octubre de 2026; ver publicacion.md.
- GitHub Actions y permisos IAM reales: su validación externa sigue pendiente; las pruebas locales de S3 usan respuestas simuladas.

Las versiones instaladas se registran en requirements.lock.txt. Las pruebas locales no sustituyen una validación de infraestructura desplegada.
