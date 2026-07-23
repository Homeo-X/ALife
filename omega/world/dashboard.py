"""The watch surface — how you *see* the living world.

Three renderers, all pure stdlib (the project takes no third-party deps):

* :func:`serve` — a live dashboard. A background thread advances the ``World`` and takes
  ``Observer`` snapshots; an ``http.server`` serves a self-contained HTML+JS page and a
  ``/state.json`` endpoint the page polls. Open it in a browser and watch the world live.
* :func:`render_html` — a single self-contained HTML snapshot (state embedded inline, no
  server) — shareable as an artifact.
* :func:`render_terminal` — an ANSI snapshot for headless watching.
"""
from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from omega.world import checkpoint as _ckpt
from omega.world.observe import Observer
from omega.world.runtime import World


def _sparkline(vals: list[float]) -> str:
    blocks = "▁▂▃▄▅▆▇█"
    if not vals:
        return ""
    hi = max(vals) or 1.0
    return "".join(blocks[min(len(blocks) - 1, int(v / hi * (len(blocks) - 1)))] for v in vals)


def render_terminal(s: dict) -> str:
    """A compact ANSI snapshot of the living world for headless watching."""
    L = []
    L.append(f"\033[1mΩ WORLD\033[0m  tick {s['tick']:,}   pop {s['population']}   "
             f"novelty {s['novelty_rate']:.3f}  classes-ever {s['classes_ever']:,}")
    L.append(f"pulse {_sparkline(s['novelty_pulse'])}")
    if "vitals" in s:
        v = s["vitals"]
        L.append(f"\033[1mvital signs\033[0m  competence {v['competence']:.3f} "
                 f"(slope {v['competence_slope']:+.5f})   closure {v['closure']:.3f}   "
                 f"self-maintaining lifeforms {v['lifeforms']}   "
                 f"genuine-novelty {v['genuine_novelty_rate']:.3f}   diversity {v['diversity']:.2f}")
        L.append(f"competence {_sparkline(v['competence_pulse'])}")
    L.append(f"construction: alphabet {s['alphabet']} ({s['reified']} reified)   "
             f"culture H/V {s['culture']['horizontal']}/{s['culture']['vertical']} "
             f"(×{s['culture']['ratio']})   collectives {s['n_collectives']}")
    L.append("\033[1mlifeforms\033[0m (persistent): " + ", ".join(
        f"{lf['name']}(age {lf['age']},d{lf['depth']})" for lf in s["lifeforms"][:6]))
    L.append("\033[1mcollectives\033[0m (communities): " + ", ".join(
        f"{c['name']}({c['size']})" for c in s["collectives"][:8]))
    L.append("\033[2mevents:\033[0m " + " · ".join(e["text"] for e in s["events"][:3]))
    return "\n".join(L)


def render_tower_terminal(st: dict) -> str:
    """A compact ANSI snapshot of the LIVE recursive tower (levels emerging over time)."""
    L = []
    L.append(f"\033[1mΩ TOWER\033[0m  tick {st['total_ticks']:,}   depth {st['tower_depth']}   "
             f"active tier {st['active_tier']}" + ("   \033[2m(complete)\033[0m" if st["done"] else ""))
    for t in st["per_tier"]:
        bar = "█" * max(0, min(30, int(t["competence"] * 12)))
        mark = "\033[32m✓\033[0m" if t["heritable"] and t["collectives"] >= 2 else "\033[2m·\033[0m"
        L.append(f"  {mark} tier {t['tier']} {t['level']:<14} competence {t['competence']:6.3f} "
                 f"{bar}  ({t['collectives']} collectives)")
    if not st["per_tier"]:
        L.append("  \033[2m(tier 0 developing…)\033[0m")
    L.append("\033[2mlevel births:\033[0m " + " · ".join(e["text"] for e in st["events"][:3]))
    return "\n".join(L)


