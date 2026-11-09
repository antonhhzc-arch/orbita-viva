# Decisiones de diseño

Registro para retomar el proyecto sin perder contexto. Lo más reciente va primero en cada sección.

## Visión

- App para celular (Android/iOS) y PC, con controles táctiles, teclado y mando de Xbox.
- Divertida, educativa y de uso masivo. Datos reales; lo inventado se marca dentro del juego.
- Estilo visual plano tipo ilustración, navegación en horizontal, rueda de acciones en lugar de menús.
- Sin piloto automático. Cinturón de asteroides real a la escala del juego.

## Progresión: "Escanear es avanzar" (v7, nov 2026)

Reemplazó el sistema de recursos anterior (combustible, energía, casco, conocimiento, metales, helio-3, materiales raros y extracción de 3 s), que resultaba difícil de entender y tedioso.

- **Dos barras:** combustible y casco.
- **Combustible:** lo gasta el motor (turbo ×3). Se recarga con:
  - +20 por cada objeto escaneado por primera vez (+8 si es una nave);
  - tanque lleno al completar un sistema (todos sus objetos escaneados);
  - base Tierra: tanque y casco llenos al acercarse (cada 60 s);
  - +15 por leer bien un espectro;
  - poco a poco cerca de una estrella cuando no aceleras;
  - si se acaba: video con recompensa (+60, solo app), vela solar de emergencia o desafío de 3 preguntas (+30 por acierto).
- **Mejoras automáticas** (se instalan solas al llegar a la meta):
  - Motor de fusión: 8 objetos naturales del sistema solar escaneados. Llega hasta 2 años luz.
  - Impulsor estelar: 18 objetos naturales del sistema solar. Llega hasta ~50 años luz.
  - Módulo de salto galáctico: 3 objetos especiales escaneados (enanas blancas o mundos de lava). Abre la galaxia.
- **Meta visible** bajo las barras: progreso hacia la siguiente mejora, o progreso del sistema estelar en el que estás.
- **Espectros:** pregunta extra opcional en la ficha, la primera vez que escaneas un tipo (gas, hielo, roca, enana blanca).
- **Conocimiento:** puntaje del explorador; ya no se gasta.
- **Casco a cero:** reapareces en el último objeto escaneado (sin perder nada más).

## Interfaz: "Cabina limpia" (v7, nov 2026)

- Arriba a la izquierda solo las barras y la meta; misión Wow! arriba al centro; rueda de acciones arriba a la derecha.
- La bitácora vive en la rueda. La fecha solo aparece cuando viajas en el tiempo.
- En pantallas chicas: etiqueta del objetivo en una línea, pistas de inicio una a la vez, sin etiquetas de estrellas lejanas dentro del sistema solar hasta tener el impulsor estelar.
- Al empezar en un celular intenta pantalla completa y bloqueo horizontal. En el panel de la nave: botón de pantalla completa y tamaño de interfaz (pequeña, normal, grande).

## Naves y Garaje espacial (v7.2, nov 2026)

Selector en el **Hangar** (panel de la nave → "Cambiar de nave", o "Elegir nave" en el inicio). Por ahora todo se puede probar (`UNLOCK_ALL=true`).

- **Arte:** las ilustraciones del dueño se usan como imagen de cada tarjeta del Hangar (`SHIP_ART`, al logo de la combi se le quitó la marca). En vuelo cada nave es un modelo 3D sencillo en el estilo plano del juego, con su forma y colores.
- **Excluido:** el caza de cuatro alas del diseño original es el X-wing de Star Wars (Lucasfilm/Disney); se reemplazó por el Halcón, un caza propio. Los vehículos son genéricos y sin marcas.
- **Pendiente de arte:** Halcón, Lupa, Vela, Expreso (bus) y Brisa (scooter) usan por ahora una imagen 3D. En la lámina original el bus y la scooter se superponen.

### Naves: cada una tiene un trabajo (v7.4, nov 2026)

Decisión del dueño: todas pueden ir a todas partes, pero cada una es mucho mejor en su trabajo; se puede cambiar de nave en cualquier momento (rueda → Hangar). La velocidad depende de la zona: "cerca de planetas" (distancia a la superficie más cercana < 60) y "espacio profundo" (> 400), con mezcla gradual entre ambas.

| Nave | Trabajo | Cerca de planetas | Espacio profundo | Consumo | Daño recibido | Otros | Plan de desbloqueo |
|---|---|---|---|---|---|---|---|
| Colibrí | Un poco de todo | ×1 | ×1 | ×1 | ×1 | — | Desde el inicio |
| Cohete | Viajar entre sistemas | ×0,8 | ×3 | ×1,1 | ×1 | giro ×0,7 | Impulsor estelar |
| Halcón | Maniobrar entre objetos | ×1,8 | ×1 | ×1,2 | ×1,4 | giro ×1,4 | Motor de fusión |
| Atlas | Viajes largos sin recargar | ×0,85 | ×1,1 | ×0,5 | ×0,5 | repara el casco | 25 objetos escaneados |
| Ovni | Peligros y misterios | ×1 | ×1 | ×1 | ×0,8 | inmune a tormentas, resiste agujeros negros, ×2 conocimiento en misterios | Primer misterio |
| Lupa | Escanear | ×0,9 | ×0,9 | ×1 | ×1,1 | alcance ×2,2, tiempo ×0,25, ×2 combustible por escaneo, radar ×2 | Completar un sistema estelar |
| Vela | Recargar combustible | ×0,9 | ×1,15 | ×0,9 | ×1,2 | recarga solar ×4, incluso acelerando | 15 objetos escaneados |

