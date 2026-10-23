---
name: CloudTrack Analytics
description: Sistema claro para explorar ventas entregadas y cumplimiento por ciudad.
colors:
  primary: "#12624C"
  ink: "#193D31"
  muted: "#536B62"
  background: "#FFFFFF"
  soft: "#F3F7F4"
  line: "#DCE6E0"
  punctuality: "#426B91"
  cancelled: "#8C6B71"
  source-background: "#E8F2EC"
  source-border: "#C7DECF"
typography:
  display:
    fontSize: "2.5rem"
    lineHeight: 1.12
    letterSpacing: "-0.035em"
  headline:
    fontSize: "1.45rem"
    letterSpacing: "-0.02em"
  title:
    fontSize: "1.1rem"
  metric:
    fontSize: "2.1rem"
    fontWeight: 650
    letterSpacing: "-0.03em"
  chart:
    fontFamily: "Arial, sans-serif"
    fontSize: "13px"
rounded:
  insights: "14px"
  source: "100px"
spacing:
  kpi-gap: "1.5rem"
  insights-padding: "1.2rem 1.4rem"
  page-padding: "2.4rem 3rem 3rem"
components:
  source:
    backgroundColor: "{colors.source-background}"
    textColor: "{colors.primary}"
    rounded: "{rounded.source}"
    padding: ".4rem .8rem"
  insights:
    backgroundColor: "{colors.soft}"
    rounded: "{rounded.insights}"
    padding: "{spacing.insights-padding}"
---

# Design System: CloudTrack Analytics

## Overview

CloudTrack conserva su identidad existente: una herramienta académica de análisis en modo **Operate**, clara para exposición en aula y con controles nativos de Streamlit. El refinamiento precisa la jerarquía, la lectura de cifras y el lenguaje de datos; no introduce otra marca, una tipografía externa ni una nueva metáfora visual.

El fondo blanco, el verde profundo y las superficies suaves organizan una interfaz de densidad moderada. La cabecera identifica el producto y su fuente; el contexto de selección precede a los indicadores; las observaciones descriptivas ayudan a interpretar los gráficos. Esta especificación registra decisiones implementadas en `app.py`, `assets/dashboard.css`, `cloudtrack/presentation.py` y `.streamlit/config.toml`.

**Key Characteristics:**

- Jerarquía textual y unidades explícitas para exposición y verificación.
- Filtros laterales y tres pestañas de análisis.
- Superficies planas, líneas suaves y color acompañado de texto.
- Fuente visible y aviso permanente de datos sintéticos en demostración.

## Colors

La paleta mantiene el verde del proyecto y añade un azul sobrio para comparar puntualidad. Los valores de frontmatter son los tokens normativos.

### Primary

- **Verde de análisis** (`primary`): ventas, entregados, marca lateral, pestaña activa, foco visible y acento del tema.

### Secondary

- **Azul de cumplimiento** (`punctuality`): barras de puntualidad por ciudad y estado «En tránsito». El significado depende del título y las etiquetas; no es un estado universal de éxito.
- **Malva de cancelación** (`cancelled`): «Cancelado», acompañado de nombre y cantidad.

### Neutral

- **Tinta verde** (`ink`): texto principal y cabecera.
- **Verde auxiliar** (`muted`): subtítulos, captions, selección, explicación de insights y pie.
- **Blanco de exposición** (`background`): fondo principal.
- **Fondo suave** (`soft`): lateral del tema y bloque de lectura de selección.
- **Línea suave** (`line`): separadores de cabecera, lateral, pestañas, indicadores y pie.
- **Fuente identificada** (`source-background`, `source-border`): fondo y borde de la etiqueta informativa de origen.

**Regla de significado visible.** El color conserva una etiqueta, unidad o contexto textual. La información de estado no depende solo del color.

Plotly mantiene valores auxiliares propios para texto (`#243D35`), rejilla (`#E5ECE8`) y controles (`#5C7169`): hay una pequeña divergencia respecto de los neutrales principales. La constante ámbar (`#A66B16`) existe en presentación, pero no se aplica a los gráficos actuales y no se promueve a token activo. Las alertas conservan los colores nativos de Streamlit. Los captions usan opacidad plena para sostener el contraste del color auxiliar.

