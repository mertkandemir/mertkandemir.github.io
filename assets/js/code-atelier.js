const atelier = document.querySelector('[data-code-atelier]');

if (atelier) {
  const tabs = [...atelier.querySelectorAll('[role="tab"]')];
  const preview = atelier.querySelector('[data-preview]');
  const status = atelier.querySelector('[data-status]');
  const inputs = Object.fromEntries(
    [...atelier.querySelectorAll('[data-code-input]')].map((input) => [input.name, input]),
  );

  const starter = {
    html: `<main class="signal-card">
  <p class="eyebrow">SYSTEM / ONLINE</p>
  <h1>Make the complex<br><em>feel simple.</em></h1>
  <div class="metric">
    <span>Production clarity</span>
    <strong id="score">92.4%</strong>
  </div>
  <button id="pulse" type="button">Run signal</button>
</main>`,
    css: `:root {
  color-scheme: light;
  font-family: Arial, sans-serif;
  background: #e9e4da;
  color: #171a1d;
}

body {
  min-height: 100vh;
  margin: 0;
  display: grid;
  place-items: center;
}

.signal-card {
  width: min(420px, 76vw);
  border-top: 2px solid #9d7542;
  padding: 32px;
  background: #f6f2ea;
  box-shadow: 0 24px 60px #2d29251f;
}

.eyebrow {
  color: #9d7542;
  font: 11px monospace;
  letter-spacing: .14em;
}

h1 {
  margin: 42px 0;
  font: 42px/1 Georgia, serif;
  letter-spacing: -.04em;
}

h1 em { color: #9d7542; font-weight: 400; }
.metric { display: flex; justify-content: space-between; }
.metric span { color: #6f6d69; }

button {
  margin-top: 24px;
  border: 0;
  padding: 12px 18px;
  background: #171a1d;
  color: #f6f2ea;
  cursor: pointer;
}`,
    js: `const button = document.querySelector('#pulse');
const score = document.querySelector('#score');

button.addEventListener('click', () => {
  const value = (90 + Math.random() * 9).toFixed(1);
  score.textContent = value + '%';
  button.textContent = 'Signal received';
});`,
  };

  const render = () => {
    const policy = "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'";
    preview.srcdoc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="${policy}"><style>${inputs.css.value}</style></head><body>${inputs.html.value}<script>${inputs.js.value}<\/script></body></html>`;
    status.textContent = atelier.dataset.updated;
  };

  const restore = () => {
    for (const [language, code] of Object.entries(starter)) inputs[language].value = code;
    render();
    status.textContent = atelier.dataset.resetDone;
  };

  const activateTab = (tab, moveFocus = true) => {
    for (const candidate of tabs) {
      const selected = candidate === tab;
      candidate.setAttribute('aria-selected', String(selected));
      candidate.tabIndex = selected ? 0 : -1;
      document.getElementById(candidate.getAttribute('aria-controls')).hidden = !selected;
    }
    if (moveFocus) tab.focus();
  };

  atelier.querySelector('[role="tablist"]').addEventListener('click', (event) => {
    const tab = event.target.closest('[role="tab"]');
    if (tab) activateTab(tab, false);
  });

  atelier.querySelector('[role="tablist"]').addEventListener('keydown', (event) => {
    const current = tabs.indexOf(event.target);
    if (current < 0) return;
    let next = current;
    if (event.key === 'ArrowRight') next = (current + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (current - 1 + tabs.length) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    activateTab(tabs[next]);
  });

  for (const input of Object.values(inputs)) {
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        event.preventDefault();
        input.setRangeText('  ', input.selectionStart, input.selectionEnd, 'end');
      }
      if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        render();
      }
    });
  }

  atelier.querySelector('[data-run]').addEventListener('click', render);
  atelier.querySelector('[data-reset]').addEventListener('click', restore);
  restore();
}
