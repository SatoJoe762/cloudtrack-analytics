# Primeros pasos para cada integrante

Repositorio del equipo: https://github.com/SatoJoe762/cloudtrack-analytics

## 1. Obtener una copia propia

Aceptar la invitación a GitHub. En VS Code, abrir la paleta de comandos, elegir Git: Clone, pegar la URL anterior y elegir una carpeta local. Abrir la carpeta clonada. Alternativa desde una terminal:

```bash
git clone https://github.com/SatoJoe762/cloudtrack-analytics.git
cd cloudtrack-analytics
```

Cada integrante clona el repositorio una sola vez. Los cambios siguientes se reciben con pull. No compartir el ZIP para intercambiar cambios, ni copiar entornos .venv de otra computadora.

## 2. Instalar y comprobar

Python recomendado: 3.12; también validado localmente con 3.13. Comenzar en la carpeta que contiene app.py.

macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m streamlit run app.py
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m streamlit run app.py
```

No hace falta activar el entorno si se usan estas rutas. Abrir http://localhost:8501, mantener Demostración y cambiar un filtro. Esperado en la base inicial sin filtros: 600 pedidos y 28 pruebas aprobadas. La cantidad de pruebas aumentará con las contribuciones. Para detener el servidor: Ctrl+C en su terminal.

Si no aparece Python, instalarlo antes de continuar. Si el puerto está ocupado, detener la instancia anterior o añadir `--server.port=8502` y abrir ese puerto. No se necesita Docker, AWS ni credenciales para esta etapa.

## 3. Tomar una tarea

Elegir una tarea de tareas-iniciales.md y abrir un issue con la plantilla Tarea del proyecto. Reemplazar los roles numerados por usuarios reales; elegir un revisor diferente del autor. Un integrante coordina el tablero de GitHub Projects con columnas Pendiente, En curso, En revisión y Terminado; si no usan Projects, los issues y PR son suficientes.

Antes de editar:

```bash
git switch main
git pull --ff-only
git switch -c feature/nombre-de-la-tarea
```

Configurar su nombre y correo con `git config user.name "Su nombre"` y `git config user.email "Su correo"` si todavía no están configurados. Esa identidad firma los commits; la autenticación de GitHub se hace con su propia cuenta.

## 4. Entregar un cambio

Ejecutar las pruebas con el Python del entorno y probar el flujo afectado. Revisar `git diff` y `git status`. Agregar únicamente los archivos de la tarea, crear el commit y publicar la rama. Ejemplo para un cambio en documentación:

```bash
git add docs/datos.md
git commit -m "docs: aclarar contrato del conjunto de datos"
git push -u origin feature/nombre-de-la-tarea
```

En GitHub abrir un Pull Request hacia main. Describir el cambio, vincular el issue con `Closes #NUMERO` y solicitar la revisión acordada. Revisar el resultado del check tests en Actions. Integrar cuando pase CI y el otro integrante apruebe; no aprobar su propio trabajo. Actualizar las copias locales después de integrar.

Ver la demo publicada no es lo mismo que desarrollar: para modificar código cada integrante necesita su copia local y permiso en el repositorio. Nunca compartir credenciales AWS entre los cinco para ejecutar el modo demo.

## Primera reunión, 30 minutos

- Comprobar que todos aceptaron la invitación y ejecutaron la demo.
- Asignar un responsable y revisor a cada una de las cinco tareas.
- Acordar fecha de entrega, preguntas de negocio y alcance del informe.
- Revisar juntos un primer PR pequeño y observar CI.
- Designar a una persona para administrar las cuentas cloud y registrar costos.
