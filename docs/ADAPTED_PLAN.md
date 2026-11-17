# Plan adaptado: 20 perfiles y 400 criterios

Fecha: 18 de noviembre de 2026. Base: `32d65db`. Estado: **adaptación revisada; ejecución en curso**.

El registro canónico es [adapted-plan.json](adapted-plan.json); el contrato de implementación es [CONTRACTS.md](CONTRACTS.md). Los perfiles representan perspectivas de revisión, no personas externas consultadas. Cada criterio conserva correspondencia ordinal con el adjunto original. Una aceptación puede preservar lo existente y compartir evidencia con otras: no se afirman 400 defectos ni se requieren 400 cambios.

## Alcance y coordinación

- Portfolio estático Python ES/EN: 26 rutas de contenido más 404, 12 artículos, 2 working papers, 6 casos y laboratorio sintético. Se conservan URLs, contacto, fuentes y atribución individual.
- Dos contextos: mantenimiento editorial local y lectura pública. No se crea una aplicación privada.
- Cambios acordados: contrato editorial y `data/site.json`; staging limpio con recuperación; UTF-8/LF; inventario permitido y `release.json` v1; normalización de filtros URL; tabla accesible del laboratorio; gates CI y documentación operativa.
- Fórmula preservada: SE = sqrt(2 SD² / n); IC = delta ± 1.96 SE. Dos grupos independientes, del mismo tamaño y SD; aproximación normal. No calcula potencia ni demuestra causalidad.
- Un escritor por módulo. El coordinador integra `build.py`, HTML compartido, CI y `public/`; fixtures en temporales aislados.
- A: contratos y adaptación (P01–P04, P07–P08). B: módulos coordinados (P05–P06, P09–P13). C: release/CI (P14, P18–P19). D: QA (P15–P17 y revisión P07). E: documentación/publicación (P20, P01, P18).
- Todos los criterios parten **pendientes**. El cierre debe registrar evidencia, revisión, límites y resultados reales; generar este plan no constituye ejecución.
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

## P01 — Dirección de producto del portfolio

Oleada: A. Evidencia común: README, CONTRACTS y recorridos headless portada/equipos/casos/contacto.

Prompt: Completa los recorridos editorial y público conservando ES/EN, evidencia profesional y acceso abierto; consolida obligaciones compartidas sin multiplicar funciones.

Aceptación del perfil: evaluar sus 20 criterios sobre el candidato común; conservar comportamientos demostrados y declarar cualquier pendiente.

1. El editor identifica qué fuentes modificar y cómo validar antes de publicar.
2. El visitante encuentra especialización, contribución individual y contacto.
3. La guía distingue mantenimiento local de lectura pública sin inventar un panel.
4. El recorrido editorial enumera edición, build, pruebas, despliegue y recuperación.
5. Las seis áreas principales siguen accesibles en ES/EN.
6. Fechas de artículos y trayectoria se distinguen de actualización editorial.
7. Modificar fuentes y publicar en Pages se describen como etapas diferentes.
8. Un build local correcto no se comunica como publicación ya disponible.
9. El manifiesto servido permite identificar el candidato publicado.
10. Se conservan 12 artículos y 2 working papers separados, sin cohortes inventadas.
11. La espera descrita corresponde a CI/Pages, sin temporizador artificial.
12. Un fallo de validación/render preserva la salida anterior y bloquea deploy.
13. Reconstruir el mismo contenido mantiene su digest sin prohibir commits legítimos.
14. Demo sintética y evidencia investigadora se diferencian en laboratorio y casos.
15. Primera visita y cero coincidencias tienen recorridos comprensibles sin cuenta.
16. README permite retomar mantenimiento desde un checkout limpio.
17. Casos, publicaciones con ancla y laboratorio conservan acceso directo.
18. El recorrido equipos→caso→perfil/contacto se completa sin callejones sin salida.
19. Obligaciones duplicadas comparten contratos y evidencia identificada.
20. El cierre distingue preservado, verificado, cambiado, limitado y pendiente.

## P02 — Dirección de metodología y rigor científico

Oleada: A. Evidencia común: app.js, lab_page, datos de casos, SOURCES y oráculo independiente.

Prompt: Preserva fórmula, supuestos y atribuciones verificadas; explica límites sin importar clasificaciones científicas del producto ajeno.

Aceptación del perfil: evaluar los 20 criterios con código, fuentes existentes y pruebas independientes; no inventar análisis nuevos.

