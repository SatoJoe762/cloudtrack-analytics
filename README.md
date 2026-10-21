# CloudTrack Analytics

Proyecto académico de analítica de comercio electrónico y entregas para cinco estudiantes de Computación en la Nube. **Base funcional, todavía sin despliegue ni repositorio remoto.**

Pregunta central: ¿qué ciudades y categorías concentran ventas y dónde se incumplen los plazos de entrega?

## Stack y alcance

| Componente | Elección | Motivo |
|---|---|---|
| Lenguaje | Python 3.12 recomendado | Un solo lenguaje para datos y panel |
| Interfaz | Streamlit | Dashboard interactivo sin frontend separado |
| Transformación | pandas | Validar CSV, agrupar y calcular KPIs |
| Visualización | Plotly Express | Gráficos interactivos con pocas líneas |
| Almacenamiento cloud | Amazon S3 privado, opcional al desarrollar | Separar datos persistentes de la aplicación |
| Publicación | Streamlit Community Cloud | Desplegar desde GitHub |
| Colaboración | GitHub, PR, Actions y pytest | Revisión y validación automática |
| Portabilidad | Docker opcional | Ejecutar el mismo servicio en otra plataforma |

Dependencias directas en requirements.txt con rangos acotados. `requirements.lock.txt` registra las versiones exactas usadas durante la validación local; regenerarlo cuando actualicen dependencias. CI usa requirements-dev.txt para comprobar compatibilidad dentro de los rangos. No hay base de datos: el CSV es el conjunto de datos y pandas procesa en memoria. Considerar PostgreSQL o un motor de consulta cuando existan escrituras concurrentes o volúmenes que superen la memoria disponible.

## Ejecutar

Desde esta carpeta, con Python instalado:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m streamlit run app.py
```

En Windows PowerShell: crear el entorno con `py -3.12 -m venv .venv` y activarlo con `.venv\Scripts\Activate.ps1`. Abrir la dirección que muestra Streamlit, habitualmente http://localhost:8501. Los datos demo están incluidos; no necesitan cuenta cloud para comenzar.

Para reproducir el entorno validado, instalar `python -m pip install -r requirements.lock.txt` en un entorno nuevo. El lock incluye herramientas de pruebas.

```bash
python scripts/generate_demo.py
# Opcional, con Docker instalado:
docker build -t cloudtrack-analytics .
docker run --rm -p 8501:8501 cloudtrack-analytics
```

## Qué funciona

- Demostración con 600 pedidos sintéticos de enero a marzo de 2026, semilla 42.
- Carga de CSV UTF-8 de hasta 10 MB, validación y normalización de espacios y estados.
- Filtros por ciudad, categoría y fecha del pedido.
- Pedidos registrados, ventas entregadas, ticket medio, porcentaje puntual y días medios de entrega.
- Ventas por fecha y categoría, estados y puntualidad por ciudad.
- Exportación del CSV filtrado y conexión de lectura a un objeto S3 privado.
- Pruebas del contrato, KPIs, acceso S3 simulado y ejecución del panel; workflow para PR y main.

## Estructura

```text
cloudtrack-analytics/
├── app.py                       # Panel y filtros
├── cloudtrack/
│   ├── analytics.py             # Validación y KPIs
│   └── storage.py               # Lectura S3 con límite y tiempos de espera
├── data/orders_demo.csv         # Solo datos sintéticos
├── scripts/generate_demo.py
├── tests/                       # Analítica, S3 y panel
├── docs/
│   ├── arquitectura.md
│   ├── datos.md
│   ├── despliegue.md
│   ├── plan-e-informe.md
│   └── s3-read-policy.json
├── .github/workflows/ci.yml
├── .github/pull_request_template.md
├── .streamlit/config.toml
├── .streamlit/secrets.toml.example
├── CONTRIBUTING.md
├── requirements.txt
├── requirements-dev.txt
├── requirements.lock.txt
├── Dockerfile
├── .dockerignore
└── .gitignore
```

## Crear el repositorio GitHub

La copia entregada ya tiene Git inicializado en main; no tiene commits ni remoto. Si trabajan desde el ZIP, ejecutar primero `git init -b main`.

1. Un integrante crea en GitHub un repositorio vacío llamado `cloudtrack-analytics`. No agregar README, licencia ni .gitignore desde la web porque ya hay archivos locales. Definir entre todos si será público o privado; no publicar datos personales.
2. Desde esta carpeta ejecutar los comandos siguientes, sustituyendo `TU_USUARIO_O_ORGANIZACION`. Si Git solicita identidad, configurar su propio nombre y correo para este repositorio con `git config user.name` y `git config user.email`.

```bash
git add .
git commit -m "feat: base inicial de CloudTrack Analytics"
git remote add origin https://github.com/TU_USUARIO_O_ORGANIZACION/cloudtrack-analytics.git
git push -u origin main
```

3. Invitar a los otros cuatro integrantes y aplicar las reglas de [CONTRIBUTING.md](CONTRIBUTING.md). Cada uno clona el remoto y crea su entorno; no se comparte la carpeta .venv.

Si tienen GitHub CLI instalada y autenticada, pueden crear el remoto tras el commit con `gh repo create cloudtrack-analytics --private --source=. --remote=origin --push`, en lugar de crearlo desde la web y ejecutar remote add/push.

## Qué demuestra de Computación en la Nube

[Arquitectura](docs/arquitectura.md): aplicación alojada, almacenamiento de objetos, IAM de mínimo privilegio, HTTPS, secretos fuera de Git, CI y separación entre cómputo y persistencia. La integración S3 debe desplegarse para demostrar esa parte; el modo local por sí solo no prueba una arquitectura cloud.

[Despliegue](docs/despliegue.md) · [Contrato y fórmulas](docs/datos.md) · [Plan e informe](docs/plan-e-informe.md).

## Límites

Análisis descriptivo por lotes, sin predicción ni captura de pedidos en tiempo real. El estado es una fotografía: no existen eventos históricos para reconstruir cada cambio. Los pedidos en tránsito pueden estar vencidos; el KPI de puntualidad solo evalúa entregados. Los filtros no permiten inferir causalidad. Los importes son BOB; no se calcula utilidad ni beneficio con solo el costo de envío. Se rechaza el archivo completo ante errores de contrato para evitar exclusiones silenciosas. La exportación conserva datos de entrada: tratar CSV externos como contenido no confiable al abrirlos en hojas de cálculo.

Usar exclusivamente datos sintéticos en la demo pública. El panel inicial no implementa autenticación propia; los filtros no son controles de acceso. S3 privado protege el objeto, pero el panel muestra sus datos a quien pueda abrir la aplicación. Máximo 10 MB por CSV; cada interacción vuelve a procesar los datos y en S3 realiza una lectura. Docker está incluido como opción y requiere validación en su equipo.

## Referencias oficiales

- [Streamlit: despliegue desde GitHub](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Streamlit: manejo de secretos](https://docs.streamlit.io/deploy/concepts/secrets)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [AWS: prácticas de seguridad de S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
