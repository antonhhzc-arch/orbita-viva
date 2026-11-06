import csv, json, math, re, sys, gzip
import xml.etree.ElementTree as ET
HYG=sys.argv[1]; OECF=sys.argv[2]
MAXPC=51.0/3.26156
EPS=math.radians(23.43928); PC_AU=206264.806; LY_PC=3.26156
def eq2ecl(x,y,z): return (x, y*math.cos(EPS)+z*math.sin(EPS), -y*math.sin(EPS)+z*math.cos(EPS))
def radec2xyz(ra,dec,d):
    ra=math.radians(ra); dec=math.radians(dec); return (d*math.cos(dec)*math.cos(ra), d*math.cos(dec)*math.sin(ra), d*math.sin(dec))
GREEK={'Alp':'Alfa','Bet':'Beta','Gam':'Gamma','Del':'Delta','Eps':'Épsilon','Zet':'Zeta','Eta':'Eta','The':'Theta','Iot':'Iota','Kap':'Kappa','Lam':'Lambda','Mu':'Mu','Nu':'Nu','Xi':'Xi','Omi':'Ómicron','Pi':'Pi','Rho':'Rho','Sig':'Sigma','Tau':'Tau','Ups':'Ípsilon','Phi':'Fi','Chi':'Ji','Psi':'Psi','Ome':'Omega'}
GEN={'And':'Andromedae','Ant':'Antliae','Aps':'Apodis','Aqr':'Aquarii','Aql':'Aquilae','Ara':'Arae','Ari':'Arietis','Aur':'Aurigae','Boo':'Boötis','Cae':'Caeli','Cam':'Camelopardalis','Cnc':'Cancri','CVn':'Canum Venaticorum','CMa':'Canis Majoris','CMi':'Canis Minoris','Cap':'Capricorni','Car':'Carinae','Cas':'Cassiopeiae','Cen':'Centauri','Cep':'Cephei','Cet':'Ceti','Cha':'Chamaeleontis','Cir':'Circini','Col':'Columbae','Com':'Comae Berenices','CrA':'Coronae Australis','CrB':'Coronae Borealis','Crv':'Corvi','Crt':'Crateris','Cru':'Crucis','Cyg':'Cygni','Del':'Delphini','Dor':'Doradus','Dra':'Draconis','Equ':'Equulei','Eri':'Eridani','For':'Fornacis','Gem':'Geminorum','Gru':'Gruis','Her':'Herculis','Hor':'Horologii','Hya':'Hydrae','Hyi':'Hydri','Ind':'Indi','Lac':'Lacertae','Leo':'Leonis','LMi':'Leonis Minoris','Lep':'Leporis','Lib':'Librae','Lup':'Lupi','Lyn':'Lyncis','Lyr':'Lyrae','Men':'Mensae','Mic':'Microscopii','Mon':'Monocerotis','Mus':'Muscae','Nor':'Normae','Oct':'Octantis','Oph':'Ophiuchi','Ori':'Orionis','Pav':'Pavonis','Peg':'Pegasi','Per':'Persei','Phe':'Phoenicis','Pic':'Pictoris','Psc':'Piscium','PsA':'Piscis Austrini','Pup':'Puppis','Pyx':'Pyxidis','Ret':'Reticuli','Sge':'Sagittae','Sgr':'Sagittarii','Sco':'Scorpii','Scl':'Sculptoris','Sct':'Scuti','Ser':'Serpentis','Sex':'Sextantis','Tau':'Tauri','Tel':'Telescopii','Tri':'Trianguli','TrA':'Trianguli Australis','Tuc':'Tucanae','UMa':'Ursae Majoris','UMi':'Ursae Minoris','Vel':'Velorum','Vir':'Virginis','Vol':'Volantis','Vul':'Vulpeculae'}
PROPER_ES={'Sirius':'Sirio','Procyon':'Proción','Arcturus':'Arturo','Pollux':'Pólux','Castor':'Cástor','Rigil Kentaurus':'Alfa Centauri A','Toliman':'Alfa Centauri B','Proxima Centauri':'Próxima Centauri',"Barnard's Star":'Estrella de Barnard',"Luyten's Star":'Estrella de Luyten',"Kapteyn's Star":'Estrella de Kapteyn',"Van Maanen's Star":'Estrella de van Maanen','Ran':'Épsilon Eridani','Keid':'Keid (40 Eridani A)','Guniibuu':'36 Ophiuchi A','Guniibuu B':'36 Ophiuchi B','Alsafi':'Sigma Draconis'}
NAMES={'Gl 559A':'Alfa Centauri A','Gl 559B':'Alfa Centauri B','Gl 406':'Wolf 359','Gl 411':'Lalande 21185','Gl 65A':'BL Ceti','Gl 65B':'UV Ceti','Gl 244A':'Sirio','Gl 244B':'Sirio B','Gl 729':'Ross 154','Gl 905':'Ross 248','Gl 887':'Lacaille 9352','Gl 447':'Ross 128','Gl 866A':'EZ Aquarii','Gl 725A':'Struve 2398 A','Gl 725B':'Struve 2398 B','Gl 820A':'61 Cygni A','Gl 820B':'61 Cygni B','Gl 280A':'Proción','Gl 280B':'Proción B','Gl 15A':'Groombridge 34 A','Gl 15B':'Groombridge 34 B','Gl 845':'Épsilon Indi A','GJ 1111':'DX Cancri','Gl 71':'Tau Ceti','Gl 54.1':'YZ Ceti','Gl 825':'Lacaille 8760','Gl 860A':'Kruger 60 A','Gl 860B':'Kruger 60 B','Gl 234A':'Ross 614 A','Gl 234B':'Ross 614 B','Gl 628':'Wolf 1061','Gl 473A':'Wolf 424 A','Gl 473B':'Wolf 424 B','Gl 83.1':'TZ Arietis','Gl 166B':'40 Eridani B','Gl 166C':'40 Eridani C','Gl 702A':'70 Ophiuchi A','Gl 702B':'70 Ophiuchi B','Gl 34A':'Achird','Gl 34B':'Achird B','Gl 139':'82 Eridani','Gl 752A':'Wolf 1055','Gl 752B':'Estrella de van Biesbroeck','Gl 229':'Gliese 229','Gl 581':'Gliese 581','Gl 667C':'Gliese 667 C','Gl 876':'Gliese 876','Gl 436':'Gliese 436','Gl 1214':'Gliese 1214'}
KNOWN_R={'Arturo':25.4,'Capella':11.98,'Pólux':9.06,'Vega':2.36,'Fomalhaut':1.84,'Cástor':2.4,'Altair':1.79,'Sirio':1.71,'Proción':2.05,'Alfa Centauri A':1.22,'Alfa Centauri B':0.86,'Próxima Centauri':0.154,'Estrella de Barnard':0.19,'Tau Ceti':0.79,'Épsilon Eridani':0.74,'Épsilon Indi A':0.71,'Wolf 359':0.16,'Estrella de van Maanen':0.011,'Sirio B':0.0084,'Proción B':0.012,'Denebola':1.73}
def bfname(bf):
    bf=(bf or '').strip()
    if not bf: return None
    m=re.match(r'^(\d*)\s*([A-Z][a-z]{1,2})?(\d?)\s+([A-Za-z]{3})$',bf)
    if not m: return None
    fl,gr,sup,con=m.groups()
    g=GEN.get(con)
    if not g: return None
    if gr and gr in GREEK: return GREEK[gr]+(sup and ' '+sup or '')+' '+g
    if fl: return fl+' '+g
    return None
