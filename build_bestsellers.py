# -*- coding: utf-8 -*-
"""楽天スキンケア売れ筋の値段帳（glow_prices.html の一番上の欄）と、商品ページ（1品1枚）を作る。2026-11-03

使い方:
  python3 build_bestsellers.py rakuten_rank_*.csv ... popular_rakuten_*.csv ...
    rakuten_rank_*    … n8n GlowGuide 05（楽天スキンケア売れ筋120位）。ランキングに出ている店の値段とリンク
    popular_rakuten_* … n8n GlowGuide 07（売れ筋の定番を楽天全体で検索）。送料込みの最安と、送料別も含めた本体最安
  各 popular には、その時刻以前でいちばん新しい rakuten_rank を組み合わせる。
  → glow_prices.html の <!--BESTSELLERS-->〜<!--/BESTSELLERS--> を書き換え / glow_item_<slug>.html / bestsellers.json

⛔️楽天のアフィリURLは手で打たない。CSVの affiliateUrl / 商品URL / 本体最安_URL を機械でそのまま入れる。
⛔️リンクの文字に値段を入れない（楽天アフィリエイトのガイドライン）。値段はリンクの外に書く。
⛔️セールの日程を書かない（楽天が公開する前の予告は禁止）。
⭐️送料が分からない店は除外せず「送料は店と地域によって異なります」と添えて本体価格で出す（本人決定 2026-10-09）。
⭐️glow_prices.html の27品の部分は build_prices_page.py が作る。こちらは印の間だけを書き換える（順番はどちらが先でもよい）。
"""
import csv, html, json, re, sys
from urllib.parse import quote
from datetime import datetime

BASE = "https://glow.stats-log.net/"
PAGE = "glow_prices.html"
A8_QOO10 = "https://px.a8.net/svt/ejp?a8mat=4AX8OC+BWOVM+4QYG+BW8O2&a8ejpredirect="   # A8.net Qoo10公式（提携済み・2026-08-28）
AMAZON_TAG = "glowskin2026-22"   # Amazonアソシエイト（値段は載せない。検索結果へのリンクだけ）
E = html.escape
yen = lambda v: f"{int(v):,}円"

# ── 売れ筋の定番（GlowGuide 07 の商品リストと同じ並び）
# rank_code … GlowGuide 05 の itemCode（ランキングの出品を特定する）
# median    … 10/10〜11/01の売れ筋8回で、8回とも上位。その中央の順位（claude/★実測_楽天スキンケア売れ筋8回分_…_20261101.md）
ITEMS = [
    dict(slug="elixir_retinopower", asin="B0FJXTTPPZ", key="エリクシール レチノパワー", brand="エリクシール", cat="クリーム",
         name="シュペリエル レチノパワー リンクルクリーム ba L 22g", amount=22, unit="g",
         rank_code="rakuten24:11354091", median=7.0, about="シワを改善する医薬部外品のクリーム（資生堂）。"),
    dict(slug="elixir_brightening_refill", asin="B0GC3J1CW7", key="エリクシール ブライトニング", brand="エリクシール", cat="化粧水",
         name="ブライトニング ローション つめかえ用 150mL", amount=150, unit="mL",
         rank_code="rakuten24:11386627", median=11.0, about="しみ・そばかすを防ぐ医薬部外品の化粧水（資生堂）。つめかえ用。"),
    dict(slug="attenir_cleanse_oil_350", asin="B0H29GJK1M", key="アテニア", brand="アテニア", cat="クレンジング",
         name="スキンクリア クレンズ オイル 350mL", amount=350, unit="mL",
         rank_code="attenir:10000252", median=1.5, about="メイク落としのオイル。350mLの大容量。"),
    dict(slug="aestura_atobarrier365", asin="B09YDCCJBJ", key="AESTURA", brand="エストラ", cat="クリーム",
         name="アトバリア365 クリーム 80mL", amount=80, unit="mL",
         rank_code="aestura-japan:10000007", median=17.0, about="セラミド配合の保湿クリーム（韓国 AESTURA）。"),
    dict(slug="fancl_mild_cleansing_oil", asin="B0GK5RBK1W", key="ファンケル", brand="ファンケル", cat="クレンジング",
         name="マイルドクレンジング オイル 120mL", amount=120, unit="mL",
         rank_code="fancl-shop:10009046", median=21.5, about="メイク落としのオイル。"),
    dict(slug="takami_skinpeel", asin="B010FZZWY8", key="タカミ", brand="タカミ", cat="美容液",
         name="タカミスキンピール 30mL", amount=30, unit="mL",
         rank_code="takami-labo:10000519", median=8.5, about="角質ケアの美容液。"),
]
CATS = ["クレンジング", "化粧水", "美容液", "クリーム"]


