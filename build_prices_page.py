# -*- coding: utf-8 -*-
"""prices.json から glow_prices.html（静的・クロールできる価格ページ）を組む。

⭐️目的：このサイト唯一の独自データ（送料込み総額の週次記録）を、
   ★JavaScript無しで読める本文テキストにする。
⛔️Amazonの価格は書かない（アソシエイト参加要件2条(b)）。prices.json は楽天とYahoo!のみ。
⛔️ブランド表示名は glow_skin_diagnosis.html のブランドDBから機械的に引く（手打ちゼロ）。
⛔️アフィリエイトURLは prices.json から機械コピーする（規則[49]）。
"""
import json, re, html, datetime, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
PRICES = os.path.join(HERE, "prices.json")
DIAG = os.path.join(HERE, "glow_skin_diagnosis.html")
OUT = os.path.join(HERE, "glow_prices.html")
URL = "https://glow.stats-log.net/glow_prices.html"

# ── カテゴリ（編集判断。商品名から振り分けている）
CAT = {
    "化粧水・ローション": ["muji", "muji_age", "muji_clear", "pola", "curel", "clinique",
                     "anua", "etvos", "chifure", "hadalabo", "minon", "transino",
                     "arouge", "astalift", "adryS", "melanocc"],
    "美容液・エッセンス": ["cosrx", "theordinary", "sofina_ip", "obagi", "iope",
                     "decorte", "sulwhasoo"],
    "日焼け止め・UV": ["lrp", "biore"],
    "保湿乳液・リップ": ["cerave", "laneige"],
}


def brands(keys):
    """診断ページのブランドDBから表示名と販売元を引く。"""
    h = open(DIAG, encoding="utf-8").read()
    out = {}
    for k in keys:
        m = re.search(r'"' + re.escape(k) + r'"\s*:\s*\{"name":"(.*?)","region":"(.*?)","maker":"(.*?)"', h)
        if not m:
            raise SystemExit(f"⛔️ブランド名が引けない: {k}")
        out[k] = {"name": m.group(1), "region": m.group(2), "maker": m.group(3)}
    return out


def esc(s):
    return html.escape(str(s), quote=True)


def yen(n):
    return f"{n:,}円"


