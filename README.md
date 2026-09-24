# taller-elixir-mexico-2026

Página web pública del **Taller ELIXIR-México de Recursos de Datos y Conocimiento**
(16 al 27 de noviembre de 2026, Centro de Ciencias Genómicas de la UNAM, Cuernavaca).

Se publica con GitHub Pages desde la rama `main`, carpeta raíz.

## Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | La página completa: portada, las dos semanas con su programa por día, registro y sede |
| `assets/estilo.css` | Estilo con la paleta y la tipografía de la guía de marca de ELIXIR 2025 |
| `assets/img/` | Banners del registro y de los días 4 y 5 de la Semana 2 (WebP) y logotipo de ELIXIR en SVG (versión estándar y negativa), proporcionado por el equipo de ELIXIR |
| `assets/fuentes/` | Tipografías Lato (texto) y Poppins (títulos de la portada, igual que en los banners), servidas desde el propio sitio; licencia SIL OFL 1.1 en `OFL.txt` y `OFL-poppins.txt` |
| `assets/img/tarjeta-redes.jpg` | Imagen de vista previa (1200 × 630) que aparece al compartir la liga en redes sociales, WhatsApp o correo |
| `assets/img/icono.svg`, `icono-180.png` | Ícono de la pestaña del navegador y del acceso directo en teléfono |
| `.nojekyll` | Indica a GitHub Pages que publique los archivos tal cual, sin procesarlos |

## Principios

- Página estática: sin JavaScript, sin cookies, sin servicios de rastreo y sin
  recursos externos (la fuente se sirve desde el propio sitio).
- Accesible: contraste conforme a WCAG AA, navegación por teclado, modo oscuro y
  diseño para teléfono.
- Solo información pública del taller. La organización interna vive en el
  repositorio privado `ELIXIR-Workshop-MX-2026`.

## Dirección de la página

Las etiquetas de vista previa (`og:url`, `og:image`) y la dirección canónica apuntan a
`https://yalbibalderas.github.io/taller-elixir-mexico-2026/`. Si el repositorio se publica
con otro usuario, organización o dominio, se actualizan esas tres líneas en `index.html`.

## Cómo se actualiza

1. Se edita `index.html` (por ejemplo, para agregar ponentes confirmados o el
   programa de un día).
2. Se revisa localmente abriendo `index.html` en el navegador.
3. `git add -A`, `git commit` y `git push`; GitHub Pages publica en uno o dos minutos.

## Licencias

- Código (`index.html`, `assets/estilo.css`): MIT (`LICENSE`).
- Tipografías Lato y Poppins: SIL Open Font License 1.1 (`assets/fuentes/OFL.txt` y `assets/fuentes/OFL-poppins.txt`).
