# Plan adaptado: 20 perfiles y 400 criterios

Fecha de cierre: 18 de noviembre de 2026. Base de adaptación: `32d65db`; plan aprobado inicialmente en `67b7d0a`. **Completado con límites: 400 criterios clasificados y cero pendientes.**

Código publicado y verificado: `ee405a5b41da3a7ff2fb17c341eb342c4dd6111e`. CI final: [44205177989](https://github.com/Teoriadejuego/teoriadejuego.github.io/actions/runs/44205177989), con `validate`, `deploy` y `confirm` correctos. El posterior commit de este informe no se atribuye a la web servida.

El registro canónico es [adapted-plan.json](adapted-plan.json); la implementación sigue [CONTRACTS.md](CONTRACTS.md). Los perfiles son perspectivas de revisión, no personas externas consultadas. La numeración conserva correspondencia con el adjunto. No se afirman 400 defectos, cambios o tests independientes.

## Estados

- **preservado** (83): Comportamiento o contenido existente conservado, con fuente/resultado de línea base identificado.
- **verificado** (199): Comprobación concreta ejecutada u observación comunicada y acotada en la evidencia.
- **cambiado** (39): Implementación inspeccionada; no implica que todas sus pruebas o el despliegue estén cerrados.
- **documentado** (70): Procedimiento o decisión descritos y revisados; no equivale a su ejecución.
- **limitado** (9): No se mide o garantiza la pretensión amplia; se declara el alcance posible.
- **pendiente** (0): Falta una prueba, integración o confirmación requerida.

## Alcance y coordinación

- Portfolio estático Python ES/EN: 26 rutas de contenido más 404, 12 artículos, 2 working papers, 6 casos y laboratorio sintético. Se conservan URLs, contacto, fuentes y atribución individual.
- Dos contextos: mantenimiento editorial local y lectura pública. No se crea una aplicación privada.
- Cambios acordados: contrato editorial y `data/site.json`; staging limpio con recuperación; UTF-8/LF; inventario permitido y `release.json` v1; normalización de filtros URL; tabla accesible del laboratorio; gates CI y documentación operativa.
- Fórmula preservada: SE = sqrt(2 SD² / n); IC = delta ± 1.96 SE. Dos grupos independientes, del mismo tamaño y SD; aproximación normal. No calcula potencia ni demuestra causalidad.
- Un escritor por módulo. El coordinador integra `build.py`, HTML compartido, CI y `public/`; fixtures en temporales aislados.
- A: contratos y adaptación (P01–P04, P07–P08). B: módulos coordinados (P05–P06, P09–P13). C: release/CI (P14, P18–P19). D: QA (P15–P17 y revisión P07). E: documentación/publicación (P20, P01, P18).
- Los criterios conservan aceptación original y ahora incorporan estados/evidencias explícitos. Generar el plan o escribir una prueba no constituye ejecutarla.
- No se realizan entrevistas, certificación WCAG, garantía de Google, prueba universal de privacidad, garantía de capacidad del hosting ni garantía futura de enlaces externos. El manifiesto acredita consistencia de bytes, no firma ni inmunidad ante un host comprometido. La recuperación no promete intercambio atómico universal de directorios.

## Reinterpretaciones y descartes

- Inglés exclusivo → ES/EN: se preserva el producto bilingüe autorizado.
- Panel investigador y web estudiantil → edición local y portfolio público; no se crean dos aplicaciones.
- Qualtrics, dos encuestas, DIC/dic_pairs, alternative_2, exportaciones y tokens → catálogos bibliográficos curados y validación offline; esos proveedores/esquemas no existen aquí.
- Login, sesiones, expiración, intentos y reconexión → permisos de GitHub/CI y ausencia de endpoints privados; no hay acciones mutables públicas.
- Cooldown de tres minutos, mutex entre pestañas y botón público de publicar → build coordinado y gates reales de Pages; no se añaden esperas artificiales.
- EndDate, cohortes históricas y selección por última respuesta → fechas editoriales e históricas explícitas; no se procesan respuestas de participantes.
- Seis decisiones binarias, 64 patrones, compasión/envidia, ocho clases y dp_efficiency → fórmula y dominios del laboratorio actual; importar reglas de otro estudio sería incorrecto.
- Supresión menor de cinco y tablas cruzadas → ausencia de microdatos y frontera de publicación; no se afirma implementar una supresión inexistente.
- Doce diapositivas y modo proyección obligatorio → casos y laboratorio explicativo; no se fuerza una presentación nueva.
- Polling de 60 segundos y reemplazo automático del lector → manifiesto operativo sin consultas cliente; se mantiene lectura estable.
- Contrato estudiantil v2/transición v1 → nuevo release.json v1 con rechazo de versiones desconocidas; no se inventa un contrato anterior.
- R, Vite, dos despliegues y Connect Cloud → Python estándar, mejora progresiva y GitHub Pages existentes.
- Carga de 30/60/200 estudiantes y velocidad de exportación → mediciones locales declaradas de bytes, build e interacción; no se infiere capacidad de hosting.
- Dashboard de telemetría → logs de comandos/CI y manifiesto, sin seguimiento de visitantes.

## Intentos de infraestructura y resolución

- **87d4916 · run 44201541791 · cancelados por el coordinador**: Descarga APT del mirror Ubuntu AWS excesivamente lenta; el segundo intento se canceló como obsoleto al sustituir candidato. Sin fallo del código web demostrado; deploy/confirm no completados.
- **955dfe2 · run 44203442849 · timeout de instalación APT**: El límite de cinco minutos venció antes de tests/deploy. Fijar ubuntu-24.04 no resolvió la lentitud del mirror; no demuestra incompatibilidad de Ubuntu 26 ni defecto del portfolio.
- **c32fd77 · run 44204424060 · fallo de configuración Firefox/HOME**: La imagen oficial evitó APT. Pasaron 100 unitarias, build/static/release y cinco suites Chromium; Firefox no arrancó por proceso root con HOME propiedad de pwuser. No se atribuyen siete suites completas ni despliegue a este intento.
- **ee405a5 · run 44205177989 · success validate/deploy/confirm**: Imagen oficial fijada por digest, UID 1001, pip --user y preflight de ambos navegadores. Todas las puertas conservadas y ejecutadas; 100 unitarias, siete suites, publicación y confirmación de 52 archivos.

La solución final conserva todas las pruebas. Imagen oficial Playwright Python v1.65.2-noble fijada por SHA-256 `38dd67fc654b56b3cba611e4c8eb71cd33750e1cd29eea2a5dc00b484817a75f`, UID 1001 y preflight Chromium/Firefox. Ningún intento cancelado o fallido se presenta como despliegue confirmado.

## Evidencias compartidas

### E-OPS — documentación revisada

**Referencia:** `docs/OPERATIONS.md`, `docs/CONTRACTS.md`.

Guía de edición, contratos, comandos, estados de publicación y recuperación revisada. Los procedimientos documentados no equivalen a un despliegue ejecutado.

### E-ARCH — inspección de fuente

**Referencia:** `build.py`, `assets/app.js`, `.gitignore`, `docs/CONTRACTS.md`.

Arquitectura estática, mejora progresiva, separación editorial/pública y ausencia de polling inspeccionadas en fuente. No supone prueba de todos los estados futuros.

### E-SOURCES — preservación editorial

**Referencia:** `data/publications.json`, `data/working-papers.json`, `data/projects.json`, `data/resources.json`, `SOURCES.md`.

Catálogos y atribuciones existentes conservados. Se reutiliza la trazabilidad de fuentes previa; no se han vuelto a verificar todos los destinos externos en esta oleada.

### E-BASELINE — regresión histórica

**Referencia:** `qa/browser-results.json`, `qa/round2-results.json`, `qa/round3-results.json`, `reviews/`.

La línea base documenta 26 páginas, no-JS, foco, responsive y revisiones anteriores. Se conserva como trazabilidad histórica; la regresión actual está en E-BROWSER/E-SUITE y su ejecución Linux en E-CI.

### E-CONTENT — implementación inspeccionada

**Referencia:** `tools/content_contract.py`, `data/site.json`, `tests/test_content_contract.py`.

Contrato offline/read-only, tipos estrictos, referencias, traducciones, autoría, fechas y URL implementados e inspeccionados; la suite completa de 100 pruebas pasa con 7 omisiones de symlink Windows. Detalle y límites en E-UNIT.

### E-BUILD — implementación y build local comunicado

**Referencia:** `build.py`, `tests/check_static.py`, `tools/release.py`, `tests/test_build.py`, `.gitattributes`.

Build local inicial: 26 páginas, 1.27 s. Build final en validate Linux: 0.184 s; reconstrucción independiente en confirm: 0.416 s. Los tres mantienen digest d466c20e7debd9e7865dbeeca615b6d0c81c89cc438b62fd27ce9db7f1b78a5a. Validación previa, staging limpio, static check interno, UTF-8/LF, inventario y recuperación cubiertos por inspección y tests aislados; véanse E-UNIT y E-CI.

**Origen del resultado:** Resultados locales previos y log_summary del run final 44205177989. Los tiempos son observaciones, no comparativa controlada entre equipos.

### E-RELEASE — prueba local ejecutada

**Referencia:** `tests/test_release.py`, `tools/release.py`, `qa/ci-44205177989.json`.

37 tests de artefacto/promoción: ejecución local OK con cinco omisiones de symlink por Windows; en CI Linux final se ejecutan también esos casos reales. Hashes independientes, límites, JSON estricto, alteración, promoción/restauración y fuentes intactas cubiertos. El verificador remoto añade 12 fixtures de transporte; la verificación pública real se registra aparte en E-REMOTE.

**Comando ejecutado:** `python -m unittest discover -s tests -p test_release.py`.

- La ejecución local no sustituye verificación remota, ahora registrada por separado en E-REMOTE.
- No prueba terminación abrupta del proceso ni atomicidad universal.

### E-SCI — pruebas Chromium y Firefox confirmadas

**Referencia:** `tests/scientific_browser.py`, `assets/app.js`, `build.py`, `qa/browser-suite.json`.

Wrapper completo confirmado: Chromium 1234 y Firefox 159, 10 casos × ES/EN por navegador, oráculo independiente, gráfico/texto/tabla, precisión cerca de cero, URL inválidas, historial, idioma, reset/foco y details nativo. Ambos scripts científicos exit 0, sin errores JS.

**Origen del resultado:** Mensaje del coordinador, 2026-11-18; servidor local 8078.

### E-PRIVACY — pruebas Chromium y Firefox confirmadas

**Referencia:** `tests/privacy_browser.py`, `assets/app.js`, `qa/browser-suite.json`.

Tras añadir la prueba de dos contextos vivos, privacy_browser.py vuelve a pasar por separado: Chromium 128 peticiones y Firefox 168, 26 rutas en ambos. Cero intentos externos/mutables, escritura storage/cookies, llamadas al portapapeles y errores JS. URLs PNAS y networks permanecen independientes; modificar el primer contexto y restablecer el segundo conserva URL, controles e IDs visibles del otro en ambas direcciones, sin peticiones adicionales. También cubre búsqueda inerte, filtros inválidos, parámetros ajenos, fragmentos, historial e idioma.

**Origen del resultado:** Resultado confirmado por coordinador/agente de navegador, 2026-11-18; código inspeccionado en tests/privacy_browser.py, commit candidato 301465d.

- Tráfico observado durante la prueba; no certificación universal de privacidad.

### E-VISUAL — capturas integradas e inspección visual

**Referencia:** `qa/scientific/table-es-320.png`, `qa/scientific/table-en-320.png`, `qa/scientific/table-es-1440.png`, `qa/scientific/table-en-1440.png`, `qa/scientific/table-es-320-text200.png`, `qa/scientific/table-en-320-text200.png`, `assets/style.css`.

Agente confirma capturas ES/EN a 320/1440 y 320 con texto 200%, sin overflow. Revisor inspeccionó además ES 320 texto 200% y EN 320: valores completos, etiquetas con numerosos saltos en el extremo estrecho. Fixture propia verificó Enter y colores forzados. No constituye certificación WCAG.

### E-LIMITS — límite explícito

**Referencia:** `docs/CONTRACTS.md`, `docs/OPERATIONS.md`.

Sin entrevistas ni frecuencia real de usuarios; sin certificación WCAG, garantía Google, capacidad masiva del hosting o disponibilidad perpetua de enlaces. Pruebas locales y revisión de código tienen alcance acotado.

### E-PLAN — registro documental

**Referencia:** `docs/adapted-plan.json`, `docs/ADAPTED_PLAN.md`.

20 perfiles × 20 criterios con referencias compartidas, estados diferenciados y correspondencia al adjunto; no 400 tests independientes ni 400 cambios.

### E-UNIT — suite unitaria local confirmada

**Referencia:** `qa/unit-results.txt`, `tests/test_content_contract.py`, `tests/test_build.py`, `tests/test_release.py`, `tests/test_remote_release.py`, `qa/ci-44205177989.json`.

Ejecución local: 100 pruebas en 31.145 s, OK con siete omisiones Windows de symlinks. Ejecución CI final Linux: las mismas 100 pruebas en 5.759 s, OK con una omisión de junction Windows; symlinks reales sí ejecutados. Cubre contratos, fuentes intactas, builds aislados y fallos, determinismo/LF, recuperación y hashes. Incluye 12 casos de transporte remoto simulado; la comprobación de producción real está en E-REMOTE.

**Comando ejecutado:** `python -m unittest discover -s tests -p "test_*.py"`.

- En Windows se omitieron siete pruebas de links; en Linux se ejecutaron symlinks reales y se omitió únicamente junction Windows.
- No prueba terminación abrupta del proceso ni atomicidad universal.

### E-BROWSER — regresión Chromium del candidato actual confirmada

**Referencia:** `qa/browser-results.json`, `qa/round2-results.json`, `qa/round3-results.json`, `tests/browser_check.py`, `tests/round2_check.py`, `tests/round3_check.py`.

Tres suites amplias pasadas y resultados JSON inspeccionados: 26 páginas a 1440/768/390 px; 320/810 adicionales; filtros, no-JS, idioma, 12 BibTeX, foco/breakpoints, 320 px con texto 200%, colores forzados, movimiento reducido y 404. Sin errores JS. Axe 4.14.1 obligatorio en esta ejecución: siete rutas sin violaciones detectadas.

- No certificación WCAG ni cobertura de todos los navegadores/estados posibles.
- La prueba de portapapeles usa stub; no accede al portapapeles del ordenador.

### E-CI-SOURCE — workflow implementado e inspeccionado

**Referencia:** `.github/workflows/pages.yml`, `requirements-dev.txt`, `tools/check_browser.py`, `tools/fetch_axe.py`.

Workflow final inspeccionado y ejecutado: runner ubuntu-24.04; imagen oficial Playwright Python v1.65.2-noble fijada por SHA-256 38dd67fc654b56b3cba611e4c8eb71cd33750e1cd29eea2a5dc00b484817a75f; usuario 1001, pip --user y preflight Chromium/Firefox. validate mantiene 100 unitarias, axe, build/static/release y siete suites antes de deploy. PR excluida de publicación, acciones fijadas por SHA, permisos separados, concurrencia y job confirm posterior con revisión esperada.

### E-SUITE — suite integral local confirmada

**Referencia:** `qa/browser-suite.json`, `tools/check_browser.py`, `qa/ci-44205177989.json`.

Siete checks locales con returncode 0 y siete checks confirmados otra vez en CI final: cinco suites Chromium y métodos/privacidad Firefox. Axe 4.14.1 en siete rutas: cero violaciones detectadas, sin equivaler a certificación WCAG.

**Comando ejecutado:** `python tools/check_browser.py --firefox`.

### E-PERF — medición local confirmada e inspeccionada

**Referencia:** `qa/performance.json`, `tools/measure.py`, `public/release.json`.

Windows 11, Python 3.12.10, Playwright 1.65.2, Chromium 151.0.7922.34; viewport 1440×1000 DPR1, loopback sin throttling. Artefacto 835024 B, assets 490266 B. Manifiesto 8400 B; HTML publicaciones ES 47698 B y EN 47024 B. Tres pares: mediana loadEventEnd contexto nuevo 65.9 ms y recarga 9.7 ms. Veinte inputs por control: medianas evento→DOM filtros 0.4 ms y lab 0.6 ms; sin requests adicionales, crecimiento de DOM/historial ni storage/cookies. Agente confirma control negativo falla sin modificar public.

**Comando ejecutado:** `python tools/measure.py`.

- Muestras locales descriptivas, sin garantía de capacidad o velocidad universal.
- Contexto nuevo no significa sistema operativo/proceso de navegador completamente frío; recarga usa caché local, no política de Pages.
- Conteos estables no prueban ausencia de fugas de heap.
- No existe una serie histórica comparable de latencia previa; no se afirma una mejora porcentual.
- Duración de build local registrada en E-BUILD; no se aisló un benchmark separado del verificador de hashes.

### E-CI — CI final completa y despliegue confirmados

**Referencia:** `qa/ci-44205177989.json`, `.github/workflows/pages.yml`.

Run 44205177989 success en ee405a5b41da3a7ff2fb17c341eb342c4dd6111e: validate, deploy y confirm completados. Linux: 100 pruebas en 5.759 s, OK con una omisión exclusiva de junction Windows; symlinks reales ejecutados. Build de validación: 26 páginas en 0.184 s; static check, release y siete suites Chromium/Firefox correctos. Build independiente de confirmación: 0.416 s. Ambos generan digest d466c20e7debd9e7865dbeeca615b6d0c81c89cc438b62fd27ce9db7f1b78a5a.

**Origen del resultado:** [GitHub Actions 44205177989](https://github.com/Teoriadejuego/teoriadejuego.github.io/actions/runs/44205177989); JSON de jobs y log_summary inspeccionados.

- La prueba de junction Windows no se ejecuta en Linux; no se oculta esta omisión.
- Tiempos observados en estos runners, sin garantía de rendimiento universal.

### E-REMOTE — producción final verificada automáticamente y desde el coordinador

**Referencia:** `qa/remote-release.json`, `qa/ci-44205177989.json`, `tools/release.py`.

Confirmación automática CI y ejecución adicional del coordinador con exit 0. JSON inspeccionado: source_revision ee405a5b41da3a7ff2fb17c341eb342c4dd6111e, digest d466c20e7debd9e7865dbeeca615b6d0c81c89cc438b62fd27ce9db7f1b78a5a; 52 archivos HTTP 200 con bytes, hashes y MIME pertinentes verificados. .nojekyll sigue siendo sentinel local, excluido de peticiones HTTP.

**Comando ejecutado:** `python tools/release.py verify-remote --url https://teoriadejuego.github.io --expected-revision ee405a5b41da3a7ff2fb17c341eb342c4dd6111e`.

- Observación fechada de la versión servida, no disponibilidad perpetua ni firma criptográfica.
- El commit documental posterior no se atribuye a la web desplegada: la fuente pública verificada es ee405a5b41da3a7ff2fb17c341eb342c4dd6111e.

### E-AUTO-CONFIRM — confirmación automática posterior al deploy ejecutada

**Referencia:** `qa/ci-44205177989.json`, `.github/workflows/pages.yml`, `tools/release.py`.

Job confirm success: checkout del SHA publicado, reconstrucción independiente y verify-remote --expected-revision GITHUB_SHA. Log REMOTE_CONFIRMED registra ee405a5b41da3a7ff2fb17c341eb342c4dd6111e y 52 archivos con digest d466c20e7debd9e7865dbeeca615b6d0c81c89cc438b62fd27ce9db7f1b78a5a. Se conservan reintentos acotados para propagación CDN; no se retiró ninguna puerta de pruebas.

**Origen del resultado:** Run 44205177989, job confirm, completado 2026-11-18T00:12:09Z.

### E-DELIVERY — revisión de entrega y smoke público

**Referencia:** `qa/adaptation-delivery-check.json`.

Informe HTML: 20 perfiles, 400 criterios, filtros de estados, anclas y móvil 320 px. Smoke público: laboratorio ES/EN, recuperación de filtros, 404 anidada y móvil 390 px; sin errores JavaScript. Integridad ZIP comprobada. Esta prueba se realizó sobre el informe provisional; los recuentos finales de JSON/Markdown se validan estructuralmente en este cierre.

### E-INFRA — historial de intentos y resolución de infraestructura

**Referencia:** `qa/ci-44201541791-attempt1.json`, `qa/ci-44203442849.json`, `qa/ci-44204424060.json`, `qa/ci-44205177989.json`.

Dos cancelaciones del run 87 por instalación lenta; timeout APT en 955; fallo Firefox/HOME en c32; resolución en ee405a5 mediante contenedor oficial fijado y UID 1001 con preflight. Los intentos incompletos no se cuentan como pruebas aprobadas ni como fallos científicos. Detalle en infrastructure_attempts.

**Origen del resultado:** Estados/logs conservados en QA y mensajes del coordinador; no se ocultan reintentos ni se debilitaron gates.

## P01 — Dirección de producto del portfolio

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Completa los recorridos editorial y público conservando ES/EN, evidencia profesional y acceso abierto; consolida obligaciones compartidas sin multiplicar funciones.

**Aceptación del perfil:** evaluar sus 20 criterios sobre el candidato común; conservar comportamientos demostrados y declarar cualquier pendiente.

**Evidencia esperada:** README, CONTRACTS y recorridos headless portada/equipos/casos/contacto.

1. **P01-C01 · documentado** — El editor identifica qué fuentes modificar y cómo validar antes de publicar.
   Evidencia: `E-OPS`.
2. **P01-C02 · preservado** — El visitante encuentra especialización, contribución individual y contacto.
   Evidencia: `E-SOURCES`.
3. **P01-C03 · documentado** — La guía distingue mantenimiento local de lectura pública sin inventar un panel.
   Evidencia: `E-ARCH`, `E-OPS`.
4. **P01-C04 · documentado** — El recorrido editorial enumera edición, build, pruebas, despliegue y recuperación.
   Evidencia: `E-OPS`.
5. **P01-C05 · verificado** — Las seis áreas principales siguen accesibles en ES/EN.
   Evidencia: `E-BROWSER`.
6. **P01-C06 · preservado** — Fechas de artículos y trayectoria se distinguen de actualización editorial.
   Evidencia: `E-SOURCES`.
7. **P01-C07 · documentado** — Modificar fuentes y publicar en Pages se describen como etapas diferentes.
   Evidencia: `E-OPS`.
8. **P01-C08 · documentado** — Un build local correcto no se comunica como publicación ya disponible.
   Evidencia: `E-OPS`.
9. **P01-C09 · verificado** — El manifiesto servido permite identificar el candidato publicado.
   Evidencia: `E-REMOTE`.
10. **P01-C10 · verificado** — Se conservan 12 artículos y 2 working papers separados, sin cohortes inventadas.
   Evidencia: `E-BUILD`.
11. **P01-C11 · documentado** — La espera descrita corresponde a CI/Pages, sin temporizador artificial.
   Evidencia: `E-OPS`.
12. **P01-C12 · verificado** — Un fallo de validación/render preserva la salida anterior y bloquea deploy.
   Evidencia: `E-UNIT`, `E-CI-SOURCE`, `E-CI`.
13. **P01-C13 · verificado** — Reconstruir el mismo contenido mantiene su digest sin prohibir commits legítimos.
   Evidencia: `E-RELEASE`.
14. **P01-C14 · preservado** — Demo sintética y evidencia investigadora se diferencian en laboratorio y casos.
   Evidencia: `E-SOURCES`.
15. **P01-C15 · verificado** — Primera visita y cero coincidencias tienen recorridos comprensibles sin cuenta.
   Evidencia: `E-PRIVACY`.
16. **P01-C16 · documentado** — README permite retomar mantenimiento desde un checkout limpio.
   Evidencia: `E-OPS`.
17. **P01-C17 · preservado** — Casos, publicaciones con ancla y laboratorio conservan acceso directo.
   Evidencia: `E-BASELINE`.
18. **P01-C18 · preservado** — El recorrido equipos→caso→perfil/contacto se completa sin callejones sin salida.
   Evidencia: `E-SOURCES`.
19. **P01-C19 · documentado** — Obligaciones duplicadas comparten contratos y evidencia identificada.
   Evidencia: `E-PLAN`.
20. **P01-C20 · documentado** — El cierre distingue preservado, verificado, cambiado, limitado y pendiente.
   Evidencia: `E-PLAN`.

## P02 — Dirección de metodología y rigor científico

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Preserva fórmula, supuestos y atribuciones verificadas; explica límites sin importar clasificaciones científicas del producto ajeno.

**Aceptación del perfil:** evaluar los 20 criterios con código, fuentes existentes y pruebas independientes; no inventar análisis nuevos.

**Evidencia esperada:** app.js, lab_page, datos de casos, SOURCES y oráculo independiente.

1. **P02-C01 · verificado** — Se conservan tres controles reales: n, diferencia y SD.
   Evidencia: `E-SCI`.
2. **P02-C02 · verificado** — Diferencia cero y signos positivo/negativo no se confunden con ausencia de datos.
   Evidencia: `E-SCI`.
3. **P02-C03 · verificado** — El mismo estado produce iguales resultados científicos en ES/EN.
   Evidencia: `E-SCI`.
4. **P02-C04 · preservado** — La explicación trata diferencia y precisión, sin categorías de compasión ajenas.
   Evidencia: `E-SOURCES`.
5. **P02-C05 · preservado** — SD se identifica como dispersión y no como error estándar por sí sola.
   Evidencia: `E-SOURCES`.
6. **P02-C06 · verificado** — Se mantienen tres interpretaciones: positivo, negativo e incluye cero.
   Evidencia: `E-SCI`.
7. **P02-C07 · verificado** — Estimación, SE y límites se derivan de las mismas entradas.
   Evidencia: `E-SCI`.
8. **P02-C08 · verificado** — Gráfico, tabla y texto representan el mismo cálculo, no pruebas independientes.
   Evidencia: `E-SCI`.
9. **P02-C09 · preservado** — La separación estadística no se presenta como utilidad empresarial automática.
   Evidencia: `E-SOURCES`.
10. **P02-C10 · verificado** — n significa observaciones por grupo y ambos grupos tienen igual tamaño.
   Evidencia: `E-SCI`.
11. **P02-C11 · verificado** — URL inválidas no producen NaN ni intervalos fuera de los dominios definidos.
   Evidencia: `E-SCI`.
12. **P02-C12 · preservado** — La demo no afirma excluir participantes o evaluar datos reales.
   Evidencia: `E-ARCH`.
13. **P02-C13 · verificado** — Repetir entradas produce resultados idénticos sin aleatoriedad.
   Evidencia: `E-SCI`.
14. **P02-C14 · cambiado** — La fecha editorial no interviene en el cálculo.
   Evidencia: `E-BUILD`.
15. **P02-C15 · preservado** — Las cifras de los casos conservan fuente y contexto de muestra.
   Evidencia: `E-SOURCES`.
16. **P02-C16 · preservado** — TeensLab no se presenta como muestra nacional representativa ni n universal por tarea.
   Evidencia: `E-SOURCES`.
17. **P02-C17 · preservado** — Las narraciones distinguen descripción, asociación y conclusión del estudio.
   Evidencia: `E-SOURCES`.
18. **P02-C18 · preservado** — El laboratorio conserva su advertencia de que no demuestra causalidad.
   Evidencia: `E-SOURCES`.
19. **P02-C19 · verificado** — Se preservan SE=sqrt(2*SD²/n) e IC=delta±1.96*SE, sin dp_efficiency.
   Evidencia: `E-SCI`.
20. **P02-C20 · documentado** — La guía vincula método, código y revisión; cambios futuros requieren revisión explícita.
   Evidencia: `E-OPS`.

## P03 — Investigación de experiencia de uso

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Inspecciona tareas reales del editor y lector; separa observaciones verificadas de hipótesis de usabilidad sin inventar entrevistas.

**Aceptación del perfil:** registrar resultados de 20 tareas/observaciones y límites del método de inspección.

**Evidencia esperada:** recorridos headless, capturas ES/EN, README e informe de tareas.

1. **P03-C01 · documentado** — El primer acceso al repo permite localizar comandos y fuentes editables.
   Evidencia: `E-OPS`.
2. **P03-C02 · documentado** — Editar y reconstruir no exige pasos manuales ocultos.
   Evidencia: `E-OPS`.
3. **P03-C03 · preservado** — El perfil distingue trabajos históricos del puesto actual.
   Evidencia: `E-SOURCES`.
4. **P03-C04 · preservado** — Se diferencian fecha científica, captura de demo y actualización editorial.
   Evidencia: `E-SOURCES`.
5. **P03-C05 · preservado** — Portada y equipos ofrecen siguiente paso hacia evidencia o contacto.
   Evidencia: `E-BASELINE`.
6. **P03-C06 · documentado** — La guía explica CI sin hacer esperar al visitante una actualización inexistente.
   Evidencia: `E-OPS`.
7. **P03-C07 · cambiado** — Los diagnósticos distinguen validación, build, verificación y despliegue.
   Evidencia: `E-BUILD`.
8. **P03-C08 · documentado** — Un campo inválido tiene corrección localizable y preserva salida anterior.
   Evidencia: `E-OPS`.
9. **P03-C09 · verificado** — Volver atrás recupera filtros válidos sin autenticación.
   Evidencia: `E-PRIVACY`.
10. **P03-C10 · cambiado** — Errores editoriales identifican ubicación sin exponer valores sensibles.
   Evidencia: `E-CONTENT`.
11. **P03-C11 · preservado** — La advertencia sintética precede a la interpretación del laboratorio.
   Evidencia: `E-SOURCES`.
12. **P03-C12 · preservado** — Los enlaces de laboratorio llevan a demo, código y materiales.
   Evidencia: `E-BASELINE`.
13. **P03-C13 · verificado** — Los casos conducen a repositorio, artículo o demo según su estado real.
   Evidencia: `E-PRIVACY`.
14. **P03-C14 · verificado** — Buscar, tema, año y reset tienen etiquetas y estado reconocible.
   Evidencia: `E-PRIVACY`.
15. **P03-C15 · verificado** — El lector puede identificar n como tamaño de cada grupo.
   Evidencia: `E-SCI`.
16. **P03-C16 · verificado** — Cero coincidencias no se confunde con efecto cero.
   Evidencia: `E-PRIVACY`.
17. **P03-C17 · preservado** — La página no cambia automáticamente mediante polling ni anuncios ficticios.
   Evidencia: `E-ARCH`.
18. **P03-C18 · verificado** — A 320 y 390 px se puede navegar, filtrar, leer y contactar sin overflow.
   Evidencia: `E-BROWSER`.
19. **P03-C19 · limitado** — Hallazgos se priorizan por impacto observado; frecuencia no medida se declara desconocida.
   Evidencia: `E-LIMITS`.
20. **P03-C20 · limitado** — El informe identifica inspección y automatización, sin atribuir entrevistas inexistentes.
   Evidencia: `E-LIMITS`.

## P04 — Diseño de interfaces accesibles

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Conserva identidad visual y verifica teclado, foco, etiquetas, texto equivalente y adaptación; no presentes la revisión como certificación WCAG.

**Aceptación del perfil:** documentar los 20 checks y su alcance, preservando las mejoras previas.

**Evidencia esperada:** CSS, HTML, teclado headless, capturas y axe cuando esté disponible.

1. **P04-C01 · preservado** — Texto principal mantiene tamaño y altura de línea legibles en móvil/escritorio.
   Evidencia: `E-BASELINE`.
2. **P04-C02 · verificado** — Cada página tiene un h1 y jerarquía comprensible de secciones.
   Evidencia: `E-BUILD`.
3. **P04-C03 · limitado** — Contraste de texto, controles y foco se comprueba en el alcance inspeccionado.
   Evidencia: `E-LIMITS`.
4. **P04-C04 · preservado** — Colores del laboratorio no implican éxito comercial automático.
   Evidencia: `E-ARCH`.
5. **P04-C05 · verificado** — Signo e intervalo se expresan con números y texto además de color.
   Evidencia: `E-SCI`.
6. **P04-C06 · verificado** — Menú, filtros, detalles y sliders funcionan por teclado.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-PRIVACY`.
7. **P04-C07 · verificado** — Foco es perceptible sobre fondos y estados seleccionados.
   Evidencia: `E-BROWSER`.
8. **P04-C08 · verificado** — El salto al contenido lleva a main y evita navegación repetida.
   Evidencia: `E-BROWSER`.
9. **P04-C09 · verificado** — Escape cierra menú móvil y devuelve foco al disparador.
   Evidencia: `E-BROWSER`.
10. **P04-C10 · verificado** — Estados de filtros y fallo de copiar correo se explican junto al control.
   Evidencia: `E-BROWSER`.
11. **P04-C11 · verificado** — Búsqueda, selectores y sliders tienen nombres accesibles asociados.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-BUILD`.
12. **P04-C12 · cambiado** — La tabla del laboratorio usa encabezados y semántica nativa.
   Evidencia: `E-SCI`, `E-VISUAL`.
13. **P04-C13 · verificado** — El detalle de tabla se abre por teclado sin una matriz artificial.
   Evidencia: `E-SCI`.
14. **P04-C14 · verificado** — Título SVG, texto y tabla ofrecen resultados equivalentes.
   Evidencia: `E-SCI`.
15. **P04-C15 · verificado** — La tabla no crea una segunda región viva duplicada.
   Evidencia: `E-SCI`.
16. **P04-C16 · verificado** — Se respeta reduced-motion sin animaciones necesarias para comprender.
   Evidencia: `E-BROWSER`.
17. **P04-C17 · verificado** — A 200% de texto y 320 px no se recorta contenido esencial.
   Evidencia: `E-VISUAL`.
18. **P04-C18 · verificado** — Objetivos táctiles inspeccionados conservan área y separación utilizables.
   Evidencia: `E-BROWSER`.
19. **P04-C19 · verificado** — Autoría, versiones y enlaces no se superponen a 320 px.
   Evidencia: `E-VISUAL`.
20. **P04-C20 · verificado** — lang y controles corresponden a es/en según ruta.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-BUILD`.

## P05 — Diseño de explicación científica y casos

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Adapta la intención docente a casos y laboratorio mediante secuencia, evidencia y límites; no fuerces doce diapositivas ni nuevas pantallas.

**Aceptación del perfil:** revisar 20 propiedades del contenido existente y mejorar solo lo acordado.

**Evidencia esperada:** case_page, lab_page, projects.json, lectura y navegación.

1. **P05-C01 · preservado** — Los seis casos presentan el problema antes de herramientas técnicas.
   Evidencia: `E-SOURCES`.
2. **P05-C02 · verificado** — La demo explica qué cambia y qué permanece fijo.
   Evidencia: `E-SCI`.
3. **P05-C03 · preservado** — Cada caso distingue el papel individual del trabajo del equipo.
   Evidencia: `E-SOURCES`.
4. **P05-C04 · verificado** — La explicación utiliza los tres controles reales, no seis decisiones ajenas.
   Evidencia: `E-SCI`.
5. **P05-C05 · verificado** — n=200, delta=3 y SD=15 forman un ejemplo inicial reproducible.
   Evidencia: `E-SCI`.
6. **P05-C06 · preservado** — Se explican incertidumbre y diferencia sin categorías ajenas.
   Evidencia: `E-SOURCES`.
7. **P05-C07 · preservado** — Los resultados visibles responden a la pregunta del ejemplo.
   Evidencia: `E-SOURCES`.
8. **P05-C08 · verificado** — Gráfico, tabla y texto se reconocen como representaciones del mismo cálculo.
   Evidencia: `E-SCI`.
9. **P05-C09 · verificado** — Etiqueta y supuestos expresan n por grupo.
   Evidencia: `E-SCI`.
10. **P05-C10 · preservado** — Los recursos públicos excluyen documentos administrativos privados.
   Evidencia: `E-SOURCES`.
11. **P05-C11 · verificado** — Los grupos sintéticos no se presentan como cohorte observada.
   Evidencia: `E-SCI`.
12. **P05-C12 · verificado** — Cero y dirección del efecto tienen explicación en ES/EN.
   Evidencia: `E-SCI`.
13. **P05-C13 · preservado** — Se conservan límites sobre potencia, causalidad y negocio.
   Evidencia: `E-SOURCES`.
14. **P05-C14 · verificado** — Se puede explorar y restablecer sin enviar datos.
   Evidencia: `E-SCI`.
15. **P05-C15 · cambiado** — Supuestos y tabla se consultan mediante detalles nativos opcionales.
   Evidencia: `E-SCI`, `E-VISUAL`.
16. **P05-C16 · verificado** — La página sigue usable ampliada sin exigir modo proyección.
   Evidencia: `E-VISUAL`.
17. **P05-C17 · verificado** — Anclas y controles son alcanzables por enlace y teclado.
   Evidencia: `E-BROWSER`.
18. **P05-C18 · verificado** — Gráfico, leyenda y resultados se leen en escritorio y móvil.
   Evidencia: `E-VISUAL`.
19. **P05-C19 · preservado** — Una página abierta no cambia de release durante su explicación.
   Evidencia: `E-ARCH`.
20. **P05-C20 · verificado** — La URL sintética reproduce el ejemplo en su idioma.
   Evidencia: `E-SCI`.

## P06 — Dirección de visualización de datos

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Conserva un intervalo con escala honesta, texto equivalente y tabla sincronizada; no añadas agregados de participantes ni gráficos ajenos.

**Aceptación del perfil:** contrastar 20 propiedades con los mismos estados numéricos y registrar límites de inspección.

**Evidencia esperada:** app.js, CSS, SVG/tabla del laboratorio y fixtures numéricas.

1. **P06-C01 · verificado** — El eje expresa puntos de diferencia, sin porcentajes injustificados.
   Evidencia: `E-SCI`.
2. **P06-C02 · verificado** — Punto, segmento, tabla y texto utilizan el mismo n, delta y SD.
   Evidencia: `E-SCI`.
3. **P06-C03 · verificado** — URL inválida se normaliza antes de dibujar sin estado contradictorio.
   Evidencia: `E-SCI`.
4. **P06-C04 · verificado** — n aparece identificado como observaciones por grupo.
   Evidencia: `E-SCI`.
5. **P06-C05 · preservado** — n sintético no se presenta como participantes publicados.
   Evidencia: `E-SOURCES`.
6. **P06-C06 · verificado** — Efecto cero se sitúa en el centro, distinto de ausencia de JavaScript.
   Evidencia: `E-SCI`.
7. **P06-C07 · verificado** — Sin JavaScript se explica la limitación y siguen disponibles los materiales.
   Evidencia: `E-BROWSER`.
8. **P06-C08 · verificado** — Los límites extremos permitidos permanecen dentro del gráfico.
   Evidencia: `E-SCI`.
9. **P06-C09 · cambiado** — La tabla ordena n, diferencia, SD, SE y límites de forma equivalente ES/EN.
   Evidencia: `E-SCI`, `E-VISUAL`.
10. **P06-C10 · verificado** — La diferencia se expresa en puntos, no crecimiento porcentual.
   Evidencia: `E-SCI`.
11. **P06-C11 · verificado** — La precisión cerca de cero conserva la dirección del intervalo.
   Evidencia: `E-SCI`.
12. **P06-C12 · verificado** — Sliders y outputs reflejan los parámetros seleccionados.
   Evidencia: `E-SCI`.
13. **P06-C13 · preservado** — La demo no se compara con una población de referencia inexistente.
   Evidencia: `E-ARCH`.
14. **P06-C14 · verificado** — El cero está centrado en una escala simétrica.
   Evidencia: `E-SCI`.
15. **P06-C15 · verificado** — Valores negativos van a izquierda y positivos a derecha.
   Evidencia: `E-SCI`.
16. **P06-C16 · verificado** — Punto y segmento conservan significado entre idiomas y estados.
   Evidencia: `E-SCI`.
17. **P06-C17 · verificado** — Valores tabulados coinciden con cálculo y precisión de los límites textuales.
   Evidencia: `E-SCI`.
18. **P06-C18 · verificado** — Entradas repetidas producen igual escala y coordenadas.
   Evidencia: `E-SCI`.
19. **P06-C19 · verificado** — Historial e idioma conservan parámetros válidos sin alterar fórmula.
   Evidencia: `E-SCI`.
20. **P06-C20 · preservado** — Origen sintético y fórmula permanecen accesibles junto al gráfico.
   Evidencia: `E-SOURCES`.

## P07 — Arquitectura de privacidad y seguridad estática

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Mantén frontera entre fuentes editoriales y artefacto público mediante validación, escape y lista permitida; no añadas autenticación ni telemetría.

**Aceptación del perfil:** comprobar 20 propiedades y declarar que escaneo/allowlist no prueban confidencialidad universal.

**Evidencia esperada:** contrato editorial, build/release, inventario, pruebas adversas y tráfico público.

1. **P07-C01 · verificado** — Cargar el portfolio no consulta Qualtrics ni adquisición privada.
   Evidencia: `E-PRIVACY`.
2. **P07-C02 · verificado** — El artefacto inspeccionado no contiene credenciales ni rutas locales del propietario.
   Evidencia: `E-RELEASE`.
3. **P07-C03 · preservado** — El visitante no edita ni publica; GitHub conserva permisos operativos.
   Evidencia: `E-ARCH`.
4. **P07-C04 · preservado** — No se añaden login/logout ni estados de sesión ficticios.
   Evidencia: `E-ARCH`.
5. **P07-C05 · preservado** — Contenido público no depende de tokens o caducidad de aplicación.
   Evidencia: `E-ARCH`.
6. **P07-C06 · verificado** — Reabrir una ruta no requiere reconectar una cuenta.
   Evidencia: `E-PRIVACY`.
7. **P07-C07 · preservado** — Se verifica ausencia de endpoint de autenticación en vez de límites de intentos innecesarios.
   Evidencia: `E-ARCH`.
8. **P07-C08 · verificado** — Fixtures y candidatos temporales no se distribuyen.
   Evidencia: `E-BUILD`.
9. **P07-C09 · verificado** — Temporales, caches y documentos privados quedan fuera de salida.
   Evidencia: `E-BUILD`.
10. **P07-C10 · verificado** — Errores indican ubicación sin reproducir valores sensibles rechazados.
   Evidencia: `E-RELEASE`.
11. **P07-C11 · verificado** — El verificador rechaza archivos extra, symlinks y escapes de ruta.
   Evidencia: `E-RELEASE`.
12. **P07-C12 · preservado** — No se publican microdatos ni se afirma supresión menor de cinco inexistente.
   Evidencia: `E-ARCH`.
13. **P07-C13 · preservado** — Recuentos bibliográficos son públicos y n del laboratorio es sintético.
   Evidencia: `E-SOURCES`.
14. **P07-C14 · preservado** — La tabla del laboratorio no incluye atributos individuales ni cruces identificables.
   Evidencia: `E-ARCH`.
15. **P07-C15 · verificado** — Filtros consultan metadatos públicos de artículos, no participantes.
   Evidencia: `E-PRIVACY`.
16. **P07-C16 · preservado** — DOM y JSON distribuidos no esconden valores privados tras estilos.
   Evidencia: `E-ARCH`, `E-SOURCES`.
17. **P07-C17 · verificado** — Diffs de releases contienen archivos públicos, no entradas administrativas.
   Evidencia: `E-BUILD`.
18. **P07-C18 · verificado** — No se crean identificadores ni historial remoto de visitantes.
   Evidencia: `E-PRIVACY`.
19. **P07-C19 · cambiado** — Texto se escapa y URL ejecutables o con credenciales se rechazan.
   Evidencia: `E-CONTENT`.
20. **P07-C20 · verificado** — La prueba registra tráfico sin conexiones privadas y declara su alcance.
   Evidencia: `E-PRIVACY`.

## P08 — Arquitectura del portfolio estático

Oleada: A. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Mantén Python estándar y HTML progresivo; separa validación, render y publicación sin migrar framework ni introducir servicios.

**Aceptación del perfil:** verificar 20 límites arquitectónicos, evitando componentes sin necesidad real.

**Evidencia esperada:** CONTRACTS, build.py, contrato editorial, app.js y workflow.

1. **P08-C01 · documentado** — Se documentan edición local y lectura pública como contextos del mismo portfolio.
   Evidencia: `E-ARCH`, `E-OPS`.
2. **P08-C02 · preservado** — El núcleo usa Python estándar y no incorpora R.
   Evidencia: `E-ARCH`.
3. **P08-C03 · cambiado** — Validación, render e interacción tienen responsabilidades identificables.
   Evidencia: `E-BUILD`.
4. **P08-C04 · cambiado** — load_content y validate_content no escriben ni hacen red.
   Evidencia: `E-CONTENT`.
5. **P08-C05 · preservado** — HTML contiene contenido y enlaces; JavaScript solo mejora la experiencia.
   Evidencia: `E-ARCH`.
6. **P08-C06 · cambiado** — Se mantienen cinco catálogos y se añade site según contrato.
   Evidencia: `E-CONTENT`.
7. **P08-C07 · verificado** — El candidato se renderiza separado de public vigente.
   Evidencia: `E-BUILD`.
8. **P08-C08 · verificado** — release.json usa schema_version 1 y campos acordados.
   Evidencia: `E-RELEASE`.
9. **P08-C09 · verificado** — El navegador no requiere backend ni manifiesto para renderizar.
   Evidencia: `E-PRIVACY`.
10. **P08-C10 · preservado** — Pages sigue disponible con el ordenador del editor apagado.
   Evidencia: `E-ARCH`.
11. **P08-C11 · verificado** — Fuentes de trabajo se distinguen del inventario aprobado de distribución.
   Evidencia: `E-BUILD`.
12. **P08-C12 · documentado** — Un escritor por módulo y coordinador para build/public evitan conflictos.
   Evidencia: `E-OPS`.
13. **P08-C13 · documentado** — Fixtures usan temporales sin sobrescribir salida compartida.
   Evidencia: `E-OPS`.
14. **P08-C14 · verificado** — Un fallo conserva salida previa o informa recuperación concreta.
   Evidencia: `E-RELEASE`.
15. **P08-C15 · preservado** — No se añade base de datos ni persistencia remota del visitante.
   Evidencia: `E-ARCH`.
16. **P08-C16 · preservado** — Git/Pages conservan material público sin incorporar expedientes privados.
   Evidencia: `E-SOURCES`.
17. **P08-C17 · cambiado** — El contrato admite catálogos actuales y rechaza versión site desconocida.
   Evidencia: `E-CONTENT`.
18. **P08-C18 · verificado** — Se mantienen 26 rutas ES/EN y 404.
   Evidencia: `E-BUILD`.
19. **P08-C19 · preservado** — El artefacto es estático y SITE_URL configura identidad canónica segura.
   Evidencia: `E-ARCH`.
20. **P08-C20 · documentado** — La recuperación reconstruye y redeploya revisión conocida sin servicios nuevos.
   Evidencia: `E-OPS`.

## P09 — Ingeniería de construcción fiable

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Valida antes de escribir, conserva salida anterior y distingue candidato correcto de publicación confirmada; no prometas atomicidad universal.

**Aceptación del perfil:** verificar 20 estados/invariantes operativos con fixtures aisladas cuando haya mutaciones.

**Evidencia esperada:** build/release, pruebas de fallos inyectados, determinismo y logs.

1. **P09-C01 · cambiado** — Diagnósticos distinguen validación, render, verificación y promoción.
   Evidencia: `E-BUILD`.
2. **P09-C02 · verificado** — Trazabilidad usa revisión y digest, sin IDs de visitante o sesión.
   Evidencia: `E-RELEASE`.
3. **P09-C03 · preservado** — Solo editor/CI ejecutan publicación; no hay acciones públicas mutables.
   Evidencia: `E-ARCH`.
4. **P09-C04 · preservado** — No se impone cooldown artificial de tres minutos.
   Evidencia: `E-ARCH`.
5. **P09-C05 · preservado** — Abrir pestañas no inicia builds ni bloqueos de publicación.
   Evidencia: `E-ARCH`.
6. **P09-C06 · documentado** — El procedimiento asigna un único escritor de public.
   Evidencia: `E-OPS`.
7. **P09-C07 · preservado** — No se añade botón público de build ni cola de clics.
   Evidencia: `E-ARCH`.
8. **P09-C08 · preservado** — Lectura pública no depende del progreso de construcción local.
   Evidencia: `E-ARCH`.
9. **P09-C09 · verificado** — Fallos de render/promoción terminan con diagnóstico, sin reintentos ilimitados.
   Evidencia: `E-RELEASE`.
10. **P09-C10 · preservado** — Build offline no falla por caída de repositorio bibliográfico.
   Evidencia: `E-ARCH`.
11. **P09-C11 · verificado** — Candidato inválido no reemplaza public anterior.
   Evidencia: `E-UNIT`.
12. **P09-C12 · verificado** — Promoción fallida intenta restauración y comunica copia recuperable si procede.
   Evidencia: `E-RELEASE`.
13. **P09-C13 · verificado** — content_digest deriva del inventario canónico, no del reloj.
   Evidencia: `E-RELEASE`.
14. **P09-C14 · verificado** — Reconstrucción idéntica conserva bytes y digest verificables.
   Evidencia: `E-RELEASE`.
15. **P09-C15 · verificado** — CI coordina despliegues y detecta candidato servido obsoleto.
   Evidencia: `E-CI`, `E-CI-SOURCE`, `E-AUTO-CONFIRM`, `E-REMOTE`.
16. **P09-C16 · documentado** — El flujo no utiliza force-push ni sobrescritura remota ajena.
   Evidencia: `E-OPS`.
17. **P09-C17 · verificado** — Reintentar valida candidato completo y no reutiliza salida parcial.
   Evidencia: `E-RELEASE`.
18. **P09-C18 · documentado** — Build local no se declara publicación remota confirmada.
   Evidencia: `E-OPS`.
19. **P09-C19 · verificado** — Error indica siguiente paso y salida conservada cuando corresponda.
   Evidencia: `E-RELEASE`.
20. **P09-C20 · verificado** — Fixtures cubren validación, render y promoción sin tocar producción.
   Evidencia: `E-RELEASE`.

## P10 — Curación sénior de fuentes bibliográficas

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Sustituye adquisición Qualtrics por catálogos curados offline; conserva versiones abiertas, DOI y autoría sin prometer acceso perpetuo.

**Aceptación del perfil:** revisar 20 propiedades de metadatos, fuentes y límites de comprobación externa.

**Evidencia esperada:** publications, working-papers, resources, SOURCES y contrato editorial.

1. **P10-C01 · preservado** — Artículos, working papers y materiales permanecen diferenciados.
   Evidencia: `E-SOURCES`.
2. **P10-C02 · cambiado** — IDs únicos/seguros y referencias locales resuelven al catálogo correcto.
   Evidencia: `E-CONTENT`.
3. **P10-C03 · cambiado** — URL editoriales rechazan esquemas ejecutables y credenciales embebidas.
   Evidencia: `E-CONTENT`.
4. **P10-C04 · verificado** — Visita y build no requieren credenciales bibliográficas.
   Evidencia: `E-PRIVACY`.
5. **P10-C05 · preservado** — Año científico no se sustituye por fecha de descarga.
   Evidencia: `E-SOURCES`.
6. **P10-C06 · cambiado** — Campos numéricos respetan tipos definidos por el contrato.
   Evidencia: `E-CONTENT`.
7. **P10-C07 · preservado** — Títulos originales se preservan sin importar variables Qualtrics.
   Evidencia: `E-SOURCES`.
8. **P10-C08 · preservado** — Lista de autores y author_parts conservan orden editorial.
   Evidencia: `E-SOURCES`.
9. **P10-C09 · preservado** — BibTeX mantiene apellidos compuestos como Alfonso Costillo.
   Evidencia: `E-SOURCES`.
10. **P10-C10 · cambiado** — Campos inesperados o incompatibles fallan antes del render.
   Evidencia: `E-CONTENT`.
11. **P10-C11 · cambiado** — site.updated usa fecha ISO válida separada de años bibliográficos.
   Evidencia: `E-CONTENT`.
12. **P10-C12 · preservado** — Etiquetas distinguen preprint, manuscrito y versión editorial cuando consta.
   Evidencia: `E-SOURCES`.
13. **P10-C13 · preservado** — Corpus no excluye artículos por hora de acceso al repositorio.
   Evidencia: `E-SOURCES`.
14. **P10-C14 · cambiado** — Cada build valida todos los catálogos requeridos.
   Evidencia: `E-CONTENT`.
15. **P10-C15 · preservado** — SOURCES distingue procedencia, publicación y limitaciones de verificación.
   Evidencia: `E-SOURCES`.
16. **P10-C16 · limitado** — Un destino bloqueado se registra no confirmado, sin borrar automáticamente el artículo.
   Evidencia: `E-LIMITS`.
17. **P10-C17 · preservado** — Build offline no finge descargar o verificar PDFs externos.
   Evidencia: `E-ARCH`.
18. **P10-C18 · preservado** — No se copian documentos privados ni microdatos al artefacto.
   Evidencia: `E-ARCH`.
19. **P10-C19 · verificado** — Archivos temporales de inspección quedan fuera del inventario público.
   Evidencia: `E-BUILD`.
20. **P10-C20 · documentado** — Pruebas usan fixtures o verificaciones explícitas, sin llamadas masivas a proveedores.
   Evidencia: `E-OPS`.

## P11 — Ingeniería de datos editoriales

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Valida tipos, traducciones, referencias y cardinalidades antes de renderizar; deriva recuentos de catálogos públicos sin modificar su significado.

**Aceptación del perfil:** ejecutar 20 comprobaciones sobre fuentes reales y fixtures inválidas, sin corregir silenciosamente datos.

**Evidencia esperada:** content_contract, data/*.json y fixtures de validación.

1. **P11-C01 · cambiado** — Los seis catálogos se cargan bajo sus claves definidas sin reescribir fuentes.
   Evidencia: `E-CONTENT`.
2. **P11-C02 · cambiado** — Tipos estrictos no confunden booleanos con enteros de esquema.
   Evidencia: `E-CONTENT`.
3. **P11-C03 · cambiado** — site.updated rechaza fechas imposibles y formatos no ISO.
   Evidencia: `E-CONTENT`.
4. **P11-C04 · cambiado** — Fecha inválida genera diagnóstico localizado, no fecha sustitutiva.
   Evidencia: `E-CONTENT`.
5. **P11-C05 · cambiado** — IDs y destacados duplicados se rechazan sin deduplicación silenciosa.
   Evidencia: `E-CONTENT`.
6. **P11-C06 · cambiado** — Actualización visible deriva de site.updated, no del reloj del build.
   Evidencia: `E-BUILD`.
7. **P11-C07 · verificado** — Datos inválidos se detectan antes de tocar salida anterior.
   Evidencia: `E-UNIT`.
8. **P11-C08 · verificado** — Lab respeta mínimos n=20, delta=-15 y SD=5.
   Evidencia: `E-SCI`.
9. **P11-C09 · verificado** — Lab respeta máximos n=2000, delta=15 y SD=40.
   Evidencia: `E-SCI`.
10. **P11-C10 · cambiado** — Artículos del mismo año no se eliminan como duplicados.
   Evidencia: `E-CONTENT`.
11. **P11-C11 · preservado** — Trabajos históricos no desaparecen por ventanas relativas al presente.
   Evidencia: `E-SOURCES`.
12. **P11-C12 · cambiado** — Corpus y destacados dependen de datos explícitos, no del reloj.
   Evidencia: `E-BUILD`.
13. **P11-C13 · cambiado** — IDs de portada resuelven al catálogo correspondiente.
   Evidencia: `E-CONTENT`.
14. **P11-C14 · cambiado** — Errores identifican archivo, registro y campo corregible.
   Evidencia: `E-CONTENT`.
15. **P11-C15 · verificado** — Totales de artículos, working papers y casos se derivan de datos.
   Evidencia: `E-BUILD`.
16. **P11-C16 · cambiado** — Temas corresponden a categorías reales sin país/género inventados.
   Evidencia: `E-CONTENT`.
17. **P11-C17 · verificado** — El corpus de esta entrega conserva 12 artículos y 2 working papers.
   Evidencia: `E-BUILD`.
18. **P11-C18 · cambiado** — Orden y serialización producen igual resultado con fuentes idénticas.
   Evidencia: `E-BUILD`.
19. **P11-C19 · cambiado** — Campo obligatorio ausente genera error, no cero o texto inventado.
   Evidencia: `E-CONTENT`.
20. **P11-C20 · cambiado** — Referencias entre casos, artículos y destacados se validan antes de publicar.
   Evidencia: `E-CONTENT`.

## P12 — Experiencia de mantenimiento editorial

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Ofrece un flujo local documentado en vez de panel autenticado; explica entradas, versión y recuperación sin añadir interfaz innecesaria.

**Aceptación del perfil:** comprobar 20 puntos de operación y documentación contra el comportamiento final.

**Evidencia esperada:** README, guía operativa, mensajes de validación/build y CONTRACTS.

1. **P12-C01 · documentado** — README indica propósito y primer comando de construcción.
   Evidencia: `E-OPS`.
2. **P12-C02 · documentado** — La guía localiza datos, render, estilos, interacción, pruebas y salida.
   Evidencia: `E-OPS`.
3. **P12-C03 · documentado** — Se explica cómo leer revisión y digest del manifiesto.
   Evidencia: `E-OPS`.
4. **P12-C04 · documentado** — El editor conoce los 12 artículos, 2 working papers y 6 casos de la entrega.
   Evidencia: `E-OPS`.
5. **P12-C05 · documentado** — Actualización editorial, año del artículo y despliegue se diferencian.
   Evidencia: `E-OPS`.
6. **P12-C06 · documentado** — Se documenta dónde editar títulos, roles y enlaces de casos.
   Evidencia: `E-OPS`.
7. **P12-C07 · preservado** — SOURCES conserva atribuciones y límites sin saturar interfaz pública.
   Evidencia: `E-SOURCES`.
8. **P12-C08 · documentado** — Edición, pruebas, commit y publicación se describen por separado.
   Evidencia: `E-OPS`.
9. **P12-C09 · documentado** — La espera remite al job real de Pages, sin contador ficticio.
   Evidencia: `E-OPS`.
10. **P12-C10 · documentado** — La guía identifica único escritor y evita public durante promoción concurrente.
   Evidencia: `E-OPS`.
11. **P12-C11 · cambiado** — Comandos/CI muestran etapas reales y no porcentajes simulados.
   Evidencia: `E-BUILD`.
12. **P12-C12 · documentado** — Digest igual se explica como mismo contenido aunque cambie documentación.
   Evidencia: `E-OPS`.
13. **P12-C13 · documentado** — Se explica cómo corregir datos y reintentar sin perder salida anterior.
   Evidencia: `E-OPS`.
14. **P12-C14 · preservado** — La versión desplegada permanece durante edición o build fallido.
   Evidencia: `E-ARCH`.
15. **P12-C15 · verificado** — Diagnósticos de desarrollo no se copian al sitio.
   Evidencia: `E-BUILD`.
16. **P12-C16 · documentado** — Esquema y errores se documentan fuera de los recorridos públicos principales.
   Evidencia: `E-OPS`.
17. **P12-C17 · documentado** — Cambiar el cálculo exige localizar código y pasar pruebas metodológicas.
   Evidencia: `E-OPS`.
18. **P12-C18 · documentado** — Instrucciones no incluyen tokens ni contraseñas reales.
   Evidencia: `E-OPS`.
19. **P12-C19 · documentado** — Retomar mantenimiento incluye comprobar revisión y estado de trabajo.
   Evidencia: `E-OPS`.
20. **P12-C20 · documentado** — README identifica URL canónica y comando de previsualización.
   Evidencia: `E-OPS`.

## P13 — Frontend público y mejora progresiva

Oleada: B. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Preserva HTML útil, normaliza filtros URL y añade equivalencia tabular del laboratorio; sin polling ni datos remotos adicionales.

**Aceptación del perfil:** comprobar 20 estados del lector en ES/EN con y sin JavaScript.

**Evidencia esperada:** app.js, HTML y pruebas de URL/historial/idioma/no-JS.

1. **P13-C01 · preservado** — HTML contiene el catálogo sin servicio remoto duplicado.
   Evidencia: `E-ARCH`.
2. **P13-C02 · verificado** — Render inicial no depende de release.json ni petición posterior de datos.
   Evidencia: `E-PRIVACY`.
3. **P13-C03 · preservado** — No se instala polling de 60 segundos ni otro refresco periódico.
   Evidencia: `E-ARCH`.
4. **P13-C04 · preservado** — Ocultar pestaña no mantiene tareas de red creadas por el portfolio.
   Evidencia: `E-ARCH`.
5. **P13-C05 · preservado** — Volver a pestaña no resetea filtros ni reemplaza página automáticamente.
   Evidencia: `E-ARCH`.
6. **P13-C06 · verificado** — Filtrar no vuelve a descargar catálogos ni PDFs externos.
   Evidencia: `E-PRIVACY`.
7. **P13-C07 · documentado** — Manifiesto se verifica operativamente, no como dependencia del visitante.
   Evidencia: `E-ARCH`, `E-OPS`.
8. **P13-C08 · verificado** — Resultados, contador y URL reflejan el mismo estado aplicado.
   Evidencia: `E-PRIVACY`.
9. **P13-C09 · verificado** — topic/year desconocidos se eliminan al cargar y navegar historial.
   Evidencia: `E-PRIVACY`.
10. **P13-C10 · verificado** — Controles normalizados muestran los valores realmente aplicados.
   Evidencia: `E-PRIVACY`.
11. **P13-C11 · verificado** — Página cargada conserva filtros/lab sin servicios privados.
   Evidencia: `E-PRIVACY`.
12. **P13-C12 · preservado** — La interfaz no anuncia releases pendientes que no observa.
   Evidencia: `E-ARCH`.
13. **P13-C13 · preservado** — Años científicos no se reemplazan por fecha del release.
   Evidencia: `E-SOURCES`.
14. **P13-C14 · cambiado** — Fecha editorial deriva de site.updated, no de apertura de página.
   Evidencia: `E-BUILD`.
15. **P13-C15 · verificado** — Búsqueda, tema y año operan sobre artículos presentes en DOM.
   Evidencia: `E-PRIVACY`.
16. **P13-C16 · verificado** — Tabla se actualiza con gráfico y usa igual precisión de límites.
   Evidencia: `E-SCI`.
17. **P13-C17 · verificado** — Estado vacío ofrece explicación y reset conservando formulario.
   Evidencia: `E-PRIVACY`.
18. **P13-C18 · verificado** — URL malformadas no ejecutan HTML ni causan errores JavaScript.
   Evidencia: `E-PRIVACY`.
19. **P13-C19 · verificado** — Cargar rutas no consulta APIs privadas ni seguimiento inesperado.
   Evidencia: `E-PRIVACY`.
20. **P13-C20 · verificado** — Filtros, navegación, tabla y casos funcionan a 320/390/768/1440 px.
   Evidencia: `E-VISUAL`.

## P14 — Arquitectura de publicación verificable

Oleada: C. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Construye candidato limpio, verifica inventario y hashes, promueve con recuperación; el manifiesto registra consistencia, no firma criptográfica.

**Aceptación del perfil:** probar 20 invariantes sobre candidatos aislados y confirmar el servido al publicar.

**Evidencia esperada:** build/release, manifiesto v1, pruebas de alteración/recuperación y CI.

1. **P14-C01 · verificado** — Render ocurre en temporal nuevo bajo repo, separado de public vigente.
   Evidencia: `E-BUILD`.
2. **P14-C02 · verificado** — content_digest es SHA-256 del inventario canónico de bytes.
   Evidencia: `E-RELEASE`.
3. **P14-C03 · verificado** — Reloj y revisión no alteran digest de archivos idénticos.
   Evidencia: `E-RELEASE`.
4. **P14-C04 · verificado** — Manifiesto respeta campos v1 y verificación rechaza esquemas desconocidos.
   Evidencia: `E-RELEASE`.
5. **P14-C05 · verificado** — Allowlist y verificación preceden al upload del artefacto.
   Evidencia: `E-BUILD`.
6. **P14-C06 · verificado** — Textos generados usan UTF-8 y LF entre entornos.
   Evidencia: `E-RELEASE`.
7. **P14-C07 · verificado** — Hash y tamaño se calculan sobre bytes de cada archivo.
   Evidencia: `E-RELEASE`.
8. **P14-C08 · verificado** — Inventario POSIX ordenado excluye release.json y .nojekyll según contrato.
   Evidencia: `E-RELEASE`.
9. **P14-C09 · verificado** — Promoción fallida intenta restauración sin prometer atomicidad universal.
   Evidencia: `E-RELEASE`.
10. **P14-C10 · verificado** — Promoción no toca fuentes ni archivos ajenos a salida/temporales propios.
   Evidencia: `E-RELEASE`.
11. **P14-C11 · verificado** — Workflow coordina despliegues y comprueba candidato esperado.
   Evidencia: `E-CI`, `E-CI-SOURCE`, `E-AUTO-CONFIRM`, `E-REMOTE`.
12. **P14-C12 · verificado** — Reintento idéntico mantiene digest sin duplicar contenido.
   Evidencia: `E-RELEASE`.
13. **P14-C13 · verificado** — source_revision es SHA limpio de 40 caracteres o null cuando no atribuible.
   Evidencia: `E-RELEASE`.
14. **P14-C14 · verificado** — Fallos de contrato, pruebas o verificación bloquean deploy.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
15. **P14-C15 · verificado** — Versión servida se compara con candidato y discrepancia se informa.
   Evidencia: `E-REMOTE`.
16. **P14-C16 · verificado** — Manifiesto y bytes servidos se contrastan sin exigir .nojekyll por HTTP.
   Evidencia: `E-REMOTE`.
17. **P14-C17 · verificado** — Fallo de validación/render conserva bytes de salida anterior.
   Evidencia: `E-UNIT`.
18. **P14-C18 · documentado** — Informe distingue preparado, validado, desplegado y confirmado.
   Evidencia: `E-OPS`.
19. **P14-C19 · documentado** — Guía permite reconstruir y redeployar revisión conocida con pruebas.
   Evidencia: `E-OPS`.
20. **P14-C20 · verificado** — Manifiesto excluye visitantes, microdatos, credenciales y tiempos individuales.
   Evidencia: `E-RELEASE`.

## P15 — QA de métodos y contratos de datos

Oleada: D. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Protege fórmula, entradas y contratos con expectativas independientes; no implementes el oráculo de 64 patrones de otro estudio.

**Aceptación del perfil:** documentar 20 checks con fixtures y tolerancias pertinentes, evitando tests que solo repitan implementación.

**Evidencia esperada:** expectativas Python independientes, navegador y fixtures temporales.

1. **P15-C01 · verificado** — Oráculo Python independiente cubre estados representativos del laboratorio.
   Evidencia: `E-SCI`.
2. **P15-C02 · verificado** — Se comparan estimación, SE y límites con tolerancias declaradas.
   Evidencia: `E-SCI`.
3. **P15-C03 · verificado** — Texto, tabla y gráfico coinciden en positivo, negativo e incluye cero.
   Evidencia: `E-SCI`.
4. **P15-C04 · verificado** — Pruebas fijan sqrt(2*SD²/n) y 1.96 sin regresión ajena.
   Evidencia: `E-SCI`.
5. **P15-C05 · verificado** — Fixtures cubren los seis tipos de catálogos definidos.
   Evidencia: `E-UNIT`.
6. **P15-C06 · verificado** — Campos desconocidos, tipos erróneos y referencias rotas se rechazan.
   Evidencia: `E-UNIT`.
7. **P15-C07 · verificado** — Faltan campos/traducciones obligatorios: ContentError localizable.
   Evidencia: `E-UNIT`.
8. **P15-C08 · verificado** — Tipos numéricos inválidos y booleanos indebidos no pasan validación pertinente.
   Evidencia: `E-UNIT`.
9. **P15-C09 · verificado** — Se prueban IDs/destacados duplicados y autoría inconsistente.
   Evidencia: `E-UNIT`.
10. **P15-C10 · verificado** — Fechas imposibles o no ISO fallan antes de construir.
   Evidencia: `E-UNIT`.
11. **P15-C11 · preservado** — Artículos antiguos permanecen en catálogo y filtros.
   Evidencia: `E-SOURCES`.
12. **P15-C12 · verificado** — Se prueban extremos/pasos de n, delta y SD y URL fuera de dominio.
   Evidencia: `E-SCI`.
13. **P15-C13 · verificado** — Datos inválidos mantienen salida previa intacta en fixture aislada.
   Evidencia: `E-UNIT`.
14. **P15-C14 · verificado** — Fecha editorial y digest no dependen de zona horaria o DST.
   Evidencia: `E-UNIT`.
15. **P15-C15 · verificado** — Conteos de filtros coinciden con registros públicos esperados.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-PRIVACY`.
16. **P15-C16 · verificado** — Casos cerca de cero verifican signo y precisión de redondeo.
   Evidencia: `E-SCI`.
17. **P15-C17 · preservado** — Fixtures no contienen participantes reales ni tablas cruzadas inexistentes.
   Evidencia: `E-ARCH`.
18. **P15-C18 · verificado** — UTF-8/LF, inventario, alteración y recuperación se prueban en temporales.
   Evidencia: `E-RELEASE`.
19. **P15-C19 · verificado** — Cambio público cambia digest; cambio solo de revisión no lo cambia.
   Evidencia: `E-RELEASE`.
20. **P15-C20 · cambiado** — Se preserva orden editorial de listas y serialización canónica de mapas.
   Evidencia: `E-CONTENT`.

## P16 — QA de navegador y accesibilidad

Oleada: D. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Prueba estados reales del portfolio: filtros, historial, idiomas, laboratorio, teclado, móvil y red; no simules login inexistente.

**Aceptación del perfil:** registrar 20 comprobaciones del candidato y límites de automatización/accesibilidad.

**Evidencia esperada:** tests headless, capturas, tráfico, fixtures y axe opcional.

1. **P16-C01 · verificado** — Rutas públicas abren sin cuenta ni controles de sesión ficticios.
   Evidencia: `E-PRIVACY`.
2. **P16-C02 · preservado** — Visita no caduca por autenticación para usar controles locales.
   Evidencia: `E-ARCH`.
3. **P16-C03 · verificado** — Interfaz y red no permiten lanzar publicación desde la visita.
   Evidencia: `E-PRIVACY`.
4. **P16-C04 · verificado** — Se verifica portada→equipos→caso→perfil/contacto en ES/EN.
   Evidencia: `E-PRIVACY`.
5. **P16-C05 · verificado** — Repetir reset/menú no rompe estado ni foco.
   Evidencia: `E-SCI`.
6. **P16-C06 · verificado** — Dos contextos mantienen URL propia sin bloqueo ni storage compartido.
   Evidencia: `E-PRIVACY`.
7. **P16-C07 · verificado** — Bloquear red externa no rompe lectura, filtros ni laboratorio locales.
   Evidencia: `E-PRIVACY`.
8. **P16-C08 · verificado** — Build fallido conserva salida anterior sin servir candidato parcial.
   Evidencia: `E-UNIT`.
9. **P16-C09 · documentado** — Informe no llama publicado a un candidato solo local.
   Evidencia: `E-OPS`.
10. **P16-C10 · verificado** — Sin JS se leen 12 artículos, enlaces y advertencia de controles.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-PRIVACY`.
11. **P16-C11 · verificado** — Verificador detecta cambio de digest sin recarga automática del visitante.
   Evidencia: `E-RELEASE`.
12. **P16-C12 · verificado** — Fixture con bytes alterados falla verificación antes de deploy.
   Evidencia: `E-RELEASE`.
13. **P16-C13 · verificado** — Versión de esquema desconocida falla de forma explícita.
   Evidencia: `E-RELEASE`.
14. **P16-C14 · verificado** — Tabla, texto y SVG coinciden con expectativas independientes.
   Evidencia: `E-SCI`.
15. **P16-C15 · verificado** — Se cubren tema/año, búsqueda, vacío, inválidos, historial e idioma.
   Evidencia: `E-PRIVACY`.
16. **P16-C16 · verificado** — Teclado verifica salto, Escape, filtros, detalles y reset con foco.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-PRIVACY`.
17. **P16-C17 · verificado** — Se inspeccionan 320/390/768/1440 px y texto al 200%.
   Evidencia: `E-BROWSER`, `E-SCI`, `E-PRIVACY`.
18. **P16-C18 · verificado** — Hay una región viva de resultados lab y anuncios de filtros comprensibles.
   Evidencia: `E-SCI`.
19. **P16-C19 · verificado** — Fixtures de texto/URL adversos no ejecutan HTML o código.
   Evidencia: `E-PRIVACY`.
20. **P16-C20 · verificado** — Tráfico registrado no contiene APIs privadas ni seguimiento inesperado.
   Evidencia: `E-PRIVACY`.

## P17 — Ingeniería de rendimiento proporcionado

Oleada: D. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Mide costes estáticos en condiciones declaradas y conserva interacción local; evita pruebas masivas o proveedores ajenos al alcance.

**Aceptación del perfil:** revisar 20 propiedades, diferenciando medición, inspección y aspectos no medidos.

**Evidencia esperada:** inventario, mediciones headless/build e informe con condiciones.

1. **P17-C01 · verificado** — Informe identifica navegador, viewport y entorno de medición.
   Evidencia: `E-PERF`.
2. **P17-C02 · verificado** — Se distingue localhost de producción y cualquier limitación de red.
   Evidencia: `E-PERF`.
3. **P17-C03 · verificado** — Se suman bytes públicos y se identifican recursos de mayor peso.
   Evidencia: `E-PERF`.
4. **P17-C04 · verificado** — Se registra peso de manifiesto/HTML sin asumir descarga cliente de catálogos.
   Evidencia: `E-PERF`.
5. **P17-C05 · verificado** — Se observa disponibilidad de filtros bajo condiciones reproducibles.
   Evidencia: `E-PERF`.
6. **P17-C06 · verificado** — Filtros/sliders responden sin esperar peticiones de red.
   Evidencia: `E-PRIVACY`.
7. **P17-C07 · limitado** — Sesión repetida se inspecciona sin afirmar presupuesto universal de memoria.
   Evidencia: `E-LIMITS`.
8. **P17-C08 · preservado** — Filtrar trabaja con registros existentes sin reconstruir toda la página.
   Evidencia: `E-ARCH`.
9. **P17-C09 · documentado** — No se añade indexación compleja para 12 artículos sin justificación medida.
   Evidencia: `E-ARCH`, `E-OPS`.
10. **P17-C10 · verificado** — Imágenes conservan dimensiones, variantes y carga diferida pertinentes.
   Evidencia: `E-BROWSER`.
11. **P17-C11 · preservado** — No hay polling ni trabajo periódico de red en pestaña oculta.
   Evidencia: `E-ARCH`.
12. **P17-C12 · verificado** — Interacciones no descargan nuevamente datos o PDFs externos.
   Evidencia: `E-PRIVACY`.
13. **P17-C13 · verificado** — Comparaciones distinguen carga fría de caché caliente.
   Evidencia: `E-PERF`.
14. **P17-C14 · preservado** — Build local no bloquea una página pública ya cargada.
   Evidencia: `E-ARCH`.
15. **P17-C15 · limitado** — No se afirma capacidad probada de 30/60/200 clientes.
   Evidencia: `E-LIMITS`.
16. **P17-C16 · verificado** — Producción comprueba estado HTTP y MIME de recursos críticos.
   Evidencia: `E-REMOTE`.
17. **P17-C17 · preservado** — Build no incluye exportaciones Qualtrics ni adquisición remota.
   Evidencia: `E-ARCH`.
18. **P17-C18 · limitado** — Se registra duración de build/verificación en el entorno usado.
   Evidencia: `E-PERF`, `E-BUILD`.
19. **P17-C19 · cambiado** — Tabla y detalles no incorporan librerías gráficas ni red nueva.
   Evidencia: `E-SCI`, `E-VISUAL`.
20. **P17-C20 · limitado** — Cambios de peso/tiempo se comparan con línea base antes de optimizar.
   Evidencia: `E-PERF`, `E-BUILD`.

## P18 — Ingeniería DevOps de GitHub Pages

Oleada: C. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Ejecuta validación y pruebas antes de Pages, separa PR de deploy y documenta recuperación con hosting existente; sin R/Vite.

**Aceptación del perfil:** comprobar 20 propiedades del pipeline y declarar comprobaciones remotas pendientes si las hubiera.

**Evidencia esperada:** workflow, guía operativa, logs CI y manifiesto servido.

1. **P18-C01 · verificado** — Solo public se sube a Pages, no fuentes privadas.
   Evidencia: `E-BUILD`.
2. **P18-C02 · preservado** — CI declara Python 3.12 y build usa biblioteca estándar.
   Evidencia: `E-ARCH`.
3. **P18-C03 · cambiado** — Dependencias de QA no se convierten en runtime del sitio.
   Evidencia: `E-CI-SOURCE`, `E-ARCH`.
4. **P18-C04 · cambiado** — Workflow e informe identifican herramientas de pruebas.
   Evidencia: `E-CI-SOURCE`, `E-ARCH`.
5. **P18-C05 · preservado** — Se conserva build.py sin añadir Vite o bundler.
   Evidencia: `E-ARCH`.
6. **P18-C06 · verificado** — CI ejecuta pruebas de contrato, build y método pertinentes.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
7. **P18-C07 · verificado** — CI incluye interacción JavaScript mediante headless.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
8. **P18-C08 · verificado** — E2E cubre filtros, idiomas y laboratorio sin proveedores privados.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
9. **P18-C09 · verificado** — Inventario y hashes se verifican antes de upload-pages-artifact.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
10. **P18-C10 · verificado** — Tests, docs, reviews y paquetes de desarrollo no se sirven.
   Evidencia: `E-BUILD`.
11. **P18-C11 · preservado** — No se añaden tokens y workflow conserva permisos mínimos.
   Evidencia: `E-ARCH`.
12. **P18-C12 · verificado** — Concurrencia de deploy está coordinada y PR no despliega.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
13. **P18-C13 · verificado** — Checkout nuevo se construye con comandos documentados sin estado oculto.
   Evidencia: `E-UNIT`.
14. **P18-C14 · verificado** — Validación, build, pruebas y verificación preceden a deploy.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
15. **P18-C15 · verificado** — Tras publicar se compara manifiesto servido con candidato.
   Evidencia: `E-REMOTE`.
16. **P18-C16 · documentado** — Rollback público se documenta como reconstrucción/redeploy verificado.
   Evidencia: `E-OPS`.
17. **P18-C17 · documentado** — Recuperación local de public no se llama rollback de un panel ficticio.
   Evidencia: `E-OPS`.
18. **P18-C18 · documentado** — Guía remite a permisos GitHub sin copiar credenciales.
   Evidencia: `E-OPS`.
19. **P18-C19 · preservado** — Artefacto es portable como archivos estáticos sin Connect Cloud.
   Evidencia: `E-ARCH`.
20. **P18-C20 · documentado** — Operación documenta comandos, entradas y resultados esperados.
   Evidencia: `E-OPS`.

## P19 — Observabilidad sin seguimiento

Oleada: C. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Diagnostica construcción y releases con revisión/digest y errores claros; no añadas telemetría de visitantes ni un nuevo servicio.

**Aceptación del perfil:** comprobar 20 señales operativas y su ausencia de datos privados.

**Evidencia esperada:** logs de comandos/CI, release.json y guía de diagnóstico.

1. **P19-C01 · cambiado** — Errores distinguen contrato, render, verificación, promoción y comprobación remota.
   Evidencia: `E-BUILD`.
2. **P19-C02 · verificado** — Informes usan revisión/candidato, no IDs de visitante.
   Evidencia: `E-RELEASE`.
3. **P19-C03 · verificado** — Resultado de build permite asociar candidato con content_digest.
   Evidencia: `E-BUILD`.
4. **P19-C04 · verificado** — source_revision vincula commit limpio o null explicado.
   Evidencia: `E-RELEASE`.
5. **P19-C05 · verificado** — Tiempos medidos indican etapa/entorno sin telemetría pública.
   Evidencia: `E-PERF`.
6. **P19-C06 · documentado** — Digest idéntico no se comunica como error o nueva evidencia científica.
   Evidencia: `E-OPS`.
7. **P19-C07 · documentado** — Falta de confirmación HTTP no se transforma en éxito.
   Evidencia: `E-OPS`.
8. **P19-C08 · verificado** — Último intento observado se identifica por CI/informe sin dashboard inventado.
   Evidencia: `E-CI`, `E-CI-SOURCE`.
9. **P19-C09 · verificado** — Último éxito se referencia con logs/manifiesto sin visitantes.
   Evidencia: `E-REMOTE`.
10. **P19-C10 · verificado** — Cierre compara digest esperado y servido.
   Evidencia: `E-REMOTE`.
11. **P19-C11 · verificado** — Verificador identifica archivos ausentes, extra o alterados.
   Evidencia: `E-RELEASE`.
12. **P19-C12 · verificado** — Contrato incompatible genera diagnóstico y bloquea promoción.
   Evidencia: `E-RELEASE`.
13. **P19-C13 · verificado** — Error de URL no imprime credenciales del valor rechazado.
   Evidencia: `E-RELEASE`.
14. **P19-C14 · limitado** — Enlaces no confirmados se registran con fecha/límite sin reintentos masivos.
   Evidencia: `E-LIMITS`.
15. **P19-C15 · preservado** — No se registran cooldowns o sesiones Qualtrics inexistentes.
   Evidencia: `E-ARCH`.
16. **P19-C16 · verificado** — Fallo de promoción informa restauración o copia recuperable.
   Evidencia: `E-RELEASE`.
17. **P19-C17 · documentado** — Diagnóstico compartible excluye documentos y valores privados.
   Evidencia: `E-OPS`.
18. **P19-C18 · preservado** — No se almacena telemetría remota y QA queda fuera del sitio.
   Evidencia: `E-ARCH`.
19. **P19-C19 · verificado** — No se añaden analytics, cookies propias o IDs persistentes.
   Evidencia: `E-PRIVACY`.
20. **P19-C20 · documentado** — Guía ofrece recuperación para cada clase de fallo implementada.
   Evidencia: `E-OPS`.

## P20 — Documentación y reproducibilidad

Oleada: E. Contrato: `docs/CONTRACTS.md`.

**Prompt:** Documenta producto y contratos reales; conserva ES/EN, separa plan de ejecución y entrega evidencias/límites sin promesas no verificadas.

**Aceptación del perfil:** revisar 20 puntos contra comportamiento final y mantener los pendientes explícitos.

**Evidencia esperada:** README, SOURCES, CONTRACTS, guía operativa e informe final.

1. **P20-C01 · documentado** — Arquitectura describe fuentes locales, Python y lector estático, no dos apps nuevas.
   Evidencia: `E-OPS`.
2. **P20-C02 · documentado** — Se indican URL pública y preview sin inventar panel privado.
   Evidencia: `E-OPS`.
3. **P20-C03 · documentado** — Guía explica editar datos/destacados/fecha y validar.
   Evidencia: `E-OPS`.
4. **P20-C04 · documentado** — Se explica acceder a casos, artículos abiertos, filtros y laboratorio.
   Evidencia: `E-OPS`.
5. **P20-C05 · documentado** — Historia científica se distingue de actualización editorial.
   Evidencia: `E-OPS`.
6. **P20-C06 · documentado** — Un ejemplo aclara que reconstruir no vuelve nuevo un artículo antiguo.
   Evidencia: `E-OPS`.
7. **P20-C07 · documentado** — Actualizar no exige cooldown inexistente de tres minutos.
   Evidencia: `E-OPS`.
8. **P20-C08 · documentado** — Se documenta evento de Pages y gates previos.
   Evidencia: `E-OPS`.
9. **P20-C09 · documentado** — Nuevas versiones aparecen al navegar/recargar, sin polling.
   Evidencia: `E-OPS`.
10. **P20-C10 · documentado** — Catálogos institucionales sustituyen dos fuentes Qualtrics ajenas.
   Evidencia: `E-OPS`.
11. **P20-C11 · documentado** — Fórmula, supuestos, n por grupo y límites sintéticos están documentados.
   Evidencia: `E-OPS`.
12. **P20-C12 · documentado** — Se explica ausencia de microdatos sin afirmar supresión no implementada.
   Evidencia: `E-OPS`.
13. **P20-C13 · documentado** — Se documenta manifiesto v1, digest, revisión e inventario/exclusiones.
   Evidencia: `E-OPS`.
14. **P20-C14 · documentado** — Se explica rechazo de versiones desconocidas y conservación de rutas.
   Evidencia: `E-OPS`.
15. **P20-C15 · documentado** — Guía cubre JSON, referencias, URL, hash y promoción inválidos.
   Evidencia: `E-OPS`.
16. **P20-C16 · documentado** — Recuperación enumera reconstrucción/redeploy de revisión conocida.
   Evidencia: `E-OPS`.
17. **P20-C17 · documentado** — Se usan permisos existentes sin publicar credenciales.
   Evidencia: `E-OPS`.
18. **P20-C18 · verificado** — Valores iniciales y URL permiten reproducir demo ES/EN.
   Evidencia: `E-SCI`.
19. **P20-C19 · documentado** — Método/pruebas se vinculan a revisión Git y límites declarados.
   Evidencia: `E-OPS`.
20. **P20-C20 · documentado** — Checklist distingue 400 aceptaciones de cambios reales y referencia pruebas/pendientes.
   Evidencia: `E-PLAN`.

## Lectura del cierre

Cero pendientes no significa 400 tests ni certificación universal. Hay 199 criterios verificados, 83 preservados, 70 documentados, 39 cambiados y nueve limitados. Se conservan límites sobre usuarios reales, certificación, capacidad, heap, comparativas históricas de latencia, tiempo aislado de verificación y disponibilidad futura de enlaces. CI final ejecutó 100 unitarias (una omisión de junction Windows en Linux), siete suites de navegador y confirmación automática de 52 archivos públicos.
