# CloudTrack Analytics

Proyecto académico de analítica de comercio electrónico y entregas para cinco estudiantes de Computación en la Nube. **Código en [GitHub](https://github.com/SatoJoe762/cloudtrack-analytics) y [demo publicada](https://cloudtrack-analytics-exmcgfwkcp9hsubskacdnw.streamlit.app/). Lectura real desde Cloudflare R2 validada el 22 de octubre de 2026.**

Pregunta central: ¿qué ciudades y categorías concentran ventas y dónde se incumplen los plazos de entrega?

## Almacenamiento elegido

Usaremos Cloudflare R2 para el CSV y mantendremos el dashboard en Streamlit. Seguir [la guía R2 paso a paso](docs/cloudflare-r2.md). La conexión requiere el endpoint de Cloudflare R2; si falta, el panel ofrece instrucciones sin intentar usar otro proveedor. No se necesitan dependencias nuevas ni una cuenta AWS para usar R2. La lectura real del bucket privado se comprobó el 22 de octubre de 2026; la demo local funciona sin secretos. Ver [evidencia y límites de la validación](docs/validacion.md).

## Stack y alcance

| Componente | Elección | Motivo |
|---|---|---|
| Lenguaje | Python 3.12 recomendado | Un solo lenguaje para datos y panel |
| Interfaz | Streamlit | Dashboard interactivo sin frontend separado |
| Transformación | pandas | Validar CSV, agrupar y calcular KPIs |
| Visualización | Plotly Express | Gráficos interactivos con pocas líneas |
| Almacenamiento cloud | Cloudflare R2 privado | Separar datos persistentes de la aplicación |
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
- Exportación del CSV filtrado y conexión de lectura a un objeto privado en R2.
- Pruebas del contrato, KPIs, acceso R2 simulado y ejecución del panel; workflow para PR y main.

## Estructura

```text
cloudtrack-analytics/
├── app.py                       # Panel y filtros
├── cloudtrack/
│   ├── analytics.py             # Validación y KPIs
│   └── storage.py               # Lectura R2 con límite y tiempos de espera
├── data/orders_demo.csv         # Solo datos sintéticos
├── scripts/generate_demo.py
├── tests/                       # Analítica, R2 y panel
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

## Repositorio del equipo

El repositorio ya está creado en https://github.com/SatoJoe762/cloudtrack-analytics. Para incorporarse, aceptar la invitación del propietario y clonar una copia propia:

```bash
git clone https://github.com/SatoJoe762/cloudtrack-analytics.git
cd cloudtrack-analytics
```

Crear un entorno local y seguir [CONTRIBUTING.md](CONTRIBUTING.md) para trabajar con ramas y PR. No hace falta crear otro repositorio, repetir git init ni compartir la carpeta .venv.

## Qué demuestra de Computación en la Nube

[Arquitectura](docs/arquitectura.md): aplicación alojada, almacenamiento de objetos, credenciales de mínimo privilegio, HTTPS, secretos fuera de Git, CI y separación entre cómputo y persistencia. La lectura real desde R2 ya se comprobó en la aplicación publicada; el modo Demostración sigue disponible para trabajar sin credenciales.

[Despliegue](docs/despliegue.md) · [Contrato y fórmulas](docs/datos.md) · [Pruebas del equipo](docs/pruebas-equipo.md) · [Dashboard para la feria](docs/dashboard-feria.md) · [Plan e informe](docs/plan-e-informe.md).

## Límites

Análisis descriptivo por lotes, sin predicción ni captura de pedidos en tiempo real. El estado es una fotografía: no existen eventos históricos para reconstruir cada cambio. Los pedidos en tránsito pueden estar vencidos; el KPI de puntualidad solo evalúa entregados. Los filtros no permiten inferir causalidad. Los importes son BOB; no se calcula utilidad ni beneficio con solo el costo de envío. Se rechaza el archivo completo ante errores de contrato para evitar exclusiones silenciosas. La exportación conserva datos de entrada: tratar CSV externos como contenido no confiable al abrirlos en hojas de cálculo.

Usar exclusivamente datos sintéticos en la demo pública. El panel inicial no implementa autenticación propia; los filtros no son controles de acceso. El bucket privado protege el objeto, pero el panel muestra sus datos a quien pueda abrir la aplicación. Máximo 10 MB por CSV; cada interacción vuelve a procesar los datos y en modo cloud realiza una lectura. Docker está incluido como opción y requiere validación en su equipo.

## Referencias oficiales

- [Streamlit: despliegue desde GitHub](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Streamlit: manejo de secretos](https://docs.streamlit.io/deploy/concepts/secrets)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Cloudflare R2: documentación](https://developers.cloudflare.com/r2/)