def read(path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def ts_of(path):
    m = re.search(r"(\d{8})_(\d{4})", path)
    return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M")


def jdt(d):
    return f"{d.month}月{d.day}日 {d.hour}時"


def aff(u):
    u = (u or "").strip()
    if not u.startswith("https://hb.afl.rakuten.co.jp/"):
        raise SystemExit("⛔️楽天の公式アフィリURLではない値があります（手で直さないこと）")
    return u


def snapshot(rank_csv, pop_csv, qoo=None):
    """1回分（ランキング1本＋売れ筋の定番1本）から、商品ごとの候補と最安を出す。"""
    rank = {r["itemCode"]: r for r in read(rank_csv)}
    pop = {r["ブランド"]: r for r in read(pop_csv)}
    out = {}
    for it in ITEMS:
        r, p = rank.get(it["rank_code"]), pop.get(it["key"])
        cands = []
        if r:
            cands.append(dict(kind="rank", media="楽天市場", shop=r["shopName"].replace("　", " "), price=int(r["itemPrice"]),
                              incl=r["postageFlag"] == "0", url=aff(r["affiliateUrl"]), rank=int(r["rank"]),
                              reviews=int(r["reviewCount"]), avg=float(r["reviewAverage"])))
        if p and p["成否"] == "取得" and p["総額"]:
            cands.append(dict(kind="incl", media="楽天市場", shop=p["ショップ名"], price=int(p["総額"]), incl=True, url=aff(p["商品URL"])))
        if p and p.get("本体最安_価格"):
            cands.append(dict(kind="body", media="楽天市場", shop=p["本体最安_店"], price=int(p["本体最安_価格"]),
                              incl=p.get("本体最安_送料") == "送料込み", url=aff(p["本体最安_URL"])))
        # Qoo10（本人のChromeで取得・A8.netのリンク）。⛔️売れ筋の店の80%未満でレビュー10件未満は別物の疑いとして出さない
        for q in ((qoo or {}).get("items", {}).get(it["slug"], [])):
            if r and q["price"] < int(r["itemPrice"]) * 0.8 and q["rev"] < 10:
                continue
            cands.append(dict(kind="qoo10", media="Qoo10", shop="Qoo10", price=int(q["price"]), incl=bool(q["free"]),
                              url=A8_QOO10 + quote("https://www.qoo10.jp/g/" + q["code"], safe=""), rev=q["rev"]))
        uniq = []
        for c in cands:
            if not any(u["shop"] == c["shop"] and u["price"] == c["price"] for u in uniq):
                uniq.append(c)
        incl = [c for c in uniq if c["incl"]]
        rk = next((c for c in uniq if c["kind"] == "rank"), None)
        out[it["slug"]] = dict(
            rank=rk, best=min(incl, key=lambda c: c["price"]) if incl else None,
            best_r=min([c for c in incl if c["media"] == "楽天市場"], key=lambda c: c["price"], default=None),
            body=min([c for c in uniq if not c["incl"] and c["kind"] != "rank"], key=lambda c: c["price"], default=None),
            qoo10=min([c for c in uniq if c["kind"] == "qoo10"], key=lambda c: (not c["incl"], c["price"]), default=None))
    return out


def snapshot_qoo_only(qoo, it, rk):
    """前回のQoo10（同じ選び方：送料込みを優先し、その中の最安）"""
    best = None
    for q in qoo.get("items", {}).get(it["slug"], []):
        if rk and q["price"] < rk["price"] * 0.8 and q["rev"] < 10:
            continue
        c = dict(price=int(q["price"]), incl=bool(q["free"]))
        if best is None or (not c["incl"], c["price"]) < (not best["incl"], best["price"]):
            best = c
    return best


def collect(rank_csvs, pop_csvs, qoo=None, qoo_prev=None):
    ranks = sorted(rank_csvs, key=ts_of)
    snaps = []
    for pf in sorted(pop_csvs, key=ts_of):
        before = [r for r in ranks if ts_of(r) <= ts_of(pf)]
        if not before:
            continue
        snaps.append((ts_of(pf), ts_of(before[-1]), snapshot(before[-1], pf, qoo if pf == sorted(pop_csvs, key=ts_of)[-1] else None)))
    if not snaps:
        raise SystemExit(__doc__)
    at, rank_at, now = snaps[-1]
    prev = snaps[-2] if len(snaps) >= 2 else None
    items = []
    for it in ITEMS:
        s = now[it["slug"]]
        if not s["rank"] or not s["best"]:
            raise SystemExit(f"⛔️{it['key']} の最新データがそろっていません")
        hist = [dict(at=t.strftime("%Y-%m-%d %H:%M"), price=sn[it["slug"]]["best"]["price"],
                     shop=sn[it["slug"]]["best"]["shop"]) for t, _, sn in snaps if sn[it["slug"]]["best"]]
        # 値下がりは同じ土台（楽天市場の送料込み最安）どうしでしか比べない
        pb = prev[2][it["slug"]]["best_r"] if prev and prev[2][it["slug"]]["best_r"] else None
        qp = None
        if qoo_prev:
            qp = snapshot_qoo_only(qoo_prev, it, s["rank"])
        items.append(dict(it, rank_now=s["rank"], best=s["best"], body=s["body"], qoo10=s["qoo10"], hist=hist,
                          r_now=s["best_r"], r_prev=pb, q_prev=qp,
                          save=s["rank"]["price"] - s["best"]["price"],
                          drop=(pb["price"] - s["best_r"]["price"]) if pb and s["best_r"] else 0, prev_price=pb["price"] if pb else None,
                          at=at.strftime("%Y-%m-%d %H:%M"), rank_at=rank_at.strftime("%Y-%m-%d %H:%M")))
    return items, at, (prev[0] if prev else None)


CSS = """<style>
#bestsellers{scroll-margin-top:60px}
.bs-tools{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px}
.bs-tools input{flex:1 1 220px;font-size:16px;padding:10px 12px;border:1px solid #ccc;border-radius:10px}
.bs-cats{display:flex;flex-wrap:wrap;gap:6px}
.bs-cats button{font-size:13px;padding:7px 12px;border:1px solid #ddd;border-radius:999px;background:#fff;cursor:pointer}
.bs-cats button[aria-pressed="true"]{background:#c0392b;color:#fff;border-color:#c0392b}
.bs-top{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:10px 0}
.bs-card{border:2px solid #c0392b;border-radius:14px;padding:12px 14px;background:#fff6f4}
.bs-card .k{font-size:12px;color:#777}.bs-card .n{font-weight:700;margin:2px 0 6px;line-height:1.4}
.bs-card .big{font-size:1.6rem;font-weight:700;color:#c0392b;line-height:1.2}
.bs-card .sv{font-size:.9rem;margin:4px 0 8px}
main.wrap a.buybtn,a.buybtn{display:inline-block;padding:8px 12px;border-radius:8px;background:#c0392b;color:#fff;border:0;text-decoration:none;font-size:.85rem;white-space:nowrap;margin:0}
main.wrap a.buybtn:hover{background:#a93226;color:#fff}
main.wrap a.buybtn.q10{background:#e4004f}main.wrap a.buybtn.amz{background:#232f3e}
.sm{display:block;font-size:.78rem;color:#777;margin-top:2px}
.save{color:#c0392b;font-weight:700}
.dn{display:block;font-size:.8rem;color:#1e7f4f;font-weight:700}.up{display:block;font-size:.8rem;color:#888}
.drop{display:inline-block;font-size:.72rem;background:#1e7f4f;color:#fff;border-radius:4px;padding:1px 6px;margin-left:4px}
table.bstbl td.num,table.bstbl th.num{text-align:right;white-space:nowrap}\ntable.bstbl td.num a.buybtn{margin-top:6px}
.bs-empty{display:none;color:#777}
.verdict{background:#fff6f4;border:2px solid #c0392b;border-radius:14px;padding:16px 18px;margin:14px 0}
.verdict .s{font-size:.85rem;color:#777}
.verdict .big{font-size:2rem;font-weight:700;color:#c0392b;line-height:1.25}
.verdict .sub{font-size:.95rem;margin-top:6px}
.buybox{display:flex;flex-direction:column;gap:10px;margin:14px 0}
.buyrow{display:flex;justify-content:space-between;align-items:center;border:1px solid #ddd;border-radius:10px;padding:10px 12px;gap:10px}
.buyrow.best{border-color:#c0392b;background:#fffaf9}
.buyrow .m{font-weight:700}.buyrow .s{font-size:.8rem;color:#777}
.buyrow .p{font-size:1.2rem;font-weight:700;white-space:nowrap}
.tag{display:inline-block;font-size:.72rem;background:#c0392b;color:#fff;border-radius:4px;padding:1px 6px;margin-left:6px}
.facts{list-style:none;padding:0;margin:10px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.facts li{background:#f7f4f1;border-radius:10px;padding:10px 12px;font-size:.85rem}
.facts b{display:block;font-size:1.15rem}
</style>
"""

JS = """<script>
(function(){var q=document.getElementById('bs-q'),bt=[].slice.call(document.querySelectorAll('.bs-cats button')),
rows=[].slice.call(document.querySelectorAll('[data-bs]')),em=document.getElementById('bs-empty'),cat='';
function norm(s){return (s||'').toLowerCase().replace(/\\s+/g,'').replace(/[ァ-ン]/g,function(c){return String.fromCharCode(c.charCodeAt(0)-96)})}
function run(){var v=norm(q.value),n=0;rows.forEach(function(r){var ok=(!v||norm(r.getAttribute('data-bs')).indexOf(v)>=0)&&(!cat||r.getAttribute('data-cat')===cat);r.style.display=ok?'':'none';if(ok&&r.tagName==='TR')n++});em.style.display=n?'none':'block'}
q.addEventListener('input',run);bt.forEach(function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-c');bt.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});run()})});})();
</script>"""

HOWTO = """<ul class="howto">
<li><strong>楽天市場のスキンケア売れ筋ランキングを毎日2回記録</strong>し、上位に居続けている商品を選んでいます。</li>
<li>その商品を<strong>楽天市場全体で毎日2回（10時台と18時台）</strong>し、同じ商品名・同じ容量のものだけを比べています。セット品・容量違いは外しています。</li>
<li><strong>Qoo10も同じ商品名・同じ容量で調べています</strong>（週に数回更新・更新日時は上に表示）。レビューが極端に少なく、値段が売れ筋の店の8割を下回るものは、別の商品のおそれがあるため載せていません。</li>
<li><strong>送料込みの値段で比べています。</strong>送料が別の店は除外せず、本体の値段に「送料は店と地域によって異なります」と添えて載せています。</li>
<li>クーポンやポイントは含めていません。<strong>値段と在庫は変わります。</strong>買う前に必ずリンク先の表示を確かめてください。</li>
</ul>"""


def btn(c):
    return f'<a class="buybtn{" q10" if c.get("media") == "Qoo10" else ""}" href="{E(c["url"])}" target="_blank" rel="sponsored nofollow noopener">{E(c.get("media", "楽天市場"))}で見る</a>'


def amazon_btn(d):
    # ASINが分かる商品はAmazonの商品ページへ直接（2026-11-03 本人のChromeで商品名・容量を照合済み）。無ければ検索結果へ
    if d.get("asin"):
        u = f'https://www.amazon.co.jp/dp/{d["asin"]}?tag={AMAZON_TAG}'
        label = "Amazonで見る"
    else:
        u = "https://www.amazon.co.jp/s?k=" + quote(f'{d["brand"]} {d["name"]}') + "&tag=" + AMAZON_TAG
        label = "Amazonで探す"
    return f'<a class="buybtn amz" href="{E(u)}" target="_blank" rel="sponsored nofollow noopener">{label}</a>'


def chg(now, prev):
    """前回比（同じ土台どうしだけ）。下がった＝緑、上がった＝灰"""
    if not now:
        return ""
    if not prev:
        return '<span class="sm">前回の記録なし（今回から記録）</span>'
    if prev.get("incl") is not None and now.get("incl") is not None and prev["incl"] != now["incl"]:
        return '<span class="sm">前回と送料の条件が違うため比べていません</span>'
    d = now["price"] - prev["price"]
    if d == 0:
        return '<span class="sm">前回と同じ</span>'
    pct = d / prev["price"] * 100
    if d < 0:
        return f'<span class="dn">▼{yen(-d)}（{pct:.1f}%）</span>'
    return f'<span class="up">▲{yen(d)}（+{pct:.1f}%）</span>'


def keyword(d):
    return f'{d["brand"]} {d["key"]} {d["name"]} {d["cat"]}'


def section(items, at, prev_at, qoo_at=None):
    by_save = sorted(items, key=lambda d: (-d["save"], d["rank_now"]["rank"]))
    top = [d for d in by_save if d["save"] > 0][:3]
    drops = [d for d in items if d["drop"] > 0]
    cards = "".join(
        f'<div class="bs-card" data-bs="{E(keyword(d))}" data-cat="{d["cat"]}"><div class="k">売れ筋 {d["rank_now"]["rank"]}位・{d["cat"]}</div>'
        f'<div class="n"><a href="/glow_item_{d["slug"]}.html">{E(d["brand"])} {E(d["name"])}</a></div>'
        f'<div class="big">{yen(d["best"]["price"])}</div>'
        f'<div class="sv">{E(d["best"]["media"])}・売れ筋の店（{yen(d["rank_now"]["price"])}）より<span class="save">{yen(d["save"])}安い</span></div>'
        f'{btn(d["best"])} {amazon_btn(d)}</div>' for d in top)
    if drops:
        drop_html = "<ul>" + "".join(
            f'<li><a href="/glow_item_{d["slug"]}.html">{E(d["brand"])} {E(d["name"])}</a>：'
            f'楽天市場 {yen(d["prev_price"])} → <strong>{yen(d["prev_price"] - d["drop"])}</strong>（{yen(d["drop"])}値下がり）</li>' for d in drops) + "</ul>"
    else:
        drop_html = f'<p>{jdt(prev_at) + "の記録から" if prev_at else "前回の記録から"}値下がりした品はありませんでした。</p>'
    def cell(c, label, prev):
        if not c:
            return f'<td data-l="{label}" class="num"><span class="sm">見つかりませんでした</span></td>'
        ship = "送料込み" if c["incl"] else "送料別"
        return (f'<td data-l="{label}" class="num"><strong>{yen(c["price"])}</strong><span class="sm">{ship}</span>'
                f'{chg(c, prev)}{btn(c)}</td>')
    trs = "".join(
        f'<tr data-bs="{E(keyword(d))}" data-cat="{d["cat"]}">'
        f'<td data-l="商品"><a href="/glow_item_{d["slug"]}.html"><strong>{E(d["brand"])}</strong><br>{E(d["name"])}</a>'
        f'<span class="sm">{d["cat"]}・売れ筋 {d["rank_now"]["rank"]}位</span>'
        f'<span class="sm">売れ筋の店 {yen(d["rank_now"]["price"])}（{E(d["rank_now"]["shop"])}）</span>'
        f'{f"<span class=save>最安は売れ筋の店より{yen(d["save"])}安い（{E(d["best"]["media"])}）</span>" if d["save"] > 0 else "<span class=sm>売れ筋の店がいちばん安い</span>"}</td>'
        + cell(d["r_now"], "楽天市場（送料込みの最安）", d["r_prev"])
        + cell(d["qoo10"], "Qoo10", d["q_prev"])
        + f'<td data-l="Amazon" class="num"><span class="sm">値段は規約により載せていません</span>{amazon_btn(d)}</td></tr>'
        for d in by_save)
    catbtn = '<button type="button" data-c="" aria-pressed="true">すべて</button>' + "".join(
        f'<button type="button" data-c="{c}" aria-pressed="false">{c}</button>' for c in CATS)
    return f"""<!--BESTSELLERS-->
{CSS}<h2 id="bestsellers">楽天スキンケア売れ筋の値段帳（楽天市場・Qoo10）</h2>
<p class="sm">楽天市場 {jdt(at)}時点{f"・Qoo10 {jdt(qoo_at)}時点" if qoo_at else ""}・送料込み・クーポンとポイントは含めていません。</p>
<div class="bs-tools"><input id="bs-q" type="search" placeholder="商品名で探す（例：レチノ、クレンジング）" aria-label="商品名で探す"><div class="bs-cats">{catbtn}</div></div>
<h3>今日いちばん得な{len(top)}品</h3>
<div class="bs-top">{cards}</div>
<h3>前回から値下がりした品</h3>
{drop_html}
<h3>売れ筋の一覧（楽天市場・Qoo10・Amazon）</h3>\n<p class="sm">並びは「いちばん安い店が、売れ筋の店よりいくら安いか」の大きい順です。▼は前回の記録から下がった額と率、▲は上がった額と率です。</p>
<table class="bstbl"><thead><tr><th>商品</th><th class="num">楽天市場</th><th class="num">Qoo10</th><th class="num">Amazon</th></tr></thead>
<tbody>{trs}</tbody></table>
<p id="bs-empty" class="bs-empty">見つかりませんでした。別の言葉で探してみてください。</p>
<p class="sm">商品名を押すと、その商品の値段の記録と、送料別の店も含めた比較が見られます。Amazonは規約により値段を載せていません。「Amazonで見る」から、Amazonの商品ページで値段をその場で確かめられます。</p>
<h3>売れ筋の値段帳の調べ方</h3>
{HOWTO}
{JS}
<!--/BESTSELLERS-->"""


def item_page(d, items, src):
    head = src.split("<header", 1)[0]
    hdr = "<header" + src.split("<header", 1)[1].split("</header>", 1)[0] + "</header>"
    hdr = hdr.replace(' aria-current="page"', "")
    foot = "<footer" + src.split("<footer", 1)[1]
    best, rk, body = d["best"], d["rank_now"], d["body"]
    full = f'{d["brand"]} {d["name"]}'
    at = datetime.strptime(d["at"], "%Y-%m-%d %H:%M")
    title = f'{full}の最安値は？売れ筋の店と楽天の他店を送料込みで毎日比較 - Glow'
    desc = (f'{full}の値段を楽天市場で毎日2回記録しています。{jdt(at)}時点の送料込みの最安は{yen(best["price"])}'
            f'（{best["shop"]}）。売れ筋ランキングに出ている店（{rk["shop"]}）は{yen(rk["price"])}。')
    url = f'{BASE}glow_item_{d["slug"]}.html'
    head = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + E(desc), head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + E(title), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + E(desc), head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head = head.replace("</head>", CSS + "</head>")

    def row(c, label, is_best=False):
        ship = "送料込み" if c["incl"] else "送料は店と地域によって異なります"
        tag = '<span class="tag">送料込みで最安</span>' if is_best else ""
        return (f'<div class="buyrow{" best" if is_best else ""}"><div><div class="m">{E(label)}{tag}</div>'
                f'<div class="s">{E(c["shop"]) + "・" if c["media"] != "Qoo10" else ""}{ship}{f"・レビュー{c['rev']}件" if c["media"] == "Qoo10" else ""}</div></div><div class="p">{yen(c["price"])}</div>{btn(c)}</div>')

    rows = [row(best, "売れ筋ランキングに出ている店" if best is rk else f'{best["media"]}で送料込みの最安', True)]
    if rk is not best:
        rows.append(row(rk, "売れ筋ランキングに出ている店"))
    if body and body is not rk and body is not best and body["price"] < best["price"]:
        rows.append(row(body, f'{body["media"]}で本体の値段がいちばん安い店'))
    q = d.get("qoo10")
    if q and q is not best and q is not body:
        rows.append(row(q, "Qoo10"))
    rows.append('<div class="buyrow"><div><div class="m">Amazon</div><div class="s">Amazonの商品ページが開きます。値段はAmazonの画面で確かめてください（規約により当サイトには載せていません）</div></div>'
                f'<div class="p"></div>{amazon_btn(d)}</div>')
    if d["save"] > 0:
        verdict = f'売れ筋ランキングに出ている店（{E(rk["shop"])}）の{yen(rk["price"])}より<strong>{yen(d["save"])}安い</strong>店があります。'
    else:
        verdict = f'売れ筋ランキングに出ている店（{E(rk["shop"])}）が、送料込みでいちばん安い値段でした。'
    h = d["hist"]
    if len(h) >= 14:
        hist_block = ('<h2>値段の記録（楽天市場・送料込みの最安）</h2><table class="bstbl"><thead><tr><th>日時</th><th class="num">値段</th><th>店</th></tr></thead><tbody>'
                      + "".join(f'<tr><td data-l="日時">{jdt(datetime.strptime(x["at"], "%Y-%m-%d %H:%M"))}</td><td data-l="値段" class="num">{yen(x["price"])}</td><td data-l="店">{E(x["shop"])}</td></tr>' for x in h)
                      + "</tbody></table>")
    else:
        hist_block = (f'<h2>値段の記録</h2><p>この商品の値段の記録は{jdt(datetime.strptime(h[0]["at"], "%Y-%m-%d %H:%M"))}から始めました。'
                      '1週間分たまったら、ここに値段の動き（今が安い時期かどうか）を載せます。</p>')
    rk_at = datetime.strptime(d["rank_at"], "%Y-%m-%d %H:%M")
    others = "".join(f'<li><a href="/glow_item_{o["slug"]}.html">{E(o["brand"])} {E(o["name"])}</a></li>'
                     for o in items if o["slug"] != d["slug"])
    main = f"""{hdr}
<main class="wrap">
<p class="pr-inline">※本ページには広告（アフィリエイトリンク）を含みます。報酬の有無は掲載順位に影響していません。</p>
<p class="crumb"><a href="/glow_prices.html#bestsellers">売れ筋の値段帳</a> ＞ {E(d["brand"])}</p>
<h1>{E(full)}は、どこで買うと安いか</h1>
<p class="lead">楽天市場のスキンケア売れ筋で上位に居続けている商品です。<strong>楽天市場全体の値段を毎日2回、Qoo10の値段もあわせて、送料込みで記録</strong>しています。{E(d["about"])}</p>
<div class="verdict">
<div class="s">{jdt(at)}時点・送料込みの最安</div>
<div class="big">{yen(best["price"])}</div>
<div class="sub">{verdict}</div>
<div class="sub">1{d["unit"]}あたり {best["price"] / d["amount"]:.0f}円（{d["amount"]}{d["unit"]}）</div>
</div>
<h2>今日の値段</h2>
<div class="buybox">{''.join(rows)}</div>
<p class="sm">※クーポン・ポイントは含めていません。値段と在庫は変わります。買う前に必ずリンク先の表示を確かめてください。</p>
<h2>売れ筋の記録</h2>
<ul class="facts">
<li>今日の順位<b>{rk["rank"]}位</b>楽天スキンケア売れ筋（{rk_at.month}月{rk_at.day}日）</li>
<li>10/10〜11/1の売れ筋8回<b>中央{d["median"]:g}位</b>8回すべてで上位に出ていた</li>
<li>レビュー<b>{rk["reviews"]:,}件</b>平均{rk["avg"]:.2f}（{E(rk["shop"])}）</li>
</ul>
{hist_block}
<h2>このページの調べ方</h2>
{HOWTO}
<h2>ほかの売れ筋の値段</h2>
<ul>{others}</ul>
<p><a href="/glow_prices.html#bestsellers">売れ筋の値段帳（一覧）へ</a></p>
</main>
"""
    return head + main + foot


def main(argv):
    ranks = [a for a in argv if "rakuten_rank_" in a]
    pops = [a for a in argv if "popular_rakuten_" in a]
    qf = [a for a in argv if "qoo10_" in a and a.endswith(".json")]
    qoo = json.load(open(sorted(qf)[-1], encoding="utf-8")) if qf else None
    qoo_prev = json.load(open(sorted(qf)[-2], encoding="utf-8")) if len(qf) >= 2 else None
    qoo_at = datetime.strptime(qoo["at"], "%Y-%m-%d %H:%M") if qoo else None
    if not ranks or not pops:
        raise SystemExit(__doc__)
    items, at, prev_at = collect(ranks, pops, qoo, qoo_prev)
    src = open(PAGE, encoding="utf-8").read()
    if src.count("<!--BESTSELLERS-->") != 1 or src.count("<!--/BESTSELLERS-->") != 1:
        raise SystemExit("⛔️glow_prices.html に印がありません（build_prices_page.py を先に流すこと）")
    new = re.sub(r"<!--BESTSELLERS-->.*?<!--/BESTSELLERS-->", lambda m: section(items, at, prev_at, qoo_at), src, flags=re.S)
    open(PAGE, "w", encoding="utf-8").write(new)
    for d in items:
        open(f'glow_item_{d["slug"]}.html', "w", encoding="utf-8").write(item_page(d, items, new))
    json.dump(dict(at=at.strftime("%Y-%m-%d %H:%M"), items=[{k: v for k, v in d.items() if k != "about"} for d in items]),
              open("bestsellers.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for d in sorted(items, key=lambda d: -d["save"]):
        print(f'{d["slug"]:28} 売れ筋{d["rank_now"]["rank"]:>3}位 {d["rank_now"]["price"]:>6} → 最安 {d["best"]["price"]:>6}'
              f' {d["best"]["media"]:4} 差{d["save"]:>6}  前回差{d["drop"]:>5}  記録{len(d["hist"])}点')


if __name__ == "__main__":
    main(sys.argv[1:])
