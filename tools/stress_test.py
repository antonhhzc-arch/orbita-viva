"""Pruebas de estrés de Órbita Viva (Playwright + Chromium).
Uso: python3 tools/stress_test.py [load places lowend ships scanall saves extreme input timewarp soak]
Resultados en tools/stress-out/results.json"""
import asyncio, os, sys, json, time, random
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'tools', 'stress-out')
os.makedirs(SP, exist_ok=True)
SRC = os.path.join(ROOT, 'src', 'orbita-viva.html')
THREE = os.path.join(ROOT, 'vendor', 'three.min.js')
R = {}

def build():
    h = open(SRC, encoding='utf-8').read().replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', 'file://' + THREE)
    old = "function loop(){try{step();}catch(err){console.error(err);}requestAnimationFrame(loop);}"
    assert old in h
    new = ("window.__dbg={ship,B,get G(){return G;},set G(v){G=v;},SHIPS,setShipModel,setTarget,camera,camQ,M4:THREE.Matrix4,renderer,scene,openMap,setView,openLog,openHangar,openShip,openCard,addReading,doScan,setSpeed,respawn,stormStart,pulse,bodies,ALL_IDS,GAL_IDS,STAR_IDS,EXO_IDS,cycleTarget,get cur(){return curShip;}};"
           "(function(){const o=renderer.render.bind(renderer);renderer.render=(s,c)=>{const t=performance.now();o(s,c);window.__rt=(window.__rt||0)+performance.now()-t;};})();"
           "function loop(){const t0=performance.now();window.__rt=0;try{step();}catch(err){console.error(err);window.__errs=(window.__errs||0)+1;}const d=performance.now()-t0,P=window.__perf||(window.__perf={f:[],r:[]});P.f.push(d);P.r.push(window.__rt);if(P.f.length>3000){P.f.shift();P.r.shift();}requestAnimationFrame(loop);}")
    h = h.replace(old, new)
    p = os.path.join(SP, 'game.html')
    open(p, 'w', encoding='utf-8').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + h + '</body></html>')
    return 'file://' + p

TP = '''(([id,k])=>{const d=window.__dbg,b=d.B[id],V=d.camera.position.constructor;const toSun=new V().sub(b.sp).normalize();if(!isFinite(toSun.x)||toSun.lengthSq()<.5)toSun.set(0,0,1);const up=new V(0,1,0);
 d.ship.pos.copy(b.sp).addScaledVector(toSun,b.R*k+0.3);d.ship.speed=0;d.ship.throttle=0;d.ship.quat.setFromRotationMatrix(new d.M4().lookAt(d.ship.pos,b.sp,up));d.camQ.copy(d.ship.quat);d.setTarget(id);})'''

async def new_page(b, vp=(1280, 720), mobile=False, dpr=1, init=None):
    ctx = await b.new_context(viewport={'width': vp[0], 'height': vp[1]}, is_mobile=mobile, has_touch=mobile, device_scale_factor=dpr)
    if init: await ctx.add_init_script(init)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:240]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:240]) if m.type == 'error' and 'ERR_TUNNEL' not in m.text and 'Failed to load resource' not in m.text else None)
    return ctx, pg, errs

async def boot(pg, url, clear=True):
    t0 = time.time()
    await pg.goto(url)
    await pg.wait_for_function('window.__dbg!==undefined', timeout=90000)
    tready = time.time() - t0
    if clear: await pg.evaluate("localStorage.clear()")
    await pg.click('#startPiloto'); await pg.wait_for_timeout(700)
    if await pg.is_visible('#guide'): await pg.click('#guideGo')
    await pg.wait_for_timeout(300)
    return tready