1. Se conservan tres controles reales: n, diferencia y SD.
2. Diferencia cero y signos positivo/negativo no se confunden con ausencia de datos.
3. El mismo estado produce iguales resultados científicos en ES/EN.
4. La explicación trata diferencia y precisión, sin categorías de compasión ajenas.
5. SD se identifica como dispersión y no como error estándar por sí sola.
6. Se mantienen tres interpretaciones: positivo, negativo e incluye cero.
7. Estimación, SE y límites se derivan de las mismas entradas.
8. Gráfico, tabla y texto representan el mismo cálculo, no pruebas independientes.
9. La separación estadística no se presenta como utilidad empresarial automática.
10. n significa observaciones por grupo y ambos grupos tienen igual tamaño.
11. URL inválidas no producen NaN ni intervalos fuera de los dominios definidos.
12. La demo no afirma excluir participantes o evaluar datos reales.
13. Repetir entradas produce resultados idénticos sin aleatoriedad.
14. La fecha editorial no interviene en el cálculo.
15. Las cifras de los casos conservan fuente y contexto de muestra.
16. TeensLab no se presenta como muestra nacional representativa ni n universal por tarea.
17. Las narraciones distinguen descripción, asociación y conclusión del estudio.
18. El laboratorio conserva su advertencia de que no demuestra causalidad.
19. Se preservan SE=sqrt(2*SD²/n) e IC=delta±1.96*SE, sin dp_efficiency.
20. La guía vincula método, código y revisión; cambios futuros requieren revisión explícita.

## P03 — Investigación de experiencia de uso

Oleada: A. Evidencia común: recorridos headless, capturas ES/EN, README e informe de tareas.

Prompt: Inspecciona tareas reales del editor y lector; separa observaciones verificadas de hipótesis de usabilidad sin inventar entrevistas.

Aceptación del perfil: registrar resultados de 20 tareas/observaciones y límites del método de inspección.

1. El primer acceso al repo permite localizar comandos y fuentes editables.
2. Editar y reconstruir no exige pasos manuales ocultos.
3. El perfil distingue trabajos históricos del puesto actual.
4. Se diferencian fecha científica, captura de demo y actualización editorial.
5. Portada y equipos ofrecen siguiente paso hacia evidencia o contacto.
6. La guía explica CI sin hacer esperar al visitante una actualización inexistente.
7. Los diagnósticos distinguen validación, build, verificación y despliegue.
8. Un campo inválido tiene corrección localizable y preserva salida anterior.
9. Volver atrás recupera filtros válidos sin autenticación.
10. Errores editoriales identifican ubicación sin exponer valores sensibles.
11. La advertencia sintética precede a la interpretación del laboratorio.
12. Los enlaces de laboratorio llevan a demo, código y materiales.
13. Los casos conducen a repositorio, artículo o demo según su estado real.
14. Buscar, tema, año y reset tienen etiquetas y estado reconocible.
15. El lector puede identificar n como tamaño de cada grupo.
16. Cero coincidencias no se confunde con efecto cero.
17. La página no cambia automáticamente mediante polling ni anuncios ficticios.
18. A 320 y 390 px se puede navegar, filtrar, leer y contactar sin overflow.
19. Hallazgos se priorizan por impacto observado; frecuencia no medida se declara desconocida.
20. El informe identifica inspección y automatización, sin atribuir entrevistas inexistentes.

## P04 — Diseño de interfaces accesibles

Oleada: A. Evidencia común: CSS, HTML, teclado headless, capturas y axe cuando esté disponible.

Prompt: Conserva identidad visual y verifica teclado, foco, etiquetas, texto equivalente y adaptación; no presentes la revisión como certificación WCAG.

Aceptación del perfil: documentar los 20 checks y su alcance, preservando las mejoras previas.

1. Texto principal mantiene tamaño y altura de línea legibles en móvil/escritorio.
2. Cada página tiene un h1 y jerarquía comprensible de secciones.
3. Contraste de texto, controles y foco se comprueba en el alcance inspeccionado.
4. Colores del laboratorio no implican éxito comercial automático.
5. Signo e intervalo se expresan con números y texto además de color.
6. Menú, filtros, detalles y sliders funcionan por teclado.
7. Foco es perceptible sobre fondos y estados seleccionados.
8. El salto al contenido lleva a main y evita navegación repetida.
9. Escape cierra menú móvil y devuelve foco al disparador.
10. Estados de filtros y fallo de copiar correo se explican junto al control.
11. Búsqueda, selectores y sliders tienen nombres accesibles asociados.
12. La tabla del laboratorio usa encabezados y semántica nativa.
13. El detalle de tabla se abre por teclado sin una matriz artificial.
14. Título SVG, texto y tabla ofrecen resultados equivalentes.
15. La tabla no crea una segunda región viva duplicada.
16. Se respeta reduced-motion sin animaciones necesarias para comprender.
17. A 200% de texto y 320 px no se recorta contenido esencial.
18. Objetivos táctiles inspeccionados conservan área y separación utilizables.
19. Autoría, versiones y enlaces no se superponen a 320 px.
20. lang y controles corresponden a es/en según ruta.

## P05 — Diseño de explicación científica y casos

