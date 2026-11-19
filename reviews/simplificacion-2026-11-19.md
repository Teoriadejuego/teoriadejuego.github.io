# Simplificación del portfolio — 19 de noviembre de 2026

La comparación con [la web de Diego Jorrat](https://dajorrat.github.io/) mostró una presentación personal directa, acceso inmediato al CV, una lista legible de trabajos y visualizaciones vinculadas a su investigación. Se inspeccionaron ambas webs en un navegador sin interfaz visible. No se reutilizaron sus textos, imágenes, código, datos o credenciales profesionales.

La instrucción posterior del propietario —pocas cosas, bien contadas— determina el resultado: una portada breve que permita entender el perfil y elegir qué profundizar.

## Cambios

- Menú principal de cuatro destinos: Proyectos, Publicaciones, Perfil y Contacto. El nombre lleva al inicio; se mantiene el selector ES/EN. Contacto conduce a la sección de la portada desde cualquier página.
- Presentación más breve, retrato menor y fondo liso. Dos acciones: ver proyectos y consultar perfil/CV. El perfil conserva su opción de imprimir o guardar en PDF.
- Dos proyectos seleccionados, SONAR y ARCO, explicados mediante propósito, estado y aportación individual. Se retiran de la portada los diagramas, las etiquetas tecnológicas y los nombres internos de herramientas que necesitaban explicación adicional.
- Dos trabajos científicos destacados, con encabezados divulgativos y enlaces a sus fichas bibliográficas completas. Los títulos científicos originales y las fuentes permanecen en Publicaciones.
- Contacto directo y breve. Se eliminan la franja de credenciales y los bloques repetidos de capacidades y demostración. El laboratorio sigue accesible desde el pie.
- Se conservan las 26 páginas, el catálogo de proyectos, los 12 artículos, los working papers, las versiones abiertas, las citas y las explicaciones metodológicas. La simplificación afecta a la entrada y a la navegación, no elimina el archivo profesional.

## Resultado observado y validación

En español, el texto visible de la portada pasa de 633 a 245 palabras, incluyendo menú y pie. A 1440 px de ancho, en el mismo Chromium local, su altura pasa de 4008 a 2156 px. Son medidas de contenido y composición de esta captura, no métricas de rendimiento real de usuarios.

Comprobados ES/EN, cuatro secciones principales, dos proyectos con aportación explícita, dos trabajos, ausencia de los bloques retirados, navegación a Contacto desde Privacidad, funcionamiento sin JavaScript y ausencia de desbordamiento a 320, 390, 768 y 1440 px. Axe no detectó infracciones en ambas portadas. Se inspeccionaron las capturas de escritorio y móvil.

La prueba de regresión del menú se actualiza para comprobar Perfil como página activa y los cuatro destinos en las páginas secundarias; la antigua comprobación de diagramas de portada se sustituye por la selección de dos casos con aportación individual. El flujo existente mantiene las pruebas unitarias, las siete suites de navegador y la confirmación de los archivos publicados antes de declarar una entrega verificada.
