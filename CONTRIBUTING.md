# Trabajo en equipo

Primera vez: seguir [Primeros pasos](docs/primeros-pasos-equipo.md). Para repartir trabajo: [cinco tareas iniciales](docs/tareas-iniciales.md).

`main` siempre debe ejecutar la demostración. Una rama corta por tarea, con PR a main. No hace falta una rama develop para cinco integrantes.

```bash
git switch main
git pull --ff-only
git switch -c feature/filtros-ciudad
# editar y probar
python -m pytest -q
git add app.py
git commit -m "feat: agregar filtro por ciudad"
git push -u origin feature/filtros-ciudad
```

Crear PR desde GitHub, asignar un revisor distinto del autor y vincular un issue. Integrar con Squash and merge después de la revisión y CI. Eliminar la rama integrada. Si main avanzó: `git fetch origin` y `git merge origin/main` desde la rama de trabajo; resolver conflictos y volver a probar. No usar force push en main.

El propietario debe invitar a los otros cuatro en Settings → Collaborators. Configurar protección de main si el plan de GitHub lo permite: PR obligatorio, una aprobación y check `tests`. Si no está disponible, mantener esas reglas como acuerdo de equipo. No hacer commits con la cuenta o claves de otro integrante.

| Integrante | Responsabilidad inicial | Resultado revisable |
|---|---|---|
| 1 | Datos y calidad | Contrato CSV, ETL y pruebas de entradas inválidas |
| 2 | Analítica | KPIs, segmentaciones y preguntas de negocio |
| 3 | Panel | Filtros, gráficos y estados vacíos |
| 4 | Cloud y CI | S3 privado, permisos, despliegue y evidencias |
| 5 | Integración e informe | Issues, pruebas de aceptación, informe y demo |

La implementación principal será coordinada por SatoJoe762. Las responsabilidades numeradas son apoyos propuestos hasta que se asignen nombres: los demás integrantes pueden verificar datos y cálculos a mano, probar el panel desde sus dispositivos, revisar PR, reunir evidencias cloud y redactar partes del informe. No necesitan una suscripción de IA para clonar, ejecutar, probar o revisar el proyecto.

Cada integrante debe dejar una contribución verificable acorde a su trabajo real (código, pruebas, documentación o revisión). El informe debe reflejar quién hizo cada aporte, sin atribuir implementación a quien no la realizó. Evitar que todos editen app.py a la vez; coordinar el diseño visual en su propia rama y los cálculos en cloudtrack/analytics.py. Prefijos de ramas: `feature/`, `fix/`, `docs/`. Commits: `feat:`, `fix:`, `docs:`, `test:`. Nunca versionar `.streamlit/secrets.toml` o CSV reales; usar `data/private/` para archivos locales.
