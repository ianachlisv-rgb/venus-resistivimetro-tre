"""Cálculos analíticos del paper: señal esperada, número de lecturas, tiempo y energía.

Reproduce las tablas y cifras del paper a partir de las fórmulas (terreno homogéneo, sin ruido,
sin fuga ni resistencia de contacto). No usa dependencias externas.

    python codigo/presupuesto_senal.py
"""
from math import pi

N = 48            # electrodos
SEP = 4.0         # separación entre electrodos adyacentes (m)


def k_wenner(a):          # a en metros
    return 2 * pi * a


def k_dd(a, n):           # dipolo-dipolo
    return pi * n * (n + 1) * (n + 2) * a


def k_ws(a, n):           # Wenner-Schlumberger
    return pi * n * (n + 1) * a


def delta_v(rho, i, k):   # ΔV = ρ I / K
    return rho * i / k


def lecturas_wenner(amax=15):
    # A-M-N-B equiespaciados: ocupa 3a posiciones de electrodo
    return sum(N - 3 * a for a in range(1, amax + 1) if N - 3 * a > 0)


def lecturas_dd(amax=4, nmax=6):
    # A-B, n a, M-N: ocupa (n+2)a posiciones
    return sum(N - (n + 2) * a for a in range(1, amax + 1) for n in range(1, nmax + 1) if N - (n + 2) * a > 0)


def lecturas_ws(amax=3, nmax=8):
    # A, M a n*a, N a (n+1)*a, B a (2n+1)*a: ocupa (2n+1)a posiciones
    return sum(N - (2 * n + 1) * a for a in range(1, amax + 1) for n in range(1, nmax + 1) if N - (2 * n + 1) * a > 0)


if __name__ == "__main__":
    print("Señal esperada ΔV = ρ I / K  (separación de electrodos 4 m)")
    casos = [
        ("Wenner a = 4 m", k_wenner(4)),
        ("Wenner a = 60 m", k_wenner(60)),
        ("DD a = 4 m, n = 1", k_dd(4, 1)),
        ("DD a = 4 m, n = 6", k_dd(4, 6)),
        ("DD a = 16 m, n = 6", k_dd(16, 6)),
        ("WS a = 4 m, n = 8", k_ws(4, 8)),
    ]
    print(f"{'configuración':<22}{'K (m)':>9}{'20Ωm 20mA':>13}{'20Ωm 50mA':>13}{'100Ωm 50mA':>13}{'500Ωm 50mA':>13}")
    for nombre, k in casos:
        fila = [delta_v(r, i, k) * 1e3 for r, i in ((20, .02), (20, .05), (100, .05), (500, .05))]
        print(f"{nombre:<22}{k:>9.0f}" + "".join(f"{v:>10.1f} mV" if v >= 1 else f"{v*1e3:>10.0f} µV" for v in fila))

    w, d, s = lecturas_wenner(), lecturas_dd(), lecturas_ws()
    # medio pulso de 0.5 s (inversión de polaridad: pulso completo = 1 s), dos apilados y 0.15 s de conmutación
    t_lectura = 2 * (2 * 0.5) + 0.15      # = 2.15 s por lectura
    print(f"\nLecturas: Wenner {w}, dipolo-dipolo {d}, Wenner-Schlumberger {s}, total {w + d + s}")
    for nombre, n in (("Wenner", w), ("dipolo-dipolo", d), ("conjunto", w + d + s)):
        print(f"  {nombre}: {n * t_lectura / 60:.1f} min (con {t_lectura} s por lectura, un canal)")

    p_bateria = 200 * 0.05 / 0.8 + 6      # W: 10 W de salida / 80 % de eficiencia + 6 W de lógica y Raspberry Pi
    wh = p_bateria * (w + d + s) * t_lectura / 3600
    print(f"\nPotencia en batería (peor caso): {p_bateria:.1f} W; energía del levantamiento: {wh:.1f} Wh;"
          f" autonomía con 256 Wh: {256 / p_bateria:.1f} h")
