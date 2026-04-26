<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glow 無料肌診断 | あなたに最適なスキンケアを提案</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;700&family=Zen+Kaku+Gothic+New:wght@300;400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --rose: #c9687a;
    --rose-light: #f0d4d8;
    --rose-pale: #fdf6f7;
    --plum: #7b4f6e;
    --plum-dark: #4a2d42;
    --sage: #8aab9a;
    --sage-light: #d4e8dc;
    --gold: #c9a86c;
    --gold-light: #f5ead5;
    --ink: #2a1f2d;
    --mist: #f7f3f5;
    --white: #ffffff;
    --shadow: 0 4px 24px rgba(42,31,45,0.10);
    --shadow-lg: 0 8px 40px rgba(42,31,45,0.15);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Zen Kaku Gothic New', sans-serif;
    background: var(--mist);
    color: var(--ink);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ── HEADER ── */
  header {
    background: linear-gradient(135deg, var(--plum-dark) 0%, var(--plum) 50%, var(--rose) 100%);
    padding: 48px 24px 56px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 60%, rgba(201,168,108,0.18) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(255,255,255,0.08) 0%, transparent 50%);
  }
  .logo {
    font-family: 'Shippori Mincho', serif;
    font-size: clamp(2.2rem, 6vw, 3.2rem);
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.18em;
    position: relative;
  }
  .logo span {
    color: var(--gold);
  }
  header p {
    color: rgba(255,255,255,0.82);
    font-size: 0.92rem;
    letter-spacing: 0.08em;
    margin-top: 10px;
    position: relative;
    font-weight: 300;
  }
  .badge {
    display: inline-block;
    background: var(--gold);
    color: var(--plum-dark);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
    position: relative;
  }

  /* ── MAIN ── */
  main {
    max-width: 680px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }

  /* ── PROGRESS ── */
  .progress-wrap {
    margin-bottom: 32px;
  }
  .progress-label {
    font-size: 0.78rem;
    color: var(--plum);
    letter-spacing: 0.1em;
    margin-bottom: 8px;
    font-weight: 700;
  }
  .progress-bar {
    height: 4px;
    background: var(--rose-light);
    border-radius: 2px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--plum), var(--rose));
    border-radius: 2px;
    transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
  }

  /* ── STEP CARD ── */
  .step-card {
    background: var(--white);
    border-radius: 20px;
    padding: 36px 32px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(201,104,122,0.10);
    display: none;
    animation: fadeSlide 0.4s cubic-bezier(0.4,0,0.2,1);
  }
  .step-card.active { display: block; }

  @keyframes fadeSlide {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .step-num {
    font-size: 0.72rem;
    color: var(--rose);
    letter-spacing: 0.15em;
    font-weight: 700;
    margin-bottom: 8px;
  }
  .step-q {
    font-family: 'Shippori Mincho', serif;
    font-size: clamp(1.15rem, 3.5vw, 1.38rem);
    font-weight: 600;
    color: var(--plum-dark);
    margin-bottom: 8px;
    line-height: 1.5;
  }
  .step-sub {
    font-size: 0.82rem;
    color: #877;
    margin-bottom: 24px;
    line-height: 1.6;
  }

  /* ── OPTIONS ── */
  .options-grid {
    display: grid;
    gap: 10px;
  }
  .options-grid.cols2 { grid-template-columns: 1fr 1fr; }
  .options-grid.cols1 { grid-template-columns: 1fr; }

  .opt-btn {
    background: var(--mist);
    border: 1.5px solid rgba(123,79,110,0.15);
    border-radius: 12px;
    padding: 14px 18px;
    cursor: pointer;
    text-align: left;
    transition: all 0.22s ease;
    position: relative;
    overflow: hidden;
  }
  .opt-btn:hover {
    border-color: var(--rose);
    background: var(--rose-pale);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(201,104,122,0.15);
  }
  .opt-btn.selected {
    background: linear-gradient(135deg, var(--rose-pale), #f7edf5);
    border-color: var(--rose);
    box-shadow: 0 4px 16px rgba(201,104,122,0.20);
  }
  .opt-btn.selected::before {
    content: '✓';
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--rose);
    font-weight: 700;
    font-size: 0.9rem;
  }
  .opt-icon { font-size: 1.3rem; display: block; margin-bottom: 4px; }
  .opt-title { font-weight: 700; font-size: 0.9rem; color: var(--plum-dark); display: block; }
  .opt-desc { font-size: 0.75rem; color: #888; margin-top: 3px; display: block; line-height: 1.4; }

  .next-btn {
    width: 100%;
    margin-top: 24px;
    padding: 16px;
    background: linear-gradient(135deg, var(--plum), var(--rose));
    color: #fff;
    border: none;
    border-radius: 12px;
    font-family: 'Zen Kaku Gothic New', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow: 0 4px 16px rgba(123,79,110,0.3);
  }
  .next-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(123,79,110,0.35); }
  .next-btn:disabled { opacity: 0.45; cursor: default; transform: none; }

  /* ── RESULT ── */
  #result { display: none; }
  #result.active { display: block; animation: fadeSlide 0.5s ease; }

  .result-hero {
    background: linear-gradient(135deg, var(--plum-dark) 0%, var(--plum) 60%, var(--rose) 100%);
    border-radius: 20px;
    padding: 36px 28px;
    color: #fff;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .result-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 80% 20%, rgba(201,168,108,0.2) 0%, transparent 50%);
  }
  .result-hero h2 {
    font-family: 'Shippori Mincho', serif;
    font-size: clamp(1.3rem, 4vw, 1.7rem);
    margin-bottom: 8px;
    position: relative;
  }
  .result-hero p { font-size: 0.88rem; opacity: 0.85; position: relative; line-height: 1.6; }

  .skin-profile {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
    position: relative;
  }
  .profile-tag {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
  }

  .section-title {
    font-family: 'Shippori Mincho', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--plum-dark);
    margin: 32px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--rose-light);
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-title::before {
    content: '';
    width: 4px;
    height: 1.1em;
    background: linear-gradient(to bottom, var(--plum), var(--rose));
    border-radius: 2px;
    flex-shrink: 0;
  }

  /* ── BRAND CARD ── */
  .brand-card {
    background: var(--white);
    border-radius: 16px;
    padding: 22px 22px;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(201,104,122,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .brand-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }

  .rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.82rem;
    margin-right: 10px;
    flex-shrink: 0;
  }
  .rank-1 { background: linear-gradient(135deg, #d4af37, #f0d060); color: #4a2d00; }
  .rank-2 { background: linear-gradient(135deg, #a8a8b3, #d0d0d8); color: #2a2a3a; }
  .rank-3 { background: linear-gradient(135deg, #c07a50, #e0a080); color: #3a1500; }

  .brand-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
  }
  .brand-name-wrap { flex: 1; }
  .brand-name { font-weight: 700; font-size: 1.05rem; color: var(--plum-dark); display: block; }
  .brand-region { font-size: 0.72rem; color: var(--rose); font-weight: 700; letter-spacing: 0.08em; }
  .brand-price { font-size: 0.82rem; color: var(--gold); font-weight: 700; background: var(--gold-light); padding: 3px 10px; border-radius: 8px; white-space: nowrap; }

  .brand-reason {
    font-size: 0.84rem;
    color: #555;
    line-height: 1.65;
    margin-bottom: 12px;
    padding: 12px 14px;
    background: var(--mist);
    border-radius: 10px;
    border-left: 3px solid var(--rose-light);
  }

  .ingredient-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 10px;
  }
  .chip {
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: 700;
  }
  .chip-good { background: var(--sage-light); color: #2d5a40; }
  .chip-series { background: var(--rose-pale); color: var(--plum); }
  .chip-step { background: var(--gold-light); color: #5a3800; }
  .chip-pharma { background: #e8e4f5; color: #3d2a6e; }

  .brand-note {
    font-size: 0.76rem;
    color: var(--sage);
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  /* ── INGREDIENT BOX ── */
  .ingredient-box {
    background: var(--white);
    border-radius: 16px;
    padding: 22px;
    box-shadow: var(--shadow);
    margin-bottom: 14px;
    border: 1px solid rgba(138,171,154,0.2);
  }
  .ingredient-box h4 {
    font-weight: 700;
    color: var(--plum-dark);
    margin-bottom: 12px;
    font-size: 0.88rem;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .ingredient-list { display: flex; flex-wrap: wrap; gap: 7px; }
  .i-chip {
    font-size: 0.76rem;
    padding: 4px 12px;
    border-radius: 14px;
    font-weight: 700;
  }
  .i-good { background: var(--sage-light); color: #1e4a30; }
  .i-avoid { background: #ffeae8; color: #8b1a1a; }
  .i-trend { background: linear-gradient(135deg, #ede8f5, #f5e8f2); color: var(--plum); border: 1px solid rgba(123,79,110,0.2); }

  /* ── STEP GUIDE ── */
  .step-guide {
    background: var(--white);
    border-radius: 16px;
    padding: 22px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(201,104,122,0.08);
    margin-bottom: 14px;
  }
  .step-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--mist);
  }
  .step-item:last-child { border-bottom: none; padding-bottom: 0; }
  .step-num-circle {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700;
    flex-shrink: 0;
    background: linear-gradient(135deg, var(--plum), var(--rose));
    color: #fff;
  }
  .step-item-content { flex: 1; }
  .step-item-name { font-weight: 700; font-size: 0.88rem; color: var(--plum-dark); }
  .step-item-desc { font-size: 0.77rem; color: #888; margin-top: 2px; }
  .step-required { font-size: 0.68rem; color: var(--rose); font-weight: 700; background: var(--rose-pale); padding: 2px 7px; border-radius: 6px; }
  .step-optional { font-size: 0.68rem; color: #aaa; font-weight: 700; background: #f5f5f5; padding: 2px 7px; border-radius: 6px; }

  /* ── CTA ── */
  .cta-box {
    background: linear-gradient(135deg, var(--plum-dark), var(--plum));
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
    color: #fff;
    margin-top: 32px;
  }
  .cta-box h3 {
    font-family: 'Shippori Mincho', serif;
    font-size: 1.2rem;
    margin-bottom: 10px;
  }
  .cta-box p { font-size: 0.84rem; opacity: 0.85; margin-bottom: 20px; line-height: 1.6; }
  .cta-btn {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #e0c07a);
    color: var(--plum-dark);
    padding: 14px 32px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    letter-spacing: 0.06em;
    transition: all 0.22s ease;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  }
  .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.25); }

  .retry-btn {
    display: block;
    width: 100%;
    margin-top: 16px;
    padding: 14px;
    background: var(--mist);
    border: 1.5px solid rgba(123,79,110,0.2);
    border-radius: 12px;
    color: var(--plum);
    font-family: 'Zen Kaku Gothic New', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 0.06em;
    transition: all 0.22s ease;
  }
  .retry-btn:hover { background: var(--rose-pale); border-color: var(--rose); }

  .stars { color: var(--gold); font-size: 0.82rem; }

  @media (max-width: 500px) {
    .options-grid.cols2 { grid-template-columns: 1fr; }
    .step-card { padding: 28px 20px; }
  }
</style>
</head>
<body>

<header>
  <div class="badge">✨ 無料 · 30秒診断</div>
  <div class="logo">G<span>low</span></div>
  <p>肌タイプ × 悩み × こだわり × 予算から<br>あなただけの最適スキンケアを提案</p>
</header>

<main>
  <!-- PROGRESS -->
  <div class="progress-wrap" id="progressWrap">
    <div class="progress-label" id="progressLabel">STEP 1 / 4</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:25%"></div></div>
  </div>

  <!-- STEP 1: 肌タイプ -->
  <div class="step-card active" id="step1">
    <div class="step-num">QUESTION 01</div>
    <div class="step-q">あなたの肌タイプは？</div>
    <div class="step-sub">洗顔後、何もつけない状態で鏡を見たときの肌の状態をイメージしてください。</div>
    <div class="options-grid cols2">
      <button class="opt-btn" onclick="select(1,'dry')">
        <span class="opt-icon">💧</span>
        <span class="opt-title">乾燥肌</span>
        <span class="opt-desc">全体的につっぱり感あり。粉吹きしやすい</span>
      </button>
      <button class="opt-btn" onclick="select(1,'oily')">
        <span class="opt-icon">✨</span>
        <span class="opt-title">脂性肌（オイリー）</span>
        <span class="opt-desc">昼ごろにはテカリが気になる</span>
      </button>
      <button class="opt-btn" onclick="select(1,'combo')">
        <span class="opt-icon">☯️</span>
        <span class="opt-title">混合肌</span>
        <span class="opt-desc">Tゾーンはテカるが頬は乾燥気味</span>
      </button>
      <button class="opt-btn" onclick="select(1,'sensitive')">
        <span class="opt-icon">🌸</span>
        <span class="opt-title">敏感肌</span>
        <span class="opt-desc">すぐ赤くなる、刺激を感じやすい</span>
      </button>
      <button class="opt-btn" onclick="select(1,'innerdry')">
        <span class="opt-icon">🫧</span>
        <span class="opt-title">インナードライ</span>
        <span class="opt-desc">外見オイリーだが内側は乾燥している</span>
      </button>
      <button class="opt-btn" onclick="select(1,'aging')">
        <span class="opt-icon">🌿</span>
        <span class="opt-title">エイジング肌</span>
        <span class="opt-desc">乾燥・ハリ低下・たるみが気になる</span>
      </button>
    </div>
    <button class="next-btn" id="next1" onclick="nextStep(2)" disabled>次の質問へ →</button>
  </div>

  <!-- STEP 2: 悩み -->
  <div class="step-card" id="step2">
    <div class="step-num">QUESTION 02</div>
    <div class="step-q">一番気になる肌の悩みは？</div>
    <div class="step-sub">複数ある場合は最も優先度の高いものを選んでください。</div>
    <div class="options-grid cols2">
      <button class="opt-btn" onclick="select(2,'pore')">
        <span class="opt-icon">🔬</span>
        <span class="opt-title">毛穴・黒ずみ</span>
        <span class="opt-desc">開き毛穴・詰まり毛穴が気になる</span>
      </button>
      <button class="opt-btn" onclick="select(2,'acne')">
        <span class="opt-icon">💊</span>
        <span class="opt-title">ニキビ・肌荒れ</span>
        <span class="opt-desc">ニキビ跡・繰り返す肌荒れ</span>
      </button>
      <button class="opt-btn" onclick="select(2,'spot')">
        <span class="opt-icon">🌟</span>
        <span class="opt-title">シミ・くすみ</span>
        <span class="opt-desc">シミ・そばかす・全体的なくすみ</span>
      </button>
      <button class="opt-btn" onclick="select(2,'wrinkle')">
        <span class="opt-icon">⏳</span>
        <span class="opt-title">シワ・たるみ</span>
        <span class="opt-desc">小じわ・ほうれい線・ハリ低下</span>
      </button>
      <button class="opt-btn" onclick="select(2,'dry')">
        <span class="opt-icon">🌊</span>
        <span class="opt-title">乾燥・インナードライ</span>
        <span class="opt-desc">保湿が長続きしない・内側の乾燥感</span>
      </button>
      <button class="opt-btn" onclick="select(2,'redness')">
        <span class="opt-icon">🌹</span>
        <span class="opt-title">赤み・炎症</span>
        <span class="opt-desc">赤み・ニキビ炎症・肌の敏感さ</span>
      </button>
    </div>
    <button class="next-btn" id="next2" onclick="nextStep(3)" disabled>次の質問へ →</button>
  </div>

  <!-- STEP 3: こだわり -->
  <div class="step-card" id="step3">
    <div class="step-num">QUESTION 03</div>
    <div class="step-q">スキンケア選びで大切にしていることは？</div>
    <div class="step-sub">あなたのスキンケア哲学を教えてください。</div>
    <div class="options-grid cols2">
      <button class="opt-btn" onclick="select(3,'ingredient')">
        <span class="opt-icon">🧪</span>
        <span class="opt-title">成分・効果重視</span>
        <span class="opt-desc">配合成分・濃度・エビデンスを確認して選ぶ</span>
      </button>
      <button class="opt-btn" onclick="select(3,'brand')">
        <span class="opt-icon">🏆</span>
        <span class="opt-title">ブランド・信頼性重視</span>
        <span class="opt-desc">有名ブランド・皮膚科医推奨を重視する</span>
      </button>
      <button class="opt-btn" onclick="select(3,'korea')">
        <span class="opt-icon">🇰🇷</span>
        <span class="opt-title">韓国コスメ好き</span>
        <span class="opt-desc">K-beauty・韓国トレンドをいち早く試したい</span>
      </button>
      <button class="opt-btn" onclick="select(3,'natural')">
        <span class="opt-icon">🌱</span>
        <span class="opt-title">無添加・自然派</span>
        <span class="opt-desc">余計な成分を入れないシンプル処方が好き</span>
      </button>
      <button class="opt-btn" onclick="select(3,'pharma')">
        <span class="opt-icon">💊</span>
        <span class="opt-title">製薬系・医薬部外品</span>
        <span class="opt-desc">医薬品・製薬会社ブランドの信頼感を重視</span>
      </button>
      <button class="opt-btn" onclick="select(3,'luxury')">
        <span class="opt-icon">👑</span>
        <span class="opt-title">プレステージ志向</span>
        <span class="opt-desc">デパコス・高級ブランドで本格的なケアをしたい</span>
      </button>
    </div>
    <button class="next-btn" id="next3" onclick="nextStep(4)" disabled>次の質問へ →</button>
  </div>

  <!-- STEP 4: 予算 -->
  <div class="step-card" id="step4">
    <div class="step-num">QUESTION 04</div>
    <div class="step-q">スキンケアに使える月の予算は？</div>
    <div class="step-sub">1アイテムあたりの価格帯を目安にしてください。</div>
    <div class="options-grid cols1">
      <button class="opt-btn" onclick="select(4,'under1500')">
        <span class="opt-title">💚 〜¥1,500 ｜ プチプラ重視</span>
        <span class="opt-desc">ドラッグストア・コンビニで買えるコスパ最強を探している</span>
      </button>
      <button class="opt-btn" onclick="select(4,'1500to5000')">
        <span class="opt-title">💙 ¥1,500〜¥5,000 ｜ ミドルレンジ</span>
        <span class="opt-desc">品質にこだわりながらコスパも意識したい</span>
      </button>
      <button class="opt-btn" onclick="select(4,'5000to15000')">
        <span class="opt-title">💜 ¥5,000〜¥15,000 ｜ プレステージ入口</span>
        <span class="opt-desc">デパコス・高機能スキンケアへの投資を検討中</span>
      </button>
      <button class="opt-btn" onclick="select(4,'over15000')">
        <span class="opt-title">🖤 ¥15,000〜 ｜ ラグジュアリー</span>
        <span class="opt-desc">最高品質のスキンケアに惜しみなく投資したい</span>
      </button>
    </div>
    <button class="next-btn" id="next4" onclick="showResult()" disabled>診断結果を見る ✨</button>
  </div>

  <!-- RESULT -->
  <div id="result">
    <div class="result-hero">
      <h2 id="resultTitle">診断結果</h2>
      <p id="resultDesc"></p>
      <div class="skin-profile" id="skinProfile"></div>
    </div>

    <div class="section-title">🏆 おすすめブランド TOP3</div>
    <div id="brandCards"></div>

    <div class="section-title">🧪 あなたの肌に効く成分</div>
    <div class="ingredient-box" id="ingredientBox"></div>

    <div class="section-title">📋 あなたに必要なスキンケアステップ</div>
    <div class="step-guide" id="stepGuide"></div>

    <div class="cta-box">
      <h3>✨ もっと詳しく知りたいですか？</h3>
      <p>Glowの公式Xでは毎日最新の美容成分情報・コスメニュースを発信中。<br>診断結果をもとにした具体的なアドバイスも受け取れます。</p>
      <a href="https://x.com/stats_log_net" target="_blank" class="cta-btn">Glow 公式X をフォローする →</a>
    </div>

    <button class="retry-btn" onclick="resetDiagnosis()">🔄 もう一度診断する</button>
  </div>
</main>

<script>
// ── STATE ──
const answers = { skin: '', concern: '', pref: '', budget: '' };

// ── BRAND DATABASE (from AlgoBeauty_v2) ──
const DB = {

  // [skin][concern][pref][budget] → brands[]
  // skin: dry|oily|combo|sensitive|innerdry|aging
  // concern: pore|acne|spot|wrinkle|dry|redness
  // pref: ingredient|brand|korea|natural|pharma|luxury
  // budget: under1500|1500to5000|5000to15000|over15000

  brands: {
    // ── 乾燥肌 ──
    dry: {
      pore:    { ingredient: ['cerave','theordinary','cosrx'],    brand: ['hadalabo','curel','shiseido'],    korea: ['cosrx','laneige','anua'],       natural: ['muji','etvos','naturie'],        pharma: ['hadalabo','minon','curel'],    luxury: ['decorte','pola','esteelauder'] },
      acne:    { ingredient: ['theordinary','cosrx','somebymi'],  brand: ['minon','curel','lrp'],            korea: ['cosrx','somebymi','anua'],      natural: ['muji_clear','etvos','dhc'],      pharma: ['minon','nov','adryS'],        luxury: ['clinique','esteelauder','lrp'] },
      spot:    { ingredient: ['theordinary','transino','obagi'],  brand: ['transino','pola','shiseido'],     korea: ['cosrx','missha','some'],        natural: ['muji_white','drcilabo','fancl'], pharma: ['transino','keshimin','adryS'],luxury: ['pola','sk2','esteelauder'] },
      wrinkle: { ingredient: ['theordinary','obagi','pola'],      brand: ['pola','shiseido','esteelauder'], korea: ['iope','laneige','sulwhasoo'],   natural: ['muji_age','aesop','johnmasters'],pharma: ['adryS','hifmid','obagi'],    luxury: ['pola','decorte','esteelauder'] },
      dry:     { ingredient: ['cerave','hadalabo','theordinary'], brand: ['hadalabo','curel','laneige'],     korea: ['laneige','cosrx','anua'],       natural: ['muji','etvos','naturie'],        pharma: ['hadalabo','minon','locobace'],luxury: ['decorte','albion','esteelauder'] },
      redness: { ingredient: ['cerave','lrp','theordinary'],      brand: ['curel','minon','lrp'],            korea: ['cosrx','anua','laneige'],       natural: ['etvos','muji','mimc'],           pharma: ['curel','minon','arouge'],     luxury: ['lrp','clinique','esteelauder'] },
    },
    // ── 脂性肌 ──
    oily: {
      pore:    { ingredient: ['theordinary','cosrx','somebymi'],  brand: ['biore','somebi','cosrx'],         korea: ['cosrx','somebymi','anua'],      natural: ['muji_clear','naturie','etvos'],   pharma: ['biore','keshimin','transino'], luxury: ['clinique','nars','mac'] },
      acne:    { ingredient: ['cosrx','theordinary','somebymi'],  brand: ['minon','cosrx','nov'],            korea: ['cosrx','somebymi','anua'],      natural: ['muji_clear','etvos','dhc'],       pharma: ['minon','nov','biore'],       luxury: ['clinique','lrp','esteelauder'] },
      spot:    { ingredient: ['theordinary','cosrx','transino'],  brand: ['transino','cosrx','biore'],       korea: ['cosrx','tonymoly','missha'],    natural: ['muji_white','drcilabo','naturie'],pharma: ['transino','keshimin','biore'],luxury: ['clinique','pola','esteelauder'] },
      wrinkle: { ingredient: ['theordinary','obagi','cerave'],    brand: ['esteelauder','clinique','pola'],  korea: ['iope','laneige','cosrx'],       natural: ['muji_age','aesop','johnmasters'], pharma: ['obagi','adryS','hifmid'],    luxury: ['pola','esteelauder','decorte'] },
      dry:     { ingredient: ['theordinary','cosrx','cerave'],    brand: ['hadalabo','laneige','cosrx'],     korea: ['laneige','anua','cosrx'],       natural: ['muji','naturie','etvos'],         pharma: ['hadalabo','minon','adryS'],  luxury: ['laneige','decorte','clinique'] },
      redness: { ingredient: ['theordinary','lrp','cosrx'],       brand: ['lrp','cosrx','minon'],            korea: ['cosrx','anua','somebymi'],      natural: ['muji','etvos','naturie'],         pharma: ['lrp','minon','biore'],       luxury: ['lrp','clinique','esteelauder'] },
    },
    // ── 混合肌 ──
    combo: {
      pore:    { ingredient: ['theordinary','cosrx','anua'],      brand: ['anua','cosrx','biore'],           korea: ['anua','cosrx','somebymi'],      natural: ['muji','naturie','etvos'],         pharma: ['biore','transino','muji_clear'],luxury: ['clinique','nars','lrp'] },
      acne:    { ingredient: ['cosrx','theordinary','somebymi'],  brand: ['cosrx','minon','nov'],            korea: ['cosrx','anua','somebymi'],      natural: ['muji_clear','etvos','dhc'],       pharma: ['minon','nov','muji_clear'], luxury: ['clinique','lrp','esteelauder'] },
      spot:    { ingredient: ['theordinary','cosrx','transino'],  brand: ['transino','cosrx','shiseido'],    korea: ['cosrx','missha','anua'],        natural: ['muji_white','drcilabo','etvos'],  pharma: ['transino','keshimin','adryS'],luxury: ['pola','shiseido','esteelauder'] },
      wrinkle: { ingredient: ['theordinary','obagi','cosrx'],     brand: ['esteelauder','pola','shiseido'], korea: ['iope','laneige','sulwhasoo'],   natural: ['muji_age','aesop','johnmasters'], pharma: ['obagi','adryS','hifmid'],   luxury: ['pola','esteelauder','decorte'] },
      dry:     { ingredient: ['theordinary','cerave','anua'],     brand: ['hadalabo','anua','laneige'],      korea: ['anua','laneige','cosrx'],       natural: ['muji','naturie','etvos'],         pharma: ['hadalabo','adryS','minon'],  luxury: ['decorte','laneige','esteelauder'] },
      redness: { ingredient: ['theordinary','lrp','cosrx'],       brand: ['lrp','curel','minon'],            korea: ['anua','cosrx','laneige'],       natural: ['muji','etvos','naturie'],         pharma: ['curel','minon','lrp'],       luxury: ['lrp','clinique','esteelauder'] },
    },
    // ── 敏感肌 ──
    sensitive: {
      pore:    { ingredient: ['lrp','cerave','theordinary'],      brand: ['curel','minon','lrp'],            korea: ['cosrx','anua','laneige'],       natural: ['etvos','mimc','naturie'],         pharma: ['curel','minon','nov'],       luxury: ['lrp','clinique','esteelauder'] },
      acne:    { ingredient: ['lrp','cosrx','cerave'],            brand: ['minon','nov','curel'],            korea: ['cosrx','anua','somebymi'],      natural: ['etvos','muji_clear','dhc'],       pharma: ['minon','nov','curel'],       luxury: ['lrp','clinique','esteelauder'] },
      spot:    { ingredient: ['lrp','theordinary','transino'],    brand: ['transino','curel','minon'],       korea: ['cosrx','anua','laneige'],       natural: ['etvos','muji_white','mimc'],      pharma: ['transino','curel','keshimin'],luxury: ['lrp','clinique','esteelauder'] },
      wrinkle: { ingredient: ['theordinary','cerave','lrp'],      brand: ['esteelauder','curel','minon'],    korea: ['laneige','iope','cosrx'],       natural: ['muji_age','aesop','etvos'],       pharma: ['adryS','hifmid','locobace'], luxury: ['esteelauder','clinique','decorte'] },
      dry:     { ingredient: ['cerave','lrp','hadalabo'],         brand: ['curel','minon','lrp'],            korea: ['laneige','anua','cosrx'],       natural: ['etvos','mimc','naturie'],         pharma: ['curel','minon','locobace'], luxury: ['lrp','clinique','esteelauder'] },
      redness: { ingredient: ['lrp','cerave','theordinary'],      brand: ['curel','minon','lrp'],            korea: ['anua','cosrx','laneige'],       natural: ['etvos','mimc','naturie'],         pharma: ['curel','minon','arouge'],   luxury: ['lrp','clinique','esteelauder'] },
    },
    // ── インナードライ ──
    innerdry: {
      pore:    { ingredient: ['theordinary','cosrx','hadalabo'],  brand: ['hadalabo','laneige','anua'],      korea: ['laneige','anua','cosrx'],       natural: ['muji','naturie','etvos'],         pharma: ['hadalabo','adryS','minon'],  luxury: ['decorte','laneige','esteelauder'] },
      acne:    { ingredient: ['cosrx','theordinary','hadalabo'],  brand: ['cosrx','minon','nov'],            korea: ['cosrx','anua','laneige'],       natural: ['muji_clear','etvos','dhc'],       pharma: ['minon','nov','hadalabo'],   luxury: ['lrp','clinique','esteelauder'] },
      spot:    { ingredient: ['theordinary','transino','hadalabo'],brand: ['transino','hadalabo','shiseido'],korea: ['cosrx','laneige','missha'],     natural: ['muji_white','drcilabo','etvos'],  pharma: ['transino','hadalabo','adryS'],luxury: ['pola','esteelauder','decorte'] },
      wrinkle: { ingredient: ['theordinary','hadalabo','obagi'],  brand: ['esteelauder','hadalabo','pola'],  korea: ['laneige','iope','sulwhasoo'],   natural: ['muji_age','aesop','johnmasters'], pharma: ['obagi','adryS','hifmid'],   luxury: ['pola','decorte','esteelauder'] },
      dry:     { ingredient: ['hadalabo','cerave','theordinary'], brand: ['hadalabo','laneige','curel'],     korea: ['laneige','cosrx','anua'],       natural: ['muji','orbis','fancl'],          pharma: ['hadalabo','minon','adryS'], luxury: ['decorte','laneige','esteelauder'] },
      redness: { ingredient: ['cerave','lrp','hadalabo'],         brand: ['curel','minon','lrp'],            korea: ['anua','laneige','cosrx'],       natural: ['muji','fancl','arouge'],         pharma: ['curel','hadalabo','minon'], luxury: ['lrp','clinique','esteelauder'] },
    },
    // ── エイジング肌 ──
    aging: {
      pore:    { ingredient: ['theordinary','obagi','pola'],      brand: ['pola','shiseido','esteelauder'], korea: ['iope','sulwhasoo','laneige'],   natural: ['muji_age','pola','fancl'],       pharma: ['obagi','adryS','hifmid'],   luxury: ['pola','decorte','esteelauder'] },
      acne:    { ingredient: ['theordinary','obagi','cosrx'],     brand: ['clinique','esteelauder','pola'], korea: ['iope','cosrx','laneige'],       natural: ['muji_age','fancl','nov'],        pharma: ['obagi','adryS','nov'],       luxury: ['clinique','esteelauder','pola'] },
      spot:    { ingredient: ['theordinary','obagi','transino'],  brand: ['pola','shiseido','transino'],    korea: ['sulwhasoo','iope','missha'],    natural: ['muji_white','muji_age','pola'],  pharma: ['transino','obagi','adryS'], luxury: ['pola','sk2','esteelauder'] },
      wrinkle: { ingredient: ['obagi','theordinary','pola'],      brand: ['pola','esteelauder','shiseido'], korea: ['sulwhasoo','iope','laneige'],   natural: ['muji_age','pola','fancl'],       pharma: ['obagi','adryS','hifmid'],   luxury: ['pola','decorte','esteelauder'] },
      dry:     { ingredient: ['obagi','hadalabo','theordinary'],  brand: ['pola','esteelauder','hadalabo'], korea: ['sulwhasoo','laneige','iope'],   natural: ['muji_age','fancl','orbis'],      pharma: ['obagi','adryS','hifmid'],   luxury: ['pola','decorte','albion'] },
      redness: { ingredient: ['cerave','lrp','theordinary'],      brand: ['curel','esteelauder','lrp'],     korea: ['laneige','iope','cosrx'],       natural: ['muji_age','fancl','orbis'],      pharma: ['curel','adryS','lrp'],       luxury: ['lrp','clinique','esteelauder'] },
    },
  },

  // ── BRAND PROFILES ──
  profiles: {
    hadalabo:     { name:'肌ラボ（HADALABO）', region:'🇯🇵 JP', maker:'ロート製薬', price:'¥500〜¥1,500', stars:5, tag:'製薬系', key:'5種ヒアルロン酸・スーパーHA', series:'極潤シリーズ・白潤プレミアム', step:'STEP3化粧水・STEP5乳液', note:'ドラッグストア最強保湿ブランド', reason:'5種ヒアルロン酸（スーパーHA）で業界トップクラスの保湿力。製薬会社ロート製薬が開発し、医薬部外品ラインも豊富。コスパと成分量のバランスが圧倒的。' },
    curel:        { name:'キュレル（Curel）', region:'🇯🇵 JP', maker:'花王', price:'¥1,000〜¥3,000', stars:5, tag:'製薬系', key:'潤浸保湿セラミド・グリセリン', series:'潤浸保湿シリーズ・UVケア', step:'STEP3化粧水・STEP5乳液', note:'乾燥性敏感肌のNo.1定番ブランド', reason:'花王が開発した独自の「潤浸保湿セラミド機能成分」がバリア機能を補強。皮膚科医推奨で、乾燥性敏感肌・アトピー傾向の方に長年支持されている。' },
    minon:        { name:'ミノン（MINON）', region:'🇯🇵 JP', maker:'第一三共ヘルスケア', price:'¥1,000〜¥3,000', stars:5, tag:'製薬系', key:'18種アミノ酸・セラミド', series:'アミノモイストシリーズ・アクネケア', step:'STEP3化粧水・STEP5乳液', note:'敏感肌の聖典ブランド', reason:'18種のアミノ酸系保湿成分がバリア機能を強化。刺激成分ゼロで敏感肌・アレルギー肌でも安心。キュレルと並ぶ皮膚科医推奨の定番。' },
    theordinary:  { name:'The Ordinary', region:'🇺🇸 US', maker:'DECIEM', price:'¥1,200〜¥3,500', stars:5, tag:'成分特化', key:'ナイアシンアミド・レチノール・AHA/BHA', series:'ナイアシンアミド10%・レチノール・AHA 30%', step:'STEP4美容液', note:'成分透明性×超低価格の革命ブランド', reason:'成分名・濃度を正直に表記する透明性と圧倒的な低価格が特徴。ナイアシンアミド・レチノール・AHA/BHAなど高濃度成分を手軽に試せる成分主義ブランドの先駆け。' },
    cosrx:        { name:'COSRX', region:'🇰🇷 KR', maker:'COSRX', price:'¥1,500〜¥3,500', stars:5, tag:'韓国コスメ', key:'スネイル分泌液・BHA・ナイアシンアミド', series:'スネイルクリーム・AHAトナー・BHAブラックヘッド', step:'STEP3化粧水・STEP4美容液', note:'成分主義Glowと方向性が完全一致', reason:'スネイル分泌液（96%）が世界的ヒット。成分の透明性を重視し、BHA・ナイアシンアミド・AHAを高配合。Glowの成分主義と完全一致する韓国コスメの代表格。' },
    anua:         { name:'anua（アヌア）', region:'🇰🇷 KR', maker:'ANUA', price:'¥1,200〜¥3,500', stars:4, tag:'韓国コスメ', key:'ドクダミ・センテラアジアチカ・ナイアシンアミド', series:'ドクダミシリーズ・ナイアシンアミドトナー', step:'STEP3化粧水・STEP4美容液', note:'日本でも爆発的人気の敏感肌向け', reason:'ドクダミ（フラボノイド）が赤みや炎症を鎮静。センテラアジアチカでバリア補強。成分特化でSNS口コミが拡散中。混合肌・脂性肌の日本人に特にフィット。' },
    laneige:      { name:'Laneige（ラネージュ）', region:'🇰🇷 KR', maker:'アモーレパシフィック', price:'¥2,000〜¥5,000', stars:4, tag:'韓国コスメ', key:'ヒアルロン酸・グリーンティー・水分成分', series:'リップスリーピングマスク・ウォータースリーピングマスク', step:'STEP3化粧水・STEP8マスク', note:'リップ・保湿マスクが世界的ヒット', reason:'ヒアルロン酸×グリーンティーの水分補給が特徴。リップスリーピングマスクが世界中でヒット。SNS特化マーケティングでZ世代に絶大な人気。' },
    somebymi:     { name:'Some By Mi（サムバイミー）', region:'🇰🇷 KR', maker:'Some By Mi', price:'¥1,200〜¥2,800', stars:4, tag:'韓国コスメ', key:'AHA・BHA・PHA・ティーツリー', series:'AHA BHA PHA 30Days トナー', step:'STEP3化粧水・STEP4美容液', note:'30日間で肌が変わると話題', reason:'AHA・BHA・PHA三重酸の角質ケアとティーツリーの抗菌作用。ニキビ・毛穴改善に実績があり、30日間チャレンジがSNSで世界的に拡散した。' },
    lrp:          { name:'La Roche-Posay（ラロッシュポゼ）', region:'🇪🇺 EU', maker:'L\'Oréal', price:'¥2,500〜¥6,000', stars:5, tag:'皮膚科学', key:'温泉水・シカルファット・ニアシンアミド', series:'シカプラスト・トレリアン・エファクラー', step:'STEP3化粧水・STEP5クリーム', note:'世界の皮膚科医が最も推奨するブランド', reason:'フランスの温泉水を配合した独自処方で、皮膚科学に基づいた設計が特徴。敏感肌・アレルギー肌に世界中の皮膚科医が推奨する最高信頼度ブランド。' },
    cerave:       { name:'CeraVe（セラヴィ）', region:'🇺🇸 US', maker:'L\'Oréal（ロレアル）', price:'¥1,500〜¥3,500', stars:5, tag:'成分特化', key:'セラミド1・3・6-II・ヒアルロン酸・MVE技術', series:'モイスチャライジングクリーム・フォーミングクレンザー', step:'STEP3化粧水・STEP5クリーム', note:'皮膚科医推奨の成分主義ブランド', reason:'独自のMVE（マルチベジクルエマルジョン）技術で成分を24時間かけてゆっくり放出。セラミド3種配合でバリア機能を修復。皮膚科医推奨のCEで最も信頼される処方。' },
    transino:     { name:'トランシーノ', region:'🇯🇵 JP', maker:'第一三共ヘルスケア', price:'¥2,000〜¥5,000', stars:4, tag:'製薬系', key:'トラネキサム酸・ビタミンC誘導体', series:'薬用美白シリーズ', step:'STEP3化粧水・STEP4美容液', note:'医薬部外品美白の代名詞', reason:'トラネキサム酸（美白有効成分）配合の全品医薬部外品。内服薬と外用化粧品の一貫ブランドで、シミ・そばかす改善の実績が高い。製薬会社の本気美白ブランド。' },
    obagi:        { name:'Obagi（オバジ）', region:'🇯🇵 JP', maker:'ロート製薬', price:'¥3,000〜¥10,000', stars:4, tag:'製薬系', key:'ピュアビタミンC・レチノール・ペプチド', series:'ObagiCシリーズ・ObagiXシリーズ', step:'STEP4美容液・STEP5クリーム', note:'製薬×皮膚科学の信頼感が高い', reason:'高濃度安定化ピュアビタミンCが特徴。ロート製薬の技術力で成分の安定性を実現。シミ・毛穴・シワへの科学的アプローチで口コミ拡散力が強い。' },
    pola:         { name:'POLA（ポーラ）', region:'🇯🇵 JP', maker:'ポーラ・オルビスHD', price:'¥7,000〜¥30,000', stars:5, tag:'プレステージ', key:'レチノール・ペプチド・独自複合成分', series:'B.A シリーズ・WRINKLESHOT', step:'STEP4美容液・STEP5クリーム', note:'エイジングケア特化の最高峰', reason:'1929年創業・独自複合成分とR&D投資が他を圧倒。WRINKLESHOTはシワ改善初の有効成分として認可。プレステージエイジングケアの頂点ブランド。' },
    shiseido:     { name:'資生堂 Shiseido', region:'🇯🇵 JP', maker:'資生堂', price:'¥5,000〜¥20,000', stars:5, tag:'プレステージ', key:'MICRO RETINOLテクノロジー・POLYREPAIRテクノロジー', series:'エリクシール・アルティミューン・WASO', step:'STEP3〜5全般', note:'世界120ヶ国展開の日本最大美容ブランド', reason:'MICRO RETINOLテクノロジーによる高浸透レチノール処方が特徴。世界120カ国以上で展開し、日本の美容科学の最先端を走る。Beauty Keyアプリで個別成分診断も提供開始。' },
    esteelauder:  { name:'Estée Lauder（エスティローダー）', region:'🇪🇺 EU', maker:'エスティローダー社', price:'¥8,000〜¥25,000', stars:5, tag:'プレステージ', key:'EGF類似成分（ANR）・ナイアシンアミド・ペプチド', series:'アドバンスナイトリペア・フューチャリスト', step:'STEP4美容液・STEP5クリーム', note:'世界最多のスキンケアInstagramフォロワー', reason:'アドバンスナイトリペア（ANR）はEGF類似成分配合の伝説的美容液。25以上のブランドを保有するグループで、R&D投資量が業界随一。' },
    decorte:      { name:'DECORTÉ（コスデコルテ）', region:'🇯🇵 JP', maker:'コーセー', price:'¥7,000〜¥25,000', stars:4, tag:'プレステージ', key:'AQ成分・独自リポソーム技術・植物幹細胞', series:'AQシリーズ・リポソームアドバンスト', step:'STEP4美容液・STEP5クリーム', note:'百貨店デパコスの頂点ブランド', reason:'コーセー傘下の最高級ラインで、独自のリポソーム技術が成分の深部浸透を実現。植物幹細胞エキスによるエイジングケアが百貨店層に絶大な人気。' },
    clinique:     { name:'Clinique（クリニーク）', region:'🇪🇺 EU', maker:'エスティローダー社', price:'¥4,000〜¥15,000', stars:4, tag:'プレステージ', key:'ヒアルロン酸・BHA・皮膚科学成分', series:'クラリファイングローション・モイスチャーサージ', step:'STEP3〜5全般', note:'アレルギーテスト済みの信頼感', reason:'全製品アレルギーテスト・皮膚科テスト済みで敏感肌でも使えるプレステージブランド。脱「派手さ」で成分と処方の質にこだわる知性派。' },
    fancl:        { name:'ファンケル FANCL', region:'🇯🇵 JP', maker:'ファンケル', price:'¥1,500〜¥6,000', stars:4, tag:'無添加', key:'ビタミンC誘導体・グリセリン・植物エキス', series:'マイルドクレンジングオイル・無添加スキンケア', step:'STEP0クレンジング・STEP3化粧水', note:'無添加化粧品の先駆けブランド', reason:'防腐剤・香料・合成色素などをすべて排除した「無添加」の先駆け。健康食品との相乗効果でインナービューティーも訴求。成分へのこだわりが強い方に最適。' },
    orbis:        { name:'オルビス ORBIS', region:'🇯🇵 JP', maker:'ポーラ・オルビスHD', price:'¥1,200〜¥5,000', stars:4, tag:'無添加', key:'ヒアルロン酸・セラミド・コラーゲン', series:'クリアシリーズ・ユードットシリーズ', step:'STEP3化粧水・STEP5乳液', note:'サステナ×無添加D2C最強', reason:'ポーラ・オルビスHD傘下のD2C美容ブランド。「ノンオイルスキンケア」の先駆けで、サステナブル志向と無添加処方が強み。定期購入モデルで継続ユーザーが多い。' },
    muji:         { name:'無印良品 敏感肌用シリーズ', region:'🇯🇵 JP', maker:'良品計画', price:'¥690〜¥1,290', stars:5, tag:'無添加', key:'セラミド・5種アミノ酸・天然水', series:'敏感肌用さっぱり/しっとり/高保湿', step:'STEP3化粧水・STEP5乳液', note:'1ブランドで全悩みに対応できる唯一の存在', reason:'岩手釜石の天然水ベースに5種アミノ酸とセラミドを配合。香料・着色料・鉱物油など7フリー設計。プチプラ最高コスパで敏感肌も安心。' },
    muji_clear:   { name:'無印良品 薬用クリアケア', region:'🇯🇵 JP', maker:'良品計画', price:'¥990〜¥1,690', stars:5, tag:'無添加', key:'グリチルリチン酸2K・ドクダミエキス', series:'薬用クリアケアシリーズ', step:'STEP3薬用化粧水', note:'医薬部外品でCOSRXと同成分アプローチ', reason:'グリチルリチン酸2K（抗炎症有効成分）配合の医薬部外品。ドクダミエキスでニキビ・肌荒れ予防。COSRXのような韓国式成分アプローチを日本の医薬部外品基準で実現。' },
    muji_white:   { name:'無印良品 エイジングケア薬用美白', region:'🇯🇵 JP', maker:'良品計画', price:'¥1,490〜¥2,490', stars:5, tag:'無添加', key:'ビタミンC誘導体・トラネキサム酸・ヒアルロン酸', series:'エイジングケア薬用美白シリーズ', step:'STEP3〜STEP6', note:'トランシーノと同有効成分が約1,500円から', reason:'トランシーノ（¥5,000超）と同じトラネキサム酸（有効成分）を配合しながら約1,490円から。ビタミンC誘導体も配合したシミ・シワ・美白の三冠医薬部外品。' },
    muji_age:     { name:'無印良品 エイジングケアシリーズ', region:'🇯🇵 JP', maker:'良品計画', price:'¥1,490〜¥2,490', stars:4, tag:'無添加', key:'11種植物エキス・レチノール誘導体・天然由来100%', series:'エイジングケアシリーズ', step:'STEP3化粧水・STEP5乳液', note:'天然由来100%×レチノール誘導体', reason:'天然由来成分100%でレチノール誘導体（パルミチン酸レチノール）とビタミンC誘導体を配合。The Ordinaryと近い成分設計を大幅低価格で実現した革命的コスパ。' },
    adryS:        { name:'AdryS（アドライズ）', region:'🇯🇵 JP', maker:'大正製薬', price:'¥3,000〜¥5,000', stars:4, tag:'製薬系', key:'ヘパリン類似物質・プラセンタエキス・セラミド', series:'アクティブローション・アクティブクリーム', step:'STEP3化粧水・STEP5クリーム', note:'ヒルドイドと同成分の市販スキンケア', reason:'皮膚科処方のヒルドイドと同成分「ヘパリン類似物質」を配合。さらに美白プラセンタエキスとセラミドも複合配合。大正製薬の本気スキンケアとしてSNS高評価。' },
    hifmid:       { name:'ヒフミド（HIFMID）', region:'🇯🇵 JP', maker:'小林製薬', price:'¥2,000〜¥5,000', stars:4, tag:'製薬系', key:'ヒト型セラミドⅡ（4%高配合）', series:'エッセンスローション・エッセンスミルク', step:'STEP3化粧水・STEP5乳液', note:'ヒト型セラミド配合量が業界トップクラス', reason:'ヒト型セラミドⅡを4%高配合（業界最高水準）。小林製薬の製薬技術でセラミド1・3を複合配合。バリア機能修復に特化した「製薬会社×セラミドの王道」。' },
    nov:          { name:'ノブ（NOV）', region:'🇯🇵 JP', maker:'常盤薬品工業', price:'¥1,500〜¥5,000', stars:4, tag:'製薬系', key:'アミノ酸系保湿成分・セラミド', series:'NOBシリーズⅠ・Ⅲ・L', step:'STEP3化粧水・STEP4美容液', note:'1985年誕生の老舗皮膚科推奨ブランド', reason:'臨床皮膚医学に基づき1985年に誕生した老舗敏感肌ブランド。皮膚科医推奨で、敏感肌からニキビ肌・エイジングまで対応するシリーズ展開が強み。' },
    locobace:     { name:'ロコベース（LOCOBACE）', region:'🇯🇵 JP', maker:'第一三共ヘルスケア', price:'¥1,000〜¥2,500', stars:3, tag:'製薬系', key:'セラミド・コレステロール・脂肪酸', series:'リペアクリーム・リペアミルク', step:'STEP5クリーム', note:'超乾燥肌・バリア補修の実力派', reason:'皮膚科学的に重要な「セラミド・コレステロール・脂肪酸」の3種肌脂質を同時補給。ナノ粒子化で浸透力を強化。超乾燥肌・アトピー傾向の方のバリア補修に特化。' },
    arouge:       { name:'アルージェ（Arouge）', region:'🇯🇵 JP', maker:'全薬工業', price:'¥1,500〜¥3,000', stars:3, tag:'製薬系', key:'温泉水・アミノ酸系成分', series:'モイスチャーシリーズ', step:'STEP3化粧水・STEP5ジェル', note:'温泉水ベースの敏感肌特化', reason:'NMFと同ミネラル組成の温泉水をベースに、アミノ酸系保湿成分でバリア機能を補強。皮膚科医監修で安全性が高く、根強いファンを持つ敏感肌特化ブランド。' },
    keshimin:     { name:'ケシミン（KESHIMIN）', region:'🇯🇵 JP', maker:'小林製薬', price:'¥800〜¥2,000', stars:3, tag:'製薬系', key:'ビタミンC誘導体・ヒアルロン酸', series:'浸透化粧水・浸透クリームC', step:'STEP3化粧水・STEP5クリーム', note:'プチプラ美白の定番入門ブランド', reason:'ビタミンC誘導体（アスコルビン酸2-グルコシド）配合の医薬部外品。薬局で手軽に購入でき、美白初心者の入門として最適なプチプラ美白ブランド。' },
    iope:         { name:'IOPE（イオペ）', region:'🇰🇷 KR', maker:'アモーレパシフィック', price:'¥3,000〜¥8,000', stars:4, tag:'韓国コスメ', key:'バイオエッセンス・植物幹細胞・レチノール', series:'バイオエッセンス・スーパービタル', step:'STEP3化粧水・STEP4美容液', note:'エアクッションファンデーション発明ブランド', reason:'エアクッションファンデーションを世界で初めて発明したイノベーションブランド。バイオエッセンスと植物幹細胞技術でテクノロジー×韓方を融合したエイジングケア。' },
    sulwhasoo:    { name:'Sulwhasoo（雪花秀）', region:'🇰🇷 KR', maker:'アモーレパシフィック', price:'¥8,000〜¥30,000', stars:5, tag:'韓国コスメ', key:'高麗人参・韓方複合エキス・発酵成分', series:'滋陰生津クリーム・エセンシャルシリーズ', step:'STEP3化粧水・STEP5クリーム', note:'韓方高級スキンケアの最高峰', reason:'高麗人参を中心とした韓方成分と最先端テクノロジーを融合。アモーレパシフィックの最高級ラインで、プレステージ韓国コスメを代表するラグジュアリーブランド。' },
    missha:       { name:'MISSHA（ミシャ）', region:'🇰🇷 KR', maker:'エイブルC&C', price:'¥1,200〜¥4,000', stars:4, tag:'韓国コスメ', key:'ナイアシンアミド・タイム革命成分・レチノール', series:'タイムレボリューション・BBクリーム', step:'STEP3化粧水・STEP4美容液', note:'BBクリームの先駆けブランド', reason:'韓国初のBBクリームブランドとして世界市場を開拓。タイムレボリューション シリーズがSK-IIのフェイシャルトリートメントエッセンスの廉価代替として口コミ拡散。' },
    tonymoly:     { name:'Tony Moly（トニーモリー）', region:'🇰🇷 KR', maker:'Tony Moly', price:'¥1,000〜¥3,000', stars:3, tag:'韓国コスメ', key:'アルブチン・ビタミンC・植物エキス', series:'パンダパック・アイブロウシリーズ', step:'STEP4美容液・STEP8マスク', note:'パッケージデザイン×SNS映え戦略', reason:'ユニークなアニマルパッケージでSNSで拡散力が高い。アルブチン・ビタミンCの美白成分を配合しながら低価格を実現。K-beautyらしい遊び心ある体験ができる。' },
    mac:          { name:'MAC Cosmetics（マック）', region:'🇺🇸 US', maker:'エスティローダー社', price:'¥3,000〜¥8,000', stars:4, tag:'プレステージ', key:'高発色色素・保湿成分・SPF', series:'スタジオフィックスフルイド・リップグラス', step:'STEP5クリームファンデ', note:'プロメイクアップアーティスト御用達', reason:'世界のプロメイクアップアーティストに選ばれる高発色・長持ち処方。多様性重視のインクルーシブ戦略で全人種・肌色に対応。40色以上のファンデーションシェード展開。' },
    nars:         { name:'NARS（ナーズ）', region:'🇺🇸 US', maker:'シャネル', price:'¥4,000〜¥10,000', stars:4, tag:'プレステージ', key:'保湿成分・シアバター・SPF', series:'オーガズムコレクション・ライトリフレクティング', step:'STEP5ファンデ・チーク', note:'「オーガズム」が世界的カルト人気', reason:'シアバター配合の高保湿処方と芸術性の高い色設計が特徴。「オーガズムブラッシュ」は世界最多売れたコスメの一つ。カラーコスメ×アート訴求のプレステージブランド。' },
    sk2:          { name:'SK-II', region:'🇯🇵 JP', maker:'P&G', price:'¥15,000〜¥35,000', stars:5, tag:'プレステージ', key:'ピテラ（発酵成分）・ナイアシンアミド', series:'フェイシャルトリートメントエッセンス', step:'STEP2導入液・STEP4美容液', note:'30年以上愛される伝説の発酵エッセンス', reason:'独自成分ピテラ（酵母発酵エキス）が30年以上の実績を持つ。ナイアシンアミドと組み合わせた透明感・ハリ改善に定評。「骨格からの輝き」がコンセプトのラグジュアリーブランド。' },
    albion:       { name:'ALBION（アルビオン）', region:'🇯🇵 JP', maker:'アルビオン', price:'¥8,000〜¥30,000', stars:4, tag:'プレステージ', key:'独自保湿成分・植物エキス複合体', series:'エクサージュ・アルティミューン', step:'STEP3化粧水・STEP5クリーム', note:'百貨店カウンセリング販売の老舗', reason:'独自処方と百貨店でのカウンセリング販売にこだわる日本の老舗高級コスメブランド。エクサージュシリーズは長年の根強いファンを持ち、乾燥肌エイジングケアに定評がある。' },
    biore:        { name:'ビオレ（Biore）', region:'🇯🇵 JP', maker:'花王', price:'¥500〜¥1,500', stars:4, tag:'製薬系', key:'アミノ酸系洗浄成分・UV吸収剤', series:'スキンケア洗顔料・ビオレUV', step:'STEP1洗顔・STEP7日焼け止め', note:'日焼け止め・洗顔のプチプラ定番', reason:'花王のアミノ酸系洗浄技術で毛穴汚れをしっかり除去しながら肌を傷めない。ビオレUVは日焼け止め国内シェア上位で、学生・若年層に特に人気の最強プチプラUVブランド。' },
    innisfree:    { name:'innisfree（イニスフリー）', region:'🇰🇷 KR', maker:'アモーレパシフィック', price:'¥1,200〜¥4,000', stars:3, tag:'韓国コスメ', key:'グリーンティー・火山岩・済州島自然成分', series:'グリーンティーシード・ポアブラー', step:'STEP3化粧水・STEP4美容液', note:'済州島自然派クリーンビューティー', reason:'済州島の清潔な自然環境から採れるグリーンティーと火山岩成分が特徴。クリーンビューティー×サステナブル訴求で、自然由来成分にこだわる方に最適な韓国コスメ。' },
    // ── D2C・自然派・プチプラ（PHASE2追加）──
    dhc:          { name:'DHC', region:'🇯🇵 JP', maker:'DHC', price:'¥500〜¥3,000', stars:4, tag:'D2C通販', key:'オリーブバージンオイル・コエンザイムQ10・ビタミンC誘導体', series:'薬用ディープクレンジングオイル・薬用Qシリーズ', step:'STEP0クレンジング・STEP3化粧水', note:'日本最多出荷クレンジングオイルの王者', reason:'オリーブバージンオイル100%配合のクレンジングオイルは日本最多出荷実績。サプリ事業との相乗効果でインナービューティーも訴求。コスパ最強のD2C通販ブランド。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/DHC+%E8%96%AC%E7%94%A8%E3%83%87%E3%82%A3%E3%83%BC%E3%83%97%E3%82%AF%E3%83%AC%E3%83%B3%E3%82%B8%E3%83%B3%E3%82%B0%E3%82%AA%E3%82%A4%E3%83%AB/' },
    drcilabo:     { name:'ドクターシーラボ', region:'🇯🇵 JP', maker:'ドクターシーラボ', price:'¥2,000〜¥8,000', stars:4, tag:'D2C高機能', key:'ビタミンC誘導体（VC100）・コラーゲン・ヒアルロン酸', series:'VC100エッセンスローション・アクアコラーゲンゲル', step:'STEP3化粧水・STEP4美容液', note:'皮膚科医監修のVC100美容液が定番', reason:'皮膚科医監修の高機能スキンケア。VC100（高濃度ビタミンC誘導体）シリーズがシミ・毛穴改善に実績。オールインワンゲルも人気で、スキンケア時短派にも対応。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/%E3%83%89%E3%82%AF%E3%82%BF%E3%83%BC%E3%82%B7%E3%83%BC%E3%83%A9%E3%83%9C+VC100/' },
    mimc:         { name:'MiMC', region:'🇯🇵 JP', maker:'MiMC', price:'¥2,500〜¥8,000', stars:4, tag:'オーガニック', key:'ミネラル成分・植物由来成分・無添加処方', series:'ミネラルリキッドリー ファンデーション・バームクレンジング', step:'STEP0クレンジング・STEP5ファンデ', note:'日本発オーガニックミネラルコスメの先駆け', reason:'日本発のオーガニックミネラルコスメブランド。敏感肌でも使えるミネラルファンデーションが主力。化粧品成分への厳しい基準と植物由来処方で、肌に優しいメイクを実現。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/MiMC+%E3%83%9F%E3%83%8D%E3%83%A9%E3%83%AB%E3%83%95%E3%82%A1%E3%83%B3%E3%83%87%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/' },
    etvos:        { name:'ETVOS（エトヴォス）', region:'🇯🇵 JP', maker:'ETVOS', price:'¥1,500〜¥6,000', stars:4, tag:'自然派', key:'セラミド・ミネラル成分・植物由来エキス', series:'モイスチャライジングセラム・ミネラルスムースファンデーション', step:'STEP4美容液・STEP5ファンデ', note:'敏感肌×ミネラルコスメの日本代表ブランド', reason:'敏感肌×ミネラルコスメの先駆けD2Cブランド。セラミドスキンケアとミネラルメイクの両輪展開。無添加処方でSNS口コミが強く、敏感肌女性に圧倒的支持を誇る。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/ETVOS+%E3%82%A8%E3%83%88%E3%83%B4%E3%82%A9%E3%82%B9+%E3%82%BB%E3%83%A9%E3%83%9F%E3%83%89/' },
    johnmasters:  { name:'ジョンマスターオーガニック', region:'🇺🇸 US', maker:'John Masters Organics', price:'¥2,500〜¥6,000', stars:4, tag:'オーガニック', key:'オーガニック植物エキス・精油・天然由来100%', series:'ラベンダー＆アボカドインテンシブコンディショナー・スカルプシャンプー', step:'STEP0クレンジング・ヘアケア', note:'NYオーガニックサロン発・日本で大人気', reason:'NYのオーガニックサロン発祥・全成分オーガニック認証取得。天然由来成分100%で頭皮・肌に優しいライフスタイルブランド。日本でも高い知名度とブランド信頼度を持つ。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/%E3%82%B8%E3%83%A7%E3%83%B3%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%AA%E3%83%BC%E3%82%AC%E3%83%8B%E3%83%83%E3%82%AF/' },
    aesop:        { name:'イソップ（Aesop）', region:'🇦🇺 AU', maker:'L\'Oréal（ロレアル）', price:'¥3,000〜¥10,000', stars:4, tag:'自然派', key:'植物由来エキス・精油・ビタミン類', series:'パリセードデイクリーム・ファーブラッシュフォームフェイシャルクレンザー', step:'STEP1洗顔・STEP5クリーム', note:'豪州発・五感に訴えるライフスタイルブランド', reason:'豪州発の植物由来成分×独特の世界観が特徴。2023年にロレアル傘下へ。店舗デザイン・香り・テクスチャーで五感に訴えるライフスタイルブランドとして世界的に人気急上昇中。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/Aesop+%E3%82%A4%E3%82%BD%E3%83%83%E3%83%97/' },
    dejavu:       { name:'デジャヴュ（dejavu）', region:'🇯🇵 JP', maker:'イミュ株式会社', price:'¥700〜¥1,500', stars:4, tag:'プチプラ', key:'ウォータープルーフ成分・密着ポリマー・アイメイク特化処方', series:'塗るつけまつげ・密着アイライナー・パウダーペンシルアイブロウ', step:'アイメイク特化', note:'落ちないアイライナーのプチプラ最強ブランド', reason:'イミュ株式会社展開のアイメイク特化ブランド。ウォータープルーフ処方で汗・皮脂に強く「落ちない」を実現。プチプラながら高機能で、アイメイク派女性に長年支持される。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/%E3%83%87%E3%82%B8%E3%83%A3%E3%83%B4%E3%83%A5+%E3%82%A2%E3%82%A4%E3%83%A9%E3%82%A4%E3%83%8A%E3%83%BC/' },
    naturie:      { name:'ナチュリエ（naturie）', region:'🇯🇵 JP', maker:'イミュ株式会社', price:'¥400〜¥1,000', stars:5, tag:'プチプラ', key:'ハトムギエキス（ヨクイニン）・グリセリン・植物エキス', series:'ハトムギ化粧水・ハトムギスキンコンディショナー', step:'STEP3化粧水', note:'コスパ最強・ハトムギ化粧水の代名詞', reason:'イミュ株式会社展開のハトムギ化粧水が爆発的人気。ヨクイニン（ハトムギエキス）の肌荒れ予防効果と驚異的なコスパでSNS口コミが拡散。プチプラスキンケアの定番中の定番。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/%E3%83%8A%E3%83%81%E3%83%A5%E3%83%AA%E3%82%A8+%E3%83%8F%E3%83%88%E3%83%A0%E3%82%AE%E5%8C%96%E7%B2%A7%E6%B0%B4/' },
    opera:        { name:'オペラ（OPERA）', region:'🇯🇵 JP', maker:'イミュ株式会社', price:'¥1,200〜¥2,000', stars:5, tag:'プチプラ', key:'保湿成分・発色持続ポリマー・植物オイル', series:'リップティントN・シアーリップカラーN', step:'リップメイク特化', note:'Z世代No.1リップ・SNS映え最強ブランド', reason:'イミュ株式会社展開のリップティントが若年層に爆発的人気。発色と保湿を両立した処方でSNS映え抜群。「落ちない・にじまない」で長時間美しいリップを実現するプチプラ最強リップブランド。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/%E3%82%AA%E3%83%9A%E3%83%A9+%E3%83%AA%E3%83%83%E3%83%97%E3%83%86%E3%82%A3%E3%83%B3%E3%83%88/' },
    canmake:      { name:'CANMAKE（キャンメイク）', region:'🇯🇵 JP', maker:'井田ラボラトリーズ', price:'¥500〜¥1,200', stars:5, tag:'プチプラ', key:'保湿成分・カラー色素安定化技術・軽量処方', series:'マシュマロフィニッシュパウダー・クリームチーク・ステイオンバームルージュ', step:'STEP5ベースメイク・チーク・リップ', note:'1,000円以下でデパコス品質のプチプラ最強', reason:'井田ラボラトリーズ展開の日本プチプラコスメ代表格。1,000円以下でデパコス並みの品質を実現。トレンドカラーを素早く投入するスピード感と可愛いデザインで10〜20代に圧倒的支持。', buyUrl:'https://hb.afl.rakuten.co.jp/hgc/50e535ae.92c750d3.50e535af.a2fe53a8/?pc=https://search.rakuten.co.jp/search/mall/CANMAKE+%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%A1%E3%82%A4%E3%82%AF/' },
  },

  // ── INGREDIENT INFO ──
  ingredients: {
    dry:       { good: ['セラミド','ヒアルロン酸','グリセリン','スクワラン','シアバター','ポリグルタミン酸'], avoid: ['アルコール','サリチル酸','強ピーリング'], trend: ['ポリグルタミン酸','ペプチド','エクソソーム'] },
    oily:      { good: ['ナイアシンアミド','BHA（サリチル酸）','AHA（グリコール酸）','ドクダミエキス'], avoid: ['シリコン過多','重めオイル','鉱物油'], trend: ['グルコノラクトン','ナイアシンアミド','PDRN'] },
    combo:     { good: ['ナイアシンアミド','ペプチド','ドクダミエキス','軽めセラミド'], avoid: ['全顔への重ベースオイル'], trend: ['グルコノラクトン','ペプチド','ポリグルタミン酸'] },
    sensitive: { good: ['シカ（ツボクサ）','パンテノール','アラントイン','トラネキサム酸','ベータグルカン'], avoid: ['エタノール','香料','強いAHA/BHA'], trend: ['グルコノラクトン','エクソソーム','PDRN'] },
    innerdry:  { good: ['セラミド','ヒアルロン酸','ポリグルタミン酸','グリセリン'], avoid: ['コメドジェニック成分'], trend: ['ポリグルタミン酸','エクソソーム','ペプチド'] },
    aging:     { good: ['レチノール','ペプチド','EGF','ナイアシンアミド','ビタミンC'], avoid: ['強アルコール','刺激系ピーリング'], trend: ['エクソソーム','PDRN','グルタチオン'] },
  },

  // ── STEP GUIDES ──
  steps: {
    dry:       [['0','クレンジング','夜のみ・ミルク or バームタイプがおすすめ','必須'], ['1','洗顔料','低刺激・クリームタイプ','必須'], ['2','導入液','成分浸透を高める・インナードライにも◎','推奨'], ['3','化粧水（高保湿）','しっとり〜高保湿タイプを選ぶ','必須'], ['4','美容液','悩みに特化した高濃度成分を届ける','推奨'], ['5','乳液/クリーム','リッチクリームで保湿をロック','必須'], ['7','日焼け止め','朝のケア最終仕上げ','必須']],
    oily:      [['0','クレンジング','夜のみ・ジェルやオイルでしっかり洗浄','必須'], ['1','洗顔料','アミノ酸系泡洗顔で皮脂を適度に落とす','必須'], ['3','化粧水（さっぱり）','ノンオイル・ライトテクスチャー','必須'], ['4','美容液','BHA・ナイアシンアミド系で毛穴・ニキビケア','推奨'], ['7','日焼け止め','ノンオイルSPF','必須']],
    combo:     [['0','クレンジング','夜のみ','必須'], ['1','洗顔料','部位によって使い分けるのが理想','必須'], ['3','化粧水','軽めローションを全顔に','必須'], ['4','美容液','悩みに合わせて部分使い','推奨'], ['5','クリーム','Uゾーンのみに薄く塗布','推奨'], ['7','日焼け止め','必須','必須']],
    sensitive: [['0','クレンジング','低刺激ミルクタイプ','必須'], ['1','洗顔料','アミノ酸系・低刺激','必須'], ['3','化粧水（低刺激）','シンプル処方・成分数の少ないもの','必須'], ['5','乳液/クリーム','バリア補強に特化','必須'], ['7','日焼け止め','無機系SPFが理想','必須']],
    innerdry:  [['0','クレンジング','夜のみ','必須'], ['1','洗顔料','洗いすぎに注意','必須'], ['2','導入液','浸透力を高める','必須'], ['3','化粧水（高保湿）','とろみのある高保湿タイプ','必須'], ['4','美容液','ヒアルロン酸・セラミド系','必須'], ['7','日焼け止め','ノンオイル','必須']],
    aging:     [['0','クレンジング','夜のみ','必須'], ['1','洗顔料','優しく丁寧に','必須'], ['3','化粧水','しっとりタイプ','必須'], ['4','美容液（レチノール/ペプチド）','エイジングケアの核心。夜使用','必須'], ['5','クリーム','リッチクリームでバリアとハリを両立','必須'], ['6','アイクリーム','目元の小じわ・くすみに集中ケア','推奨'], ['7','日焼け止め','老化防止の最重要ケア','必須']],
  },

  skinLabel: { dry:'乾燥肌', oily:'脂性肌', combo:'混合肌', sensitive:'敏感肌', innerdry:'インナードライ', aging:'エイジング肌' },
  concernLabel: { pore:'毛穴・黒ずみ', acne:'ニキビ・肌荒れ', spot:'シミ・くすみ', wrinkle:'シワ・たるみ', dry:'乾燥・インナードライ', redness:'赤み・炎症' },
  prefLabel: { ingredient:'成分重視', brand:'ブランド・信頼性', korea:'韓国コスメ', natural:'無添加・自然派', pharma:'製薬系', luxury:'プレステージ' },
  budgetLabel: { under1500:'〜¥1,500', '1500to5000':'¥1,500〜¥5,000', '5000to15000':'¥5,000〜¥15,000', over15000:'¥15,000〜' },
};

// ── FUNCTIONS ──
function select(step, value) {
  const keys = ['', 'skin', 'concern', 'pref', 'budget'];
  answers[keys[step]] = value;
  document.querySelectorAll(`#step${step} .opt-btn`).forEach(b => b.classList.remove('selected'));
  event.currentTarget.classList.add('selected');
  document.getElementById(`next${step}`).disabled = false;
}

function nextStep(n) {
  document.querySelectorAll('.step-card').forEach(c => c.classList.remove('active'));
  document.getElementById(`step${n}`).classList.add('active');
  const pct = (n / 4) * 100;
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressLabel').textContent = `STEP ${n} / 4`;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function stars(n) {
  return '★'.repeat(n) + '☆'.repeat(5 - n);
}

function showResult() {
  document.querySelectorAll('.step-card').forEach(c => c.classList.remove('active'));
  document.getElementById('progressWrap').style.display = 'none';

  const { skin, concern, pref, budget } = answers;

  // Get brand IDs
  let brandIds = [];
  try { brandIds = DB.brands[skin][concern][pref]; } catch(e) { brandIds = ['hadalabo','cosrx','theordinary']; }

  // Filter by budget
  const budgetFilter = {
    under1500: ['hadalabo','biore','muji','muji_clear','muji_white','cosrx','anua','somebymi','theordinary','keshimin','curel','naturie','canmake','dejavu'],
    '1500to5000': ['hadalabo','curel','minon','lrp','cerave','theordinary','cosrx','anua','laneige','somebymi','transino','iope','missha','tonymoly','fancl','orbis','muji','muji_clear','muji_white','muji_age','adryS','hifmid','nov','locobace','arouge','obagi','innisfree','dhc','etvos','opera','canmake','naturie','dejavu'],
    '5000to15000': ['obagi','pola','shiseido','esteelauder','decorte','clinique','lrp','cerave','iope','sulwhasoo','fancl','orbis','mac','nars','adryS','drcilabo','mimc','johnmasters','aesop','etvos'],
    over15000: ['pola','shiseido','esteelauder','decorte','clinique','sk2','albion','sulwhasoo','nars','mac','aesop'],
  };
  const allowed = budgetFilter[budget] || Object.keys(DB.profiles);

  // Reorder: prefer budget-fitting
  let ordered = [...brandIds].sort((a, b) => {
    const aOk = allowed.includes(a) ? 0 : 1;
    const bOk = allowed.includes(b) ? 0 : 1;
    return aOk - bOk;
  });
  // If fewer than 3 valid, add fallbacks
  if (ordered.filter(id => allowed.includes(id)).length < 2) {
    const extras = allowed.filter(id => DB.profiles[id] && !ordered.includes(id));
    ordered = [...ordered, ...extras];
  }
  const top3 = ordered.slice(0, 3).filter(id => DB.profiles[id]);

  // Build result hero
  document.getElementById('resultTitle').textContent =
    `${DB.skinLabel[skin]} × ${DB.concernLabel[concern]} の処方箋`;
  document.getElementById('resultDesc').textContent =
    `${DB.prefLabel[pref]}・予算${DB.budgetLabel[budget]}に合わせて、AlgoBeautyデータベースから最適なブランドをTop3選定しました。`;

  const tags = [DB.skinLabel[skin], DB.concernLabel[concern], DB.prefLabel[pref], DB.budgetLabel[budget]];
  document.getElementById('skinProfile').innerHTML = tags.map(t => `<span class="profile-tag">${t}</span>`).join('');

  // Brand cards
  const bc = document.getElementById('brandCards');
  bc.innerHTML = top3.map((id, idx) => {
    const b = DB.profiles[id];
    if (!b) return '';
    const rankClass = `rank-${idx + 1}`;
    return `
      <div class="brand-card">
        <div class="brand-header">
          <div class="rank-badge ${rankClass}">${idx + 1}</div>
          <div class="brand-name-wrap">
            <span class="brand-name">${b.name}</span>
            <span class="brand-region">${b.region} · ${b.maker}</span>
          </div>
          <span class="brand-price">${b.price}</span>
        </div>
        <div class="brand-reason">${b.reason}</div>
        <div class="ingredient-chips">
          ${b.key.split('・').map(k => `<span class="chip chip-good">✓ ${k}</span>`).join('')}
        </div>
        <div class="ingredient-chips">
          ${b.series.split('・').map(s => `<span class="chip chip-series">📦 ${s}</span>`).join('')}
          <span class="chip chip-step">📋 ${b.step}</span>
          ${b.tag ? `<span class="chip chip-pharma">${b.tag}</span>` : ''}
        </div>
        <div class="brand-note">
          <span class="stars">${stars(b.stars)}</span>
          &nbsp;${b.note}
        </div>
        ${b.buyUrl ? `<a href="${b.buyUrl}" target="_blank" rel="noopener" style="display:inline-block;margin-top:10px;padding:8px 20px;background:#bf0000;color:#fff;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;letter-spacing:0.05em;">🛒 楽天市場で購入（PR）</a>` : ''}
      </div>`;
  }).join('');

  // Ingredient box
  const ing = DB.ingredients[skin] || DB.ingredients['dry'];
  document.getElementById('ingredientBox').innerHTML = `
    <h4>✅ 積極的に取り入れたい成分</h4>
    <div class="ingredient-list">${ing.good.map(i => `<span class="i-chip i-good">${i}</span>`).join('')}</div>
    <h4 style="margin-top:16px">⚠️ 避けた方が良い成分</h4>
    <div class="ingredient-list">${ing.avoid.map(i => `<span class="i-chip i-avoid">${i}</span>`).join('')}</div>
    <h4 style="margin-top:16px">🌟 2026年注目トレンド成分</h4>
    <div class="ingredient-list">${ing.trend.map(i => `<span class="i-chip i-trend">${i}</span>`).join('')}</div>
  `;

  // Step guide
  const sg = DB.steps[skin] || DB.steps['dry'];
  document.getElementById('stepGuide').innerHTML = sg.map(([num, name, desc, req]) => `
    <div class="step-item">
      <div class="step-num-circle">S${num}</div>
      <div class="step-item-content">
        <div class="step-item-name">${name} &nbsp;<span class="${req === '必須' ? 'step-required' : 'step-optional'}">${req}</span></div>
        <div class="step-item-desc">${desc}</div>
      </div>
    </div>
  `).join('');

  const resultEl = document.getElementById('result');
  resultEl.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetDiagnosis() {
  Object.assign(answers, { skin: '', concern: '', pref: '', budget: '' });
  document.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('selected'));
  document.querySelectorAll('.next-btn').forEach(b => b.disabled = true);
  document.getElementById('result').classList.remove('active');
  document.getElementById('progressWrap').style.display = 'block';
  document.getElementById('progressFill').style.width = '25%';
  document.getElementById('progressLabel').textContent = 'STEP 1 / 4';
  document.querySelectorAll('.step-card').forEach(c => c.classList.remove('active'));
  document.getElementById('step1').classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>
</body>
</html>
