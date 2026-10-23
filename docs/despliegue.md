# Despliegue paso a paso

## 1. Publicar la demostración

1. Subir main a GitHub y comprobar que Actions apruebe las pruebas.
2. Abrir Streamlit Community Cloud, conectar GitHub y crear una app desde el repositorio.
3. Seleccionar main, archivo `app.py` y Python 3.12 en opciones avanzadas.
4. Desplegar. requirements.txt está en la raíz; el modo Demostración no necesita secretos.
5. Verificar filtros, datos vacíos, descarga y mensajes de error. Guardar URL, fecha y capturas para el informe.

## 2. Almacenamiento elegido: Cloudflare R2

Seguir [la guía R2](cloudflare-r2.md): activación de la cuenta, bucket privado, credenciales limitadas a lectura, endpoint y secretos de Streamlit. Esta es la ruta elegida por el equipo. No hace falta crear una cuenta AWS.

## 3. Evidencias mínimas y cierre

- URL funcionando y commit desplegado, ejecución exitosa de CI y PR revisado.
- Captura del objeto R2, acceso público deshabilitado y alcance de lectura del token, sin mostrar claves.
- Mismo resultado de KPIs en modo demo y Almacenamiento cloud con el mismo CSV y filtros.
- Capturas de CSV inválido, selección vacía y error controlado de conexión.
- Estimación de costos con región, fecha y supuestos, tomada de los precios oficiales vigentes. No asumir gratuidad permanente.
- Al terminar el curso, revisar recursos activos, versiones almacenadas y credenciales; retirar lo que ya no se usa según las reglas de la cuenta.

Documentación: [Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app), [secretos](https://docs.streamlit.io/deploy/concepts/secrets), [Cloudflare R2](https://developers.cloudflare.com/r2/).