Oleada: B. Evidencia común: case_page, lab_page, projects.json, lectura y navegación.

Prompt: Adapta la intención docente a casos y laboratorio mediante secuencia, evidencia y límites; no fuerces doce diapositivas ni nuevas pantallas.

Aceptación del perfil: revisar 20 propiedades del contenido existente y mejorar solo lo acordado.

1. Los seis casos presentan el problema antes de herramientas técnicas.
2. La demo explica qué cambia y qué permanece fijo.
3. Cada caso distingue el papel individual del trabajo del equipo.
4. La explicación utiliza los tres controles reales, no seis decisiones ajenas.
5. n=200, delta=3 y SD=15 forman un ejemplo inicial reproducible.
6. Se explican incertidumbre y diferencia sin categorías ajenas.
7. Los resultados visibles responden a la pregunta del ejemplo.
8. Gráfico, tabla y texto se reconocen como representaciones del mismo cálculo.
9. Etiqueta y supuestos expresan n por grupo.
10. Los recursos públicos excluyen documentos administrativos privados.
11. Los grupos sintéticos no se presentan como cohorte observada.
12. Cero y dirección del efecto tienen explicación en ES/EN.
13. Se conservan límites sobre potencia, causalidad y negocio.
14. Se puede explorar y restablecer sin enviar datos.
15. Supuestos y tabla se consultan mediante detalles nativos opcionales.
16. La página sigue usable ampliada sin exigir modo proyección.
17. Anclas y controles son alcanzables por enlace y teclado.
18. Gráfico, leyenda y resultados se leen en escritorio y móvil.
19. Una página abierta no cambia de release durante su explicación.
20. La URL sintética reproduce el ejemplo en su idioma.

## P06 — Dirección de visualización de datos

Oleada: B. Evidencia común: app.js, CSS, SVG/tabla del laboratorio y fixtures numéricas.

Prompt: Conserva un intervalo con escala honesta, texto equivalente y tabla sincronizada; no añadas agregados de participantes ni gráficos ajenos.

Aceptación del perfil: contrastar 20 propiedades con los mismos estados numéricos y registrar límites de inspección.

1. El eje expresa puntos de diferencia, sin porcentajes injustificados.
2. Punto, segmento, tabla y texto utilizan el mismo n, delta y SD.
3. URL inválida se normaliza antes de dibujar sin estado contradictorio.
4. n aparece identificado como observaciones por grupo.
5. n sintético no se presenta como participantes publicados.
6. Efecto cero se sitúa en el centro, distinto de ausencia de JavaScript.
7. Sin JavaScript se explica la limitación y siguen disponibles los materiales.
8. Los límites extremos permitidos permanecen dentro del gráfico.
9. La tabla ordena n, diferencia, SD, SE y límites de forma equivalente ES/EN.
10. La diferencia se expresa en puntos, no crecimiento porcentual.
11. La precisión cerca de cero conserva la dirección del intervalo.
12. Sliders y outputs reflejan los parámetros seleccionados.
13. La demo no se compara con una población de referencia inexistente.
14. El cero está centrado en una escala simétrica.
15. Valores negativos van a izquierda y positivos a derecha.
16. Punto y segmento conservan significado entre idiomas y estados.
17. Valores tabulados coinciden con cálculo y precisión de los límites textuales.
18. Entradas repetidas producen igual escala y coordenadas.
19. Historial e idioma conservan parámetros válidos sin alterar fórmula.
20. Origen sintético y fórmula permanecen accesibles junto al gráfico.

## P07 — Arquitectura de privacidad y seguridad estática

Oleada: A. Evidencia común: contrato editorial, build/release, inventario, pruebas adversas y tráfico público.

Prompt: Mantén frontera entre fuentes editoriales y artefacto público mediante validación, escape y lista permitida; no añadas autenticación ni telemetría.

Aceptación del perfil: comprobar 20 propiedades y declarar que escaneo/allowlist no prueban confidencialidad universal.

1. Cargar el portfolio no consulta Qualtrics ni adquisición privada.
2. El artefacto inspeccionado no contiene credenciales ni rutas locales del propietario.
3. El visitante no edita ni publica; GitHub conserva permisos operativos.
4. No se añaden login/logout ni estados de sesión ficticios.
5. Contenido público no depende de tokens o caducidad de aplicación.
6. Reabrir una ruta no requiere reconectar una cuenta.
7. Se verifica ausencia de endpoint de autenticación en vez de límites de intentos innecesarios.
8. Fixtures y candidatos temporales no se distribuyen.
9. Temporales, caches y documentos privados quedan fuera de salida.
10. Errores indican ubicación sin reproducir valores sensibles rechazados.
11. El verificador rechaza archivos extra, symlinks y escapes de ruta.
12. No se publican microdatos ni se afirma supresión menor de cinco inexistente.
13. Recuentos bibliográficos son públicos y n del laboratorio es sintético.
14. La tabla del laboratorio no incluye atributos individuales ni cruces identificables.
15. Filtros consultan metadatos públicos de artículos, no participantes.
16. DOM y JSON distribuidos no esconden valores privados tras estilos.
17. Diffs de releases contienen archivos públicos, no entradas administrativas.
18. No se crean identificadores ni historial remoto de visitantes.
19. Texto se escapa y URL ejecutables o con credenciales se rechazan.
20. La prueba registra tráfico sin conexiones privadas y declara su alcance.