def glname(gl):
    g=gl.replace('Gl ','Gliese ').replace('GJ ','GJ ')
    m=re.match(r'^(.*\d)([A-D])$',g)
    return (m.group(1)+' '+m.group(2)) if m else g
def sclass(sp):
    sp=(sp or '').strip()
    if not sp: return ''
    s=sp
    if s.startswith('sd'): s=s[2:]
    if s.startswith('d'): s=s[1:]
    s=s.lstrip()
    if s.startswith('D'): return 'D'
    c=s[:1].upper()
    return c if c in 'OBAFGKM' else ''
def lumclass(sp):
    s=(sp or '')
    if re.search(r'(?<![A-Za-z])(Ia|Ib|II)(?![I])',s) and 'III' not in s: return 'I'
    if 'III' in s: return 'III'
    if re.search(r'IV(?!I)',s): return 'IV'
    return 'V'
def sub(sp):
    m=re.search(r'[OBAFGKM](\d(\.\d)?)',(sp or '').upper())
    return float(m.group(1)) if m else 5.0
def est_radius(cl,sb,lc):
    if lc=='III': return 10.0
    if lc=='IV': return 2.0
    if cl=='D': return 0.012
    if cl=='M': return 0.55 if sb<2 else 0.4 if sb<3.5 else 0.25 if sb<5 else 0.15
    if cl=='K': return 0.8 if sb<4 else 0.66
    if cl=='G': return 1.0
    if cl=='F': return 1.35
    if cl=='A': return 1.8
    return 0.3
