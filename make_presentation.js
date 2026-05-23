const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "House Price Prediction — Final Project";

// ── Color palette: Deep Teal + Off-white + Gold accent ──────
const C = {
  dark:    "0D3349",   // deep navy
  teal:    "0D9488",   // teal
  teal2:   "14B8A6",
  mint:    "CCFBF1",
  white:   "FFFFFF",
  offwht:  "F8FAFC",
  gold:    "F59E0B",
  grey:    "64748B",
  lgrey:   "E2E8F0",
  text:    "1E293B",
};

const makeShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 });

// ╔══════════════════════════════════════════════╗
// ║  Slide 1 — Title                            ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  // Teal accent left strip
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: C.teal } });

  // Left panel content
  s.addText("FINAL PROJECT", {
    x: 0.6, y: 1.0, w: 6, h: 0.4,
    fontSize: 13, bold: true, color: C.teal2, charSpacing: 4, fontFace: "Calibri"
  });
  s.addText("House Price\nPrediction", {
    x: 0.6, y: 1.5, w: 6.5, h: 2.1,
    fontSize: 52, bold: true, color: C.white, fontFace: "Calibri", lineSpacingMultiple: 1.05
  });
  s.addText("Machine Learning Pipeline for King County, WA", {
    x: 0.6, y: 3.65, w: 7, h: 0.45,
    fontSize: 16, color: C.mint, fontFace: "Calibri", italic: true
  });

  // Stats strip
  const stats = [
    { label: "21,613", sub: "Sales Records" },
    { label: "20", sub: "Features" },
    { label: "88.9%", sub: "R² Score" },
    { label: "$69K", sub: "Avg Error (MAE)" },
  ];
  stats.forEach((st, i) => {
    const x = 0.6 + i * 2.3;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 4.3, w: 2.1, h: 0.9, fill: { color: C.teal, transparency: 70 }, shadow: makeShadow() });
    s.addText(st.label, { x, y: 4.32, w: 2.1, h: 0.45, fontSize: 18, bold: true, color: C.white, align: "center", fontFace: "Calibri" });
    s.addText(st.sub,   { x, y: 4.75, w: 2.1, h: 0.35, fontSize: 10, color: C.mint, align: "center", fontFace: "Calibri" });
  });

  // Right panel decorative
  s.addShape(pres.shapes.RECTANGLE, { x: 7.8, y: 0, w: 2.2, h: 5.625, fill: { color: C.teal, transparency: 88 } });
  s.addText("🏠", { x: 7.9, y: 1.8, w: 2, h: 2, fontSize: 80, align: "center" });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 2 — Project Overview                 ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Project Overview", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  const modules = [
    { icon: "📥", title: "Data Loader", desc: "Load & inspect 21,613 King County home sales. Validates shape, dtypes & missing values." },
    { icon: "⚙️", title: "Preprocessor", desc: "Parses dates, removes outliers, engineers 8 new features (house age, renovation flag, price/sqft…)" },
    { icon: "📊", title: "Analyzer (EDA)", desc: "Generates 4 analysis plots: distribution, correlation heatmap, feature scatter, geo price map." },
    { icon: "🤖", title: "Trainer", desc: "Trains Ridge, Random Forest & Gradient Boosting. Auto-selects best model by R² & saves to disk." },
    { icon: "🧪", title: "Evaluator", desc: "Residual plots, actual vs predicted, feature importances. Exports full model report." },
    { icon: "🌐", title: "Streamlit App", desc: "4-page interactive dashboard: overview, explorer, model results & live price predictor." },
  ];

  modules.forEach((m, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.45 + col * 3.1;
    const y = 1.15 + row * 2.05;

    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.95, h: 1.8, fill: { color: C.white }, shadow: makeShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.95, h: 0.08, fill: { color: C.teal } });
    s.addText(m.icon + " " + m.title, { x: x+0.08, y: y+0.12, w: 2.8, h: 0.42, fontSize: 13, bold: true, color: C.dark, fontFace: "Calibri" });
    s.addText(m.desc, { x: x+0.1, y: y+0.55, w: 2.76, h: 1.15, fontSize: 10, color: C.grey, fontFace: "Calibri", valign: "top" });
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 3 — Dataset & EDA                   ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Dataset & EDA Insights", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  // Left: dataset facts
  const facts = [
    ["📍 Source", "King County, WA (2014–2015)"],
    ["📏 Size", "21,613 rows × 20 columns"],
    ["💰 Avg Price", "$540,084 · Median $450,000"],
    ["🏠 Avg Sqft", "2,080 sqft living area"],
    ["🛏️ Avg Rooms", "3.4 beds · 2.1 baths"],
    ["🌊 Waterfront", "0.75% of listings"],
    ["🔧 Renovated", "~4% of homes"],
    ["📅 Sale Period", "Oct 2014 – May 2015"],
  ];

  facts.forEach((f, i) => {
    const y = 1.1 + i * 0.5;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 4.4, h: 0.44,
      fill: { color: i % 2 === 0 ? C.white : C.lgrey } });
    s.addText(f[0], { x: 0.55, y: y+0.04, w: 1.4, h: 0.36, fontSize: 11, bold: true, color: C.teal, fontFace: "Calibri" });
    s.addText(f[1], { x: 1.95, y: y+0.04, w: 2.85, h: 0.36, fontSize: 11, color: C.text, fontFace: "Calibri" });
  });

  // Right: top correlations bar chart
  s.addText("Top Feature Correlations with Price", {
    x: 5.2, y: 1.0, w: 4.5, h: 0.35, fontSize: 13, bold: true, color: C.dark, fontFace: "Calibri"
  });

  s.addChart(pres.charts.BAR, [{
    name: "Correlation",
    labels: ["sqft_living","grade","sqft_above","sqft_living15","bathrooms","view","sqft_basement","bedrooms"],
    values: [0.702, 0.667, 0.606, 0.585, 0.525, 0.397, 0.324, 0.308]
  }], {
    x: 5.0, y: 1.35, w: 4.7, h: 3.8,
    barDir: "bar",
    chartColors: ["0D9488"],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.grey,
    valAxisLabelColor: C.grey,
    valGridLine: { color: C.lgrey, size: 0.5 },
    catGridLine: { style: "none" },
    showValue: true,
    dataLabelColor: C.text,
    dataLabelFontSize: 10,
    showLegend: false,
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 4 — Feature Engineering             ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Feature Engineering", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  const orig = ["date", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront",
                 "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built",
                 "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"];
  const eng = [
    { name: "house_age", formula: "sale_year − yr_built", desc: "Property age at time of sale" },
    { name: "was_renovated", formula: "yr_renovated > 0", desc: "Binary renovation flag" },
    { name: "renovated_age", formula: "sale_year − yr_renovated", desc: "Years since last renovation" },
    { name: "price_per_sqft", formula: "price / sqft_living", desc: "Price density metric" },
    { name: "total_rooms", formula: "bedrooms + bathrooms", desc: "Combined room count" },
    { name: "basement_flag", formula: "sqft_basement > 0", desc: "Binary basement indicator" },
    { name: "sale_year/month", formula: "parsed from date", desc: "Temporal sale features" },
    { name: "log_price", formula: "log1p(price)", desc: "Log-transformed target (EDA only)" },
  ];

  // Original features list
  s.addText("Original Features (20)", { x: 0.45, y: 1.05, w: 3.5, h: 0.35, fontSize: 12, bold: true, color: C.dark, fontFace: "Calibri" });
  orig.forEach((f, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45 + col * 1.55, y: 1.45 + row * 0.42, w: 1.5, h: 0.38,
      fill: { color: C.lgrey } });
    s.addText(f, { x: 0.5 + col * 1.55, y: 1.5 + row * 0.42, w: 1.45, h: 0.3, fontSize: 9, color: C.grey, fontFace: "Consolas" });
  });

  // Arrow
  s.addShape(pres.shapes.RECTANGLE, { x: 3.2, y: 2.8, w: 0.6, h: 0.1, fill: { color: C.teal } });
  s.addText("→", { x: 3.1, y: 2.55, w: 0.8, h: 0.5, fontSize: 28, color: C.teal, align: "center", fontFace: "Calibri" });

  // Engineered features
  s.addText("Engineered Features (+8)", { x: 4.0, y: 1.05, w: 5.5, h: 0.35, fontSize: 12, bold: true, color: C.teal, fontFace: "Calibri" });
  eng.forEach((f, i) => {
    const y = 1.45 + i * 0.49;
    s.addShape(pres.shapes.RECTANGLE, { x: 4.0, y, w: 5.65, h: 0.44, fill: { color: i % 2 === 0 ? C.mint : C.white } });
    s.addText(f.name, { x: 4.1, y: y+0.04, w: 1.6, h: 0.36, fontSize: 10, bold: true, color: C.dark, fontFace: "Consolas" });
    s.addText("=", { x: 5.7, y: y+0.04, w: 0.3, h: 0.36, fontSize: 10, color: C.grey, align: "center", fontFace: "Calibri" });
    s.addText(f.formula, { x: 6.0, y: y+0.04, w: 1.65, h: 0.36, fontSize: 9, color: C.teal, fontFace: "Consolas" });
    s.addText(f.desc, { x: 7.65, y: y+0.04, w: 1.9, h: 0.36, fontSize: 9, color: C.grey, fontFace: "Calibri" });
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 5 — Model Training & Results        ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Model Training & Results", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  // Three model cards
  const models = [
    { name: "Ridge\nRegression", r2: "0.70", mae: "$126K", rmse: "$207K", emoji: "📐", color: C.grey },
    { name: "Random\nForest", r2: "0.86", mae: "$73K", rmse: "$142K", emoji: "🌲", color: C.teal },
    { name: "Gradient\nBoosting ⭐", r2: "0.89", mae: "$69K", rmse: "$127K", emoji: "🚀", color: C.dark },
  ];

  models.forEach((m, i) => {
    const x = 0.35 + i * 3.1;
    const isBest = i === 2;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.05, w: 2.9, h: 3.5,
      fill: { color: isBest ? C.dark : C.white }, shadow: makeShadow() });
    if (isBest) {
      s.addShape(pres.shapes.RECTANGLE, { x, y: 1.05, w: 2.9, h: 0.1, fill: { color: C.gold } });
    }
    s.addText(m.emoji, { x, y: 1.2, w: 2.9, h: 0.7, fontSize: 32, align: "center" });
    s.addText(m.name, { x: x+0.1, y: 1.9, w: 2.7, h: 0.7, fontSize: 14, bold: true,
      color: isBest ? C.white : C.dark, align: "center", fontFace: "Calibri" });

    const rows = [["R²", m.r2], ["MAE", m.mae], ["RMSE", m.rmse]];
    rows.forEach(([label, val], ri) => {
      const ry = 2.7 + ri * 0.58;
      s.addText(label + ":", { x: x+0.25, y: ry, w: 1.0, h: 0.4, fontSize: 11,
        color: isBest ? C.mint : C.grey, fontFace: "Calibri" });
      s.addText(val, { x: x+1.2, y: ry, w: 1.55, h: 0.4, fontSize: 13, bold: true,
        color: isBest ? C.gold : C.teal, align: "right", fontFace: "Calibri" });
    });
  });

  // R² comparison chart
  s.addText("R² Score Comparison", {
    x: 0.35, y: 4.7, w: 3.5, h: 0.35, fontSize: 12, bold: true, color: C.dark, fontFace: "Calibri"
  });
  s.addChart(pres.charts.BAR, [{
    name: "R²",
    labels: ["Ridge", "Random Forest", "Gradient Boosting"],
    values: [0.70, 0.86, 0.89]
  }], {
    x: 3.6, y: 4.55, w: 6.1, h: 0.9,
    barDir: "bar",
    chartColors: [C.grey, C.teal, C.gold],
    chartArea: { fill: { color: C.offwht } },
    catAxisLabelColor: C.grey,
    valAxisLabelColor: C.grey,
    valGridLine: { style: "none" },
    catGridLine: { style: "none" },
    showValue: true,
    dataLabelColor: C.text,
    dataLabelFontSize: 10,
    showLegend: false,
    valAxisMinVal: 0,
    valAxisMaxVal: 1,
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 6 — Evaluation Deep-Dive            ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Best Model — Evaluation Deep-Dive", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  // Key metrics
  const kpis = [
    { label: "R² Score", value: "0.889", sub: "89% variance explained" },
    { label: "MAE", value: "$68,984", sub: "Mean absolute error" },
    { label: "RMSE", value: "$126,683", sub: "Root mean squared error" },
    { label: "MAPE", value: "12.77%", sub: "Mean abs % error" },
    { label: "Median AE", value: "$40,352", sub: "50th percentile error" },
  ];

  kpis.forEach((k, i) => {
    const x = 0.35 + i * 1.87;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.05, w: 1.75, h: 1.15,
      fill: { color: C.dark }, shadow: makeShadow() });
    s.addText(k.value, { x, y: 1.1, w: 1.75, h: 0.6, fontSize: 16, bold: true,
      color: C.gold, align: "center", fontFace: "Calibri" });
    s.addText(k.label, { x, y: 1.68, w: 1.75, h: 0.28, fontSize: 9, bold: true,
      color: C.white, align: "center", fontFace: "Calibri" });
    s.addText(k.sub, { x, y: 1.93, w: 1.75, h: 0.22, fontSize: 8,
      color: C.mint, align: "center", fontFace: "Calibri" });
  });

  // Feature importance table
  s.addText("Top 10 Most Important Features", {
    x: 0.45, y: 2.45, w: 4.5, h: 0.38, fontSize: 13, bold: true, color: C.dark, fontFace: "Calibri"
  });

  const feats = [
    ["1.", "lat", "0.178"], ["2.", "long", "0.106"], ["3.", "sqft_living", "0.098"],
    ["4.", "grade", "0.089"], ["5.", "yr_built", "0.071"],
    ["6.", "sqft_living15", "0.068"], ["7.", "house_age", "0.061"],
    ["8.", "sqft_above", "0.054"], ["9.", "view", "0.038"], ["10.", "bathrooms", "0.029"],
  ];

  feats.forEach(([rank, name, imp], i) => {
    const y = 2.9 + i * 0.26;
    const barW = parseFloat(imp) * 12;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 4.3, h: 0.22,
      fill: { color: i % 2 === 0 ? C.white : C.lgrey } });
    s.addText(rank, { x: 0.5, y, w: 0.35, h: 0.22, fontSize: 9, color: C.grey, fontFace: "Calibri" });
    s.addText(name, { x: 0.85, y, w: 1.8, h: 0.22, fontSize: 9, bold: true, color: C.dark, fontFace: "Consolas" });
    s.addShape(pres.shapes.RECTANGLE, { x: 2.65, y: y+0.04, w: barW, h: 0.14, fill: { color: C.teal } });
    s.addText(imp, { x: 4.3, y, w: 0.42, h: 0.22, fontSize: 9, color: C.teal, align: "right", fontFace: "Calibri" });
  });

  // Interpretation text
  s.addText("Key Findings", {
    x: 5.1, y: 2.45, w: 4.5, h: 0.38, fontSize: 13, bold: true, color: C.dark, fontFace: "Calibri"
  });

  const findings = [
    "📍 Location (lat/long) is the strongest price predictor — geography matters most",
    "📐 Living area & grade together explain ~18% of model gains",
    "🏗️ House age & renovation status have measurable impact",
    "🌊 Waterfront & view ratings drive premium pricing",
    "📉 Model struggles most on luxury homes (>$2M) — limited samples",
    "✅ Median error of $40K on a $450K median home = 8.9% typical error",
  ];

  findings.forEach((f, i) => {
    const y = 2.9 + i * 0.43;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y, w: 4.55, h: 0.38,
      fill: { color: i % 2 === 0 ? C.white : C.lgrey } });
    s.addText(f, { x: 5.18, y: y+0.04, w: 4.4, h: 0.3, fontSize: 10, color: C.text, fontFace: "Calibri" });
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 7 — Streamlit App                   ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Streamlit Web Application", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  const pages = [
    { icon: "📊", title: "Dashboard", desc: "KPI cards, price distribution histogram, price-by-grade chart, interactive geographic map." },
    { icon: "🔍", title: "Data Explorer", desc: "Raw data table, descriptive statistics, feature-vs-price scatter, correlation bar chart." },
    { icon: "🤖", title: "Model Results", desc: "Model comparison table, R² bar chart, actual-vs-predicted, residuals & feature importance plots." },
    { icon: "💰", title: "Price Predictor", desc: "30+ interactive sliders for property features. Live prediction with $±12% confidence range." },
  ];

  pages.forEach((p, i) => {
    const y = 1.1 + i * 1.08;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 9.1, h: 0.95,
      fill: { color: i % 2 === 0 ? C.white : C.lgrey }, shadow: makeShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 0.08, h: 0.95, fill: { color: C.teal } });
    s.addText(p.icon + " " + p.title, { x: 0.65, y: y+0.07, w: 2.2, h: 0.4,
      fontSize: 15, bold: true, color: C.dark, fontFace: "Calibri" });
    s.addText(p.desc, { x: 0.65, y: y+0.48, w: 8.7, h: 0.38,
      fontSize: 11, color: C.grey, fontFace: "Calibri" });
  });

  // Run instructions
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 5.2, w: 9.1, h: 0.3, fill: { color: C.dark } });
  s.addText("▶  streamlit run app.py", {
    x: 0.55, y: 5.22, w: 8.9, h: 0.25, fontSize: 12, color: C.gold, fontFace: "Consolas", bold: true
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 8 — System Architecture             ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.offwht };

  s.addText("Modular System Architecture", {
    x: 0.5, y: 0.3, w: 9, h: 0.65, fontSize: 32, bold: true, color: C.dark, fontFace: "Calibri"
  });

  // Pipeline boxes with arrows
  const pipeline = [
    { label: "data/\nhouse_sales.csv", emoji: "📁", color: C.lgrey, textC: C.dark },
    { label: "src/\ndata_loader.py", emoji: "📥", color: C.teal, textC: C.white },
    { label: "src/\npreprocessor.py", emoji: "⚙️", color: C.teal, textC: C.white },
    { label: "src/\nanalyzer.py", emoji: "📊", color: C.teal, textC: C.white },
    { label: "src/\ntrainer.py", emoji: "🤖", color: C.dark, textC: C.white },
    { label: "src/\nevaluator.py", emoji: "🧪", color: C.dark, textC: C.white },
    { label: "app.py\n(Streamlit)", emoji: "🌐", color: C.gold, textC: C.dark },
  ];

  pipeline.forEach((p, i) => {
    const x = 0.3 + i * 1.35;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 1.2, h: 1.35,
      fill: { color: p.color }, shadow: makeShadow() });
    s.addText(p.emoji, { x, y: 1.25, w: 1.2, h: 0.5, fontSize: 22, align: "center" });
    s.addText(p.label, { x, y: 1.72, w: 1.2, h: 0.75, fontSize: 8.5, color: p.textC,
      align: "center", fontFace: "Consolas" });

    if (i < pipeline.length - 1) {
      s.addText("→", { x: x+1.2, y: 1.6, w: 0.15, h: 0.5, fontSize: 16, color: C.teal, align: "center" });
    }
  });

  // Outputs
  s.addText("Outputs", { x: 0.45, y: 2.85, w: 1.5, h: 0.35, fontSize: 12, bold: true, color: C.dark, fontFace: "Calibri" });

  const outputs = [
    ["models/best_model.pkl", "Serialized Gradient Boosting model"],
    ["reports/price_distribution.png", "Price histogram & log-price"],
    ["reports/correlation_heatmap.png", "Full feature correlation matrix"],
    ["reports/actual_vs_predicted.png", "Evaluation scatter plot"],
    ["reports/feature_importance.png", "Top 15 features ranked"],
    ["reports/model_report.txt", "Plain-text evaluation summary"],
    ["tests/test_pipeline.py", "11 unit tests (all passing ✅)"],
  ];

  outputs.forEach((o, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.45 + col * 4.75;
    const y = 3.25 + row * 0.55;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.6, h: 0.48, fill: { color: col === 0 ? C.white : C.lgrey } });
    s.addText("→ " + o[0], { x: x+0.08, y: y+0.04, w: 2.8, h: 0.35, fontSize: 9, color: C.teal, fontFace: "Consolas" });
    s.addText(o[1], { x: x+2.85, y: y+0.04, w: 1.7, h: 0.35, fontSize: 9, color: C.grey, fontFace: "Calibri" });
  });
}

