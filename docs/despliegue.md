# Despliegue paso a paso

## 1. Publicar la demostración

1. Subir main a GitHub y comprobar que Actions apruebe las pruebas.
2. Abrir Streamlit Community Cloud, conectar GitHub y crear una app desde el repositorio.
3. Seleccionar main, archivo `app.py` y Python 3.12 en opciones avanzadas.
4. Desplegar. requirements.txt está en la raíz; el modo Demostración no necesita secretos.
5. Verificar filtros, datos vacíos, descarga y mensajes de error. Guardar URL, fecha y capturas para el informe.

## 2. Agregar almacenamiento S3

1. En AWS crear un bucket con nombre propio y anotar región. Mantener activado Block Public Access y deshabilitadas las ACL. No usar datos personales. Antes de crear recursos, revisar precios vigentes y configurar una alerta de presupuesto; una alerta no impone un tope de consumo.
2. Desde la consola de AWS subir `data/orders_demo.csv` como `raw/orders.csv`. Esta carga la hace un miembro autorizado; el panel no necesita permiso de escritura.
3. Aplicar la política de identidad de `s3-read-policy.json` sustituyendo `TU_BUCKET`. Autoriza únicamente GetObject del CSV. No requiere ListBucket. No poner esta política como política pública de bucket.
4. Local: usar un perfil AWS configurado o credenciales temporales; boto3 usa su cadena habitual de credenciales. Establecer CLOUDTRACK_S3_BUCKET, CLOUDTRACK_S3_KEY y AWS_DEFAULT_REGION en el entorno. Alternativamente copiar `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y completar los valores.
5. Community Cloud: pegar esos valores TOML en la configuración de Secrets. Fuera de AWS, administrar allí credenciales con alcance mínimo; rotarlas o revocarlas al terminar. Si son temporales, incluir AWS_SESSION_TOKEN y renovarlas cuando expiren. No usar claves de la cuenta raíz. En alojamiento AWS preferir un rol IAM para evitar claves persistentes.
6. Reiniciar el panel, seleccionar Amazon S3 y contrastar indicadores con el CSV local. Probar también una ruta inválida para comprobar el error controlado. Las interacciones del panel leen S3 nuevamente y pueden generar solicitudes facturables.

Las credenciales del panel son de lectura; la persona que sube el CSV necesita su propio permiso de carga por separado. Usar SSE-S3 para la base académica. SSE-KMS exigiría permisos KMS adicionales y no está configurado por esta política.

## 3. Evidencias mínimas y cierre

- URL funcionando y commit desplegado, ejecución exitosa de CI y PR revisado.
- Captura del objeto S3, bloqueo de acceso público y política con datos sensibles ocultos.
- Mismo resultado de KPIs en modo demo y S3.
- Capturas de CSV inválido, selección vacía y error controlado de conexión.
- Estimación de costos con región, fecha y supuestos, tomada de los precios oficiales vigentes. No asumir gratuidad permanente.
- Al terminar el curso, revisar recursos activos, versiones almacenadas y credenciales; retirar lo que ya no se usa según las reglas de la cuenta.

Documentación: [Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app), [secretos](https://docs.streamlit.io/deploy/concepts/secrets), [seguridad S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html).