async def measure(pg, secs):
    await pg.evaluate("window.__perf={f:[],r:[]};window.__fc=0")
    t0 = await pg.evaluate("performance.now()")
    await pg.wait_for_timeout(int(secs * 1000))
    return await pg.evaluate("""(t0=>{const P=window.__perf,n=P.f.length,el=(performance.now()-t0)/1000,s=a=>a.slice().sort((x,y)=>x-y),q=(a,p)=>a.length?s(a)[Math.min(a.length-1,Math.floor(a.length*p))]:0,avg=a=>a.reduce((x,y)=>x+y,0)/Math.max(1,a.length);
      const logic=P.f.map((v,i)=>v-P.r[i]);const i=__dbg.renderer.info;return {fps:+(n/el).toFixed(1),frame_ms:+avg(P.f).toFixed(1),frame_p95:+q(P.f,.95).toFixed(1),logic_ms:+avg(logic).toFixed(2),logic_p95:+q(logic,.95).toFixed(2),render_ms:+avg(P.r).toFixed(1),calls:i.render.calls,tris:i.render.triangles,geos:i.memory.geometries,tex:i.memory.textures};})(%s)""" % t0)

def heap(pg): return pg.evaluate("(()=>{if(window.gc){gc();gc();}return performance.memory?Math.round(performance.memory.usedJSHeapSize/1048576):-1;})()")
async def finite(pg): return await pg.evaluate("(()=>{const d=__dbg;const ok=v=>isFinite(v.x)&&isFinite(v.y)&&isFinite(v.z);let bad=0;for(const b of d.bodies)if(!ok(b.sp))bad++;return {ship:ok(d.ship.pos)&&isFinite(d.ship.speed),cam:ok(d.camera.position),badBodies:bad};})()")

async def s_load(b, url):
    out = {}
    for name, vp, mob, dpr in [('escritorio', (1280, 720), False, 1), ('celular', (740, 340), True, 2)]:
        ctx, pg, errs = await new_page(b, vp, mob, dpr)
        t = await boot(pg, url)
        out[name] = {'listo_s': round(t, 1), 'heap_MB': await heap(pg), 'errores': errs[:5]}
        await ctx.close()
    out['peso_index_KB'] = round(os.path.getsize(os.path.join(ROOT, 'index.html')) / 1024)
    R['carga'] = out

async def s_places(b, url, throttle=None, tag='lugares'):
    ctx, pg, errs = await new_page(b, (740, 340), True, 2)
    if throttle:
        cdp = await ctx.new_cdp_session(pg); await cdp.send('Emulation.setCPUThrottlingRate', {'rate': throttle})
    await boot(pg, url)
    await pg.evaluate("__dbg.G.tier=2;__dbg.G.jump=true")
    out = {}
    for label, js in [('Tierra', TP + '(["earth",3])'), ('Saturno', TP + '(["saturn",3])'), ('Próxima Centauri', TP + '(["st_gl551",6])'),
                      ('Sagitario A*', TP + '(["g_sgra",6])'), ('Nebulosa de Orión', TP + '(["g_orion",1.4])')]:
        await pg.evaluate(js); await pg.evaluate("__dbg.ship.throttle=.5")
        await pg.wait_for_timeout(800)
        out[label] = await measure(pg, 4)
    out['errores'] = errs[:5]
    R[tag] = out
    await ctx.close()

