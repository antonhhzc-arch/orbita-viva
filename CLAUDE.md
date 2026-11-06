# Órbita Viva — contexto para Claude

Juego educativo de exploración espacial en un solo archivo HTML (three.js r128). Lee `docs/DECISIONES.md` antes de cambiar mecánicas: ahí están las decisiones del dueño del proyecto.

## Flujo de trabajo

- Edita **solo** `src/orbita-viva.html`. Después ejecuta `python3 tools/build_standalone.py` para regenerar `index.html` (GitHub Pages). No edites `index.html` a mano.
- El mismo `src/orbita-viva.html` se publica también como artefacto de Claude.
- Prueba con Playwright + Chromium (swiftshader) en 1280×720 y en celular horizontal 740×340, revisando que no haya errores en consola.
- Todo el texto del juego está en español (Ecuador), tono cercano y claro.
- El dueño prefiere que se planteen objeciones antes de implementar cambios, y feedback directo.

## Mapa del código (src/orbita-viva.html)

- CSS al inicio; el HTML de capas (`#card`, `#map`, `#log`, `#ship`, `#guide`, `#mis`, `#intro`…) después.
- Escala comprimida: `toScene(au)=SC·r^PW` con SC=60, PW=0.55; `fromScene` es la inversa.
- Datos: `STAR_DATA` (estrellas y exoplanetas), bloque de galaxia (`GAL`, `OBS`, `buildGalaxy`).
- Juego: estado `G` en localStorage `orbita-viva-juego`; `ENGINES` (metas de escaneo), `nextGoal`, `checkProgress`, `scanReward`, radar, tormentas, misión `MIS`, puntos de interés `POI_DATA`.
- Naves: `SHIPS` (estadísticas y modelo `build`), `curShip`, `setShipModel`, hangar `openHangar`; `UNLOCK_ALL` deja probar todas.
- Bucle: `step()` → `gameStep`, `fuelStep`, `overlay` (etiquetas y HUD), `lodTick`.

## Reglas

- Datos reales; todo lo inventado (radar, módulo de salto, final de la misión Wow!) debe decirse dentro del juego.
- Créditos: HYG (CC BY-SA 4.0), Open Exoplanet Catalogue (MIT), three.js (MIT).
