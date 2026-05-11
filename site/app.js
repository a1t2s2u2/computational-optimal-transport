/* ==========================================================================
   Living Mathematical Manuscript — Interactions
   ========================================================================== */

/* ---------- Glossary ---------- */

const glossary = {
  polish: {
    title: "Polish 空間",
    body: "完備かつ可分な距離空間。確率測度の弱収束やカップリングの存在を扱いやすい。"
  },
  coupling: {
    title: "カップリング",
    body: "二つの周辺分布を固定した積空間上の確率測度。Kantorovich 緩和の未知量。"
  },
  entropy: {
    title: "離散エントロピー / エントロピー正則化",
    body: "離散エントロピーは \\(H(P)=-\\sum_{ij}P_{ij}(\\log P_{ij}-1)\\)。正則化では線形コストに \\(-\\varepsilon H(P)\\) を加える。"
  },
  kl: {
    title: "KL ダイバージェンス",
    body: "非負行列 \\(P,K\\) の差を測る量。\\(\\sum_{ij}P_{ij}\\log(P_{ij}/K_{ij})-P_{ij}+K_{ij}\\) で定義する。"
  },
  gibbs: {
    title: "Gibbs カーネル",
    body: "コスト行列から作る正行列。\\(K_{ij}=\\exp(-C_{ij}/\\varepsilon)\\)。Sinkhorn はこの行列を周辺制約に合わせてスケーリングする。"
  },
  sinkhorn: {
    title: "Sinkhorn 反復",
    body: "Gibbs カーネルを行方向と列方向に交互にスケールし、指定された周辺分布に合わせる反復。KL 交互射影、双対の交互最大化としても解釈できる。"
  }
};

/* ---------- Reading Progress ---------- */

const progressFill = document.querySelector(".reading-progress__fill");

function updateProgress() {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  if (docHeight > 0 && progressFill) {
    progressFill.style.width = (scrollTop / docHeight) * 100 + "%";
  }
}

window.addEventListener("scroll", updateProgress, { passive: true });

/* ---------- Navigation Rail ---------- */

const rail = document.querySelector(".nav-rail");
const railMark = document.querySelector(".nav-rail__mark");
const navNodes = document.querySelectorAll(".nav-rail__node");
const chapters = Array.from(navNodes)
  .map((n) => document.querySelector(n.getAttribute("href")))
  .filter(Boolean);

if (railMark) {
  railMark.addEventListener("click", () => {
    rail.classList.toggle("is-expanded");
  });
  document.addEventListener("click", (e) => {
    if (rail && !rail.contains(e.target)) {
      rail.classList.remove("is-expanded");
    }
  });
}

const chapterObserver = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((e) => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    navNodes.forEach((node) => {
      node.classList.toggle(
        "is-active",
        node.getAttribute("href") === `#${visible.target.id}`
      );
    });
  },
  { rootMargin: "-10% 0px -70% 0px", threshold: [0, 0.1, 0.25, 0.5] }
);

chapters.forEach((ch) => chapterObserver.observe(ch));

/* ---------- Block Reference: Floating Cards ---------- */

const marginCol = document.querySelector(".margin-col");
const refSheet = document.getElementById("ref-sheet");
const MAX_CARDS = 3;
let activeCards = [];

const typeLabels = { definition: "定義", theorem: "定理", remark: "注意", example: "例", algorithm: "アルゴリズム" };
const typeColors = {
  definition: "var(--teal)",
  theorem: "var(--indigo)",
  remark: "var(--muted)",
  example: "var(--wine)",
  algorithm: "var(--amber)"
};