async def s_soak(b, url, minutes=3):
    ctx, pg, errs = await new_page(b, (740, 340), True, 2)
    await boot(pg, url)
    await pg.evaluate("__dbg.G.tier=2;__dbg.G.jump=true")
    ids = await pg.evaluate("__dbg.ALL_IDS.filter(id=>!__dbg.B[id].hidden&&!__dbg.B[id].obs)")
    ships = await pg.evaluate("__dbg.SHIPS.map(s=>s.id)")
    acts = ['thr', 'turbo', 'turn', 'scan', 'target', 'ship', 'map', 'log', 'hangar', 'card', 'time', 'tp', 'radar', 'storm', 'close', 'close', 'thr']
    samples = []; n = 0; t_end = time.time() + minutes * 60; t_s = 0
    rnd = random.Random(7)
    while time.time() < t_end:
        a = rnd.choice(acts); n += 1
        try:
            if a == 'thr': await pg.evaluate("__dbg.ship.throttle=%f" % rnd.uniform(-.2, 1))
            elif a == 'turbo': await pg.keyboard.down('Shift'); await pg.wait_for_timeout(300); await pg.keyboard.up('Shift')
            elif a == 'turn': k = rnd.choice(['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']); await pg.keyboard.down(k); await pg.wait_for_timeout(250); await pg.keyboard.up(k)
            elif a == 'scan': await pg.evaluate("__dbg.doScan()")
            elif a == 'target': await pg.evaluate("__dbg.cycleTarget(1)")
            elif a == 'ship': await pg.evaluate("__dbg.setShipModel(%r)" % rnd.choice(ships))
            elif a == 'map': await pg.evaluate("__dbg.openMap();__dbg.setView(%r)" % rnd.choice(['inner', 'all', 'neigh', 'gal']))
            elif a == 'log': await pg.evaluate("__dbg.openLog()")
            elif a == 'hangar': await pg.evaluate("__dbg.openHangar()")
            elif a == 'card': await pg.evaluate("(id=>{__dbg.addReading(__dbg.B[id]);__dbg.openCard(__dbg.B[id],true);})(%r)" % rnd.choice(ids))
            elif a == 'time': await pg.evaluate("__dbg.setSpeed(%d)" % rnd.randint(0, 3))
            elif a == 'tp': await pg.evaluate(TP + '([%r,%f])' % (rnd.choice(ids), rnd.uniform(1.5, 8)))
            elif a == 'radar': await pg.evaluate("__dbg.pulse()")
            elif a == 'storm': await pg.evaluate(TP + '(["earth",4])'); await pg.evaluate("__dbg.stormStart()")
            elif a == 'close': await pg.evaluate("for(const id of ['map','card','log','ship','out','quiz','spec','guide','mis','hangar'])document.getElementById(id).hidden=true")
        except Exception as e:
            errs.append('harness: ' + a + ' ' + str(e)[:120])
        await pg.wait_for_timeout(120)
        if time.time() > t_s:
            t_s = time.time() + 15
            m = await pg.evaluate("(()=>{const i=__dbg.renderer.info;return {geos:i.memory.geometries,tex:i.memory.textures,dom:document.getElementsByTagName('*').length};})()")
            m['heap_MB'] = await heap(pg); m['acciones'] = n; samples.append(m)
    await pg.evaluate("__dbg.setSpeed(0)")
    R['uso_prolongado'] = {'minutos': minutes, 'acciones': n, 'muestras': samples, 'valores_finitos': await finite(pg), 'errores': errs[:8], 'n_errores': len(errs)}
    await ctx.close()

async def s_ships(b, url):
    ctx, pg, errs = await new_page(b)
    await boot(pg, url)
    g0 = await pg.evaluate("__dbg.renderer.info.memory.geometries")
    h0 = await heap(pg)
    t = await pg.evaluate("(()=>{const t=performance.now();const ids=__dbg.SHIPS.map(s=>s.id);for(let i=0;i<340;i++)__dbg.setShipModel(ids[i%ids.length]);return performance.now()-t;})()")
    await pg.wait_for_timeout(1500)
    g1 = await pg.evaluate("__dbg.renderer.info.memory.geometries"); h1 = await heap(pg)
    tt = await pg.evaluate("(()=>{const t=performance.now();for(let i=0;i<30;i++){__dbg.openHangar();}document.getElementById('hangar').hidden=true;return (performance.now()-t)/30;})()")
    R['cambio_de_naves'] = {'cambios': 340, 'ms_por_cambio': round(t / 340, 2), 'geometrias_antes': g0, 'geometrias_despues': g1, 'heap_antes_MB': h0, 'heap_despues_MB': h1, 'abrir_hangar_ms': round(tt, 1), 'errores': errs[:5]}
    await ctx.close()

async def s_timewarp(b, url):
    ctx, pg, errs = await new_page(b)
    await boot(pg, url)
    await pg.evaluate("__dbg.setSpeed(3)")
    await pg.wait_for_timeout(45000)
    f = await finite(pg)
    date = await pg.evaluate("document.getElementById('dateChip').textContent")
    await pg.evaluate("__dbg.setSpeed(0)")
    R['viaje_en_el_tiempo'] = {'segundos_a_30_dias_por_s': 45, 'fecha_final': date, 'valores_finitos': f, 'errores': errs[:5]}
    await ctx.close()

