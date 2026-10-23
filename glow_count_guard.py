#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブランド数の直書きを見つけるガード（2026-10-23 追加）

なぜ要るか
  2026-09-18 に肌タイプ別ページを5枚足したとき、data-bc="n" の印は付けたのに
  sync_brand_count.py の TARGETS に足さなかった。印があるので自動で直ると
  思い込んだまま、10箇所が「132ブランド」で5週間放置された。
  glow_sale_amazon_prime.html は印すら無く「124ブランド」のままだった。
  --check は TARGETS しか見ないので「差分0」と答え続けた。

  このガードは TARGETS ではなく **リポジトリの全HTML** を見る。
  新しいページを作って数字を手で書いた瞬間に落ちる。

判定のルール
  ページ中の「◯◯◯ブランド」は、次のどれかでなければ FAIL。
    1. <span data-bc="n">◯◯◯</span>ブランド   … 自動同期される。常に正しい
    2. いまの正しい件数と同じ数字            … 手で書く場所（NEWチップ・📊今回の更新内容）
    3. data-bc-ignore を付けた要素の中       … 更新履歴。過去の記録なので触らない

  2 が FAIL になるのは「前回の件数のまま更新し忘れた」とき。それが見つけたい事故。

使い方
  python3 glow_count_guard.py            # FAIL があれば終了コード 1
  python3 glow_count_guard.py --verbose  # 通った箇所も全部出す
"""
import re
import sys
import pathlib

SRC = "glow_skin_diagnosis.html"
# 数字と「ブランド」の間にタグの閉じが挟まる形（<span data-bc="n">142</span>ブランド）も拾う
NUM_RE = re.compile(r'(\d{2,4})\s*(?:</span>)?\s*ブランド')


def current_count(root: pathlib.Path) -> int:
    """唯一の正解＝診断ページの DB.profiles のキー数"""
    s = (root / SRC).read_text(encoding="utf-8")
    i = s.find("profiles: {")
    if i < 0:
        sys.exit("⛔️ profiles が見つからない。中止")
    j = s.find("{", i)
    d = 0
    for k in range(j, len(s)):
        if s[k] == "{":
            d += 1
        elif s[k] == "}":
            d -= 1
            if d == 0:
                import json
                return len(json.loads(s[j:k + 1]))
    sys.exit("⛔️ profiles の終わりが見つからない。中止")


def ignored_spans(text: str):
    """data-bc-ignore を付けた要素の範囲（開始位置, 終了位置）を返す"""
    out = []
    for m in re.finditer(r'<(\w+)[^>]*\bdata-bc-ignore\b[^>]*>', text):
        tag = m.group(1)
        depth = 0
        pos = m.start()
        for t in re.finditer(r'<(/?)%s\b[^>]*>' % tag, text[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                out.append((pos, m.start() + t.end()))
                break
        else:
            out.append((pos, len(text)))
    return out


def main() -> int:
    verbose = "--verbose" in sys.argv
    root = pathlib.Path(__file__).resolve().parent
    n = current_count(root)
    print(f"いまの正しい件数 = {n}（{SRC} の DB.profiles を数えた値）")
    print("")

    fails = []
    for path in sorted(root.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        skips = ignored_spans(text)
        for m in NUM_RE.finditer(text):
            if any(a <= m.start() < b for a, b in skips):
                continue  # 更新履歴
            before = text[max(0, m.start() - 24):m.start()]
            auto = before.rstrip().endswith('data-bc="n">')
            ok = int(m.group(1)) == n
            if ok:
                if verbose:
                    kind = "自動同期" if auto else "手書きだが現在値と一致"
                    print(f"  OK   {path.name}: {kind}（{m.group(1)}）")
                continue
            line = text[:m.start()].count("\n") + 1
            ctx = text[max(0, m.start() - 55):m.end() + 12].replace("\n", " ")
            # 印があるのに値が古い＝ sync の TARGETS 漏れ。2026-09-18 の事故がこれ
            why = "印はあるが同期されていない（TARGETS漏れ）" if auto else "印が無く直書き"
            fails.append((path.name, line, m.group(1), why, ctx))

    if fails:
        print(f"★FAIL {len(fails)}箇所：利用者に古いブランド数が見えている")
        for name, line, num, why, ctx in fails:
            print(f"  {name}:{line}  「{num}ブランド」  {why}")
            print(f"       …{ctx}…")
        print("")
        print("直し方：")
        print("  印が無い        → その数字を <span data-bc=\"n\">…</span> で包む")
        print("  TARGETS漏れ     → sync_brand_count.py の TARGETS にそのファイルを足す")
        print("  同期していないだけ → python3 sync_brand_count.py を実行する")
        print("  過去の記録      → 囲む要素に data-bc-ignore を付ける")
        return 1

    print("PASS  ブランド数の直書きは無い（全HTMLを確認）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
