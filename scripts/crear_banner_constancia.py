"""Crea el banner del formulario «Solicitud de constancia · Taller ELIXIR-México 2026».

Sigue el diseño de assets/img/banner-registro.webp, que es el banner del otro
formulario que abarca las dos semanas: mismo tamaño (1600 x 400), mismo fondo
degradado, mismo título y subtítulo; solo cambian la etiqueta amarilla
(«CONSTANCIAS» en lugar de «REGISTRO») y el dibujo de la derecha. Usa las
tipografías del sitio (Poppins, en assets/fuentes). El dibujo es una constancia con
un sello, con los mismos colores de trazo que el dibujo del registro.

Cómo funciona:
  1. Ajusta un degradado suave a los píxeles de fondo de banner-registro.webp (sin
     texto ni dibujo) y lo usa como fondo limpio.
  2. Dibuja el texto y el dibujo con Chromium (Playwright) sobre fondo transparente
     y los superpone.

Uso (desde la raíz del repositorio):
    python3 scripts/crear_banner_constancia.py
Escribe assets/img/banner-constancia.webp. Requiere Pillow, NumPy y Playwright
para Python con Chromium. No descarga nada ni modifica otros archivos.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "assets" / "img"
FUENTES = RAIZ / "assets" / "fuentes"
ANCHO, ALTO = 1600, 400
DESTINO = IMG / "banner-constancia.webp"

# Colores medidos en banner-registro.webp
AMARILLO = "#F2B234"
TEXTO_ETIQUETA = "#1E2319"
MENTA = "#BEF4EB"
SUBTITULO = "#D7EEEC"

PLANTILLA = """<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:600;src:url({f}/poppins-latin-600-normal.woff2)}}
@font-face{{font-family:P;font-weight:700;src:url({f}/poppins-latin-700-normal.woff2)}}
html,body{{margin:0;background:transparent}}
.b{{position:relative;width:{w}px;height:{h}px;font-family:P;color:#fff}}
.t{{position:absolute;left:90px;top:59px;width:1060px}}
.e{{display:inline-block;background:{am};color:{te};font-weight:700;font-size:27px;
   letter-spacing:3.4px;padding:9px 20px 7px;border-radius:7px;margin-bottom:22px}}
h1{{margin:0 0 16px;font-weight:700;font-size:62px;line-height:1.13;white-space:nowrap}}
.s{{font-weight:700;font-size:31px;color:{su};white-space:nowrap}}
svg{{position:absolute;left:1180px;top:30px}}
</style></head><body><div class="b">
<div class="t"><div class="e">CONSTANCIAS</div>
<h1>Taller ELIXIR-México de Recursos<br>de Datos y Conocimiento</h1>
<div class="s">16 al 27 de noviembre de 2026 · Cuernavaca, Morelos</div></div>
<svg width="380" height="340" viewBox="0 0 380 340" fill="none" stroke-linecap="round"
     stroke-linejoin="round">
  <!-- hoja de la constancia -->
  <rect x="40" y="20" width="250" height="300" rx="16" stroke="{me}" stroke-width="5"/>
  <rect x="58" y="38" width="214" height="264" rx="8" stroke="{me}" stroke-width="2"
        opacity=".45"/>
  <!-- encabezado y renglones -->
  <circle cx="165" cy="78" r="13" fill="{me}"/>
  <line x1="95" y1="118" x2="235" y2="118" stroke="{me}" stroke-width="6"/>
  <line x1="85" y1="152" x2="245" y2="152" stroke="{me}" stroke-width="3" opacity=".6"/>
  <line x1="85" y1="178" x2="245" y2="178" stroke="{me}" stroke-width="3" opacity=".6"/>
  <line x1="85" y1="204" x2="200" y2="204" stroke="{me}" stroke-width="3" opacity=".6"/>
  <!-- firma -->
  <path d="M85 262 q14 -22 26 -4 t24 -6 t20 2" stroke="{me}" stroke-width="3"/>
  <line x1="85" y1="276" x2="170" y2="276" stroke="{me}" stroke-width="2" opacity=".6"/>
  <!-- sello con listones -->
  <path d="M262 290 l-16 46 l20 -10 l12 18 l10 -44" fill="{am}" stroke="{am}"
        stroke-width="3"/>
  <path d="M302 290 l16 46 l-20 -10 l-12 18 l-10 -44" fill="{am}" stroke="{am}"
        stroke-width="3"/>
  <circle cx="282" cy="262" r="44" fill="{am}"/>
  <circle cx="282" cy="262" r="33" stroke="#0F5560" stroke-width="3"/>
  <path d="M266 262 l11 11 l21 -23" stroke="#0F5560" stroke-width="6"/>
</svg>
</div></body></html>"""


def fondo_limpio(original):
    """Degradado ajustado a los píxeles de fondo (sin texto ni trazos) del original."""
    a = np.asarray(original, dtype=float)
    ys, xs = np.mgrid[0:ALTO, 0:ANCHO]
    oscuro = (a.mean(axis=2) < 110) & (a[..., 0] < 60)
    trazos = Image.fromarray((~oscuro * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))
    sel = oscuro & (np.asarray(trazos) == 0)
    u, v = xs / ANCHO, ys / ALTO
    base = np.stack([np.ones_like(u), u, u ** 2, v, u * v], axis=-1)
    salida = np.zeros((ALTO, ANCHO, 3))
    for c in range(3):
        coef, *_ = np.linalg.lstsq(base[sel], a[..., c][sel], rcond=None)
        salida[..., c] = base @ coef
    ruido = np.random.default_rng(0).normal(0, 0.6, salida.shape)   # evita bandas
    return Image.fromarray(np.clip(salida + ruido, 0, 255).astype("uint8"))


def main():
    original = Image.open(IMG / "banner-registro.webp").convert("RGB")
    imagen = fondo_limpio(original).convert("RGBA")
    capa = IMG / "banner-constancia-texto.png"
    html = capa.with_suffix(".html")
    html.write_text(PLANTILLA.format(f=FUENTES.as_uri(), w=ANCHO, h=ALTO, am=AMARILLO,
                                     te=TEXTO_ETIQUETA, me=MENTA, su=SUBTITULO),
                    encoding="utf-8")
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={"width": ANCHO, "height": ALTO})
        pagina.goto(html.as_uri())
        pagina.evaluate("document.fonts.ready")
        pagina.screenshot(path=str(capa), omit_background=True)
        navegador.close()
    imagen.alpha_composite(Image.open(capa).convert("RGBA"))
    html.unlink()
    capa.unlink()
    imagen.convert("RGB").save(DESTINO, quality=90, method=6)
    print("creado:", DESTINO.relative_to(RAIZ))


if __name__ == "__main__":
    main()