async def s_scanall(b, url):
    ctx, pg, errs = await new_page(b)
    await boot(pg, url)
    t = await pg.evaluate("(()=>{const t=performance.now();for(const id of __dbg.ALL_IDS)__dbg.addReading(__dbg.B[id]);return performance.now()-t;})()")
    await pg.wait_for_timeout(2500)
    for _ in range(3):
        await pg.evaluate("for(const id of ['mis','card'])document.getElementById(id).hidden=true")
        await pg.wait_for_timeout(300)
    tl = await pg.evaluate("(()=>{const t=performance.now();__dbg.openLog();return performance.now()-t;})()")
    dom = await pg.evaluate("document.getElementById('logGrid').children.length")
    await pg.evaluate("document.getElementById('log').hidden=true")
    tm = {}
    for v in ['inner', 'all', 'neigh', 'gal']:
        tm[v] = await pg.evaluate("(v=>{__dbg.openMap();const t=performance.now();__dbg.setView(v);return +(performance.now()-t).toFixed(1);})(%r)" % v)
    size = await pg.evaluate("(()=>{let s=0;for(const k in localStorage)if(localStorage.hasOwnProperty(k))s+=localStorage[k].length;return Math.round(s/1024);})()")
    g = await pg.evaluate("({tier:__dbg.G.tier,jump:__dbg.G.jump,know:__dbg.G.know})")
    R['escanear_todo'] = {'objetos': await pg.evaluate("__dbg.ALL_IDS.length"), 'ms_total': round(t), 'abrir_bitacora_ms': round(tl), 'entradas_bitacora': dom, 'mapa_ms': tm, 'guardado_KB': size, 'estado': g, 'errores': errs[:5]}
    await ctx.close()

async def s_saves(b, url):
    out = {}
    cases = {
        'json_roto': "localStorage.setItem('orbita-viva-juego','{esto no es json');localStorage.setItem('orbita-viva-v2','[[[');",
        'tipos_raros': "localStorage.setItem('orbita-viva-juego',JSON.stringify({fuel:'abc',hull:null,tier:-3,ship:'nave-que-no-existe',mis:99,learned:5,disc:'x',sysDone:null,mode:'otro'}));",
        'nivel_alto': "localStorage.setItem('orbita-viva-juego',JSON.stringify({tier:9,jump:true,mis:3,fuel:500,hull:-20}));",
        'bitacora_enorme': "const L={};for(let i=0;i<4000;i++)L['x'+i]={r:Array.from({length:30},(_,j)=>({at:j,sim:j,sun:1,earth:1}))};try{localStorage.setItem('orbita-viva-v2',JSON.stringify(L));}catch(e){}",
    }
    for name, js in cases.items():
        ctx, pg, errs = await new_page(b)
        await pg.goto(url); await pg.wait_for_function('window.__dbg!==undefined', timeout=90000)
        await pg.evaluate(js); await pg.reload(); await pg.wait_for_function('window.__dbg!==undefined', timeout=90000)
        try:
            await boot(pg, url, clear=False)
            st = await pg.evaluate("({fuel:__dbg.G.fuel,hull:__dbg.G.hull,tier:__dbg.G.tier,ship:__dbg.cur.id})")
            await pg.wait_for_timeout(2500); m = await measure(pg, 2)
            out[name] = {'arranca': True, 'estado': st, 'fps': m['fps'], 'finitos': await finite(pg), 'errores': errs[:4]}
        except Exception as e:
            out[name] = {'arranca': False, 'fallo': str(e)[:200], 'errores': errs[:4]}
        await ctx.close()
    # storage blocked (private mode on some browsers)
    ctx, pg, errs = await new_page(b, init="Object.defineProperty(window,'localStorage',{get(){throw new Error('bloqueado');}});")
    try:
        await pg.goto(url); await pg.wait_for_function('window.__dbg!==undefined', timeout=30000)
        await pg.click('#startPiloto'); await pg.wait_for_timeout(1500)
        out['almacenamiento_bloqueado'] = {'arranca': True, 'errores': errs[:4]}
    except Exception as e:
        out['almacenamiento_bloqueado'] = {'arranca': False, 'fallo': str(e)[:160], 'errores': errs[:4]}
    await ctx.close()
    R['guardados_danados'] = out