# --- the browser dashboard (self-contained HTML + JS; polls /state.json) ---------------
_PAGE = """<!doctype html><meta charset=utf-8><title>Ω World</title>
<style>
 :root{color-scheme:dark}
 body{margin:0;background:#0b0e14;color:#c8d3e0;font:14px/1.5 ui-monospace,Menlo,monospace}
 header{padding:14px 20px;border-bottom:1px solid #1d2433;display:flex;gap:24px;align-items:baseline;flex-wrap:wrap}
 h1{font-size:16px;margin:0;color:#7fd1ff;letter-spacing:.08em}
 .k{color:#5b6b82}.v{color:#e8eef7}
 main{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px 20px}
 .card{background:#111624;border:1px solid #1d2433;border-radius:8px;padding:12px 14px}
 .card h2{font-size:12px;margin:0 0 8px;color:#7fd1ff;text-transform:uppercase;letter-spacing:.1em}
 .pulse{font-size:22px;letter-spacing:2px;color:#8affc1;word-break:break-all}
 .row{display:flex;justify-content:space-between;border-bottom:1px solid #161d2b;padding:2px 0}
 .row:last-child{border:0}.tag{color:#5b6b82}
 .ev{color:#9fb0c8;border-left:2px solid #2b3550;padding-left:8px;margin:3px 0}
 .born{color:#8affc1}.reify{color:#ffd479}.lifeform{color:#7fd1ff}
 .big{font-size:26px;color:#e8eef7}
 #ctl button{background:#1b2436;color:#c8d3e0;border:1px solid #2b3550;border-radius:5px;
   padding:6px 10px;margin:0 6px 6px 0;cursor:pointer;font:inherit}
 #ctl button:hover{background:#26324a;color:#8affc1}
 #ctl input[type=range]{width:60%;vertical-align:middle}
</style>
<header>
 <h1>Ω WORLD</h1>
 <div><span class=k>tick</span> <span class=v id=tick>–</span></div>
 <div><span class=k>population</span> <span class=v id=pop>–</span></div>
 <div><span class=k>novelty</span> <span class=v id=nov>–</span></div>
 <div><span class=k>classes ever</span> <span class=v id=ce>–</span></div>
 <div><span class=k>alphabet</span> <span class=v id=alpha>–</span></div>
</header>
<main>
 <div class=card style=grid-column:1/3><h2>novelty pulse — the world keeps discovering</h2>
   <div class=pulse id=pulse></div></div>
 <div class=card style=grid-column:1/3><h2>vital signs — is it alive &amp; getting better?</h2>
   <div class=row><span class=k>competence (rising = compounding)</span><span class=v id=vcomp>–</span></div>
   <div class=pulse id=vpulse style=color:#ffd18a></div>
   <div class=row><span class=k>autocatalytic closure — the life signal</span><span class=v id=vclos>–</span></div>
   <div class=row><span class=k>self-maintaining lifeforms</span><span class=v id=vlife>–</span></div>
   <div class=row><span class=k>genuine novelty (eviction-robust)</span><span class=v id=vgen>–</span></div>
   <div class=row><span class=k>ecological diversity</span><span class=v id=vdiv>–</span></div></div>
 <div class=card><h2>world map — geography</h2><canvas id=map width=320 height=320
   style="width:100%;image-rendering:pixelated;background:#0b0e14;border-radius:4px"></canvas>
   <div class=tag style=margin-top:6px>cell = a patch; hue = dominant lifeform, brightness = population</div></div>
 <div class=card><h2>reach in — steer the world</h2><div id=ctl>
   <button data-a=seed>seed life</button>
   <button data-a=shock>mass extinction</button>
   <button data-a=reify>force reify</button>
   <div style=margin-top:8px><span class=k>culture (horizontal transfer)</span>
     <input type=range min=0 max=1 step=0.05 value=0.3 id=ht></div>
   <div><span class=k>mutation rate</span>
     <input type=range min=0 max=0.3 step=0.01 value=0.05 id=mut></div>
   <div id=actlog class=tag style=margin-top:6px></div></div></div>
 <div class=card><h2>lifeforms — persistent characters</h2><div id=life></div></div>
 <div class=card><h2>collectives — living communities <span id=nc></span></h2><div id=coll></div></div>
 <div class=card><h2>culture &amp; construction</h2><div id=cc></div></div>
 <div class=card><h2>event feed</h2><div id=ev></div></div>
</main>
<script>
async function tick(){
 let s; try{ s=await (await fetch('/state.json')).json() }catch(e){ return }
 const $=id=>document.getElementById(id);
 $('tick').textContent=s.tick.toLocaleString();
 $('pop').textContent=s.population;
 $('nov').textContent=s.novelty_rate.toFixed(3);
 $('ce').textContent=s.classes_ever.toLocaleString();
 $('alpha').textContent=s.alphabet+' ('+s.reified+' reified)';
 const bl='▁▂▃▄▅▆▇█'; const hi=Math.max(...s.novelty_pulse,1e-9);
 $('pulse').textContent=s.novelty_pulse.map(v=>bl[Math.min(7,Math.floor(v/hi*7))]).join('');
 if(s.vitals){ const v=s.vitals;
   $('vcomp').textContent=v.competence.toFixed(3)+'  (slope '+(v.competence_slope>=0?'+':'')+v.competence_slope.toFixed(5)+')';
   const vh=Math.max(...v.competence_pulse,1e-9);
   $('vpulse').textContent=v.competence_pulse.map(x=>bl[Math.min(7,Math.floor(x/vh*7))]).join('');
   $('vclos').textContent=v.closure.toFixed(3);
   $('vlife').textContent=v.lifeforms;
   $('vgen').textContent=v.genuine_novelty_rate.toFixed(3)+'  ('+v.genuine_distinct.toLocaleString()+' ever)';
   $('vdiv').textContent=v.diversity.toFixed(2); }
 $('life').innerHTML=s.lifeforms.map(l=>`<div class=row><span class=v>${l.name}</span>`+
   `<span class=tag>age ${l.age.toLocaleString()} · depth ${l.depth} · peak ${l.peak}</span></div>`).join('');
 $('nc').textContent='('+s.n_collectives+')';
 $('coll').innerHTML=s.collectives.slice(0,12).map(c=>`<div class=row><span class=v>${c.name}</span>`+
   `<span class=tag>${c.size} motifs${c.patches>1?' ×'+c.patches:''}</span></div>`).join('');
 const cu=s.culture;
 $('cc').innerHTML=`<div class=row><span class=k>cultural transmission (H/V)</span><span class=v>${cu.horizontal} / ${cu.vertical} (×${cu.ratio})</span></div>`+
   `<div class=row><span class=k>constructed primitives</span><span class=v>${s.reified}</span></div>`+
   `<div class=row><span class=k>registry (windowed)</span><span class=v>${s.registry_size.toLocaleString()}</span></div>`;
 $('ev').innerHTML=s.events.slice(0,14).map(e=>`<div class="ev ${e.kind}">`+
   `<span class=tag>${e.tick.toLocaleString()}</span> ${e.text}</div>`).join('');
 drawMap(s.space);
}
function hue(name){let h=0;for(const c of(name||''))h=(h*31+c.charCodeAt(0))%360;return h;}
function drawMap(sp){
 const cv=document.getElementById('map'); if(!sp){cv.style.display='none';return;}
 const g=cv.getContext('2d'); const W=sp.w,H=sp.h; const cw=cv.width/W, ch=cv.height/H;
 const mx=Math.max(1,...sp.cells.map(c=>c.pop));
 g.clearRect(0,0,cv.width,cv.height);
 for(const c of sp.cells){
   const l=c.pop?(18+62*c.pop/mx):8;
   g.fillStyle=c.dominant?`hsl(${hue(c.dominant)},70%,${l}%)`:'#0b0e14';
   g.fillRect(c.x*cw,c.y*ch,cw-1,ch-1);
 }
}
async function act(action,params){ try{ await fetch('/act',{method:'POST',
   headers:{'Content-Type':'application/json'},body:JSON.stringify({action,params})});
   document.getElementById('actlog').textContent=action+' sent @tick '+
     (document.getElementById('tick').textContent); }catch(e){} }
document.querySelectorAll('#ctl button').forEach(b=>b.onclick=()=>({
   seed:()=>act('seed_life',{n:12}), shock:()=>act('shock',{magnitude:0.5}),
   reify:()=>act('reify_now',{})})[b.dataset.a]());
document.getElementById('ht').oninput=e=>act('set_law',{name:'horizontal_transfer',value:+e.target.value});
document.getElementById('mut').oninput=e=>act('set_law',{name:'mut_prob',value:+e.target.value});
tick(); setInterval(tick, 1000);
</script>"""


