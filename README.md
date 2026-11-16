# Antonio Alfonso — portfolio profesional

Web estática bilingüe para GitHub Pages. El contenido y los enlaces principales existen en HTML, también sin JavaScript. Sin servicios de seguimiento, cookies propias ni dependencias de ejecución.

## Construir y revisar

```sh
python build.py
python -m http.server 8078 --directory public
```

Verificación estática: `python tests/check_static.py`. Para revisar la interacción: instalar Playwright y Chromium (`python -m pip install playwright`, `python -m playwright install chromium`), iniciar el servidor anterior y ejecutar `python tests/browser_check.py`. Opcionalmente, `PLAYWRIGHT_CHROMIUM_EXECUTABLE` permite indicar un Chromium existente y `TEST_BASE_URL` otra URL de prueba. Las capturas se guardan en `qa/`, excluido del repositorio.

Editar `data/publications.json`, `data/projects.json`, `build.py` y `assets/`. `build.py` usa únicamente la biblioteca estándar de Python. El workflow publica exclusivamente `public/`; los documentos privados de trabajo no forman parte del repositorio.

La URL canónica se configura con `SITE_URL` y por defecto es `https://teoriadejuego.github.io`. La portada es española; `/en/` contiene la versión inglesa. Los artículos mantienen sus títulos originales.

## Criterios editoriales

- El papel individual se distingue de los resultados del equipo.
- Las aplicaciones en evaluación y los datos sintéticos se identifican expresamente.
- Los trabajos seleccionados se destacan por relevancia, alcance y evidencia; no se presenta una clasificación bibliométrica sin verificar.
- Las descargas de artículos apuntan al repositorio o editor que conserva la versión. No se redistribuyen PDFs editoriales en este repositorio.
- Los enlaces institucionales pueden tener protección antibots o cambiar. Cada entrada incluye el DOI y una alternativa cuando existe.
- Fecha de referencia: 16 de noviembre de 2026.

## Publicación y buscadores

El workflow construye y publica en GitHub Pages. Incluye sitemap, robots.txt, URL canónica, hreflang, Open Graph y datos estructurados Person/ProfilePage y ScholarlyArticle. La indexación y el posicionamiento dependen de Google y no se garantizan. Después del despliegue, el propietario puede verificar el dominio en Search Console y enviar `/sitemap.xml`.

No se modifica el dominio `antonioalfonso.org`: su migración requiere una decisión y acceso DNS independientes.

## Referencias

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Google Search Essentials](https://developers.google.com/search/docs/essentials/technical)
- [Datos estructurados de perfiles](https://developers.google.com/search/docs/appearance/structured-data/profile-page)

Los prompts aplicados están en `PROMPTS.md`; la trazabilidad editorial, en `SOURCES.md`.
