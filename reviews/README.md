# Registro de revisión

Se aplicaron 20 perspectivas profesionales simuladas con IA en tres rondas consecutivas. No son dictámenes de 20 personas contratadas ni testimonios profesionales. Cada perspectiva examinó el resultado de la anterior, registró diez observaciones, formuló un prompt y aplicó una mejora antes de continuar.

- [Ronda 1: fundamentos](round-1.json)
- [Ronda 2: refinamiento](round-2.json)
- [Ronda 3: cierre y comprobación](round-3.json)

Los 60 registros contienen 600 observaciones y 60 prompts. Las observaciones distinguen defectos comprobados, decisiones de diseño y cualidades que conviene conservar; no equivalen a 600 defectos. Cada registro enlaza su commit de implementación, los archivos modificados y su validación.

Las perspectivas abarcan dirección de arte, diseño gráfico, composición espacial, diseño web, tipografía, diagramas, fotografía, arquitectura de información, interacción, accesibilidad, selección tecnológica, contratación en consultoría, copywriting, posicionamiento, contenidos, SEO técnico, SEO semántico, edición científica, métodos estadísticos y calidad técnica.

## Validación de cierre

La construcción estática y las tres baterías de navegador pasan. Se comprobaron las 26 páginas bilingües, navegación sin JavaScript, pantallas de 320 a 1440 píxeles, ampliación de texto al 200 %, filtros y cambio de idioma, parámetros del laboratorio, foco del menú, citas y metadatos. Axe no detectó infracciones automáticas en las siete rutas evaluadas; esto no constituye una certificación de accesibilidad ni sustituye una prueba con usuarios.

La impresión del perfil se exportó y revisó visualmente en A4: dos páginas en español y dos en inglés, sin páginas vacías ni contenido recortado. Los PDF y las capturas son evidencias locales de QA y no forman parte del sitio publicado. Las imágenes sociales y la captura de PBIS se revisaron visualmente; esta última muestra datos sintéticos de demostración.

Fecha de referencia: 16 de noviembre de 2026. La indexación, el posicionamiento y la disponibilidad futura de repositorios externos no se garantizan.

## Micromejoras gráficas del 17 de noviembre

Una revisión posterior preparó [20 prompts acotados](micro-2026-11-17-prompts.json), ejecutados uno a uno por tres subagentes de IA. El [registro de resultados](micro-2026-11-17-results.json) conserva la solución aplicada, los archivos, las comprobaciones y un commit de implementación distinto por prompt. Complementa las tres rondas anteriores.

Los ajustes refinan cabecera, navegación, foco, botones, retratos, etiquetas, diagramas, columnas para empresas, cronología, índice de casos, ampliación de captura, publicaciones, filtros, laboratorio y pie móvil. Se conservan el contenido científico, los datos, las fotografías y los cálculos. La fecha de actualización visual del sitio pasa al 17 de noviembre; la fecha de captura de PBIS permanece en el 16.

El cierre de estas micromejoras pasó la comprobación estática y las tres baterías de navegador existentes. Axe evaluó siete rutas sin infracciones automáticas. Se revisaron también dos páginas A4 por idioma del perfil, sin recortes.
