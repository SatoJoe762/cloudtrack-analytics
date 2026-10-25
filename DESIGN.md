---
name: CloudTrack Analytics
description: Panel BI de ventas entregadas y cumplimiento, con controles nativos de Streamlit.
colors:
  primary: "#4F46E5"
  primary-hover: "#4338CA"
  secondary: "#2563EB"
  accent: "#0891B2"
  success: "#059669"
  warning: "#B45309"
  danger: "#DC2626"
  background: "#F5F7FC"
  surface: "#FFFFFF"
  ink: "#172033"
  muted: "#64748B"
  line: "#E2E8F0"
  soft: "#EEF2FF"
  sidebar: "#151E38"
  sidebar-surface: "#202C49"
  sidebar-ink: "#F1F5FF"
  sidebar-muted: "#B7C5DF"
  category-violet: "#9333EA"
  category-pink: "#DB2777"
  category-slate: "#475569"
  sidebar-focus: "#A5B4FC"
  sidebar-border: "#40506D"
  sidebar-tag: "#334365"
  sidebar-divider: "#35415C"
  sidebar-hover: "#2C3B5B"
typography:
  display:
    fontFamily: 'Inter, "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "1.95rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.035em"
  headline:
    fontSize: "1.25rem"
    fontWeight: 650
    letterSpacing: "-0.02em"
  title:
    fontSize: "1rem"
    fontWeight: 650
    letterSpacing: "-0.01em"
  metric:
    fontSize: "1.95rem"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-0.035em"
  label:
    fontSize: "0.78rem"
    fontWeight: 550
  caption:
    fontSize: "0.8rem"
    lineHeight: 1.5
  chart:
    fontFamily: "Inter, Source Sans 3, sans-serif"
    fontSize: "12px"
rounded:
  card: "14px"
  control: "8px"
  filter-state: "6px"
  tag: "5px"
spacing:
  "1": "0.25rem"
  "2": "0.5rem"
  "3": "0.75rem"
  "4": "1rem"
  "5": "1.5rem"
  "6": "2rem"
components:
  button-reset:
    backgroundColor: "{colors.sidebar-surface}"
    textColor: "{colors.sidebar-ink}"
    rounded: "{rounded.control}"
  button-reset-hover:
    backgroundColor: "{colors.sidebar-hover}"
  button-download:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.control}"
  button-download-hover:
    backgroundColor: "{colors.soft}"
  input-date:
    backgroundColor: "{colors.sidebar-surface}"
    textColor: "{colors.sidebar-ink}"
    rounded: "{rounded.control}"
  tabs:
    textColor: "{colors.muted}"
  tabs-active:
    textColor: "{colors.primary}"
  source:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0.65rem 0.85rem"
  kpi:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "1.15rem 1rem 0.9rem"
  insights:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "1rem 1.25rem 0.75rem"
  chart-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "1.1rem 1.1rem 0.5rem"
---

# Design System: CloudTrack Analytics

## Overview

**Creative North Star: "La mesa de análisis BI"**

La dirección elegida combina la claridad de Power BI y Tableau con superficies SaaS: lateral azul profundo, acentos índigo y azul, fondo gris azulado y tarjetas blancas. La marca geométrica y los iconos lineales acompañan una lectura sobria de cifras, unidades y contexto.

La presentación conserva Streamlit como interfaz nativa. Fuente, selección y resultados verificables comparten un lenguaje visual; las observaciones son descriptivas. Este documento registra el rediseño implementado y reemplaza la anterior identidad verde.

**Key Characteristics:**

- Contraste entre lateral profundo y superficies claras.
- Cifras tabulares, unidades visibles y etiquetas junto al color.
- Tarjetas de borde fino y controles nativos.
- Composición adaptable con iconos decorativos discretos.

## Colors

Los valores de frontmatter reflejan la implementación. `assets/design-tokens.json` es la fuente de color ejecutable: `dashboard_styles()` inyecta sus cadenas como variables `--ct-*` y Plotly consume los mismos tokens. Los colores adicionales de categorías provienen de su lista; los auxiliares del lateral se extraen del CSS. `.streamlit/config.toml` refleja la paleta para widgets nativos y usa el acento claro `sidebar-focus` en el lateral.

### Primary

- **Índigo de análisis** (`primary`): ventas, cifra principal, marca, pestaña activa, foco principal y acciones de descarga.
- **Índigo profundo** (`primary-hover`): token disponible en el JSON; los botones implementados usan sus estados específicos, no un relleno índigo universal.

### Secondary

