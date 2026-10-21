# Arquitectura propuesta y estado inicial

```mermaid
flowchart LR
    E[Equipo: CSV sintético] -->|Carga manual autenticada| S[(Amazon S3 privado: raw/orders.csv)]
    S -->|HTTPS + IAM GetObject| A[Streamlit: validación y ETL con pandas]
    A --> G[Agregaciones y Plotly]
    G -->|HTTPS| N[Navegador del docente]
    R[GitHub: branches y PR] --> C[GitHub Actions: pruebas]
    R -->|Despliegue desde main| A
```

El gráfico representa la ruta objetivo cloud. La demo entregada funciona desde CSV local; el código de lectura S3 está incluido. La infraestructura y la publicación todavía no están creadas. El ETL se ejecuta dentro de la aplicación en cada interacción: no hay Lambda, scheduler ni pipeline independiente.

## Relación con la materia

| Concepto | Implementación o evidencia esperada |
|---|---|
| Servicio administrado de aplicación | Streamlit Community Cloud ejecuta el panel |
| Almacenamiento de objetos | CSV persistente en S3, independiente del proceso |
| Identidad y acceso | Permiso GetObject para un solo objeto; bucket sin acceso público |
| Seguridad | HTTPS, secretos fuera del código, datos sintéticos |
| Automatización | Workflow de pruebas; despliegue conectado a main |
| Portabilidad | Dockerfile opcional; permite cambiar el hospedaje |
| Costos y operación | Registrar lecturas, tamaño, región, disponibilidad y alertas de gasto |
| Escalabilidad y límites | Procesamiento en memoria de máximo 10 MB; medir y discutir cuándo separar ETL o motor de consultas |

Cambiar un archivo en S3 cambia la fuente de la siguiente interacción del panel. Una carga en el navegador solo se analiza durante la sesión y no escribe en S3. El bucket puede contener versiones si habilitan versionado; eso no implementa por sí mismo respaldos externos.

## Variante si el docente exige IaaS o un solo proveedor

Ejecutar el contenedor en EC2, habilitar HTTPS con un proxy y asociar un rol IAM de lectura S3. Esta variante requiere administrar sistema, red, certificados y costos; es una ampliación documentada, no implementada en esta base. Para la entrega mínima, usar Community Cloud + S3 y justificar ambos servicios.

## Experimentos para el informe

Medir tiempo de lectura y procesamiento con conjuntos sintéticos de tamaños crecientes dentro de 10 MB. Registrar entorno, tamaño, número de filas y varias repeticiones; no inventar latencias ni capacidad. Documentar que S3 puede escalar independientemente mientras la aplicación sigue limitada por CPU y memoria del alojamiento. Concurrencia y tolerancia a fallos deben describirse como límites a menos que se prueben.