## P08 — Arquitectura del portfolio estático

Oleada: A. Evidencia común: CONTRACTS, build.py, contrato editorial, app.js y workflow.

Prompt: Mantén Python estándar y HTML progresivo; separa validación, render y publicación sin migrar framework ni introducir servicios.

Aceptación del perfil: verificar 20 límites arquitectónicos, evitando componentes sin necesidad real.

1. Se documentan edición local y lectura pública como contextos del mismo portfolio.
2. El núcleo usa Python estándar y no incorpora R.
3. Validación, render e interacción tienen responsabilidades identificables.
4. load_content y validate_content no escriben ni hacen red.
5. HTML contiene contenido y enlaces; JavaScript solo mejora la experiencia.
6. Se mantienen cinco catálogos y se añade site según contrato.
7. El candidato se renderiza separado de public vigente.
8. release.json usa schema_version 1 y campos acordados.
9. El navegador no requiere backend ni manifiesto para renderizar.
10. Pages sigue disponible con el ordenador del editor apagado.
11. Fuentes de trabajo se distinguen del inventario aprobado de distribución.
12. Un escritor por módulo y coordinador para build/public evitan conflictos.
13. Fixtures usan temporales sin sobrescribir salida compartida.
14. Un fallo conserva salida previa o informa recuperación concreta.
15. No se añade base de datos ni persistencia remota del visitante.
16. Git/Pages conservan material público sin incorporar expedientes privados.
17. El contrato admite catálogos actuales y rechaza versión site desconocida.
18. Se mantienen 26 rutas ES/EN y 404.
19. El artefacto es estático y SITE_URL configura identidad canónica segura.
20. La recuperación reconstruye y redeploya revisión conocida sin servicios nuevos.

## P09 — Ingeniería de construcción fiable

Oleada: B. Evidencia común: build/release, pruebas de fallos inyectados, determinismo y logs.

Prompt: Valida antes de escribir, conserva salida anterior y distingue candidato correcto de publicación confirmada; no prometas atomicidad universal.

Aceptación del perfil: verificar 20 estados/invariantes operativos con fixtures aisladas cuando haya mutaciones.

1. Diagnósticos distinguen validación, render, verificación y promoción.
2. Trazabilidad usa revisión y digest, sin IDs de visitante o sesión.
3. Solo editor/CI ejecutan publicación; no hay acciones públicas mutables.
4. No se impone cooldown artificial de tres minutos.
5. Abrir pestañas no inicia builds ni bloqueos de publicación.
6. El procedimiento asigna un único escritor de public.
7. No se añade botón público de build ni cola de clics.
8. Lectura pública no depende del progreso de construcción local.
9. Fallos de render/promoción terminan con diagnóstico, sin reintentos ilimitados.
10. Build offline no falla por caída de repositorio bibliográfico.
11. Candidato inválido no reemplaza public anterior.
12. Promoción fallida intenta restauración y comunica copia recuperable si procede.
13. content_digest deriva del inventario canónico, no del reloj.
14. Reconstrucción idéntica conserva bytes y digest verificables.
15. CI coordina despliegues y detecta candidato servido obsoleto.
16. El flujo no utiliza force-push ni sobrescritura remota ajena.
17. Reintentar valida candidato completo y no reutiliza salida parcial.
18. Build local no se declara publicación remota confirmada.
19. Error indica siguiente paso y salida conservada cuando corresponda.
20. Fixtures cubren validación, render y promoción sin tocar producción.

## P10 — Curación sénior de fuentes bibliográficas

Oleada: B. Evidencia común: publications, working-papers, resources, SOURCES y contrato editorial.

Prompt: Sustituye adquisición Qualtrics por catálogos curados offline; conserva versiones abiertas, DOI y autoría sin prometer acceso perpetuo.

Aceptación del perfil: revisar 20 propiedades de metadatos, fuentes y límites de comprobación externa.