- **Azul de cumplimiento** (`secondary`): puntualidad por ciudad, estado En tránsito e icono de entregados.
- **Cian de apoyo** (`accent`): ticket e identificación de categorías.
- **Verde de entrega**, **ámbar de atención** y **rojo de cancelación** (`success`, `warning`, `danger`): estados o iconos con significado textual explícito. El verde es semántico, no la identidad de marca.
- **Violeta, rosa y pizarra de categoría**: completan la paleta categórica.

### Neutral

- **Fondo bruma**, **blanco de tarjeta**, **tinta** y **texto auxiliar** (`background`, `surface`, `ink`, `muted`): capas y jerarquía.
- **Línea suave** y **lavado índigo** (`line`, `soft`): delimitación, filtros activos y hover de descargas/pestañas.
- **Azul profundo**, **superficie lateral**, **tinta clara** y **texto lateral auxiliar**: marca, filtros y contexto sobre el lateral.
- Los auxiliares `sidebar-focus`, `sidebar-border`, `sidebar-tag`, `sidebar-divider` y `sidebar-hover` sostienen foco, campos, selecciones y estados.

**The Visible Meaning Rule.** Cada color de datos conserva nombre, unidad o etiqueta; el color por sí solo no identifica una categoría o estado.

La paleta categórica sigue el orden primary → accent → secondary → warning → category-violet → success → category-pink → category-slate. Se asigna por orden alfabético del conjunto completo y permanece estable al filtrar. Sus ocho colores se repiten cíclicamente si hay más categorías; no garantizan identificadores únicos. Las rampas del sidecar son muestras derivadas para el panel, no nuevos tokens de la aplicación.

## Typography

**Display / Body Font:** Inter si está disponible localmente; en caso contrario, Source Sans 3 suministrada por Streamlit, seguida de fuentes del sistema. No se descarga una fuente externa. Plotly comparte las dos primeras familias.

La cabecera usa `display`; secciones y gráficos usan `headline` y `title`. Las cifras KPI usan `metric`, números tabulares y envoltura de texto, incluidos «Sin entregas». No se fija una escala nueva para el cuerpo nativo. El subtítulo usa tamaño (0.9rem) y ancho máximo (65ch); insights destacan nombres (1.2rem, peso 650, interlineado 1.3). Los captions conservan opacidad plena. Plotly usa ejes (11px) y hover (13px).

En móvil, cabecera y secciones bajan a (1.6rem / 1.15rem), KPI a (1.5rem) y etiquetas KPI a (0.72rem). Las ayudas nativas permanecen disponibles.

## Layout

El contenedor principal tiene ancho máximo (1600px), padding (3.8rem 2rem 2rem) y ritmo basado en los seis pasos de `spacing`. Cabecera y contexto permiten envolver fuente, fechas y filtros activos. El lateral conserva su apertura/cierre nativos.

Los cuatro KPI forman cuatro columnas; a (1250px) o menos pasan a dos, con padding horizontal principal (1.5rem). No hay una regla propia de una sola columna KPI. Los gráficos de Ventas usan proporción (3:2), los de Entregas (2:3). Entre (641px) y (1050px) se apilan explícitamente; en móvil interviene el apilado nativo.

A (640px) o menos, el contenido usa padding (3.75rem 1rem 1.5rem). Los KPI conservan dos columnas con gap (0.65rem), altura mínima (140px) y ocultan los iconos decorativos. Los insights se apilan y sustituyen su divisor vertical por uno horizontal; fechas y resumen de selección ocupan líneas propias. Se compactan fuente, pestañas y tarjetas gráficas. Las tablas conservan su navegación nativa dentro del componente.

## Elevation & Depth

La separación procede del fondo, las tarjetas blancas y bordes finos. El CSS declara `--ct-shadow` (`0 3px 12px rgb(23 32 51 / 5%)`), pero las tarjetas implementadas no lo aplican; no constituye una elevación visible obligatoria. Widgets y popovers conservan tratamientos del framework.

Las transiciones de color y borde duran (160ms, ease-out). No hay desplazamiento decorativo. `prefers-reduced-motion: reduce` desactiva transiciones y animaciones y restaura el scroll automático.

## Shapes

Tarjetas, insights y uploader usan `card`; campos, botones, fuente y expanders usan `control`. Filtros activos y selecciones laterales usan esquinas más pequeñas. Los bordes de tarjeta son (1px). La marca es un bloque geométrico con icono SVG local; los iconos propios son decorativos y llevan `aria-hidden="true"`.

## Components

### Buttons and native controls