async def s_extreme(b, url):
    ctx, pg, errs = await new_page(b)
    await boot(pg, url)
    await pg.evaluate("__dbg.G.tier=2;__dbg.G.jump=true;__dbg.setShipModel('cohete')")
    out = {}
    for label, pos in [('fuera_de_la_galaxia', '4e7,1e6,-2e7'), ('muy_lejos', '1e9,0,0'), ('dentro_del_sol', '0.5,0,0')]:
        await pg.evaluate("__dbg.ship.pos.set(%s);__dbg.ship.speed=0;__dbg.ship.throttle=1" % pos)
        await pg.keyboard.down('Shift'); await pg.wait_for_timeout(4000); await pg.keyboard.up('Shift')
        out[label] = {'finitos': await finite(pg), 'distancia_final': await pg.evaluate("Math.round(__dbg.ship.pos.length())")}
        await pg.evaluate("__dbg.ship.throttle=0")
    # black hole dive in Piloto
    await pg.evaluate(TP + '(["g_sgra",2])'); await pg.evaluate("__dbg.ship.throttle=1"); await pg.wait_for_timeout(4000)
    out['agujero_negro'] = {'casco': await pg.evaluate("Math.round(__dbg.G.hull)"), 'finitos': await finite(pg)}
    out['errores'] = errs[:5]
    R['posiciones_extremas'] = out
    await ctx.close()

async def s_input(b, url):
    ctx, pg, errs = await new_page(b, (740, 340), True, 2)
    await boot(pg, url)
    rnd = random.Random(3); n = 0
    t_end = time.time() + 60
    while time.time() < t_end:
        x, y = rnd.randint(0, 739), rnd.randint(0, 339)
        k = rnd.random()
        try:
            if k < .6: await pg.touchscreen.tap(x, y)
            elif k < .85: await pg.mouse.move(x, y); await pg.mouse.down(); await pg.mouse.move(rnd.randint(0, 739), rnd.randint(0, 339), steps=3); await pg.mouse.up()
            else: await pg.keyboard.press(rnd.choice(['Escape', 'm', 'b', 'n', 'x', ' ', 'Tab', 'f', 'p']))
        except Exception as e: errs.append('harness ' + str(e)[:80])
        n += 1
    # resize churn
    for i in range(40):
        await pg.set_viewport_size({'width': rnd.randint(320, 1600), 'height': rnd.randint(260, 1000)}); await pg.wait_for_timeout(60)
    await pg.set_viewport_size({'width': 740, 'height': 340}); await pg.wait_for_timeout(500)
    R['toques_y_pantallas'] = {'toques_y_teclas': n, 'cambios_de_tamano': 40, 'finitos': await finite(pg), 'errores': errs[:6], 'n_errores': len(errs)}
    await ctx.close()

async def main():
    url = build()
    want = sys.argv[1:] or ['load', 'places', 'lowend', 'ships', 'scanall', 'saves', 'extreme', 'input', 'timewarp', 'soak']
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--enable-precise-memory-info', '--js-flags=--expose-gc'])
        for w in want:
            t = time.time()
            try:
                if w == 'load': await s_load(b, url)
                elif w == 'places': await s_places(b, url)
                elif w == 'lowend': await s_places(b, url, throttle=4, tag='celular_lento_cpu_x4')
                elif w == 'ships': await s_ships(b, url)
                elif w == 'scanall': await s_scanall(b, url)
                elif w == 'saves': await s_saves(b, url)
                elif w == 'extreme': await s_extreme(b, url)
                elif w == 'input': await s_input(b, url)
                elif w == 'timewarp': await s_timewarp(b, url)
                elif w == 'soak': await s_soak(b, url, 3)
            except Exception as e:
                R[w + '_FALLO_HARNESS'] = str(e)[:300]
            print(w, 'ok', round(time.time() - t), 's', flush=True)
            json.dump(R, open(os.path.join(SP, 'results.json'), 'w'), ensure_ascii=False, indent=1)
        await b.close()

asyncio.run(main())
