# Antonio Alfonso — portfolio profesional

Web estática bilingüe para GitHub Pages. El contenido y los enlaces principales existen en HTML, también sin JavaScript. Sin servicios de seguimiento, cookies propias ni dependencias de ejecución.

## Construir y revisar

```sh
python build.py
python tools/preview.py --port 8078
```

Python 3.12. El build valida los datos, genera un candidato limpio y lo verifica antes de sustituir `public/`. La fecha editorial y las selecciones de portada se editan en `data/site.json`. La reconstrucción no cambia la fecha por sí sola.

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium firefox
python -m unittest discover -s tests -p "test_*.py"
python build.py
python tests/check_static.py
python tools/release.py verify
python tools/fetch_axe.py
python tools/check_browser.py --firefox
python tools/measure.py
```

Los controles de navegador levantan su propio servidor local. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` permite indicar un Chromium existente. Las pruebas individuales aceptan `TEST_BASE_URL`. Capturas, resultados y axe se guardan en `qa/`, excluido del repositorio y de la distribución pública. Las mediciones locales no representan capacidad del hosting.

Editar `data/publications.json`, `data/projects.json`, `build.py` y `assets/`. `build.py` usa únicamente la biblioteca estándar de Python. El workflow publica exclusivamente `public/`; los documentos privados de trabajo no forman parte del repositorio.

La URL canónica se configura con `SITE_URL` y por defecto es `https://teoriadejuego.github.io`. La portada es española; `/en/` contiene la versión inglesa. Los artículos mantienen sus títulos originales.

## Criterios editoriales

- El papel individual se distingue de los resultados del equipo.
- Las aplicaciones en evaluación y los datos sintéticos se identifican expresamente.
- Los trabajos seleccionados se destacan por relevancia, alcance y evidencia; no se presenta una clasificación bibliométrica sin verificar.
- Las descargas de artículos apuntan al repositorio o editor que conserva la versión. No se redistribuyen PDFs editoriales en este repositorio.
- Los enlaces institucionales pueden tener protección antibots o cambiar. Cada entrada incluye el DOI y una alternativa cuando existe.
- Fecha editorial: `data/site.json`; fechas históricas de artículos y capturas conservadas.

## Publicación y buscadores

El workflow valida datos, recuperación, enlaces, accesibilidad automatizada y comportamiento en Chromium/Firefox antes de publicar en GitHub Pages. Las pull requests solo validan. Incluye sitemap, robots.txt, URL canónica, hreflang, Open Graph y datos estructurados Person/ProfilePage y ScholarlyArticle. La indexación y el posicionamiento dependen de Google y no se garantizan. Después del despliegue, el propietario puede verificar el dominio en Search Console y enviar `/sitemap.xml`.

`release.json` registra el inventario SHA-256 y la revisión del código cuando el árbol está limpio. Para confirmar los archivos realmente servidos: `python tools/release.py verify-remote --url https://teoriadejuego.github.io --expected-revision SHA_COMPLETO`. Es un registro de consistencia, no una firma criptográfica.

La adaptación del plan de 20 perfiles está en [ADAPTED_PLAN.md](docs/ADAPTED_PLAN.md), sus 400 criterios en [adapted-plan.json](docs/adapted-plan.json) y las instrucciones de edición, validación, publicación y recuperación en [OPERATIONS.md](docs/OPERATIONS.md).

No se modifica el dominio `antonioalfonso.org`: su migración requiere una decisión y acceso DNS independientes.

## Referencias

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Google Search Essentials](https://developers.google.com/search/docs/essentials/technical)
- [Datos estructurados de perfiles](https://developers.google.com/search/docs/appearance/structured-data/profile-page)

Los prompts aplicados están en `PROMPTS.md`; la trazabilidad editorial, en `SOURCES.md`.

La revisión posterior comprende 20 perspectivas profesionales simuladas en tres rondas, con 60 prompts aplicados y cambios trazables: [registro de revisión](reviews/README.md). Las pruebas adicionales se ejecutan con `python tests/round2_check.py` y `python tests/round3_check.py`, usando el mismo servidor y las mismas variables de entorno de la prueba principal. Para incluir el análisis automatizado de accesibilidad, `AXE_SCRIPT` debe apuntar a una copia local de axe-core.
