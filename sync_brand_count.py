#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブランド数・地域内訳・更新日を「1箇所」から全ページへ流し込む。

★唯一の正解の источник = glow_skin_diagnosis.html の DB.profiles
  - 件数        : profiles のキー数
  - 地域内訳    : profiles[*].region の集計
  - 更新日      : 更新履歴の最新の「YYYY年M月D日更新」

対象は HTML 内の <span data-bc="..."> のみ。
  data-bc="n"       -> 件数（例 128）
  data-bc="regions" -> 日本80・韓国21・アメリカ14・ヨーロッパ12・オーストラリア1
  data-bc="updated" -> 2026年9月11日

⛔️歯止め
  [1] 件数が 100 未満、または前回比 ±10 を超えたら中止（--force で解除）
  [2] profiles が読めなければ中止。ファイルは1文字も書き換えない
  [3] 置換対象が0件のファイルは触らない（mtime も変えない）
  [4] --check は書き換えずに差分の有無だけ返す（終了コード 1 = 要更新）
"""
import argparse, collections, datetime, json, re, sys, pathlib

SRC = "glow_skin_diagnosis.html"
TARGETS = ["index.html", "about.html", "glow_skin_diagnosis.html", "glow_type_dry.html"]

REGION_JA = {"JP": "日本", "KR": "韓国", "US": "アメリカ", "EU": "ヨーロッパ", "AU": "オーストラリア"}
REGION_ORDER = ["JP", "KR", "US", "EU", "AU"]


def read_profiles(root: pathlib.Path):
    s = (root / SRC).read_text(encoding="utf-8")
    i = s.find("profiles: {")
    if i < 0:
        sys.exit("⛔️ profiles が見つからない。中止（1文字も書き換えていない）")
    j = s.find("{", i)
    d = 0
    end = -1
    for k in range(j, len(s)):
        if s[k] == "{":
            d += 1
        elif s[k] == "}":
            d -= 1
            if d == 0:
                end = k + 1
                break
    if end < 0:
        sys.exit("⛔️ profiles の括弧が閉じていない。中止")
    try:
        p = json.loads(s[j:end])
    except Exception as e:
        sys.exit(f"⛔️ profiles を JSON として読めない: {e}。中止")

    cnt = collections.Counter()
    for v in p.values():
        m = re.search(r"([A-Z]{2})\s*$", v.get("region", ""))
        cnt[m.group(1) if m else "??"] += 1
    regions = "・".join(
        f"{REGION_JA.get(c, c)}{cnt[c]}" for c in REGION_ORDER if cnt.get(c)
    )
    extra = [c for c in cnt if c not in REGION_ORDER]
    if extra:
        sys.exit(f"⛔️ 未知の region: {extra}。REGION_JA に追記してから再実行")

    dates = re.findall(r"(\d{4})年(\d{1,2})月(\d{1,2})日更新", s)
    if not dates:
        sys.exit("⛔️ 更新履歴の日付が見つからない。中止")
    y, mo, da = max(dates, key=lambda t: (int(t[0]), int(t[1]), int(t[2])))
    return len(p), regions, f"{int(y)}年{int(mo)}月{int(da)}日"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="書き換えずに差分だけ見る")
    ap.add_argument("--force", action="store_true", help="歯止め[1]を解除")
    a = ap.parse_args()
    root = pathlib.Path(a.root)

    n, regions, updated = read_profiles(root)
    vals = {"n": str(n), "regions": regions, "updated": updated}

    pat = re.compile(r'(<span[^>]*\bdata-bc="(n|regions|updated)"[^>]*>)(.*?)(</span>)')

    # 歯止め[1][2]：いま HTML に入っている値と比べる
    cur, cur_date = None, None
    for f in TARGETS:
        for m in pat.finditer((root / f).read_text(encoding="utf-8")):
            if m.group(2) == "n" and m.group(3).isdigit() and cur is None:
                cur = int(m.group(3))
            if m.group(2) == "updated" and cur_date is None:
                cur_date = m.group(3)
    if not a.force:
        # [1] 件数が急変したら止める
        if cur is not None and (n < 100 or abs(n - cur) > 10):
            sys.exit(f"⛔️ 件数が {cur} → {n}。異常の可能性があるので中止（意図通りなら --force）")
        # [2] 更新日が「後退する」「遠すぎる未来」なら止める
        def ymd(t):
            m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", t or "")
            return datetime.date(*map(int, m.groups())) if m else None
        nd, od = ymd(updated), ymd(cur_date)
        if nd and od and nd < od:
            sys.exit(f"⛔️ 更新日が {cur_date} → {updated} と後退する。"
                     "更新履歴に今回の行を足し忘れていないか確認（意図通りなら --force）")
        if nd and nd > datetime.date.today() + datetime.timedelta(days=7):
            sys.exit(f"⛔️ 更新日 {updated} が未来すぎる。更新履歴の年月日の誤記を疑う（意図通りなら --force）")

    total, changed_files = 0, []
    for f in TARGETS:
        p = root / f
        s = p.read_text(encoding="utf-8")
        hits = [0]

        def rep(m):
            new = vals[m.group(2)]
            if m.group(3) != new:
                hits[0] += 1
            return m.group(1) + new + m.group(4)

        out = pat.sub(rep, s)
        marks = len(pat.findall(s))
        if marks == 0:
            print(f"⚠️ {f}: data-bc の印が1つも無い")
        if hits[0]:
            total += hits[0]
            changed_files.append(f)
            if not a.check:
                p.write_text(out, encoding="utf-8")
        print(f"  {f}: 印 {marks} 箇所 / 書き換え {hits[0]}")

    print(f"\n★ 件数={n} 内訳={regions} 更新日={updated}")
    if a.check:
        print("（--check：書き換えていない）")
        sys.exit(1 if total else 0)
    print(f"★ {total} 箇所を更新 / 変更ファイル: {changed_files or 'なし'}")


if __name__ == "__main__":
    main()
