# Qué tecnología usamos y para qué

## Framework principal: Streamlit

CloudTrack Analytics es una aplicación Python cuyo panel se construye con Streamlit. app.py declara títulos, filtros, tablas y gráficos. Streamlit ejecuta ese código en un servidor y entrega la interfaz al navegador; al interactuar con filtros normalmente vuelve a ejecutar el script. El equipo no necesita desarrollar por separado una interfaz JavaScript y una API para este alcance.

| Tecnología o archivo | Tipo | Función | Necesario para empezar |
|---|---|---|---|
| Python | Lenguaje | Ejecuta la lógica y el panel | Sí |
| Streamlit | Framework | Construye y sirve la interfaz | Sí |
| pandas | Biblioteca de datos | Lee, valida y agrupa los pedidos | Sí |
| Plotly Express | Biblioteca de gráficos | Dibuja gráficos interactivos | Sí |
| boto3 | SDK de AWS | Lee el CSV desde S3 cuando se selecciona ese modo | Se instala, pero no requiere cuenta AWS para la demo |
| pytest | Herramienta de pruebas | Comprueba fórmulas y comportamiento | Sí para contribuir |
| Git / GitHub | Control de versiones / servicio de colaboración | Historial, ramas, PR y revisión | Sí para contribuir |
| GitHub Actions | Automatización | Ejecuta las pruebas en PR y main | Funciona en GitHub |
| requirements.txt | Lista de dependencias | Rangos de bibliotecas para la aplicación | Sí |
| requirements.lock.txt | Versiones exactas del entorno validado | Instalar una base común para el equipo | Recomendado al incorporarse |
| .venv | Entorno local | Aísla dependencias de cada computadora | Se crea localmente; no se sube |
| Dockerfile | Receta de contenedor | Empaqueta Python, bibliotecas y aplicación | Opcional |
| .dockerignore | Configuración de Docker | Excluye secretos y archivos locales del contexto de construcción | Solo al usar Docker |
| Amazon S3 | Servicio cloud | Guarda el conjunto de datos fuera del servidor | Para demostrar almacenamiento cloud |
| Streamlit Community Cloud | Alojamiento administrado | Publica el panel desde GitHub | Para compartir una URL con el equipo |

Docker no reemplaza Streamlit: contiene la misma aplicación. Community Cloud instala requirements.txt y ejecuta app.py, por lo que no necesita usar el Dockerfile. Mantener Docker como alternativa de portabilidad; su imagen todavía no está validada en este equipo.

## Recorrido de una consulta

Un CSV demo, cargado por el usuario o leído desde S3 pasa por load_orders en cloudtrack/analytics.py. Allí se valida y transforma. pandas calcula agregaciones; Streamlit muestra indicadores y Plotly los gráficos. cloudtrack/storage.py solo resuelve la lectura S3. Las pruebas se encuentran en tests/.

Actualmente no hay una base de datos, una tienda online, autenticación propia ni un sistema de predicciones. La persistencia cloud elegida para el dataset es S3. La publicación de la aplicación y el almacenamiento son servicios distintos y se deben demostrar ambos en el informe.

Fuentes: [conceptos de Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts), [publicación en Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
