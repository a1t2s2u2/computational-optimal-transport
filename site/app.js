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

function setGlossary(term) {
  const box = document.querySelector("#glossary-box");
  const item = glossary[term];
  if (!box || !item) return;
  const header = box.closest(".glossary-panel")?.querySelector("h2");
  if (header) header.textContent = "用語";
  box.innerHTML = `<h3>${item.title}</h3><p>${item.body}</p>`;
  if (window.MathJax?.typesetPromise) {
    window.MathJax.typesetPromise([box]);
  }
}

function showBlock(name) {
  const blocks = window.__blocks || [];
  const block = blocks.find((b) => b.name === name);
  if (!block) return;
  const box = document.querySelector("#glossary-box");
  if (!box) return;
  const header = box.closest(".glossary-panel")?.querySelector("h2");
  const color = block.type === "definition" ? "var(--teal)" : "var(--indigo)";
  const label = block.type === "definition" ? "定義" : "定理";
  if (header) header.textContent = label;
  box.innerHTML = `<div class="block-preview" style="border-left: 4px solid ${color}; padding-left: 12px;">${block.html}</div>`;
  const target = document.getElementById(block.id);
  if (target) {
    box.innerHTML += `<p class="ref-jump"><a href="#${block.id}">本文で見る →</a></p>`;
  }
  if (window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([box]);
  }
}

document.addEventListener("click", (e) => {
  const term = e.target.closest(".term");
  if (term) return setGlossary(term.dataset.term);
  const ref = e.target.closest(".ref");
  if (ref) return showBlock(ref.dataset.ref);
});

const navLinks = Array.from(document.querySelectorAll(".chapter-nav a"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`);
    });
  },
  { rootMargin: "-12% 0px -70% 0px", threshold: [0.1, 0.25, 0.5] }
);

sections.forEach((section) => observer.observe(section));

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
  const kernel = cost.map((row) => row.map((value) => Math.exp(-value / epsilon)));
  let u = Array(n).fill(1);
  let v = Array(m).fill(1);

  for (let step = 0; step < 70; step += 1) {
    u = u.map((_, i) => {
      const denom = kernel[i].reduce((sum, kij, j) => sum + kij * v[j], 0);
      return a[i] / denom;
    });
    v = v.map((_, j) => {
      const denom = kernel.reduce((sum, row, i) => sum + row[j] * u[i], 0);
      return b[j] / denom;
    });
  }

  return kernel.map((row, i) => row.map((kij, j) => u[i] * kij * v[j]));
}

function renderMatrix(target, values, mode) {
  const el = document.querySelector(target);
  if (!el) return;
  const flat = values.flat();
  const min = Math.min(...flat);
  const max = Math.max(...flat);
  el.innerHTML = "";

  values.flat().forEach((value) => {
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
