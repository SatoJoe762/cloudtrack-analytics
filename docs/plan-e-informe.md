# Plan de cuatro semanas e informe

## Semana 1 — Base y datos

Invitar a los cinco integrantes, acordar contrato CSV y reglas de revisión. Ejecutar el proyecto en cada equipo. Crear issues para datos, KPIs, panel, cloud e informe. Definir preguntas: ¿qué categoría genera más ventas entregadas?, ¿qué ciudad tiene peor puntualidad?, ¿cómo cambian por período? Cada integrante debe cerrar una tarea mediante PR.

Aceptación: todos ejecutan demo y pruebas; contrato y fórmulas revisados en equipo.

## Semana 2 — Análisis y panel

Ampliar segmentaciones justificadas, revisar fórmulas con un conjunto pequeño calculado a mano, ajustar etiquetas y probar archivos inválidos. Definir cualquier ampliación como issue antes de programarla; una tienda online completa queda fuera del alcance.

Aceptación: filtros coherentes, indicadores con denominadores explícitos y gráficos que respondan preguntas de negocio.

## Semana 3 — Cloud

Publicar demo en Community Cloud, configurar S3 privado y credenciales de lectura, probar errores y documentar arquitectura, disponibilidad observada y costos estimados. Registrar tiempos con datasets crecientes sin superar el límite de carga.

Aceptación: URL operativa, lectura S3 real validada, CI en verde y evidencias sin secretos.

## Semana 4 — Informe y defensa

Consolidar resultados y limitaciones, revisar documentación y ensayar una demo de 8–10 minutos. Etiquetar versión v0.1.0 después de validar main. Tener el CSV sintético disponible para mostrar la demo local si la conexión falla.

Aceptación: cada integrante explica su contribución y al menos una decisión cloud; el equipo reproduce los resultados desde el README.

## Índice sugerido del informe

1. Portada y resumen.
2. Problema, justificación y preguntas de negocio.
3. Objetivo general: implementar y desplegar una solución cloud de análisis descriptivo de ventas y entregas. Objetivos específicos: validar datos, calcular indicadores, visualizarlos, proteger almacenamiento y validar el despliegue.
4. Alcance y exclusiones.
5. Marco conceptual: analítica descriptiva, servicios administrados, almacenamiento de objetos, IAM, CI y contenedores.
6. Arquitectura y elección tecnológica; alternativas consideradas y motivos.
7. Datos: origen sintético, diccionario, calidad, transformaciones y fórmulas.
8. Implementación y colaboración: estructura, issues, PR y aportes verificables.
9. Pruebas: resultados reales, casos inválidos y demostración cloud.
10. Resultados: hallazgos sobre el conjunto sintético, gráficos y limitaciones. No generalizar a empresas reales.
11. Costos y operación: región, fecha, supuestos, seguridad, mediciones y restricciones de escalabilidad.
12. Conclusiones y mejoras justificadas.
13. Referencias y anexos: URL, commit o tag, capturas y guía de ejecución.

## Guion de demostración

Explicar el problema → mostrar arquitectura → filtrar ciudad y período → interpretar ventas y puntualidad → cargar CSV inválido → mostrar S3 y el mismo análisis → enseñar un PR y CI → cerrar con límites y costos. No presentar pruebas simuladas de S3 como prueba de un despliegue real.