function createMarginCard(block, sourceEl) {
  if (activeCards.length >= MAX_CARDS) {
    const oldest = activeCards.shift();
    oldest.remove();
  }

  const card = document.createElement("div");
  card.className = "context-card";
  card.dataset.blockId = block.id;

  card.innerHTML =
    `<div class="context-card__header">` +
    `<span class="context-card__type" style="color:${typeColors[block.type] || "var(--teal)"}">${typeLabels[block.type] || "参照"}</span>` +
    `<button class="context-card__close" type="button" aria-label="閉じる">&times;</button>` +
    `</div>` +
    `<div class="context-card__body">${block.html}</div>` +
    `<a class="context-card__jump" href="#${block.id}">本文で見る &rarr;</a>`;

  const proseEl = document.querySelector(".prose");
  if (proseEl && marginCol) {
    const sourceY = sourceEl.getBoundingClientRect().top + window.scrollY;
    const proseY = proseEl.getBoundingClientRect().top + window.scrollY;
    let targetTop = sourceY - proseY;

    for (const existing of activeCards) {
      const eBottom = existing.offsetTop + existing.offsetHeight;
      if (targetTop < eBottom + 12) {
        targetTop = eBottom + 12;
      }
    }

    card.style.top = targetTop + "px";
  }

  card.querySelector(".context-card__close").addEventListener("click", () => {
    card.remove();
    activeCards = activeCards.filter((c) => c !== card);
  });

  if (marginCol) {
    marginCol.appendChild(card);
  }
  activeCards.push(card);

  if (window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([card]);
  }
}

function showRefMobile(block) {
  if (!refSheet) return;
  const content = refSheet.querySelector(".ref-sheet__content");
  if (!content) return;
  const label = typeLabels[block.type] || "参照";
  content.innerHTML =
    `<h3 style="color:${typeColors[block.type] || "var(--teal)"}">${label}: ${block.name}</h3>` +
    `<div>${block.html}</div>` +
    `<p style="margin-top:12px"><a href="#${block.id}" style="color:var(--teal);text-decoration:none">本文で見る &rarr;</a></p>`;
  refSheet.showModal();
  if (window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([content]);
  }
}

/* ---------- Hover Tooltip ---------- */

let hoverTimeout = null;
let tooltip = null;

function showTooltip(refEl, block) {
  tooltip = document.createElement("div");
  tooltip.className = "ref-tooltip";
  const tmp = document.createElement("div");
  tmp.innerHTML = block.html;
  const text = tmp.textContent.slice(0, 100);
  tooltip.textContent = text + (tmp.textContent.length > 100 ? "..." : "");
  const rect = refEl.getBoundingClientRect();
  tooltip.style.top = rect.bottom + 6 + "px";
  tooltip.style.left = Math.min(rect.left, window.innerWidth - 340) + "px";
  document.body.appendChild(tooltip);
}

function hideTooltip() {
  clearTimeout(hoverTimeout);
  if (tooltip) {
    tooltip.remove();
    tooltip = null;
  }
}

document.addEventListener("mouseover", (e) => {
  const ref = e.target.closest(".ref");
  if (!ref) return;
  const blocks = window.__blocks || [];
  const block = blocks.find((b) => b.name === ref.dataset.ref);
  if (!block) return;
  hoverTimeout = setTimeout(() => showTooltip(ref, block), 400);
});

document.addEventListener("mouseout", (e) => {
  if (e.target.closest(".ref")) hideTooltip();
});

/* ---------- Click Handlers ---------- */

document.addEventListener("click", (e) => {
  const term = e.target.closest(".term");
  if (term) {
    const item = glossary[term.dataset.term];
    if (!item) return;
    const isWide = window.matchMedia("(min-width: 1200px)").matches;
    const fakeBlock = {
      id: "glossary-" + term.dataset.term,
      name: item.title,
      type: "definition",
      html: `<h3>${item.title}</h3><p>${item.body}</p>`
    };
    if (isWide && marginCol) {
      createMarginCard(fakeBlock, term);
    } else {
      showRefMobile(fakeBlock);
    }
    return;
  }

  const ref = e.target.closest(".ref");
  if (ref) {
    hideTooltip();
    const blocks = window.__blocks || [];
    const block = blocks.find((b) => b.name === ref.dataset.ref);
    if (!block) return;
    const isWide = window.matchMedia("(min-width: 1200px)").matches;
    if (isWide && marginCol) {
      createMarginCard(block, ref);
    } else {
      showRefMobile(block);
    }
    return;
  }
});