def bv2rgb(bv,cl,teff=None):
    if cl=='D': return '#e6eeff'
    if bv is None: bv={'O':-0.3,'B':-0.15,'A':0.05,'F':0.4,'G':0.65,'K':1.0,'M':1.6}.get(cl,1.5)
    T=4600*(1/(0.92*bv+1.7)+1/(0.92*bv+0.62))
    if teff: T=teff
    pts=[(2600,(255,122,74)),(3000,(255,138,84)),(3700,(255,166,102)),(4500,(255,190,120)),(5300,(255,214,138)),(5800,(255,226,160)),(6600,(255,244,225)),(7500,(230,236,255)),(10000,(200,214,255)),(30000,(170,190,255))]
    if T<=pts[0][0]: c=pts[0][1]
    elif T>=pts[-1][0]: c=pts[-1][1]
    else:
        for (t0,c0),(t1,c1) in zip(pts,pts[1:]):
            if t0<=T<=t1: f=(T-t0)/(t1-t0); c=tuple(round(c0[i]+(c1[i]-c0[i])*f) for i in range(3)); break
    return '#%02x%02x%02x'%c
rows=list(csv.DictReader(open(HYG)))
stars={}
for r in rows:
    if r['id']=='0': continue
    d=float(r['dist'])
    if not (0<d<MAXPC): continue
    lc=lumclass(r['spect']);absm=float(r['absmag'])
    if lc=='I' or absm<-1.5: continue
    gl=r['gl'].strip(); key=gl or ('HIP '+r['hip'] if r['hip'] else 'HYG '+r['id'])
    name=None
    if r['proper']: name=PROPER_ES.get(r['proper'],r['proper'])
    if not name and gl in NAMES: name=NAMES[gl]
    if not name: name=bfname(r['bf'])
    if not name and gl: name=glname(gl)
    if not name and r['hd']: name='HD '+r['hd']
    if not name: name=key
    cl=sclass(r['spect']); x,y,z=(float(r['x']),float(r['y']),float(r['z']))
    R=KNOWN_R.get(name) or est_radius(cl,sub(r['spect']),lc)
    stars[key]=dict(key=key,gl=gl,name=name,pos=list(eq2ecl(x,y,z)),dist=d,absmag=absm,spect=r['spect'].strip(),cl=cl,lc=lc,R=R,ci=float(r['ci']) if r['ci'] else None,
        base=r['base'].strip(),comp=int(r['comp'] or 1),hip=r['hip'],hd=r['hd'],proper=r['proper'])
byhip={s['hip']:k for k,s in stars.items() if s['hip']}
byhd={s['hd']:k for k,s in stars.items() if s['hd']}
def normgl(s):
    m=re.match(r'^(?:GJ|Gl|Gliese)\s*([\d.]+)\s*([A-D])?$',s.strip())
    return m and (m.group(1),(m.group(2) or ''))
