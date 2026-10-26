"""Собирает страницы мест по образцу burana.html: 3D сверху, три цифры, гид с вопросами, другие места.
Тексты гида — media/guide.json (с источниками). Запуск из папки сайта: python tools/pages.py"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE = json.load(open(os.path.join(ROOT, "media", "guide.json"), encoding="utf-8"))

# все страницы мест — для блока «Другие места»
PLACES = [("burana.html", "Бурана", "Чуйская обл."), ("tash-rabat.html", "Таш-Рабат", "Нарынская обл."),
          ("kel-suu.html", "Кель-Суу", "Нарынская обл."), ("sulaiman-too.html", "Сулайман-Тоо", "Ош")]

# стиль один на все страницы мест; на компьютере — модель слева, гид справа
CSS = """
:root{
  --sand:#f8f3ea; --paper:#fffdf8; --ink:#2b2118; --muted:#86715d; --line:#e8dccb;
  --clay:#b5532c; --clay-ink:#ffffff; --sky:#d7e7f1; --steppe:#e6d4b3;
  --display:"Rubik","Segoe UI",Arial,sans-serif; --body:"PT Sans","Segoe UI",Arial,sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
body{background:var(--sand);color:var(--ink);font:16px/1.45 var(--body);margin:0}
.app{max-width:520px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:14px 28px;display:flex;flex-direction:column;gap:14px}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.brand{font:800 18px/1 var(--display);letter-spacing:.06em;color:var(--clay);text-decoration:none}
.langs{display:flex;gap:4px}
.langs button{font:700 12px var(--body);padding:5px 10px;border-radius:20px;border:1px solid var(--line);background:var(--paper);color:var(--muted);cursor:pointer}
.langs button[aria-pressed="true"]{background:var(--clay);border-color:var(--clay);color:var(--clay-ink)}
h1{font:800 clamp(28px,8vw,36px)/1.05 var(--display);margin:0;text-wrap:balance}
.meta{color:var(--muted);font-size:14px;margin-top:4px}
.stage{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--line);background:linear-gradient(var(--sky) 0%,#eef4f6 100%)}
model-viewer{width:100%;height:min(62vh,460px);display:block;--poster-color:transparent;background:transparent}
.tog{position:absolute;top:12px;left:12px;display:flex;border-radius:20px;overflow:hidden;border:1px solid var(--line);background:rgba(255,253,248,.92)}
.tog button{font:700 13px var(--body);padding:7px 13px;border:0;background:transparent;color:var(--muted);cursor:pointer}
.tog button[aria-pressed="true"]{background:var(--clay);color:var(--clay-ink)}
.chip360{position:absolute;top:12px;right:12px;font:700 12px var(--body);padding:6px 11px;border-radius:20px;background:rgba(255,253,248,.92);border:1px solid var(--line)}
.note{font-size:12.5px;line-height:1.35;color:var(--muted)}
.load{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:14px;color:var(--muted);pointer-events:none}
.hs{background:none;border:0;padding:0;display:block;transform:translateY(-50%)}
.hs::before{content:"";display:block;width:10px;height:10px;margin:0 auto;border-radius:50%;background:var(--clay);border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.35)}
.hs span{display:block;margin-top:3px;padding:2px 7px;border-radius:9px;background:rgba(255,253,248,.92);color:var(--ink);font:700 11.5px/1.2 var(--body);white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.18)}
.hs.up{display:flex;flex-direction:column-reverse;transform:translateY(-88%)}
.hs.up span{margin:0 0 3px}
.hs[data-visible=false]{opacity:.25}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.fact{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:10px 10px 9px}
.fact b{display:block;font:700 20px/1.1 var(--display);font-variant-numeric:tabular-nums}
.fact span{font-size:12px;color:var(--muted);line-height:1.25;display:block;margin-top:3px}
.guide{display:flex;flex-direction:column;gap:9px}
.b{padding:10px 13px;border-radius:18px;max-width:90%;font-size:15px}
.g{background:var(--paper);border:1px solid var(--line);align-self:flex-start;border-bottom-left-radius:6px}
.g .who{display:block;font:700 11px var(--body);letter-spacing:.08em;color:var(--clay);margin-bottom:3px}
.g .src{display:block;font-size:11.5px;color:var(--muted);margin-top:5px}
.u{background:var(--clay);color:var(--clay-ink);align-self:flex-end;border-bottom-right-radius:6px}
.asks{display:flex;flex-wrap:wrap;gap:7px}
.asks button{font:15px var(--body);padding:8px 13px;border-radius:20px;border:1px solid var(--clay);background:var(--paper);color:var(--clay);cursor:pointer}
.asks button:disabled{opacity:.45;cursor:default}
.bar{display:flex;gap:10px;align-items:center}
.inp{flex:1;min-width:0;height:46px;border-radius:23px;border:1px solid var(--line);background:var(--paper);display:flex;align-items:center;padding:0 16px;font-size:14px;color:var(--muted)}
.mic{width:50px;height:50px;border-radius:50%;border:0;background:var(--clay);display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 6px 16px rgba(181,83,44,.35);flex:none}
h2{font:700 15px var(--display);margin:6px 0 0;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}
.places{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
.place{flex:none;padding:9px 13px;border-radius:14px;border:1px solid var(--line);background:var(--paper);font-size:14px;color:var(--ink);text-decoration:none}
.place.on{border-color:var(--clay);color:var(--clay);font-weight:700}
.place small{display:block;color:var(--muted);font-size:11.5px;font-weight:400}
.demo{font-size:12.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:10px}
button:focus-visible,a:focus-visible{outline:2px solid var(--clay);outline-offset:2px}
/* компьютер: модель слева на всю высоту, текст и гид справа */
@media (min-width:900px){
  .app{max-width:1240px;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(360px,1fr);column-gap:28px;row-gap:14px;align-items:start}
  .app>*{grid-column:2}
  .app>.top{grid-column:1 / -1}
  .app>.stage{grid-column:1;grid-row:2 / span 20;position:sticky;top:14px}
  .stage model-viewer{height:calc(100vh - 90px)}
}
"""

HEAD = """<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — Кыргызстан 3D</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;700;800&family=PT+Sans:wght@400;700&display=swap">
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
<style>
/* Тёплый шёлк, как страница Бураны. Собрано tools/pages.py — правки вносить туда. */{css}</style>
"""

MIC = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="12" rx="3" fill="#fff"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3" stroke="#fff" stroke-width="2" fill="none"/></svg>'

PAGES = {
    "tash-rabat": dict(
        title="Караван-сарай Таш-Рабат", meta="Нарынская область · Великий шёлковый путь",
        model='<model-viewer id="mv" src="tash-rabat.glb" alt="3D-модель караван-сарая Таш-Рабат" camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000" rotation-per-second="10deg" camera-orbit="70deg 74deg 80m" min-camera-orbit="auto 0deg 25m" max-camera-orbit="auto 88deg 200m" field-of-view="30deg" shadow-intensity="1" exposure="1.05" interaction-prompt="none">',
        toggle=("Сейчас", "Жизнь караван-сарая"),
        facts=[("~31", "комната с куполами (en.wikipedia)"), ("~3200 м", "над уровнем моря (источники расходятся)"), ("X или XV в.", "время постройки — спорно")],
        notes=["Модель приблизительная: фасады 32,4 м и центральный зал 9,1 × 9,26 м — по обмерам (informer.kg), высоты, башни, портал и купол — по фото Wikimedia Commons.",
               "«Жизнь караван-сарая» — иллюстрация, а не реконструкция: так могла выглядеть стоянка каравана на Шёлковом пути."]),
    "kel-suu": dict(
        title="Озеро Кель-Суу", meta="Нарынская область · Ат-Башинский район",
        model='<model-viewer id="mv" src="kel-suu.glb" alt="3D-макет озера Кель-Суу" camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000" rotation-per-second="10deg" camera-orbit="15deg 52deg 19000m" min-camera-orbit="auto 0deg 4000m" max-camera-orbit="auto 85deg 40000m" field-of-view="30deg" shadow-intensity="1" exposure="1.05" interaction-prompt="none">',
        facts=[("3514 м", "над уровнем моря"), ("4,5 км²", "площадь озера (en.wikipedia)"), ("июнь–окт.", "сезон поездок")],
        notes=["Макет 14 × 14 км: высоты — AWS Terrain Tiles, снимок — Sentinel-2 cloudless (s2maps.eu, EOX). Горы по высоте усилены в 1,3 раза."]),
    "sulaiman-too": dict(
        title="Гора Сулайман-Тоо", meta="Город Ош · Всемирное наследие ЮНЕСКО",
        model='<model-viewer id="mv" src="sulaiman-too.glb" alt="3D-макет горы Сулайман-Тоо" camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000" rotation-per-second="10deg" camera-orbit="10deg 60deg 2100m" camera-target="150m 90m 0m" min-camera-orbit="auto 0deg 500m" max-camera-orbit="auto 85deg 6000m" field-of-view="30deg" shadow-intensity="1" exposure="1.05" interaction-prompt="none">\n'
              '      <button class="hs up" slot="hotspot-0" data-position="543.7m 152.5m -57.3m" data-normal="0m 1m 0m"><span>Дом Бабура</span></button>\n'
              '      <button class="hs" slot="hotspot-1" data-position="-22.7m 167.5m 149.1m" data-normal="0m 1m 0m"><span>Музей в скале</span></button>\n'
              '      <button class="hs" slot="hotspot-2" data-position="424.8m 165.0m -48.4m" data-normal="0m 1m 0m"><span>Пещера Тамчы-Тамар</span></button>\n'
              '      <button class="hs" slot="hotspot-3" data-position="161.4m 186.0m 15.4m" data-normal="0m 1m 0m"><span>Пещера Чилтен</span></button>',
        facts=[("2009", "внесена в список ЮНЕСКО"), ("1110 м", "над уровнем моря"), ("7 пещер", "на склонах горы")],
        notes=["Макет 2 × 2 км: высоты — AWS Terrain Tiles, снимок — Sentinel-2 cloudless (s2maps.eu, EOX), дома, дороги, тропы и названия — © участники OpenStreetMap (ODbL). Рельеф по высоте усилен в 1,25 раза."]),
}


def places_html(current):
    out = []
    for href, name, reg in PLACES:
        on = ' on" aria-current="page' if href == current else ""
        out.append(f'    <a class="place{on}" href="{href}">{name}<small>{reg}</small></a>')
    return "\n".join(out)


def page(pid, p):
    e = html.escape
    g = GUIDE[pid]
    tog = ""
    if p.get("toggle"):
        a, b = p["toggle"]
        tog = (f'\n    <div class="tog" role="group" aria-label="Вид">\n      <button id="v-now" type="button" aria-pressed="true">{a}</button>\n'
               f'      <button id="v-life" type="button" aria-pressed="false">{b}</button>\n    </div>')
    notes = "".join(f'\n  <div class="note" id="note-{i}"{" hidden" if i else ""}>{e(n)} Крутите пальцем, приближайте двумя.</div>' for i, n in enumerate(p["notes"]))
    facts = "\n".join(f'    <div class="fact"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["facts"])
    asks = "\n".join(f'    <button type="button" data-q="{k}">{e(q[0])}</button>' for k, q in g["qa"].items())
    life_js = ""
    if p.get("toggle"):
        life_js = """
const bNow = document.getElementById("v-now"), bLife = document.getElementById("v-life");
function view(life) {
  mv.src = life ? "tash-rabat-karavan.glb" : "tash-rabat.glb";
  mv.cameraOrbit = life ? "80deg 66deg 70m" : "70deg 74deg 80m";
  mv.cameraTarget = life ? "16m 2m 0m" : "auto auto auto";
  mv.maxCameraOrbit = life ? "auto 88deg 260m" : "auto 88deg 200m";
  bLife.setAttribute("aria-pressed", life); bNow.setAttribute("aria-pressed", !life);
  document.getElementById("note-1").hidden = !life; document.getElementById("note-0").hidden = life;
}
bNow.onclick = () => view(false); bLife.onclick = () => view(true);
if (location.hash === "#life") view(true);"""
    body = f"""
<div class="app">
  <div class="top">
    <a class="brand" href="index.html">← КАРТА</a>
    <div class="langs" role="group" aria-label="Язык">
      <button id="lang-kg" type="button" aria-pressed="false">KG</button>
      <button id="lang-ru" type="button" aria-pressed="true">RU</button>
      <button id="lang-en" type="button" aria-pressed="false">EN</button>
    </div>
  </div>

  <div>
    <h1>{e(p["title"])}</h1>
    <div class="meta">{e(p["meta"])}</div>
  </div>

  <div class="stage">
    {p["model"]}
      <div slot="poster" class="load" id="load">Загружаю модель…</div>
    </model-viewer>{tog}
    <div class="chip360">↻ 360°</div>
  </div>
{notes}

  <div class="facts">
{facts}
  </div>

  <div class="guide" id="chat" aria-live="polite">
    <div class="b g"><span class="who">ГИД</span>{e(g["hello"])}</div>
  </div>
  <div class="asks" id="asks">
{asks}
  </div>
  <div class="bar">
    <div class="inp">Спросите гида…</div>
    <button class="mic" id="mic" type="button" aria-label="Спросить голосом">{MIC}</button>
  </div>

  <h2>Другие места</h2>
  <div class="places">
{places_html(pid + ".html")}
  </div>

  <div class="demo">Демо для конкурса «100 идей для Кыргызстана». Ответы гида пока заготовлены заранее и проверены по источникам, в рабочей версии гид — нейросеть, говорит голосом на кыргызском, русском и английском.</div>
</div>

<script>
const A = {json.dumps(g["qa"], ensure_ascii=False, indent=1)};
const mv = document.getElementById("mv"), chat = document.getElementById("chat");
mv.addEventListener("error", () => {{ document.getElementById("load").textContent = "Модель не загрузилась — обновите страницу"; }});{life_js}
function esc(s) {{ return String(s).replace(/[&<>"]/g, c => ({{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}}[c])); }}
function bubble(cls, h) {{ const d = document.createElement("div"); d.className = "b " + cls; d.innerHTML = h; chat.appendChild(d); return d; }}
document.getElementById("asks").addEventListener("click", e => {{
  const k = e.target.dataset && e.target.dataset.q; if (!k) return;
  const [q, a, s] = A[k]; e.target.disabled = true;
  bubble("u", esc(q));
  const t = bubble("g", '<span class="who">ГИД</span>…');
  setTimeout(() => {{ t.innerHTML = '<span class="who">ГИД</span>' + esc(a) + '<span class="src">Источник: ' + esc(s) + '</span>'; }}, 450);
}});
document.getElementById("mic").onclick = () => bubble("g", '<span class="who">ГИД</span>Голосом можно будет спрашивать в рабочей версии. Пока выберите вопрос выше.');
for (const id of ["lang-kg", "lang-en"]) document.getElementById(id).onclick = () => bubble("g", '<span class="who">ГИД</span>Кыргызча жана English — в рабочей версии. Тексты сейчас переводим и проверяем.');
</script>
</html>
"""
    return HEAD.format(title=e(p["title"]), css=CSS) + body


for pid, p in PAGES.items():
    with open(os.path.join(ROOT, pid + ".html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page(pid, p))
    print("готово", pid + ".html")
