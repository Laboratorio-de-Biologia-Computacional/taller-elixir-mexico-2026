"""Recolorea los banners de la Semana 2 para distinguirlos de los de la Semana 1.

Desplaza 40 grados el tono de los píxeles verde azulado (tono entre 150 y 215
grados y saturación suficiente): el fondo degradado y los trazos color menta pasan
a azul índigo. El amarillo de la fecha, el blanco del texto y los demás colores no
cambian.

Se aplicó UNA sola vez, el 1 de octubre de 2026, a los banners originales
(versión del commit 9287ada). Volver a correrlo sobre los banners ya recoloreados
NO los deja igual: los desplaza otra vez. Para regenerarlos, primero se recuperan
los originales con:
    git show 9287ada:assets/img/banner-s2-dia-N.webp > assets/img/banner-s2-dia-N.webp

Uso (desde la raíz del repositorio):
    python3 scripts/recolorear_banners_semana2.py
Requiere Pillow y NumPy.
"""
from pathlib import Path

import numpy as np
from PIL import Image

DESPLAZAMIENTO_GRADOS = 40       # verde azulado -> azul índigo
TONO_MIN, TONO_MAX = 150, 215    # rango de tonos que se recolorean (grados)
SATURACION_MIN = 40              # en escala 0-255: deja fuera blancos y grises


def recolorear(imagen):
    hsv = np.array(imagen.convert("RGB").convert("HSV")).astype(int)
    tono, saturacion = hsv[..., 0], hsv[..., 1]
    # Pillow guarda el tono en escala 0-255 en lugar de 0-360 grados
    mascara = ((tono >= int(TONO_MIN / 360 * 256)) & (tono <= int(TONO_MAX / 360 * 256))
               & (saturacion >= SATURACION_MIN))
    tono[mascara] = (tono[mascara] + round(DESPLAZAMIENTO_GRADOS / 360 * 256)) % 256
    return Image.fromarray(hsv.astype("uint8"), "HSV").convert("RGB")


if __name__ == "__main__":
    carpeta = Path("assets/img")
    for dia in range(1, 6):
        ruta = carpeta / f"banner-s2-dia-{dia}.webp"
        recolorear(Image.open(ruta)).save(ruta, quality=90, method=6)
        print("recoloreado:", ruta)