## Typography

**Body Font:** sans serif del tema de Streamlit; la familia concreta depende del framework. **Chart Font:** Arial con fallback sans serif. No se carga una fuente de marca adicional.

La cabecera usa `display`; las secciones, `headline`; los títulos de gráficos, `title`. El subtítulo principal tiene tamaño (`1rem`) y ancho máximo (`65ch`). Los valores KPI usan `metric` y números tabulares. Etiquetas y valores permiten envolver el texto para mostrar «Sin entregas» sin truncado.

Los insights distinguen título auxiliar (`.85rem`), nombre destacado (`1.2rem`, peso 650, interlineado 1.4) y explicación (`.9rem`, interlineado 1.5). La fuente usa (`.85rem`, peso 600); el pie, (`.82rem`). En gráficos el hover usa (`14px`) y los títulos de ejes, (`12px`). Los pesos no especificados conservan los del framework.

## Layout

El contenido principal tiene ancho máximo (`1440px`) y padding `page-padding`. La cabecera usa flex y puede envolver la fuente debajo del título. El lateral agrupa fuente, carga de archivo cuando corresponde, restablecimiento, ciudades, categorías y fecha del pedido.

Los cuatro indicadores usan **CSS grid de cuatro columnas** sobre las columnas nativas. A un viewport de (`1150px`) o menos pasan a **dos columnas**, con gap vertical (`.75rem`) y horizontal (`1.5rem`); no hay regla propia de una columna. En ese umbral el padding principal pasa a (`2rem 1.6rem`).

A (`640px`) o menos, el padding pasa a (`1.5rem 1rem`), el título a (`1.9rem`), los valores KPI a (`1.55rem`) y se compactan pestañas e insights. Streamlit determina el resto del apilado: observaciones en dos columnas, gráficos de ventas en proporción (`3:2`), gráficos de entregas (`2:3`) y descargas en dos columnas. No hay breakpoint propio para estos grupos.

Orden de navegación: **Ventas**, **Entregas**, **Datos y metodología**. El contexto de selección muestra fechas, ciudades, categorías y pedidos seleccionados frente al total. Los gráficos tienen altura base (`330px`); categorías y ciudades crecen según la cantidad de filas (`38px` por fila como mínimo de cálculo).

## Elevation & Depth

La capa CSS del proyecto no añade sombras. La profundidad surge de superficies suaves, líneas y espacio entre secciones. Los controles nativos pueden conservar tratamientos del framework; no se define un sistema adicional de elevación ni animaciones propias.

## Shapes

Los insights usan la esquina `insights`; la fuente usa la cápsula `source` con borde fino. Los indicadores tienen línea inferior (`2px`), sin tarjetas cerradas. Botones, inputs, desplegables, tablas y alertas mantienen formas nativas. No se inventan radios ni estados hover personalizados.

## Components

### Cabecera y fuente

Título y descriptor «Comercio electrónico y entregas · Ventas y cumplimiento por ciudad», junto a una etiqueta informativa para Demostración, CSV de esta sesión, Cloudflare R2 o Amazon S3. La etiqueta no es interactiva. Se identifica R2 cuando existe un endpoint configurado.

### Filtros y botones

Radio de fuente, uploader CSV, multiselects y calendario nativos. Restablecer ocupa el ancho lateral y tiene altura mínima (`2.7rem`); las descargas tienen altura mínima (`2.75rem`). Cambiar fuente o contenido reinicia filtros para mantener opciones compatibles. El foco visible de botones, enlaces e inputs recibe contorno verde (`2px`) separado (`3px`). Hover, disabled y otros estados internos siguen al framework; no se define foco personalizado para todos los subelementos de multiselect o calendario.

### Indicadores

Pedidos registrados; ventas entregadas en BOB; entregas a tiempo; tiempo medio de entrega en días. Ayudas y caption explican los denominadores. Sin entregados, puntualidad y tiempo muestran «Sin entregas»; ventas y conteo conservan las cifras válidas. Entregas añade cantidad tardía y promedio de retraso entre tardías, con «Sin entregas tardías» cuando corresponde.

### Lectura de la selección