1. Artículos, working papers y materiales permanecen diferenciados.
2. IDs únicos/seguros y referencias locales resuelven al catálogo correcto.
3. URL editoriales rechazan esquemas ejecutables y credenciales embebidas.
4. Visita y build no requieren credenciales bibliográficas.
5. Año científico no se sustituye por fecha de descarga.
6. Campos numéricos respetan tipos definidos por el contrato.
7. Títulos originales se preservan sin importar variables Qualtrics.
8. Lista de autores y author_parts conservan orden editorial.
9. BibTeX mantiene apellidos compuestos como Alfonso Costillo.
10. Campos inesperados o incompatibles fallan antes del render.
11. site.updated usa fecha ISO válida separada de años bibliográficos.
12. Etiquetas distinguen preprint, manuscrito y versión editorial cuando consta.
13. Corpus no excluye artículos por hora de acceso al repositorio.
14. Cada build valida todos los catálogos requeridos.
15. SOURCES distingue procedencia, publicación y limitaciones de verificación.
16. Un destino bloqueado se registra no confirmado, sin borrar automáticamente el artículo.
17. Build offline no finge descargar o verificar PDFs externos.
18. No se copian documentos privados ni microdatos al artefacto.
19. Archivos temporales de inspección quedan fuera del inventario público.
20. Pruebas usan fixtures o verificaciones explícitas, sin llamadas masivas a proveedores.

## P11 — Ingeniería de datos editoriales

