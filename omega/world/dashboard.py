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
    L.append(f"construction: alphabet {s['alphabet']} ({s['reified']} reified)   "
             f"culture H/V {s['culture']['horizontal']}/{s['culture']['vertical']} "
             f"(×{s['culture']['ratio']})   collectives {s['n_collectives']}")
    L.append("\033[1mlifeforms\033[0m (persistent): " + ", ".join(
        f"{lf['name']}(age {lf['age']},d{lf['depth']})" for lf in s["lifeforms"][:6]))
    L.append("\033[1mcollectives\033[0m (communities): " + ", ".join(
        f"{c['name']}({c['size']})" for c in s["collectives"][:8]))
    L.append("\033[2mevents:\033[0m " + " · ".join(e["text"] for e in s["events"][:3]))
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
}
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

    def loop(self) -> None:
        chunks = 0
        while not self._stop.is_set():
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