Bloque descriptivo solo sobre entregados: categoría de mayor venta y ciudad de menor puntualidad. Los empates enumeran todos los nombres en orden alfabético. La cuota corresponde a cada categoría indicada; con ventas totales cero, se explica el cero y se omite el porcentaje. Con una sola ciudad se indica su puntualidad sin sugerir comparación. Sin entregados se omite el bloque. Las observaciones no atribuyen causas ni predicen resultados.

### Gráficos

Ventas en el tiempo usa área verde con línea (`2.5px`) y relleno de opacidad (`.09`), agrupada por fecha del pedido. El hover unifica la fecha y muestra BOB con dos decimales. Las fechas sin observaciones no se rellenan: el caption avisa que la línea conecta días disponibles.

Categorías usa barras horizontales verdes. Estados usa barras con nombres, cantidades y colores explícitos. Puntualidad por ciudad usa barras azules, porcentaje con un decimal y conteo de entregados en hover; el eje se extiende a (`105%`) para alojar etiquetas. Se ocultan leyendas redundantes y el logotipo de Plotly, se desactiva scroll zoom y se permite exportar PNG a escala 2. Fondos transparentes y márgenes automáticos mantienen continuidad con la página.

### Navegación, tablas y exportaciones

Pestañas con separador inferior y texto activo verde de peso 650; la interacción por teclado y estados internos pertenecen a Streamlit/BaseWeb. Las tablas nativas ocultan el índice y ocupan el ancho disponible. Cumplimiento muestra ciudad, entregados, porcentaje y días promedio; Datos muestra las columnas originales verificables. CSV y reporte JSON exportan solo la selección activa. Metodología y resumen JSON usan expanders.

### Estados y confianza

- Sin CSV: mensaje informativo para seleccionar el archivo; se detiene el análisis.
- Rango incompleto: mensaje informativo para completar ambas fechas.
- Sin pedidos seleccionados: advertencia para ampliar fechas o ciudades.
- Sin entregados: avisos específicos en ventas y puntualidad; no se inventan observaciones.
- CSV inválido: error de validación visible. Fallo cloud: error con orientación sobre endpoint, credenciales, bucket y objeto.
- Datos válidos: confirmación con total y selección en Datos y metodología.

Demostración mantiene el aviso «Datos sintéticos de demostración. No representan una empresa real.». CSV aclara que el archivo solo dura en la sesión; cloud aclara que el bucket privado se lee sin modificar el archivo. El pie recuerda usar datos sintéticos o autorizados e importes en bolivianos.

La presentación preserva las fórmulas de `cloudtrack/analytics.py`: ventas y ticket medio consideran entregados; puntualidad usa entregados en fecha prometida o antes; días son calendario; retraso medio considera solo tardías; los filtros usan `order_date`. Los helpers de presentación dan estilo y observaciones descriptivas sin sustituir esas fórmulas.

## Do's and Don'ts

### Do

- Conservar identidad, componentes nativos y tema claro para exposición.
- Mantener unidad, fuente, denominador y alcance de filtros junto a los resultados.
- Mostrar empates, ceros y ausencia de datos explícitamente.
- Preservar fórmulas y aviso de datos sintéticos en demostración.
- Revisar indicadores, pestañas y controles después de actualizar Streamlit.

### Don't

- Convertir observaciones descriptivas en causalidad o predicción.
- Mostrar un porcentaje o promedio inexistente como cero.
- Introducir marca, escala tipográfica o estado visual sin evidencia de implementación.
- Asumir que el CSS personalizado constituye una API estable del framework.

**Validación y límites.** La revisión del equipo incluye capturas de escritorio y Entregas a ancho 1440, y móvil a ancho 390; el hallazgo de contraste se resolvió con opacidad plena en captions. No se ha probado lector de pantalla ni otros dispositivos físicos. El CSS depende de `data-testid` de Streamlit, atributos BaseWeb y contenedores con key; los primeros dos son detalles internos susceptibles a cambios. Algunas reglas tipográficas, captions, métricas y foco son globales. La regla de overflow de Plotly puede recortar contenido que exceda el contenedor y debe revisarse con etiquetas largas. La paleta auxiliar de Plotly mantiene la divergencia descrita y los widgets mantienen estados nativos. Esta actualización se limita a `DESIGN.md`: no genera sidecar ni cambia código, datos o cálculos.
