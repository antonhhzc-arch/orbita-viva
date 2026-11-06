# Órbita Viva

Juego educativo de exploración espacial con datos reales. Pilotas una nave por el sistema solar tal como está hoy, viajas a más de mil estrellas cercanas y llegas hasta el centro de la galaxia.

**Jugar:** https://antonhhzc-arch.github.io/orbita-viva/ (en el celular, en horizontal; en Chrome usa ⋮ → "Agregar a pantalla principal" para jugar a pantalla completa).

## Qué tiene

- Sistema solar en tiempo real: planetas, lunas, asteroides grandes y naves reales en su posición de hoy.
- 1.052 estrellas hasta 50 años luz y 234 exoplanetas reales.
- La galaxia: agujeros negros (Gaia BH1, BH3, Cygnus X-1, Sagitario A*), púlsares, nebulosas y la estrella de Tabby.
- Misión opcional de la señal Wow! (6 capítulos) y misterios reales documentados.
- **Escanear es avanzar:** cada objeto escaneado da combustible y acerca la siguiente mejora de la nave.
- Controles táctiles, teclado y mando de Xbox. Modo Piloto (con amenazas) y modo Explorador (escuelas).

## Estructura

| Ruta | Qué es |
|---|---|
| `src/orbita-viva.html` | Código fuente del juego (un solo archivo, carga three.js desde CDN). Es la versión publicada como artefacto de Claude. |
| `index.html` | Versión jugable sin internet, generada a partir de `src/`. Es la que sirve GitHub Pages. |
| `vendor/three.min.js` | three.js r128 (licencia MIT). |
| `tools/build_standalone.py` | Genera `index.html` desde `src/`. |
| `tools/build_stars2.py` | Genera los datos de estrellas y exoplanetas desde los catálogos HYG y Open Exoplanet Catalogue. |
| `docs/DECISIONES.md` | Decisiones de diseño, historial de versiones y pendientes. |

Para actualizar el juego: edita `src/orbita-viva.html` y luego ejecuta `python3 tools/build_standalone.py`.

## Datos y créditos

- Órbitas planetarias: elementos de JPL (NASA).
- Asteroides: JPL Small-Body Database.
- Estrellas: [HYG Database v4.1](https://github.com/astronexus/HYG-Database) (astronexus), licencia CC BY-SA 4.0.
- Exoplanetas: NASA Exoplanet Archive, vía [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/oec_gzip) (licencia MIT).
- Objetos de la galaxia: NASA, ESA y publicaciones científicas citadas en las fichas.
- Motor 3D: [three.js](https://threejs.org) r128 (licencia MIT).

Las distancias están comprimidas para que el viaje sea jugable; las direcciones y los datos son reales. Lo que es invento del juego (radar, módulo de salto, final de la misión Wow!) está marcado como tal dentro del juego.
