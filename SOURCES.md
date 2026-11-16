# Fuentes y decisiones editoriales

Revisión: 16 de noviembre de 2026. Este archivo documenta el contenido público; no incluye expedientes personales ni documentos administrativos.

## Identidad y trayectoria

- [Perfil institucional, Universidad de Sevilla](https://investigacion.us.es/sisius/sis_showpub.php?idpers=45496).
- [ORCID 0000-0002-5396-3711](https://orcid.org/0000-0002-5396-3711).
- [Loyola Behavioral Lab](https://loyolabehlab.org/members/antonio-alfonso/).
- [Google Scholar](https://scholar.google.com/citations?user=tplq8tMAAAAJ), enlazado como catálogo adicional, sin atribuir recuentos de citas no verificados.
- CV y certificados facilitados por el titular: contraste de formación, puestos, estancias y méritos. Se publican los hechos profesionales pertinentes, no los documentos ni sus identificadores personales. Los campos automáticos del CVA que discrepaban de los certificados no se han trasladado a la web.

El doctorado se identifica por su denominación oficial, Administración y Dirección de Empresas, y por la especialización investigadora en economía del comportamiento. No se atribuye una acreditación de Profesor Titular pendiente. La codirección doctoral se describe como completada en 2025.

## Publicaciones y versiones abiertas

`data/publications.json` contiene los doce artículos identificados en el material aportado y contrastados con sus DOI y metadatos editoriales/Crossref. `data/working-papers.json` contiene dos trabajos en desarrollo. Los títulos y la autoría completa se conservan en los datos y en la bibliografía BibTeX; en pantalla se abrevia la autoría extensa.

| Trabajo | Fuente abierta utilizada | Versión / criterio |
| --- | --- | --- |
| Private solution trap | [LSE](https://researchonline.lse.ac.uk/id/eprint/137840/) | PDF institucional verificado |
| Voting with dissatisfaction | [RIO, Universidad Pablo de Olavide](https://hdl.handle.net/10433/26388) | Ficha institucional; primer online 2025, volumen 2026 |
| Baking of preferences | [Loyola 5445](https://repositorio.uloyola.es/handle/20.500.12412/5445) | Manuscrito de marzo de 2024, previo al artículo de 2025 |
| TeensLab | [Loyola 5492](https://repositorio.uloyola.es/handle/20.500.12412/5492) | Manuscrito de 2024; se enlaza además el artículo editorial de 2025 |
| Paper airplanes | [Frontiers](https://doi.org/10.3389/feduc.2024.1301952), [MPRA](https://mpra.ub.uni-muenchen.de/108541/) | Artículo abierto y preprint diferenciados |
| Climate change mitigation | [IOP](https://doi.org/10.1088/2632-072X/ad2372) | Artículo abierto del editor |
| Adventure in the classroom | [PsyArXiv](https://osf.io/preprints/psyarxiv/zphx9) | Preprint diferenciado del artículo |
| Triadic influence | [Loyola 4102](https://repositorio.uloyola.es/handle/20.500.12412/4102) | Copia con portada de ResearchGate |
| Die-under-the-cup | [Loyola 4444](https://repositorio.uloyola.es/handle/20.500.12412/4444) | Manuscrito depositado |
| COVID-19 and generosity | [Loyola 4110](https://repositorio.uloyola.es/handle/20.500.12412/4110) | Versión editorial de 2022 |
| Volunteering | [Loyola 7550](https://repositorio.uloyola.es/handle/20.500.12412/7550) | Documento MPRA de noviembre de 2020, previo al artículo de 2021 |
| Delay of gratification | [Editor](https://doi.org/10.1016/j.socec.2026.102668) | Disponible online; número de diciembre de 2026 |
| Reading Minds to Win | [Loyola 6585](https://repositorio.uloyola.es/handle/20.500.12412/6585) | Documento de trabajo, no se duplica su título anterior |
| Four Directed Balance Rules | [SSRN](https://doi.org/10.2139/ssrn.7687098) | Preprint, separado de artículos evaluados |

Se comprobó la respuesta HTTP y la firma `%PDF` de ocho descargas de artículos/documentos de trabajo en LSE y Loyola y de catorce materiales docentes de Loyola. Se inspeccionó el texto inicial de seis PDFs para ajustar las etiquetas de versión. Los PDF se sirven desde sus instituciones; no se almacenan ni redistribuyen en este repositorio.

Limitaciones de comprobación: SSRN respondió 403 al cliente automatizado; se conserva el DOI aportado en el registro de investigación. Nature devolvió una página intermedia en su ruta PDF: se utiliza el artículo HTML y se mantiene el PDF institucional de Loyola. La ficha RIO responde, pero su interfaz JavaScript requiere consulta en el repositorio para descargar. Los registros de `data/resources.json` conservan el enlace a la ficha y al material original.

## Proyectos y selección

- [SONAR](https://github.com/Teoriadejuego/sonar-2026): arquitectura y protocolo tomados del código/documentación pública. La responsabilidad del proyecto se contrastó con la documentación FIUS–Cotec aportada; no se publica el contrato.
- [ARCO](https://github.com/Teoriadejuego/arco) y [PBIS](https://github.com/Teoriadejuego/pbis-poc): versiones de evaluación con demostraciones sintéticas, sin atribuir implantaciones, clientes ni mejoras comerciales medidas.
- El resto de herramientas procede de los repositorios públicos enlazados en `data/software.json`.
- Los casos de redes, acción colectiva y TeensLab derivan de sus artículos y versiones abiertas. El trabajo en equipo y la participación individual se distinguen.

Se destacan PNAS, Scientific Data y el experimento de honestidad por alcance, método, disponibilidad de evidencia y relevancia aplicada. Esta selección no equivale a un ranking de citas. Los tamaños de muestra que aparecen en los casos son los del estudio o versión identificada, no métricas de uso del software.

## Referencia visual, imágenes y buscadores

La web de [Pablo Brañas-Garza](https://economiaexperimental.es/) orienta la jerarquía: identificación inmediata, biografía compacta, selección de publicaciones y acceso abierto. El diseño, la redacción y los diagramas de este portfolio son propios. El retrato procede de una fotografía facilitada por el titular, con fondo e iluminación editados; la cabecera es una ilustración generada. Prompts en `PROMPTS.md`.

Implementación y SEO según [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [requisitos técnicos de Google](https://developers.google.com/search/docs/essentials/technical) y [ProfilePage](https://developers.google.com/search/docs/appearance/structured-data/profile-page). La preparación técnica facilita el rastreo; no acredita que Google ya haya indexado o posicionado la web.