Oleada: B. Evidencia común: content_contract, data/*.json y fixtures de validación.

Prompt: Valida tipos, traducciones, referencias y cardinalidades antes de renderizar; deriva recuentos de catálogos públicos sin modificar su significado.

Aceptación del perfil: ejecutar 20 comprobaciones sobre fuentes reales y fixtures inválidas, sin corregir silenciosamente datos.

1. Los seis catálogos se cargan bajo sus claves definidas sin reescribir fuentes.
2. Tipos estrictos no confunden booleanos con enteros de esquema.
3. site.updated rechaza fechas imposibles y formatos no ISO.
4. Fecha inválida genera diagnóstico localizado, no fecha sustitutiva.
5. IDs y destacados duplicados se rechazan sin deduplicación silenciosa.
6. Actualización visible deriva de site.updated, no del reloj del build.
7. Datos inválidos se detectan antes de tocar salida anterior.
8. Lab respeta mínimos n=20, delta=-15 y SD=5.
9. Lab respeta máximos n=2000, delta=15 y SD=40.
10. Artículos del mismo año no se eliminan como duplicados.
11. Trabajos históricos no desaparecen por ventanas relativas al presente.
12. Corpus y destacados dependen de datos explícitos, no del reloj.
13. IDs de portada resuelven al catálogo correspondiente.
14. Errores identifican archivo, registro y campo corregible.
15. Totales de artículos, working papers y casos se derivan de datos.
16. Temas corresponden a categorías reales sin país/género inventados.
17. El corpus de esta entrega conserva 12 artículos y 2 working papers.
18. Orden y serialización producen igual resultado con fuentes idénticas.
19. Campo obligatorio ausente genera error, no cero o texto inventado.
20. Referencias entre casos, artículos y destacados se validan antes de publicar.

## P12 — Experiencia de mantenimiento editorial

Oleada: B. Evidencia común: README, guía operativa, mensajes de validación/build y CONTRACTS.

Prompt: Ofrece un flujo local documentado en vez de panel autenticado; explica entradas, versión y recuperación sin añadir interfaz innecesaria.

Aceptación del perfil: comprobar 20 puntos de operación y documentación contra el comportamiento final.

1. README indica propósito y primer comando de construcción.
2. La guía localiza datos, render, estilos, interacción, pruebas y salida.
3. Se explica cómo leer revisión y digest del manifiesto.
4. El editor conoce los 12 artículos, 2 working papers y 6 casos de la entrega.
5. Actualización editorial, año del artículo y despliegue se diferencian.
6. Se documenta dónde editar títulos, roles y enlaces de casos.
7. SOURCES conserva atribuciones y límites sin saturar interfaz pública.
8. Edición, pruebas, commit y publicación se describen por separado.
9. La espera remite al job real de Pages, sin contador ficticio.
10. La guía identifica único escritor y evita public durante promoción concurrente.
11. Comandos/CI muestran etapas reales y no porcentajes simulados.
12. Digest igual se explica como mismo contenido aunque cambie documentación.
13. Se explica cómo corregir datos y reintentar sin perder salida anterior.
14. La versión desplegada permanece durante edición o build fallido.
15. Diagnósticos de desarrollo no se copian al sitio.
16. Esquema y errores se documentan fuera de los recorridos públicos principales.
17. Cambiar el cálculo exige localizar código y pasar pruebas metodológicas.
18. Instrucciones no incluyen tokens ni contraseñas reales.
19. Retomar mantenimiento incluye comprobar revisión y estado de trabajo.
20. README identifica URL canónica y comando de previsualización.

## P13 — Frontend público y mejora progresiva

Oleada: B. Evidencia común: app.js, HTML y pruebas de URL/historial/idioma/no-JS.

Prompt: Preserva HTML útil, normaliza filtros URL y añade equivalencia tabular del laboratorio; sin polling ni datos remotos adicionales.

Aceptación del perfil: comprobar 20 estados del lector en ES/EN con y sin JavaScript.

1. HTML contiene el catálogo sin servicio remoto duplicado.
2. Render inicial no depende de release.json ni petición posterior de datos.
3. No se instala polling de 60 segundos ni otro refresco periódico.
4. Ocultar pestaña no mantiene tareas de red creadas por el portfolio.
5. Volver a pestaña no resetea filtros ni reemplaza página automáticamente.
6. Filtrar no vuelve a descargar catálogos ni PDFs externos.
7. Manifiesto se verifica operativamente, no como dependencia del visitante.
8. Resultados, contador y URL reflejan el mismo estado aplicado.
9. topic/year desconocidos se eliminan al cargar y navegar historial.
10. Controles normalizados muestran los valores realmente aplicados.
11. Página cargada conserva filtros/lab sin servicios privados.
12. La interfaz no anuncia releases pendientes que no observa.
13. Años científicos no se reemplazan por fecha del release.
14. Fecha editorial deriva de site.updated, no de apertura de página.
15. Búsqueda, tema y año operan sobre artículos presentes en DOM.
16. Tabla se actualiza con gráfico y usa igual precisión de límites.
17. Estado vacío ofrece explicación y reset conservando formulario.
18. URL malformadas no ejecutan HTML ni causan errores JavaScript.
19. Cargar rutas no consulta APIs privadas ni seguimiento inesperado.
20. Filtros, navegación, tabla y casos funcionan a 320/390/768/1440 px.

## P14 — Arquitectura de publicación verificable

Oleada: C. Evidencia común: build/release, manifiesto v1, pruebas de alteración/recuperación y CI.

Prompt: Construye candidato limpio, verifica inventario y hashes, promueve con recuperación; el manifiesto registra consistencia, no firma criptográfica.

Aceptación del perfil: probar 20 invariantes sobre candidatos aislados y confirmar el servido al publicar.

1. Render ocurre en temporal nuevo bajo repo, separado de public vigente.
2. content_digest es SHA-256 del inventario canónico de bytes.
3. Reloj y revisión no alteran digest de archivos idénticos.
4. Manifiesto respeta campos v1 y verificación rechaza esquemas desconocidos.
5. Allowlist y verificación preceden al upload del artefacto.
6. Textos generados usan UTF-8 y LF entre entornos.
7. Hash y tamaño se calculan sobre bytes de cada archivo.
8. Inventario POSIX ordenado excluye release.json y .nojekyll según contrato.
9. Promoción fallida intenta restauración sin prometer atomicidad universal.
10. Promoción no toca fuentes ni archivos ajenos a salida/temporales propios.
11. Workflow coordina despliegues y comprueba candidato esperado.
12. Reintento idéntico mantiene digest sin duplicar contenido.
13. source_revision es SHA limpio de 40 caracteres o null cuando no atribuible.
14. Fallos de contrato, pruebas o verificación bloquean deploy.
15. Versión servida se compara con candidato y discrepancia se informa.
16. Manifiesto y bytes servidos se contrastan sin exigir .nojekyll por HTTP.
17. Fallo de validación/render conserva bytes de salida anterior.
18. Informe distingue preparado, validado, desplegado y confirmado.
19. Guía permite reconstruir y redeployar revisión conocida con pruebas.
20. Manifiesto excluye visitantes, microdatos, credenciales y tiempos individuales.

## P15 — QA de métodos y contratos de datos

Oleada: D. Evidencia común: expectativas Python independientes, navegador y fixtures temporales.

Prompt: Protege fórmula, entradas y contratos con expectativas independientes; no implementes el oráculo de 64 patrones de otro estudio.

Aceptación del perfil: documentar 20 checks con fixtures y tolerancias pertinentes, evitando tests que solo repitan implementación.

1. Oráculo Python independiente cubre estados representativos del laboratorio.
2. Se comparan estimación, SE y límites con tolerancias declaradas.
3. Texto, tabla y gráfico coinciden en positivo, negativo e incluye cero.
4. Pruebas fijan sqrt(2*SD²/n) y 1.96 sin regresión ajena.
5. Fixtures cubren los seis tipos de catálogos definidos.
6. Campos desconocidos, tipos erróneos y referencias rotas se rechazan.
7. Faltan campos/traducciones obligatorios: ContentError localizable.
8. Tipos numéricos inválidos y booleanos indebidos no pasan validación pertinente.
9. Se prueban IDs/destacados duplicados y autoría inconsistente.
10. Fechas imposibles o no ISO fallan antes de construir.
11. Artículos antiguos permanecen en catálogo y filtros.
12. Se prueban extremos/pasos de n, delta y SD y URL fuera de dominio.
13. Datos inválidos mantienen salida previa intacta en fixture aislada.
14. Fecha editorial y digest no dependen de zona horaria o DST.
15. Conteos de filtros coinciden con registros públicos esperados.
16. Casos cerca de cero verifican signo y precisión de redondeo.
17. Fixtures no contienen participantes reales ni tablas cruzadas inexistentes.
18. UTF-8/LF, inventario, alteración y recuperación se prueban en temporales.
19. Cambio público cambia digest; cambio solo de revisión no lo cambia.
20. Se preserva orden editorial de listas y serialización canónica de mapas.

## P16 — QA de navegador y accesibilidad

Oleada: D. Evidencia común: tests headless, capturas, tráfico, fixtures y axe opcional.

Prompt: Prueba estados reales del portfolio: filtros, historial, idiomas, laboratorio, teclado, móvil y red; no simules login inexistente.

Aceptación del perfil: registrar 20 comprobaciones del candidato y límites de automatización/accesibilidad.

1. Rutas públicas abren sin cuenta ni controles de sesión ficticios.
2. Visita no caduca por autenticación para usar controles locales.
3. Interfaz y red no permiten lanzar publicación desde la visita.
4. Se verifica portada→equipos→caso→perfil/contacto en ES/EN.
5. Repetir reset/menú no rompe estado ni foco.
6. Dos contextos mantienen URL propia sin bloqueo ni storage compartido.
7. Bloquear red externa no rompe lectura, filtros ni laboratorio locales.
8. Build fallido conserva salida anterior sin servir candidato parcial.
9. Informe no llama publicado a un candidato solo local.
10. Sin JS se leen 12 artículos, enlaces y advertencia de controles.
11. Verificador detecta cambio de digest sin recarga automática del visitante.
12. Fixture con bytes alterados falla verificación antes de deploy.
13. Versión de esquema desconocida falla de forma explícita.
14. Tabla, texto y SVG coinciden con expectativas independientes.
15. Se cubren tema/año, búsqueda, vacío, inválidos, historial e idioma.
16. Teclado verifica salto, Escape, filtros, detalles y reset con foco.
17. Se inspeccionan 320/390/768/1440 px y texto al 200%.
18. Hay una región viva de resultados lab y anuncios de filtros comprensibles.
19. Fixtures de texto/URL adversos no ejecutan HTML o código.
20. Tráfico registrado no contiene APIs privadas ni seguimiento inesperado.

## P17 — Ingeniería de rendimiento proporcionado

Oleada: D. Evidencia común: inventario, mediciones headless/build e informe con condiciones.

Prompt: Mide costes estáticos en condiciones declaradas y conserva interacción local; evita pruebas masivas o proveedores ajenos al alcance.

Aceptación del perfil: revisar 20 propiedades, diferenciando medición, inspección y aspectos no medidos.

1. Informe identifica navegador, viewport y entorno de medición.
2. Se distingue localhost de producción y cualquier limitación de red.
3. Se suman bytes públicos y se identifican recursos de mayor peso.
4. Se registra peso de manifiesto/HTML sin asumir descarga cliente de catálogos.
5. Se observa disponibilidad de filtros bajo condiciones reproducibles.
6. Filtros/sliders responden sin esperar peticiones de red.
7. Sesión repetida se inspecciona sin afirmar presupuesto universal de memoria.
8. Filtrar trabaja con registros existentes sin reconstruir toda la página.
9. No se añade indexación compleja para 12 artículos sin justificación medida.
10. Imágenes conservan dimensiones, variantes y carga diferida pertinentes.
11. No hay polling ni trabajo periódico de red en pestaña oculta.
12. Interacciones no descargan nuevamente datos o PDFs externos.
13. Comparaciones distinguen carga fría de caché caliente.
14. Build local no bloquea una página pública ya cargada.
15. No se afirma capacidad probada de 30/60/200 clientes.
16. Producción comprueba estado HTTP y MIME de recursos críticos.
17. Build no incluye exportaciones Qualtrics ni adquisición remota.
18. Se registra duración de build/verificación en el entorno usado.
19. Tabla y detalles no incorporan librerías gráficas ni red nueva.
20. Cambios de peso/tiempo se comparan con línea base antes de optimizar.

## P18 — Ingeniería DevOps de GitHub Pages

Oleada: C. Evidencia común: workflow, guía operativa, logs CI y manifiesto servido.

Prompt: Ejecuta validación y pruebas antes de Pages, separa PR de deploy y documenta recuperación con hosting existente; sin R/Vite.

Aceptación del perfil: comprobar 20 propiedades del pipeline y declarar comprobaciones remotas pendientes si las hubiera.

1. Solo public se sube a Pages, no fuentes privadas.
2. CI declara Python 3.12 y build usa biblioteca estándar.
3. Dependencias de QA no se convierten en runtime del sitio.
4. Workflow e informe identifican herramientas de pruebas.
5. Se conserva build.py sin añadir Vite o bundler.
6. CI ejecuta pruebas de contrato, build y método pertinentes.
7. CI incluye interacción JavaScript mediante headless.
8. E2E cubre filtros, idiomas y laboratorio sin proveedores privados.
9. Inventario y hashes se verifican antes de upload-pages-artifact.
10. Tests, docs, reviews y paquetes de desarrollo no se sirven.
11. No se añaden tokens y workflow conserva permisos mínimos.
12. Concurrencia de deploy está coordinada y PR no despliega.
13. Checkout nuevo se construye con comandos documentados sin estado oculto.
14. Validación, build, pruebas y verificación preceden a deploy.
15. Tras publicar se compara manifiesto servido con candidato.
16. Rollback público se documenta como reconstrucción/redeploy verificado.
17. Recuperación local de public no se llama rollback de un panel ficticio.
18. Guía remite a permisos GitHub sin copiar credenciales.
19. Artefacto es portable como archivos estáticos sin Connect Cloud.
20. Operación documenta comandos, entradas y resultados esperados.

## P19 — Observabilidad sin seguimiento

Oleada: C. Evidencia común: logs de comandos/CI, release.json y guía de diagnóstico.

Prompt: Diagnostica construcción y releases con revisión/digest y errores claros; no añadas telemetría de visitantes ni un nuevo servicio.

Aceptación del perfil: comprobar 20 señales operativas y su ausencia de datos privados.

1. Errores distinguen contrato, render, verificación, promoción y comprobación remota.
2. Informes usan revisión/candidato, no IDs de visitante.
3. Resultado de build permite asociar candidato con content_digest.
4. source_revision vincula commit limpio o null explicado.
5. Tiempos medidos indican etapa/entorno sin telemetría pública.
6. Digest idéntico no se comunica como error o nueva evidencia científica.
7. Falta de confirmación HTTP no se transforma en éxito.
8. Último intento observado se identifica por CI/informe sin dashboard inventado.
9. Último éxito se referencia con logs/manifiesto sin visitantes.
10. Cierre compara digest esperado y servido.
11. Verificador identifica archivos ausentes, extra o alterados.
12. Contrato incompatible genera diagnóstico y bloquea promoción.
13. Error de URL no imprime credenciales del valor rechazado.
14. Enlaces no confirmados se registran con fecha/límite sin reintentos masivos.
15. No se registran cooldowns o sesiones Qualtrics inexistentes.
16. Fallo de promoción informa restauración o copia recuperable.
17. Diagnóstico compartible excluye documentos y valores privados.
18. No se almacena telemetría remota y QA queda fuera del sitio.
19. No se añaden analytics, cookies propias o IDs persistentes.
20. Guía ofrece recuperación para cada clase de fallo implementada.

## P20 — Documentación y reproducibilidad

Oleada: E. Evidencia común: README, SOURCES, CONTRACTS, guía operativa e informe final.

Prompt: Documenta producto y contratos reales; conserva ES/EN, separa plan de ejecución y entrega evidencias/límites sin promesas no verificadas.

Aceptación del perfil: revisar 20 puntos contra comportamiento final y mantener los pendientes explícitos.

1. Arquitectura describe fuentes locales, Python y lector estático, no dos apps nuevas.
2. Se indican URL pública y preview sin inventar panel privado.
3. Guía explica editar datos/destacados/fecha y validar.
4. Se explica acceder a casos, artículos abiertos, filtros y laboratorio.
5. Historia científica se distingue de actualización editorial.
6. Un ejemplo aclara que reconstruir no vuelve nuevo un artículo antiguo.
7. Actualizar no exige cooldown inexistente de tres minutos.
8. Se documenta evento de Pages y gates previos.
9. Nuevas versiones aparecen al navegar/recargar, sin polling.
10. Catálogos institucionales sustituyen dos fuentes Qualtrics ajenas.
11. Fórmula, supuestos, n por grupo y límites sintéticos están documentados.
12. Se explica ausencia de microdatos sin afirmar supresión no implementada.
13. Se documenta manifiesto v1, digest, revisión e inventario/exclusiones.
14. Se explica rechazo de versiones desconocidas y conservación de rutas.
15. Guía cubre JSON, referencias, URL, hash y promoción inválidos.
16. Recuperación enumera reconstrucción/redeploy de revisión conocida.
17. Se usan permisos existentes sin publicar credenciales.
18. Valores iniciales y URL permiten reproducir demo ES/EN.
19. Método/pruebas se vinculan a revisión Git y límites declarados.
20. Checklist distingue 400 aceptaciones de cambios reales y referencia pruebas/pendientes.