/* Close dialog */
if (refSheet) {
  const closeBtn = refSheet.querySelector(".ref-sheet__close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => refSheet.close());
  }
  refSheet.addEventListener("click", (e) => {
    if (e.target === refSheet) refSheet.close();
  });
}

/* ---------- Keyboard Navigation ---------- */

const allBlocks = document.querySelectorAll(
  ".block, .example-band, .margin-note"
);
let currentBlockIdx = -1;

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

  if (e.key === "j") {
    currentBlockIdx = Math.min(currentBlockIdx + 1, allBlocks.length - 1);
    allBlocks[currentBlockIdx]?.scrollIntoView({ behavior: "smooth", block: "center" });
    e.preventDefault();
  }
  if (e.key === "k") {
    currentBlockIdx = Math.max(currentBlockIdx - 1, 0);
    allBlocks[currentBlockIdx]?.scrollIntoView({ behavior: "smooth", block: "center" });
    e.preventDefault();
  }
  if (e.key === "Escape") {
    activeCards.forEach((c) => c.remove());
    activeCards = [];
    refSheet?.close();
  }
});

/* ---------- Sinkhorn Demo ---------- */

const cost = [
  [0.08, 0.46, 0.92, 1.28],
  [0.38, 0.12, 0.36, 0.84],
  [0.86, 0.42, 0.18, 0.44],
  [1.24, 0.74, 0.40, 0.10]
];

const a = [0.28, 0.22, 0.31, 0.19];
const b = [0.20, 0.30, 0.27, 0.23];

function sinkhorn(epsilon) {
  const n = cost.length;
  const m = cost[0].length;
  const kernel = cost.map((row) => row.map((v) => Math.exp(-v / epsilon)));
  let u = Array(n).fill(1);
  let v = Array(m).fill(1);
  for (let step = 0; step < 70; step++) {
    u = u.map((_, i) => a[i] / kernel[i].reduce((s, k, j) => s + k * v[j], 0));
    v = v.map((_, j) => b[j] / kernel.reduce((s, row, i) => s + row[j] * u[i], 0));
  }
  return kernel.map((row, i) => row.map((k, j) => u[i] * k * v[j]));
}

function renderMatrix(target, values, mode) {
  const el = document.querySelector(target);
  if (!el) return;
  const flat = values.flat();
  const min = Math.min(...flat);
  const max = Math.max(...flat);
  el.innerHTML = "";
  flat.forEach((value) => {
    const t = max === min ? 0 : (value - min) / (max - min);
    const hue = mode === "cost" ? 32 - t * 18 : 176 - t * 142;
    const lightness = mode === "cost" ? 94 - t * 30 : 94 - t * 42;
    const cell = document.createElement("span");
    cell.className = "cell";
    cell.style.background = `hsl(${hue} 72% ${lightness}%)`;
    cell.textContent = value.toFixed(2);
    el.appendChild(cell);
  });
}

function updateDemo() {
  const slider = document.querySelector("#epsilon-slider");
  const output = document.querySelector("#epsilon-value");
  if (!slider || !output) return;
  const epsilon = Number(slider.value);
  output.value = epsilon.toFixed(2);
  output.textContent = epsilon.toFixed(2);
  renderMatrix("#cost-matrix", cost, "cost");
  renderMatrix("#plan-matrix", sinkhorn(epsilon), "plan");
}

const slider = document.querySelector("#epsilon-slider");
if (slider) {
  slider.addEventListener("input", updateDemo);
  updateDemo();
}

/* ---------- Mermaid ---------- */

window.addEventListener("load", async () => {
  if (window.mermaid) {
    window.mermaid.initialize({
      startOnLoad: false,
      theme: "base",
      themeVariables: {
        primaryColor: "#d9f0ed",
        primaryTextColor: "#20262d",
        primaryBorderColor: "#0f766e",
        lineColor: "#64707d",
        secondaryColor: "#f6e8c4",
        tertiaryColor: "#e1e4ff"
      }
    });
    if (window.mermaid.run) {
      await window.mermaid.run({ querySelector: ".mermaid" });
    } else if (window.mermaid.init) {
      window.mermaid.init(undefined, document.querySelectorAll(".mermaid"));
    }
  }
});
