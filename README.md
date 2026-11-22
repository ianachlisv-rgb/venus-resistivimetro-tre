# VENUS: resistivímetro multielectrodo de bajo costo para tomografía de resistividad eléctrica (TRE)

VENUS es la propuesta de diseño, modelado analítico y análisis de costos de un resistivímetro de un canal y 48 electrodos para tendidos simples de unos 200 m. **No se construyó hardware**: todas las cifras de desempeño son estimaciones analíticas pendientes de validación en banco y en campo.

Autor: Ian A. Sandoval-Valderrábano, Facultad de Ingeniería, Benemérita Universidad Autónoma de Puebla (BUAP).

## Dos versiones

- **VENUS-B (básica):** riel de 200 V limitado a 80 mA, conmutación con PhotoMOS. Es la versión de bajo costo.
- **VENUS-S (suelos secos):** versión reforzada para sitios donde la resistencia de contacto de los electrodos es alta. Es la versión vigente del diseño.

> **Aviso sobre el contenido del repositorio:** este README describe VENUS-S. Los archivos de `paper/`, `interactivo/`, `datos/` y `codigo/` pueden corresponder todavía a VENUS-B (29 líneas de materiales, 6 páginas) hasta que se suba la documentación nueva de VENUS-S (paper de 8 páginas, resumen de una página y página interactiva actualizada).

## Qué cambia en VENUS-S

| Bloque | VENUS-B | VENUS-S |
|---|---|---|
| Transmisor | 200 V, 80 mA | elevador de 45 a 390 V, 100 W; puente H con MOSFET de 650 V; lazo de corriente hasta 250 mA |
| Conmutación | PhotoMOS (96 piezas) | 192 relevadores reed de alto voltaje, con regla de conmutación en frío para los electrodos de corriente |
| Receptor | ADS1262 | ADS1262 con buffers OPA2188 (impedancia de entrada de unos 1 GΩ) |
| Aislamiento y seguridad | aislamiento digital | aislamiento ISO7741, interlocks de alto voltaje, paro de emergencia, llave, baliza y monitor de fugas |
| Cable y conectores | cable estándar | cable de 1 kV y conectores de 500 V o más |
| Energía y carcasa | LiFePO4 12.8 V, 20 Ah; Pelican 1450 | LiFePO4 12.8 V, 30 Ah; Pelican 1550 |

## Resultados (estimaciones analíticas)

Corriente inyectada con un contacto de 10 kΩ por electrodo:

| Caso | Corriente |
|---|---|
| VENUS-B | unos 10 mA |
| VENUS-S, solo con más voltaje | unos 19.5 mA |
| VENUS-S, con tratamiento del contacto (supuesto: la resistencia baja a una quinta parte) | unos 97.5 mA |

Con la configuración de VENUS-S, un Wenner completo (360 lecturas, un canal) toma unos 14 min y los tres arreglos juntos (1 857 lecturas) unos 71 min.

**Lectura honesta del resultado:** subir solo el voltaje apenas duplica la corriente cuando el contacto limita. La mejora grande viene de bajar la resistencia de contacto (doble estaca con bentonita y sal) y de eliminar errores por fuga de los interruptores y por el divisor de entrada. El factor de tratamiento (resistencia de contacto por 0.2) es un supuesto que falta validar en campo.

## Costo estimado

| Concepto | VENUS-B | VENUS-S |
|---|---|---|
| Sistema completo | unos 2 866 USD (1 584 a 4 234) | unos 6 950 USD (3 100 a 10 850) |

VENUS-S cuesta unas 2.4 veces lo que VENUS-B. Solo 9 de las 33 líneas de materiales de VENUS-S tienen precio visto en un distribuidor; el resto son estimaciones del autor. Quedan fuera impuestos, envío, repuestos y la tableta del operador. El costo de desarrollo (ingeniería, validación, certificación) es mucho mayor que el de las piezas.

## Límites que conviene leer

- Todo es analítico: no hay mediciones de banco ni de campo.
- Supuestos por validar: factor de tratamiento del contacto (0.2, rango de 0.1 a 0.5), fuga de los relevadores reed (unos 20 pA), confiabilidad del elevador de 100 W y que los contactos abiertos resistan 800 V o más.
- **Seguridad:** VENUS-S trabaja hasta 390 V, por encima del umbral de 60 V CC de la norma IEC 61010-1. Las medidas de seguridad del diseño deben revisarse con un laboratorio y con personal calificado antes de construir nada.

## Contenido del repositorio

- `paper/`: documento en estilo IEEE (no es la plantilla oficial).
- `interactivo/index.html`: página única con resumen, modelo 3D del interior, calculadora de costos y el paper (ábrela en el navegador, sin internet).
- `datos/lista_materiales.csv`: lista de materiales con rangos bajo, base y alto, fuente de cada precio y si es precio visto (V) o estimación (E).
- `codigo/presupuesto_senal.py`: reproduce la señal esperada, el número de lecturas, el tiempo y la energía.

## Licencia

El código, la página interactiva y la lista de materiales están bajo licencia MIT (ver LICENSE). El texto y las figuras del paper son del autor. La página interactiva incluye three.js (licencia MIT, © los autores de three.js). Las marcas y números de parte pertenecen a sus fabricantes.