bygl={}
for k,s in stars.items():
    if s['gl']:
        n=normgl(s['gl'])
        if n: bygl[n]=k
def ids_of(el):
    return [n.text.strip() for n in el.findall('name') if n.text]
def match(names,ra,dec,dist):
    for n in names:
        m=re.match(r'^HIP\s*(\d+)',n)
        if m and m.group(1) in byhip: return byhip[m.group(1)]
    for n in names:
        m=re.match(r'^HD\s*(\d+)$',n)
        if m and m.group(1) in byhd: return byhd[m.group(1)]
    for n in names:
        g=normgl(n)
        if g and g in bygl: return bygl[g]
        if g and (g[0],'A') in bygl and g[1]=='': return bygl[(g[0],'A')]
    if ra is None: return None
    u=radec2xyz(ra,dec,1); ue=eq2ecl(*u); best=None;bd=1e9
    for k,s in stars.items():
        p=s['pos'];n=math.sqrt(sum(v*v for v in p));
        if n==0: continue
        ang=math.degrees(math.acos(max(-1,min(1,sum(p[i]/n*ue[i] for i in range(3))))))
        if ang<0.05 and abs(n-dist)/dist<0.25 and ang<bd: bd=ang;best=k
    return best
def ra2deg(s):
    h,m,sec=[float(v) for v in s.split()]; return 15*(h+m/60+sec/3600)
def dec2deg(s):
    sg=-1 if s.strip().startswith('-') else 1; d,m,sec=[abs(float(v)) for v in s.split()]; return sg*(d+m/60+sec/3600)
def f(e,tag):
    x=e.find(tag)
    if x is None or x.text is None: return None
    try: return float(x.text)
    except: return x.text.strip()
root=ET.parse(gzip.open(OECF)).getroot()
exo=[];added=0;matched=0
for sy in root.findall('system'):
    dist=f(sy,'distance')
    if dist is None or not isinstance(dist,float) or dist>=MAXPC: continue
    if not list(sy.iter('planet')): continue
    ra=ra2deg(sy.find('rightascension').text) if sy.find('rightascension') is not None else None
    de=dec2deg(sy.find('declination').text) if sy.find('declination') is not None else None
    sysnames=ids_of(sy)
    for st in sy.iter('star'):
        pls=st.findall('planet')
        if not pls: continue
        key=match(ids_of(st)+sysnames,ra,de,dist)
        if key is None:
            if ra is None: continue
            key='OEC '+ids_of(st)[0];sp=f(st,'spectraltype') or ''
            if not isinstance(sp,str): sp=''
            cl=sclass(sp) or ('M' if (f(st,'temperature') or 3000)<3900 else 'K' if (f(st,'temperature') or 0)<5300 else 'G')
            mv=f(st,'magV');absm=(mv-5*math.log10(dist)+5) if isinstance(mv,float) else {'M':12,'K':7,'G':5,'F':3.5}.get(cl,10)
            ex,ey,ez=eq2ecl(*radec2xyz(ra,de,dist))
            nm=ids_of(st)[0];nm={"Teegarden's Star":'Estrella de Teegarden'}.get(nm,nm)
            stars[key]=dict(key=key,gl='',name=nm,pos=[ex,ey,ez],dist=dist,absmag=absm,spect=sp,cl=cl,lc='V',R=f(st,'radius') if isinstance(f(st,'radius'),float) else est_radius(cl,5,'V'),ci=None,base='',comp=1,hip='',hd='',proper='')
            added+=1
        else:
            matched+=1
            S=stars[key]
            if ra is not None and S['base']=='' :
                ex,ey,ez=eq2ecl(*radec2xyz(ra,de,dist)); S['pos']=[ex,ey,ez]; S['dist']=dist
            if isinstance(f(st,'radius'),float) and S['name'] not in KNOWN_R: S['R']=f(st,'radius')
            if isinstance(f(st,'temperature'),float): S['teff']=f(st,'temperature')
        S=stars[key];S['host']=1
        mstar=f(st,'mass') if isinstance(f(st,'mass'),float) else 0.5
        for p in pls:
            a=f(p,'semimajoraxis');P=f(p,'period')
            a=a if isinstance(a,float) else None;P=P if isinstance(P,float) else None
            if a is None and P: a=(mstar*(P/365.25)**2)**(1/3)
            if P is None and a: P=365.25*math.sqrt(a**3/mstar)
            if not a or not P: continue
            r=f(p,'radius');m=f(p,'mass');T=f(p,'temperature');y=f(p,'discoveryyear');meth=f(p,'discoverymethod')
            exo.append(dict(name=ids_of(p)[0],host=key,a=round(a,5),P=round(P,4),Re=round(r*11.209,3) if isinstance(r,float) else None,Me=round(m*317.83,3) if isinstance(m,float) else None,
                T=round(T,1) if isinstance(T,float) else None,y=int(y) if isinstance(y,float) else None,meth=meth if isinstance(meth,str) else None))
