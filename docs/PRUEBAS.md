# Pruebas de estrés

Herramienta: `python3 tools/stress_test.py` (Playwright + Chromium). Resultados en `tools/stress-out/results.json`.

## Ronda 1 — 6 nov 2026 (v7.4)

**Limitación importante:** las pruebas corren en un servidor sin tarjeta gráfica (render por software). Por eso los cuadros por segundo medidos (5–15 fps) **no representan un celular real**. Lo que sí es confiable: el tiempo de la lógica del juego (JavaScript), la memoria, los errores y la estabilidad. Falta probar en un Android económico real.

| Prueba | Qué se hizo | Resultado |
|---|---|---|
| Carga | Abrir el juego en escritorio y celular | Listo en 1,1–1,9 s; memoria 27 MB; archivo de 1,2 MB; sin errores |
| Lugares | 4 s volando en Tierra, Saturno, Próxima, Sagitario A*, Orión | Lógica 3,6–4,6 ms por cuadro (p95 7,5 ms); 38–78 llamadas de dibujo; 35–61 mil triángulos |
| Celular lento (CPU ×4) | Lo mismo con el procesador 4 veces más lento | Lógica 12–16 ms por cuadro (p95 hasta 30 ms): **se come casi todo el presupuesto de 60 fps** |
| Cambio de naves | 340 cambios seguidos | 2 ms por cambio, sin fugas de memoria (27 → 28 MB) |
| Escanear todo | Los 1.341 objetos | 1,2 s en total; la bitácora abre en 60 ms; guardado de 150 KB |
| Guardados dañados | JSON roto, tipos raros, valores fuera de rango, bitácora enorme, almacenamiento bloqueado | Siempre arranca, pero **con nivel de motor inválido (−3 o 9) se rompe el combustible en cada cuadro** |
| Posiciones extremas | Fuera de la galaxia, a 1.000 millones de unidades, dentro del Sol, caída a Sagitario A* | Sin valores inválidos; el Sol te expulsa; el agujero negro te reaparece. **Con el módulo de salto no hay límite: puedes perderte en el vacío** |
| Toques y pantallas | 249 toques/arrastres/teclas al azar + 40 cambios de tamaño | 0 errores |
| Viaje en el tiempo | 45 s a 30 días por segundo (~3,7 años) | Órbitas estables, 0 errores |
| Uso prolongado | 3 min, 1.037 acciones al azar (volar, escanear, mapas, hangar, tormentas, saltos) | 0 errores; memoria estable (27–29 MB); geometrías y texturas suben y bajan sin fuga |

## Dónde se va el tiempo de la lógica (perfil de 6 s)

- Actualizar la posición de los ~1.400 objetos de la escena en cada cuadro (`updateMatrixWorld` de three.js): ~25 % de la lógica, aunque las estrellas no se mueven.
- Etiquetas sobre los objetos (`overlay`, proyecta 1.341 etiquetas cada cuadro): ~30 %.
- El resto: puntos de interés, órbitas, HUD.

## Propuestas de la ronda 1

1. Marcar estrellas y objetos de la galaxia como estáticos (no recalcular su posición cada cuadro).
2. Etiquetas: descartar antes las lejanas y actualizar las de estrellas cada 2–3 cuadros.
3. Validar el guardado al cargarlo (números dentro de rango, nave existente).
4. Poner un borde al universo jugable con el módulo de salto (por ejemplo, el borde de la Vía Láctea).
5. Probar en un Android económico real (Chrome) y medir fps con el contador del navegador.

## Ronda 2 — 6 nov 2026 (v7.5, después de los 4 cambios)

Cambios aplicados:
1. **Guardado validado al cargar:** números dentro de rango, nave y modo válidos, casco en cero pasa a 60.
2. **Borde de la Vía Láctea:** con el módulo de salto, el límite es de unos 65.000 años luz desde el Sol (`GAL_LIMIT`), con un mensaje sobre Andrómeda.
3. **Estrellas y objetos quietos de la galaxia marcados como fijos** (`freezeStatic`): su posición se calcula una sola vez; los halos solo se orientan si la estrella está visible.
4. **Etiquetas más baratas:** primero se descartan por distancia (sin proyectar) y el DOM solo se toca cuando cambia la visibilidad.

| Medición | Ronda 1 | Ronda 2 |
|---|---|---|
| Lógica por cuadro, escritorio (5 lugares) | 3,6–4,6 ms | 2,4–3,3 ms |
| Lógica por cuadro, CPU ×4 (lejos de la Tierra) | 12,4–13,2 ms | 8,4–11,6 ms |
| Lógica por cuadro, CPU ×4 (junto a la Tierra) | 16,2 ms | 15,4–17,2 ms (la zona más cargada) |
| Peso del juego en el perfil (junto a la Tierra) | 4,4 % del tiempo | 2,3 % del tiempo |
| Guardados dañados | 2 casos con error en cada cuadro | 0 errores |
| Volar sin límite | llegó a 6.000 millones de unidades | se detiene en el borde (11,6 millones) |

Pendiente: la zona de la Tierra sigue siendo la más pesada en CPU lenta (muchos objetos, lunas, naves, puntos de interés y basura espacial a la vez). Siguiente ronda: medir en un Android económico real.