### Garaje espacial (colección, futura parte de pago)

Cada vehículo copia el trabajo de una nave (campo `base`): Aleta y Expreso → Atlas; Neón y Rayo → Halcón; Chatarra → Ovni; Rugido y Trueno → Cohete; Burbuja → Lupa; Combi → Vela; Brisa → Colibrí. Pagar da estilo, no ventaja.

### Modelos 3D

Estilo caricatura: sombreado de 3 tonos horneado en colores de vértice, contorno negro (malla inversa) y llamas animadas que crecen al acelerar. Kit en `SHIPS` (funciones `part`, `lathe`, `side`, `plate`, `nozzle`, `flame`).

Recomendación: lo de pago debe ser distinto, no más poderoso, para no romper el juego ni la confianza de padres y escuelas.

## Escala (v7.6, nov 2026)

- **Escala dinámica:** la nave y la cámara se encogen juntas al acercarse a un objeto (`shipK`, de 1 a 0,07 según la distancia a la superficie respecto al radio). La nave mantiene su tamaño en pantalla, pero el planeta se siente enorme. Cerca de la Tierra la nave equivale a decenas de km en vez de 500 km.
- **Polvo espacial** alrededor de la nave para sentir velocidad y escala (`dustStep`).
- **Atmósfera delgada** que abraza el borde del planeta desde cualquier distancia (`ATMS`).
- **Basura espacial más pequeña.**
- **Indicador de altura** bajo la velocidad, con comparaciones reales (Estación Espacial, línea de Kármán, órbita geoestacionaria, Apolo en la Luna).
- Pendiente: texturas con más detalle al acercarse (parte 3) y datos de escala real en las fichas (parte 4).

## Contenido

- Vecindario de 50 años luz (1.052 estrellas, 234 exoplanetas, 61 enanas blancas).
- Galaxia detrás del módulo de salto: Gaia BH1 y BH3, Cygnus X-1, Sagitario A* (meta), púlsares del Cangrejo y de Vela, Nebulosa de Orión, Pléyades, Betelgeuse, Eta Carinae, estrella de Tabby, ASKAP J1832-0911, la estrella candidata de la señal Wow! y la nube de hidrógeno de Sagitario. Andrómeda y la Gran Nube de Magallanes se observan desde lejos.
- Información por niveles al acercarse; puntos de interés tocables en la superficie (Quito, Apolo 11, Olympus Mons, Gran Mancha Roja, etc.).
- Misión Wow! (opcional, 6 capítulos). El final en Sagitario A* es ficción y está marcado.
- Amenazas (solo modo Piloto): tormentas solares visibles, asteroides y basura espacial, frío lejano, agujeros negros.

## Negocio y publicación

- Gratis con videos con recompensa + compra única para quitarlos. Gancho preparado: `window.OrbitaAds.showRewarded()`.
- Camino a tiendas: Capacitor + plugin de AdMob. Google Play: pago único de 25 USD; cuentas personales nuevas necesitan 12 testers durante 14 días. Apple: ~99 USD al año y requiere Mac.
- Guardado en el dispositivo (localStorage) por ahora.

## Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| v7.6 | nov 2026 | Escala dinámica, polvo espacial, atmósfera delgada, indicador de altura |
| v7.5 | nov 2026 | Guardado validado, borde de la Vía Láctea, optimizaciones de rendimiento |
| v7.4 | nov 2026 | Cada nave con un trabajo propio y modelos 3D estilo caricatura |
| v7.3 | nov 2026 | Hangar más visible (inicio y rueda) |
| v7.2 | nov 2026 | Diseños del dueño: 7 naves + Garaje espacial con 10 vehículos |
| v7.1 | nov 2026 | Hangar con 6 naves y estadísticas propias |
| v7 | nov 2026 | Escanear es avanzar, Cabina limpia, pantalla completa, migración a GitHub |
| v6.1 | oct 2026 | Menos consumo de combustible (tanque ≈ 3 min a fondo, turbo ×3) |
| v6 | oct 2026 | Galaxia, 50 años luz, misión Wow!, misterios, puntos de interés, materiales raros |
| v5 | oct 2026 | Recursos, motores, amenazas, modos Piloto/Explorador, guía de la nave |
| v4 y anteriores | oct 2026 | Sistema solar real, estrellas cercanas, exoplanetas, estilo visual plano |

## Pendientes

- Naves: activar el desbloqueo progresivo, compra de la nave de pago, más naves y mejoras por nave.
- Navegar los paneles con el mando de Xbox.
- Sonido y música.
- Datos aportados por los usuarios.
- Empaquetado para Play Store (Capacitor, AdMob, política de privacidad) y luego iOS.
- Servidor (cuentas, progreso en la nube) cuando haga falta.