// ╔══════════════════════════════════════════════╗
// ║  Slide 9 — Conclusion                      ║
// ╚══════════════════════════════════════════════╝
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: 5.625, fill: { color: C.gold } });

  s.addText("Conclusions &\nNext Steps", {
    x: 0.6, y: 0.4, w: 5, h: 1.6, fontSize: 40, bold: true, color: C.white, fontFace: "Calibri"
  });

  const conclusions = [
    "✅ Gradient Boosting achieves R²=0.889, outperforming Ridge & Random Forest",
    "✅ 8 engineered features meaningfully improved model accuracy",
    "✅ Location (lat/long) is the single most predictive variable",
    "✅ Pipeline is fully modular — each stage is independently testable",
    "✅ 11/11 unit tests pass covering all core modules",
  ];

  const nexts = [
    "🔮 Add XGBoost / LightGBM for further gains",
    "🔮 Hyperparameter tuning via Optuna or GridSearchCV",
    "🔮 Add zipcode/neighborhood one-hot encoding",
    "🔮 Deploy app to Streamlit Cloud or Hugging Face Spaces",
    "🔮 Incorporate walk score & school rating external data",
  ];

  s.addText("What We Achieved", { x: 0.6, y: 2.1, w: 4.5, h: 0.38, fontSize: 13, bold: true, color: C.teal2, fontFace: "Calibri" });
  conclusions.forEach((c, i) => {
    s.addText(c, { x: 0.6, y: 2.55 + i * 0.55, w: 4.3, h: 0.48,
      fontSize: 11, color: C.white, fontFace: "Calibri" });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.1, w: 4.5, h: 4.2,
    fill: { color: "FFFFFF", transparency: 6 }, shadow: makeShadow() });

  s.addText("Future Improvements", { x: 5.3, y: 1.25, w: 4.2, h: 0.38, fontSize: 13, bold: true, color: C.gold, fontFace: "Calibri" });
  nexts.forEach((n, i) => {
    s.addText(n, { x: 5.3, y: 1.75 + i * 0.6, w: 4.2, h: 0.5,
      fontSize: 11, color: C.white, fontFace: "Calibri" });
  });

  s.addText("Thank You", {
    x: 0.6, y: 5.0, w: 9, h: 0.45,
    fontSize: 14, color: C.mint, italic: true, fontFace: "Calibri", align: "center"
  });
}

// ── Write file ────────────────────────────────────────────────
pres.writeFile({ fileName: "/mnt/user-data/outputs/HousePricePrediction_Presentation.pptx" })
  .then(() => console.log("✅ Presentation saved."))
  .catch(e => { console.error(e); process.exit(1); });