Restablecer ocupa el ancho lateral; descargas usan superficie blanca con texto índigo y hover suave. Ambos mantienen altura mínima (44px), radio `control` y estados nativos. Radio de fuente, multiselects, uploader, calendario, expanders y tablas siguen siendo Streamlit; las selecciones laterales usan tags.

El rango nativo y el resumen visible usan **DD/MM/YYYY**. Cambiar fuente o contenido restablece filtros compatibles. El foco visible recibe contorno (2px) y separación (3px) en botones, enlaces, inputs, pestañas y summary; botones e inputs laterales usan acento claro. Los subcontroles internos conservan el comportamiento del framework; no se afirma cobertura exhaustiva de foco.

### Navigation and source

Ventas, Entregas y Datos y metodología son pestañas nativas: texto auxiliar, activo índigo, indicador inferior y hover suave. La etiqueta de fuente es informativa, no un botón. «Panel de análisis» en el lateral identifica la vista actual, no añade una ruta.

### KPI cards

Ventas entregadas · BOB; Pedidos entregados; Entregas a tiempo; Ticket promedio · BOB. Cada tarjeta mantiene métrica y ayuda nativas, contexto y denominador. La cifra de ventas es índigo; los iconos no transmiten información exclusiva. Sin entregados, los promedios y porcentajes muestran «Sin entregas».

Entregas conserva un panel secundario de entregas tardías, retraso medio entre tardías y tiempo medio de entrega. Datos mantiene el total de pedidos registrados.

### Insights

Un panel compartido presenta categoría de mayor venta y ciudad de menor puntualidad. Expone todos los empates alfabéticamente, omite cuota si las ventas son cero y evita comparar ciudades cuando solo hay una. Sin entregados se omite. La advertencia de alcance descriptivo permanece visible.

### Chart cards

Área índigo para ventas diarias, barras categóricas multicolor, estados verde/azul/rojo y puntualidad azul. Las leyendas redundantes están ocultas; nombres de ejes, categorías, etiquetas de estado y porcentajes identifican los datos. No todos los valores tienen etiqueta persistente: ventas y categorías muestran detalle en hover.

Altura base (310px), crecimiento por fila (42px) en categorías/ciudades, fondo transparente y rejilla del token `line`. Puntualidad extiende el eje hasta (105%) para etiquetas. La línea temporal conecta observaciones disponibles y lo explica en caption. Plotly desactiva scroll zoom y su logotipo; exporta PNG a escala 2.

### States, data and exports

Mensajes nativos cubren CSV pendiente/inválido, rango incompleto, selección vacía, ausencia de entregados y configuración o fallo R2. Demostración identifica los datos sintéticos. CSV permanece en sesión; R2 se lee sin modificar el objeto. Tablas sin índice y descargas CSV/JSON corresponden a la selección activa.

Se conservan fórmulas de analítica, almacenamiento y reporting, sin nuevas dependencias. Ventas y ticket consideran entregados; puntualidad compara fecha real y prometida; los filtros usan fecha del pedido. El rediseño presenta esos resultados sin redefinirlos.

## Do's and Don'ts

### Do

- Do mantener sincronizados JSON de color, CSS, Plotly y tema nativo.
- Do conservar etiquetas, unidades, fuente, denominadores y estados sin datos.
- Do mantener controles nativos, foco visible y reducción de movimiento.
- Do revisar móvil, etiquetas largas y widgets tras actualizar Streamlit.

### Don't

- Don't restablecer el verde como identidad principal.
- Don't usar color como identificador único ni prometer colores únicos para más de ocho categorías.
- Don't convertir insights en causalidad o predicción ni ausencia de promedio en cero.
- Don't presentar esta documentación como auditoría WCAG completa o aprobación del revisor.

**Evidencia registrada y límites no canonizados.** Se registraron 57 pruebas aprobadas; navegador en siete anchos de 375 a 1440, las tres pestañas sin desbordamiento horizontal de página ni errores JS; carga real de CSV demo, rechazo de CSV inválido y fuente R2 real con 600 pedidos usando el entorno existente; foco y reducción de movimiento verificados. Las seis capturas completas y los resultados están en `.impeccable/review/`. Son comprobaciones registradas de la sesión, no repetidas por esta documentación. La revisión independiente dio disposición `ship` a las seis correcciones solicitadas y al contraste de tags; ese veredicto cubre esos ajustes. El CSS usa selectores internos Streamlit/BaseWeb y contenedores con key, sujetos a cambios. No hubo pruebas en dispositivos físicos ni lector de pantalla; los resultados no acreditan cobertura WCAG exhaustiva. Estos límites no son reglas de diseño.
