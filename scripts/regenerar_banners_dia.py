"""Regenera el texto de los banners de día cuyo título ya no coincide con el programa.

Conserva de cada banner original el fondo degradado y el dibujo de la derecha, y
vuelve a escribir a la izquierda la etiqueta de la semana, la fecha y el título del
día con las mismas tipografías del sitio (Poppins, en assets/fuentes).

Cómo funciona, banner por banner:
  1. Ajusta un degradado suave a los píxeles de fondo del banner original (sin texto
     ni trazos) y lo usa como fondo limpio de toda la imagen.
  2. Copia sin cambios la franja derecha del original (el dibujo), con bordes
     difuminados para que no se note la unión.
  3. Dibuja el texto nuevo con Chromium (Playwright) sobre fondo transparente y lo
     superpone.

Se aplicó el 4 de noviembre de 2026 a los banners de la lista BANNERS, para que su
título coincida con la hoja de organización del taller. Correrlo otra vez sobre los
banners ya regenerados da prácticamente el mismo resultado, porque solo reutiliza el fondo y el
dibujo, que no cambian.

Uso (desde la raíz del repositorio):
    python3 scripts/regenerar_banners_dia.py
Requiere Pillow, NumPy y Playwright para Python con Chromium.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "assets" / "img"
FUENTES = RAIZ / "assets" / "fuentes"
ANCHO, ALTO = 1600, 320
X_DIBUJO = 1090          # a partir de aquí se conserva el dibujo original
ARRIBA = 40              # margen superior del bloque de texto, como en los originales

# archivo, semana, fecha, título
BANNERS = [
    ("banner-s1-dia-3", 1, "Miércoles 18 de noviembre",
     "Interoperabilidad, estándares y soberanía de datos"),
    ("banner-s1-dia-5", 1, "Viernes 20 de noviembre",
     "Hoja de ruta y planificación"),
    ("banner-s2-dia-3", 2, "Miércoles 25 de noviembre",
     "Conceptos básicos de la inteligencia artificial (IA) y bioinformática "
     "microbiana en la era de la IA"),
    ("banner-s2-dia-4", 2, "Jueves 26 de noviembre",
     "Aplicaciones de la inteligencia artificial en la investigación y la salud"),
]

# Colores medidos en los banners originales
COLOR_ETIQUETA = {1: "#C1F6F5", 2: "#CCE4F7"}
COLOR_FECHA_FONDO = "#F1B235"
COLOR_FECHA_TEXTO = "#1E2319"

PLANTILLA = """<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:600;src:url({f}/poppins-latin-600-normal.woff2)}}
@font-face{{font-family:P;font-weight:700;src:url({f}/poppins-latin-700-normal.woff2)}}
html,body{{margin:0;background:transparent}}
.b{{position:relative;width:{w}px;height:{h}px;font-family:P;color:#fff}}
.t{{position:absolute;left:80px;top:{arriba}px;width:980px;display:flex;
   flex-direction:column}}
.e{{font-weight:700;font-size:25px;letter-spacing:2.7px;color:{ce};margin:0 0 16px}}
.f{{align-self:flex-start;background:{cf};color:{ct};font-weight:600;font-size:28px;
   padding:5px 18px;border-radius:6px;margin-bottom:12px}}
h1{{margin:0;font-weight:700;font-size:{tam}px;line-height:1.21}}
</style></head><body><div class="b"><div class="t">
<div class="e">TALLER ELIXIR-MÉXICO · SEMANA {s}</div>
<div class="f">{fecha}</div><h1 id="h">{titulo}</h1></div></div></body></html>"""


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


def texto(pagina, semana, fecha, titulo, destino):
    """Dibuja el texto en PNG transparente; reduce el título si no cabe en dos líneas."""
    for tam in range(44, 31, -2):
        html = PLANTILLA.format(f=FUENTES.as_uri(), w=ANCHO, h=ALTO, ce=COLOR_ETIQUETA[semana],
                                cf=COLOR_FECHA_FONDO, ct=COLOR_FECHA_TEXTO, tam=tam, arriba=ARRIBA,
                                s=semana, fecha=fecha, titulo=titulo)
        tmp = destino.with_suffix(".html")
        tmp.write_text(html, encoding="utf-8")
        pagina.goto(tmp.as_uri())
        pagina.evaluate("document.fonts.ready")
        lineas = pagina.evaluate(
            "(() => { const h = document.getElementById('h');"
            " return Math.round(h.getBoundingClientRect().height /"
            " parseFloat(getComputedStyle(h).lineHeight)); })()")
        if lineas <= 2:
            break
    pagina.screenshot(path=str(destino), omit_background=True)
    tmp.unlink()
    return tam


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={"width": ANCHO, "height": ALTO})
        for nombre, semana, fecha, titulo in BANNERS:
            ruta = IMG / f"{nombre}.webp"
            original = Image.open(ruta).convert("RGB")
            imagen = fondo_limpio(original)
            dibujo = original.crop((X_DIBUJO, 0, ANCHO, ALTO))
            mascara = np.zeros((ALTO, ANCHO - X_DIBUJO), "uint8")
            mascara[8:ALTO - 8, 30:] = 255
            imagen.paste(dibujo, (X_DIBUJO, 0),
                         Image.fromarray(mascara).filter(ImageFilter.GaussianBlur(10)))
            capa = IMG / f"{nombre}-texto.png"
            tam = texto(pagina, semana, fecha, titulo, capa)
            imagen = imagen.convert("RGBA")
            imagen.alpha_composite(Image.open(capa).convert("RGBA"))
            capa.unlink()
            imagen.convert("RGB").save(ruta, quality=90, method=6)
            print(f"regenerado: {ruta.name} (título a {tam} px)")
        navegador.close()


if __name__ == "__main__":
    main()