# companions
groups={}
for k,S in stars.items():
    if S['base']: groups.setdefault(S['base'],[]).append(k)
for base,members in groups.items():
    if len(members)<2: continue
    members.sort(key=lambda g:stars[g]['comp']); prim=members[0]; P=stars[prim]
    for g in members[1:]:
        S=stars[g]; pa=P['pos']; sa=S['pos']
        n1=math.sqrt(sum(v*v for v in pa)); n2=math.sqrt(sum(v*v for v in sa))
        u1=[v/n1 for v in pa]; u2=[v/n2 for v in sa]
        d=[u2[i]-u1[i] for i in range(3)]; ang=math.sqrt(sum(v*v for v in d))
        S['primary']=prim; S['sepAU']=max(8.0,min(20000.0,ang*n1*PC_AU))
        t=[d[i]-sum(d[j]*u1[j] for j in range(3))*u1[i] for i in range(3)]; tn=math.sqrt(sum(v*v for v in t))
        S['dir']=[v/tn for v in t] if tn>1e-12 else [u1[1],-u1[0],0]
ids={};used=set()
for k,S in sorted(stars.items(),key=lambda kv:kv[1]['dist']):
    sid='st_'+re.sub(r'[^a-z0-9]','',k.lower().replace("'",''))
    while sid in used: sid+='x'
    used.add(sid);ids[k]=sid
out=[]
for k,S in sorted(stars.items(),key=lambda kv:kv[1]['dist']):
    au=[round(v*PC_AU,1) for v in S['pos']]
    rec=[ids[k],S['name'],S['gl'] or k,au,round(S['absmag'],2),S['spect'],S['cl'],round(S['R'],4),bv2rgb(S['ci'],S['cl'],S.get('teff')),round(S['dist']*LY_PC,3),S['lc']]
    if 'primary' in S: rec+=[ids[S['primary']],round(S['sepAU'],1),[round(v,4) for v in S['dir']]]
    out.append(rec)
exout=[]; pused=set()
for p in exo:
    pid='ex_'+re.sub(r'[^a-z0-9]','',p['name'].lower())
    if pid in pused: continue
    pused.add(pid)
    exout.append([pid,p['name'],ids[p['host']],p['a'],p['P'],p['Re'],p['Me'],p['T'],p['y'],p['meth']])
json.dump({'stars':out,'exo':exout},open('stars_data2.json','w'),ensure_ascii=False,separators=(',',':'))
print('stars',len(out),'exo',len(exout),'hosts matched',matched,'added',added,'size',len(json.dumps({'stars':out,'exo':exout},ensure_ascii=False,separators=(',',':'))))
for rec in out:
    if rec[1] in ('Vega','Arturo','Capella','Pólux','Fomalhaut','Cástor','51 Pegasi','55 Cancri','Próxima Centauri','TRAPPIST-1','Estrella de Teegarden','Gliese 581'): print(rec[:3],rec[9],rec[10],rec[7])
hostnames=sorted(set(r[1] for r in out if any(e[2]==r[0] for e in exout)))
print(len(hostnames),'hosts:',', '.join(hostnames[:60]))
