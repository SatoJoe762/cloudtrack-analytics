# Conectar CloudTrack Analytics con Cloudflare R2

Arquitectura elegida: GitHub guarda el código, Streamlit Community Cloud ejecuta el panel y Cloudflare R2 guarda el CSV. R2 utiliza una API compatible con S3; no hace falta una cuenta AWS para esta configuración. La conexión real se comprobó el 22 de octubre de 2026 en la aplicación publicada: bucket privado `cloudtrack-datos`, objeto `raw/orders.csv` y credencial limitada a lectura del bucket, almacenada en Secrets de Streamlit. Ver [evidencia y pendientes](validacion.md). Los pasos siguientes permiten reproducir la configuración; no hace falta crear otro bucket o token para la instalación actual. La preparación pasó 52 pruebas locales, incluidas lectura R2 simulada, endpoint, filtros y validación del CSV.

## 1. Crear la cuenta y activar R2

1. Abrir https://dash.cloudflare.com/ y crear una cuenta. Completar personalmente la verificación de correo y el registro.
2. Entrar en Storage & databases → R2 → Overview. La posición o traducción del menú puede variar.
3. Revisar y completar la activación de la suscripción R2. Si pide datos de pago o aceptar condiciones, hacerlo personalmente después de revisar lo que muestra la pantalla.

R2 tiene cuotas mensuales incluidas; no es un servicio con consumo ilimitado. Standard incluye 10 GB-mes de almacenamiento, un millón de operaciones de escritura/administración y diez millones de lectura al mes; el exceso se factura. La cuota gratuita no corresponde a la clase Infrequent Access. Para el proyecto elegiremos Standard y un CSV pequeño. Consultar [precios vigentes](https://developers.cloudflare.com/r2/pricing/) y el consumo de la cuenta.

## 2. Crear el bucket privado

1. Crear un bucket llamado `cloudtrack-datos` o anotar el nombre que elijas.
2. Seleccionar Standard para la clase de almacenamiento. Para comenzar no hace falta configurar una jurisdicción específica.
3. Mantener deshabilitados el acceso público, r2.dev y dominios personalizados. Streamlit leerá el objeto desde el servidor con credenciales; no hace falta hacer público el archivo ni configurar CORS para el navegador.
4. En el bucket crear un prefijo/carpeta `raw` y subir un CSV válido con nombre `orders.csv`. Para reproducir la referencia original de 600 pedidos, usar `data/orders_cloud_reference.csv`; la demo local actual `data/orders_demo.csv` tiene 100 pedidos distintos. La ruta final debe ser `raw/orders.csv`, independientemente del nombre del archivo original.

La carga se hace con tu sesión del panel de Cloudflare. El dashboard de analítica no tendrá permiso para escribir o borrar archivos.

## 3. Crear credenciales de lectura

1. Desde la configuración R2 de la cuenta, abrir Manage R2 API Tokens y crear una credencial para la aplicación.
2. Elegir el permiso `Object Read only` y limitar el alcance únicamente al bucket del proyecto. No elegir permisos administrativos o de escritura para el dashboard.
3. Copiar el Access Key ID y el Secret Access Key. El secreto se muestra al crearlo y debe guardarse en un lugar privado.
4. Copiar también el endpoint S3 API de R2 que muestra la cuenta. No es la URL pública r2.dev y no incluye el bucket o el nombre del CSV.

Si el bucket tiene jurisdicción específica, copiar su endpoint correspondiente tal como aparece en Cloudflare. El código admite endpoints normales y jurisdiccionales de R2 y exige HTTPS. El panel requiere el endpoint de R2; no utiliza otro proveedor si falta ese valor.

## 4. Configurar secretos

Para probar localmente, copiar `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y reemplazar los valores. Ese archivo está excluido de Git. Reiniciar Streamlit después de crearlo o cambiarlo.

Para la app publicada, entrar en su configuración de Streamlit Community Cloud → Secrets y pegar TOML de este formato:

```toml
CLOUDTRACK_S3_BUCKET = "cloudtrack-datos"
CLOUDTRACK_S3_KEY = "raw/orders.csv"
CLOUDTRACK_S3_ENDPOINT = "https://TU_ACCOUNT_ID.r2.cloudflarestorage.com"
AWS_ACCESS_KEY_ID = "TU_R2_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "TU_R2_SECRET_ACCESS_KEY"
```

Los nombres AWS los reconoce boto3, pero los valores son las credenciales creadas en Cloudflare. La aplicación configura la región `auto` para R2. No pegar claves AWS ni un AWS_SESSION_TOKEN de otra cuenta. Nunca enviar secretos por el chat, incluirlos en capturas ni subirlos a GitHub.

El [PR de Cloudflare R2 #3](https://github.com/SatoJoe762/cloudtrack-analytics/pull/3) ya se integró en main. En una instalación nueva, comprobar que el despliegue incluya ese soporte antes de probar la opción cloud. Guardar secretos no actualiza por sí solo una versión antigua del código.

## 5. Comprobar la integración real

1. Abrir el dashboard, seleccionar `Almacenamiento cloud` y mantener todas las ciudades/categorías y el rango de fechas.
2. Solo si se subió la referencia original de 600 pedidos, esperar ventas entregadas BOB 535.460,90, 255 entregas tardías y 2,89 días de retraso medio. Con otro CSV, usar sus propios resultados validados.
3. Comparar con el mismo archivo mediante Cargar CSV usando los mismos filtros. La demostración local de 100 pedidos tiene resultados diferentes.
4. Probar una ruta equivocada y comprobar el mensaje de error, luego restaurar la ruta correcta.
5. Registrar fecha, commit desplegado, URL y captura sin secretos para el informe. Pedir a un compañero que abra el dashboard desde otro dispositivo.

El bucket es privado; el dashboard publicado puede mostrar los datos a cualquier visitante que tenga acceso a la aplicación. Mantener datos sintéticos para la demo pública. Cada interacción y cada revisión automática activa de 30 segundos en modo cloud hacen una lectura del objeto, sin caché compartida ni escrituras. El control de actualización del sidebar permite pausar las revisiones o leer inmediatamente. Para agregar pedidos, editar el CSV fuera del panel, validarlo y reemplazar el objeto con la misma ruta; no hace falta desplegar código.

## Si algo falla

- Cloudflare R2 aún no está configurado en este equipo: revisar .streamlit/secrets.toml y reiniciar Streamlit. Los secretos de la app publicada no se sincronizan con el equipo local.
- Endpoint inválido: copiar el endpoint S3 API de R2, con HTTPS y sin rutas, parámetros o credenciales en la URL.
- Error de lectura: revisar bucket, ruta, credenciales, alcance del permiso y si el objeto existe. Si el token expiró o fue revocado, reemplazarlo en Secrets.
- No aparece Almacenamiento cloud: el código del PR todavía no se integró o la aplicación no terminó de actualizarse.
- El archivo supera 10 MB: es el límite que establecimos en CloudTrack, no la cuota de R2.

## Al terminar el curso

Conservar una copia local del CSV, revocar credenciales que ya no se utilicen y revisar los recursos y la suscripción activos en Cloudflare. Si cambian el secreto, actualizarlo en Streamlit; no publicarlo mediante un commit.

Fuentes oficiales: [inicio y activación](https://developers.cloudflare.com/r2/get-started/), [credenciales y permisos](https://developers.cloudflare.com/r2/api/tokens/), [boto3](https://developers.cloudflare.com/r2/examples/aws/boto3/).