def main():
    d = json.load(open(PRICES, encoding="utf-8"))
    items = d["items"]
    B = brands(list(items))

    gen = datetime.datetime.fromisoformat(d["generated_at"])
    asof = f"{gen.year}年{gen.month}月{gen.day}日"
    asof_iso = gen.strftime("%Y-%m-%d")

    # ── 集計
    rakuten = [k for k, v in items.items() if v["live"]["media"] == "楽天"]
    yahoo = [k for k, v in items.items() if v["live"]["media"] != "楽天"]
    # moved … 価格・店・媒体・土台のいずれかが先週と変わった品
    # swapped … そのうち、安い店か媒体そのものが入れ替わった品
    # gated … 先週と土台（送料込み／送料別）が違い、差を出せない品
    moved, swapped, gated = [], [], []
    for k, v in items.items():
        l = v["live"]
        pn = l.get("prev_note", "")
        if pn.startswith("先週は送料"):
            gated.append(k)
        if pn:
            swapped.append(k)
        if pn or l["total"] != l.get("prev"):
            moved.append(k)
    cheapest = min(items, key=lambda k: items[k]["live"]["total"])
    dearest = max(items, key=lambda k: items[k]["live"]["total"])

    covered = sum(len(v) for v in CAT.values())
    if covered != len(items):
        raise SystemExit(f"⛔️カテゴリの振り分けが {covered} 件、データは {len(items)} 件")

    # ── 本文を組む
    P = []
    A = P.append

    A(f'<h1>スキンケア{len(items)}品は、いまどこが安いのか</h1>')
    A('<p class="lead">このページは、国内外のスキンケア'
      f'{len(items)}品について、<strong>楽天市場とYahoo!ショッピングで「送料込みの総額」が'
      'いちばん安かった店</strong>を、毎週ひとつずつ記録したものです。'
      f'調査は<strong>{asof}</strong>。先週の同じ時間帯に記録した値も並べているので、'
      '上がったのか下がったのか、そのまま読めます。</p>')
    A('<p class="pr-inline">※本ページには広告（アフィリエイトリンク）を含みます。'
      '報酬の有無は掲載順位に影響していません。</p>')

    A('<div class="glance"><div><span class="g-n">'
      f'{len(items)}</span><span class="g-l">記録した品目</span></div>'
      f'<div><span class="g-n">{len(rakuten)} / {len(yahoo)}</span>'
      '<span class="g-l">楽天 / Yahoo!</span></div>'
      f'<div><span class="g-n">{len(moved)}</span><span class="g-l">先週から動いた品</span></div>'
      f'<div><span class="g-n">{yen(items[cheapest]["live"]["total"])}</span>'
      '<span class="g-l">いちばん安い品</span></div></div>')

    # ── 調べ方
    A('<h2 id="howto">このページの調べ方</h2>')
    A('<ul class="howto">')
    A('<li><strong>本体価格ではなく、送料込みの総額で比べています。</strong>'
      '本体が安くても送料で逆転することがあるため、支払う金額そのもので並べました。'
      '送料が商品ページで確定できないものは、その旨を品目ごとに書いています。</li>')
    A('<li><strong>同じ商品名・同じ容量に限って比べています。</strong>'
      '容量違いやセット品は別物として扱い、突き合わせの対象から外しました。</li>')
    A('<li><strong>店は毎週入れ替わります。</strong>'
      f'今週は{len(items)}品のうち{len(moved)}品で、価格・店・媒体のいずれかが先週と変わりました。'
      f'そのうち{len(swapped)}品は、いちばん安い店そのものか、媒体が入れ替わっています。'
      '「どこが安いか」は商品ではなく店の都合で動く、というのがこの記録でいちばん繰り返し出てくる事実です。</li>')
    A('<li><strong>価格と在庫は変動します。</strong>'
      'ここに書いてあるのは調査時点の数字です。買うときは必ずリンク先の表示をご確認ください。</li>')
    A('</ul>')

    # ── 今週動いたもの
    A('<h2 id="moved">今週、先週から動いたもの</h2>')
    if not moved:
        A('<p>今週は、価格・媒体・店のいずれも先週から変わった品目がありませんでした。</p>')
    else:
        A(f'<p>{len(items)}品のうち{len(moved)}品が動きました。残り{len(items) - len(moved)}品は'
          '先週とまったく同じ金額です。</p>')
        A('<table class="movetbl"><thead><tr><th>品目</th><th>先週</th><th>今週</th>'
          '<th>差</th><th>何が変わったか</th></tr></thead><tbody>')
        for k in sorted(moved, key=lambda k: -abs(items[k]["live"]["total"] - items[k]["live"]["prev"])):
            l = items[k]["live"]
            diff = l["total"] - l["prev"]
            if l.get("prev_note", "").startswith("先週は送料"):
                sign = '<span class="d-na">比較できません</span>'
            elif diff > 0:
                sign = f'<span class="d-up">＋{diff:,}円</span>'
            elif diff < 0:
                sign = f'<span class="d-dn">−{abs(diff):,}円</span>'
            else:
                sign = '<span class="d-eq">同額</span>'
            A(f'<tr><td data-l="品目"><strong>{esc(B[k]["name"])}</strong><br>'
              f'<span class="pname">{esc(l["product"])}</span></td>'
              f'<td data-l="先週">{yen(l["prev"])}</td>'
              f'<td data-l="今週"><strong>{yen(l["total"])}</strong></td>'
              f'<td data-l="差">{sign}</td>'
              f'<td data-l="何が変わったか">{esc(l.get("prev_note") or "価格だけが動きました")}</td></tr>')
        A('</tbody></table>')
        if gated:
            g = gated[0]
            A('<p class="caveat"><strong>比べられないものは、比べていません。</strong>'
              f'{esc(B[g]["name"])}は、先週が送料別の価格、今週が送料込みの総額です。'
              '土台が違うので、差を出さずに両方の数字だけを載せています。'
              '安くなった・高くなったと書けるのは、同じ土台どうしのときだけです。</p>')

    # ── 全品
    A(f'<h2 id="list">{len(items)}品の記録（{asof} 調べ）</h2>')
    for cat, keys in CAT.items():
        keys = sorted(keys, key=lambda k: items[k]["live"]["total"])
        A(f'<h3>{esc(cat)}（{len(keys)}品）</h3>')
        A('<table class="ptbl"><thead><tr><th>ブランド・商品</th><th>媒体・店</th>'
          '<th>送料込みの総額</th><th>先週</th></tr></thead><tbody>')
        for k in keys:
            l = items[k]["live"]
            b = B[k]
            note = f'<span class="note">{esc(l["note"])}</span>' if l.get("note") else ""
            link = ""
            if l.get("url"):
                link = (f'<a class="buy" href="{esc(l["url"])}" target="_blank" '
                        f'rel="sponsored nofollow noopener">楽天市場で見る</a>')
            diff = l["total"] - l["prev"]
            if l.get("prev_note", "").startswith("先週は送料"):
                pv = f'{yen(l["prev"])}<br><span class="d-na">土台が違うため比較なし</span>'
            elif diff == 0:
                pv = f'{yen(l["prev"])}<br><span class="d-eq">同額</span>'
            elif diff > 0:
                pv = f'{yen(l["prev"])}<br><span class="d-up">＋{diff:,}円</span>'
            else:
                pv = f'{yen(l["prev"])}<br><span class="d-dn">−{abs(diff):,}円</span>'
            # 販売元がブランド名に含まれているときは重ねて出さない
            mk = "" if b["maker"] in b["name"] else f'<span class="maker">{esc(b["maker"])}</span>'
            A(f'<tr><td data-l="ブランド・商品"><strong>{esc(b["name"])}</strong> {mk}<br>'
              f'<span class="pname">{esc(l["product"])}</span> {note}</td>'
              f'<td data-l="媒体・店">{esc(l["media"])}<br>'
              f'<span class="shop">{esc(l["shop"])}</span><br>'
              f'<span class="at">{esc(l["at_label"])} 時点</span></td>'
              f'<td class="total" data-l="送料込みの総額"><strong>{yen(l["total"])}</strong><br>{link}</td>'
              f'<td data-l="先週">{pv}</td></tr>')
        A('</tbody></table>')

    # ── FAQ
    FAQ = [
        ("なぜ本体価格ではなく、送料込みの総額で比べているのですか？",
         "支払う金額が変わるからです。本体が数百円安くても、送料を足すと別の店のほうが安くなることがあります。"
         "このページは「いま、いくら払えば届くか」を知るための記録なので、総額でそろえています。"),
        ("安い店が毎週変わるのはなぜですか？",
         "クーポン・ポイント施策・在庫の入れ替わりで、同じ商品を出している店の価格は週単位で動きます。"
         f"今週も{len(items)}品のうち{len(moved)}品で金額か店が動き、そのうち{len(swapped)}品は"
         "いちばん安い店そのものか媒体が入れ替わりました。"
         "だから「この店が安い」ではなく「この週はこの店だった」という記録の形にしています。"),
        ("Amazonの価格は載せていないのですか？",
         "このページで比べているのは楽天市場とYahoo!ショッピングの2媒体です。"),
        ("価格はいつ更新されますか？",
         "週に1回、同じ曜日・同じ時間帯に記録しています。先週と同じ条件で測るためです。"
         f"最新の記録は{asof}時点のものです。"),
        ("どの商品を選べばいいかわかりません。",
         "肌タイプと悩みから絞るほうが先です。4問・約30秒の無料診断と、肌タイプ別の解説ページを用意しています。"),
    ]
    A('<h2 id="faq">よくある質問</h2><dl class="faq">')
    for q, a in FAQ:
        A(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>')
    A('</dl>')

    # ── 導線
    A('<h2 id="next">肌タイプから選ぶ</h2>')
    A('<p>価格だけで選ぶと、合わないものを安く買うことになります。'
      'まず自分の肌タイプを決めてから、このページの価格を見てください。</p>')
    A('<p class="cta"><a href="/glow_skin_diagnosis.html">無料の肌診断（4問・約30秒）を受ける →</a></p>')
    A('<ul class="typelinks">'
      '<li><a href="/glow_type_dry.html">乾燥肌の見分け方と化粧水の選び方</a></li>'
      '<li><a href="/glow_type_oily.html">脂性肌の見分け方と化粧水の選び方</a></li>'
      '<li><a href="/glow_type_innerdry.html">インナードライの見分け方と化粧水の選び方</a></li>'
      '<li><a href="/glow_type_combo.html">混合肌の見分け方と化粧水の選び方</a></li>'
      '<li><a href="/glow_type_sensitive.html">敏感肌の見分け方と化粧水の選び方</a></li>'
      '<li><a href="/glow_type_dry_sensitive.html">乾燥性敏感肌とは？見分け方と選び方</a></li>'
      '<li><a href="/glow_type_aging.html">エイジングケアの始めどきと化粧水の選び方</a></li>'
      '</ul>')

    body = "\n".join(P)

    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    }, ensure_ascii=False, indent=1)

    page_ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "name": f"スキンケア{len(items)}品の価格記録",
        "description": f"楽天市場とYahoo!ショッピングで送料込みの総額がいちばん安い店を、スキンケア{len(items)}品について毎週記録しています。",
        "inLanguage": "ja", "datePublished": "2026-10-26", "dateModified": asof_iso,
        "isAccessibleForFree": True,
        "publisher": {"@type": "Organization", "name": "Glow", "url": "https://glow.stats-log.net/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
    }, ensure_ascii=False, indent=1)

    bc_ld = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://glow.stats-log.net/"},
            {"@type": "ListItem", "position": 2, "name": "価格記録"},
        ]
    }, ensure_ascii=False, indent=1)

    # 既存ページから共通の枠（GA4・CSS・ヘッダ・フッタ）を機械コピーする
    src = open(os.path.join(HERE, "glow_type_dry.html"), encoding="utf-8").read()
    ga = re.search(r'(?s)<link rel="icon".*?</script>\n', src).group(0)
    gcss = re.search(r'(?s)<style id="glow-global-css">.*?</style>', src).group(0)
    nav = re.search(r'(?s)<header class="gnav-bar">.*?</header>', src).group(0)
    # このページ自身のナビ項目には、サイトの慣例どおり aria-current を付ける
    nav = nav.replace('<a href="/glow_prices.html">',
                      '<a href="/glow_prices.html" aria-current="page">')
    foot = re.search(r'(?s)<footer class="gfoot">.*?</footer>', src).group(0)
    fonts = ('<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;700'
             '&family=Zen+Kaku+Gothic+New:wght@300;400;700&display=swap" rel="stylesheet">')

    title = f"スキンケア{len(items)}品の価格を毎週くらべた記録｜楽天・Yahoo!を送料込みの総額で - Glow"
    desc = (f"国内外のスキンケア{len(items)}品について、楽天市場とYahoo!ショッピングで"
            f"「送料込みの総額」がいちばん安い店を毎週記録しています。{asof}調べ。"
            "先週との差、安い店の入れ替わり、同じ商品名・同じ容量にそろえた比べ方まで掲載。")

    css = """
<style>
/* 共通CSSの全幅指定は 100vw を使っており、縦スクロールバーの分だけ横にはみ出す。
   このページでは body 直下の子要素として width:auto で全幅にする（はみ出しゼロ）。 */
.gnav-bar,.gfoot{margin-left:0;margin-right:0;width:auto}
:root{--ink:#2a2724;--sub:#6d675f;--line:#ece7e2;--accent:#c0392b;--up:#b03a2e;--dn:#1e7a4b;--bg:#fbf9f7}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Zen Kaku Gothic New',-apple-system,BlinkMacSystemFont,'Hiragino Sans',sans-serif;line-height:1.85;font-size:16px}
.wrap{max-width:860px;margin:0 auto;padding:0 16px 64px}
h1{font-family:'Shippori Mincho',serif;font-size:27px;line-height:1.5;margin:28px 0 14px;letter-spacing:.01em}
h2{font-family:'Shippori Mincho',serif;font-size:22px;margin:44px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--line)}
h3{font-size:17px;margin:30px 0 8px;color:var(--accent)}
.lead{font-size:16.5px}
.pr-inline{font-size:13px;color:var(--sub);background:#f4f0ec;border-radius:7px;padding:9px 12px;margin:14px 0 0}
.glance{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 6px}
.glance>div{flex:1 1 150px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.g-n{display:block;font-family:'Shippori Mincho',serif;font-size:22px;font-weight:700}
.g-l{display:block;font-size:12.5px;color:var(--sub);margin-top:2px}
ul.howto{padding-left:1.15em}
ul.howto li{margin:11px 0}
table{width:100%;border-collapse:collapse;margin:14px 0 8px;background:#fff;font-size:14.5px}
th,td{border:1px solid var(--line);padding:10px 11px;text-align:left;vertical-align:top}
th{background:#f4f0ec;font-weight:700;font-size:13.5px;white-space:nowrap}
td.total{white-space:nowrap}
.pname{color:var(--sub);font-size:13px}
.maker{color:var(--sub);font-size:12px}
.shop{font-size:13px}
.at{color:var(--sub);font-size:12px}
.note{display:inline-block;background:#fdf3e3;color:#8a6417;border-radius:5px;padding:1px 7px;font-size:12px;margin-left:3px}
.d-up{color:var(--up);font-size:13px;font-weight:700}
.d-dn{color:var(--dn);font-size:13px;font-weight:700}
.d-eq{color:var(--sub);font-size:13px}
.d-na{color:#8a6417;font-size:12.5px}
a.buy{display:inline-block;margin-top:6px;font-size:12.5px;color:var(--accent);text-decoration:none;border:1px solid var(--accent);border-radius:999px;padding:2px 10px}
a.buy:hover{background:var(--accent);color:#fff}
.caveat{background:#fdf3e3;border-left:4px solid #d8a93a;padding:12px 14px;border-radius:0 8px 8px 0;font-size:14.5px}
dl.faq dt{font-weight:700;margin:18px 0 5px}
dl.faq dd{margin:0;color:#3a3630}
p.cta a{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;border-radius:999px;padding:11px 22px;font-weight:700}
ul.typelinks{padding-left:1.15em}
ul.typelinks li{margin:6px 0}
ul.typelinks a,p.cta+ul a{color:var(--accent)}
main.wrap a{color:var(--accent)}
main.wrap a.buy{color:var(--accent)}
@media(max-width:640px){
 h1{font-size:22px}h2{font-size:19px}
 table,thead,tbody{display:block;width:100%;box-sizing:border-box}
 thead{display:none}
 table{border:0;background:transparent}
 tr{display:grid;background:#fff;border:1px solid var(--line);border-radius:10px;
    margin:0 0 10px;padding:2px 0;column-gap:0}
 td{display:block;border:0;border-bottom:1px dashed var(--line);padding:8px 12px}
 td:before{content:attr(data-l);display:block;font-size:11px;color:var(--sub);margin-bottom:1px}
 .ptbl tr{grid-template-columns:1fr 1fr;
          grid-template-areas:"name name" "total prev" "shop shop"}
 .ptbl td:nth-child(1){grid-area:name}
 .ptbl td:nth-child(2){grid-area:shop;border-bottom:0}
 .ptbl td:nth-child(3){grid-area:total;border-right:1px dashed var(--line)}
 .ptbl td:nth-child(4){grid-area:prev}
 .movetbl tr{grid-template-columns:1fr 1fr;
             grid-template-areas:"name name" "prev now" "diff diff" "why why"}
 .movetbl td:nth-child(1){grid-area:name}
 .movetbl td:nth-child(2){grid-area:prev;border-right:1px dashed var(--line)}
 .movetbl td:nth-child(3){grid-area:now}
 .movetbl td:nth-child(4){grid-area:diff}
 .movetbl td:nth-child(5){grid-area:why;border-bottom:0}
}
</style>"""

    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
{ga}<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="robots" content="index,follow" />
<link rel="canonical" href="{URL}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{URL}" />
<meta property="og:image" content="https://glow.stats-log.net/ogp_prices.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:image" content="https://glow.stats-log.net/ogp_prices.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@stats_log_net" />
{fonts}
<script type="application/ld+json">
{page_ld}
</script>
<script type="application/ld+json">
{bc_ld}
</script>
<script type="application/ld+json">
{faq_ld}
</script>
{gcss}
{css}
</head>
<body>
{nav}
<main class="wrap">
{body}
<p class="pr-inline">価格・在庫は変動します。掲載しているのは各品目に記載した調査日時点の表示です。
購入前に必ずリンク先の最新の表示をご確認ください。</p>
</main>
{foot}
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(doc)

    # ── 検算
    vis = re.sub(r"(?is)<script.*?</script>", "", doc)
    vis = re.sub(r"(?is)<style.*?</style>", "", vis)
    vis = re.sub(r"(?s)<[^>]+>", " ", vis)
    vis = re.sub(r"\s+", " ", vis).strip()
    print(f"★出力 {OUT}")
    print(f"★HTML {len(doc):,} バイト／★スクリプトを除いた本文 {len(vis):,} 字")
    print(f"★本文中の『円』{vis.count('円')} 回／★商品名 {sum(1 for k in items if items[k]['live']['product'] in vis)}/{len(items)} 件が本文に出ている")
    print(f"★アフィリンク {doc.count('hb.afl.rakuten.co.jp')} 本（prices.jsonのurl {len(rakuten)} 本と一致：{doc.count('hb.afl.rakuten.co.jp')==len(rakuten)}）")
    print(f"★rel未設定のアフィリンク {len(re.findall(r'hb.afl.rakuten', doc)) - len(re.findall(r'rel=.sponsored nofollow noopener', doc))} 本")
    print(f"★『Amazon』の出現 {vis.count('Amazon')} 回（★価格は書いていない：{'円' not in vis.split('Amazon')[1][:40] if 'Amazon' in vis else True}）")
    print(f"★動いた品 {len(moved)} 件（うち店・媒体が入れ替わった品 {len(swapped)} 件）／"
          f"★土台が違い比較を見送った品 {len(gated)} 件")
    same = [k for k in items if k not in moved]
    print(f"★先週と同額のまま {len(same)} 件（{len(moved)}＋{len(same)}＝{len(items)}："
          f"{len(moved) + len(same) == len(items)}）")
    print(f"★いちばん安い {B[cheapest]['name']} {yen(items[cheapest]['live']['total'])}／"
          f"★いちばん高い {B[dearest]['name']} {yen(items[dearest]['live']['total'])}")


if __name__ == "__main__":
    main()