def render_html(snapshot: dict) -> str:
    """A self-contained HTML snapshot with the state embedded inline (no server needed)."""
    inject = ("<script>window.__state=" + json.dumps(snapshot) +
              ";fetch=async()=>({json:async()=>window.__state});</script>")
    return _PAGE + inject


class _Runner:
    """Advances the world in a background thread; holds the latest snapshot for the server."""

    def __init__(self, world: World, chunk: int, checkpoint_path: str | None,
                 checkpoint_every: int) -> None:
        self.world, self.chunk = world, chunk
        self.obs = Observer()
        self.checkpoint_path, self.checkpoint_every = checkpoint_path, checkpoint_every
        self.latest: dict = self.obs.snapshot(world)
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._queue: list = []                 # pending interactions (applied between chunks)

    def enqueue(self, action: str, params: dict) -> None:
        with self._lock:
            self._queue.append((action, params))

    def _apply_pending(self) -> None:
        with self._lock:
            pending, self._queue = self._queue, []
        for action, pr in pending:             # applied between steps -> no race with step()
            try:
                if action == "seed_life":
                    self.world.seed_life(int(pr.get("n", 8)), pr.get("patch"))
                elif action == "shock":
                    self.world.shock(float(pr.get("magnitude", 0.5)), pr.get("patch"))
                elif action == "set_law":
                    self.world.set_law(str(pr["name"]), float(pr["value"]))
                elif action == "reify_now":
                    self.world.reify_now()
            except (KeyError, ValueError, TypeError):
                pass

    def loop(self) -> None:
        chunks = 0
        while not self._stop.is_set():
            self._apply_pending()
            self.world.step(self.chunk)
            snap = self.obs.snapshot(self.world)
            with self._lock:
                self.latest = snap
            chunks += 1
            if self.checkpoint_path and chunks % self.checkpoint_every == 0:
                _ckpt.save(self.world, self.checkpoint_path)

    def state_json(self) -> bytes:
        with self._lock:
            return json.dumps(self.latest).encode()

    def stop(self) -> None:
        self._stop.set()


def serve(world: World, port: int = 8000, chunk: int = 40,
          checkpoint_path: str | None = None, checkpoint_every: int = 25) -> None:
    """Run the world in a thread and serve the live dashboard on ``port`` (blocking)."""
    runner = _Runner(world, chunk, checkpoint_path, checkpoint_every)
    t = threading.Thread(target=runner.loop, daemon=True)
    t.start()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet
            pass

        def do_GET(self):
            if self.path.startswith("/state.json"):
                body = runner.state_json()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
            else:
                body = _PAGE.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if not self.path.startswith("/act"):
                self.send_response(404); self.end_headers(); return
            n = int(self.headers.get("Content-Length", 0))
            try:
                req = json.loads(self.rfile.read(n) or b"{}")
                runner.enqueue(str(req.get("action", "")), req.get("params", {}))
                body = b'{"ok":true}'
            except (ValueError, TypeError):
                body = b'{"ok":false}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    httpd = ThreadingHTTPServer(("", port), Handler)
    print(f"Ω world live at http://localhost:{port}  (Ctrl-C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        runner.stop()
        if checkpoint_path:
            _ckpt.save(world, checkpoint_path)
        httpd.server_close()
