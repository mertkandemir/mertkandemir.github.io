const atelier = document.querySelector('[data-code-atelier]');

if (atelier) {
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

  const copy = atelier.dataset.lang === 'tr' ? {
    plan: 'Planlanan miktar', actual: 'Gerçekleşen miktar', difference: 'Fark', status: 'Başarılı',
    start: 'Başlangıç tarihi', finish: 'Ay sonu tarihi', days: 'Ayın gün sayısı',
    main: 'Ana malzeme maliyeti', reuse: 'Geri kullanım maliyeti', extra: 'Ek maliyet', total: 'Toplam',
  } : {
    plan: 'Planned quantity', actual: 'Actual quantity', difference: 'Difference', status: 'Successful',
    start: 'Start date', finish: 'Month-end date', days: 'Days in month',
    main: 'Main material cost', reuse: 'Reuse material cost', extra: 'Additional cost', total: 'Total',
  };

  const scenarios = {
    production: {
      fields: [
        { label: copy.plan, type: 'number', value: '100' },
        { label: copy.actual, type: 'number', value: '92' },
      ],
      code: ({ first, second }) => `PLANQTY = ${first};
ACTUALQTY = ${second};
DIFFQTY = ACTUALQTY - PLANQTY;

IF DIFFQTY == 0 THEN
    RESULTTEXT = 'Tam eşleşme';
ELSE
    RESULTTEXT = 'Üretim farkı';
ENDIF;`,
      result: ({ first, second }) => {
        const plan = Number(first) || 0;
        const actual = Number(second) || 0;
        return { labels: [copy.plan, copy.actual, copy.difference], values: [plan, actual, actual - plan] };
      },
    },
    date: {
      fields: [{ label: copy.start, type: 'date', value: '2026-11-28' }],
      code: () => `TXTSTARTDATE = SYS_CURRENTDATE;
TXTFINISHDATE = ADDDAYS(
    ADDMONTHS(
        DATE(YEAR(TXTSTARTDATE), MONTH(TXTSTARTDATE), 1),
        1
    ),
    -1
);`,
      result: ({ first }) => {
        const parts = first.split('-').map(Number);
        const safe = parts.length === 3 ? parts : [2026, 11, 28];
        const lastDay = new Date(safe[0], safe[1], 0).getDate();
        const format = (year, month, day) => `${String(day).padStart(2, '0')}.${String(month).padStart(2, '0')}.${year}`;
        return { labels: [copy.start, copy.finish, copy.days], values: [format(...safe), format(safe[0], safe[1], lastDay), lastDay] };
      },
    },
    cost: {
      fields: [
        { label: copy.main, type: 'number', value: '128450' },
        { label: copy.reuse, type: 'number', value: '12400' },
        { label: copy.extra, type: 'number', value: '6800' },
      ],
      code: ({ first, second, third }) => `MAINMAT = ${first};
REUSEMAT = ${second};
EXTRACOST = ${third};

TOTALMAT = MAINMAT - REUSEMAT + EXTRACOST;`,
      result: ({ first, second, third }) => {
        const main = Number(first) || 0;
        const reuse = Number(second) || 0;
        const extra = Number(third) || 0;
        return { labels: [copy.main, copy.reuse, copy.total], values: [main, reuse, main - reuse + extra] };
      },
    },
  };

  const renderWeb = () => {
    const policy = "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'";
    preview.srcdoc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="${policy}"><style>${inputs.css.value}</style></head><body>${inputs.html.value}<script>${inputs.js.value}<\/script></body></html>`;
    status.textContent = atelier.dataset.updated;
  };

  const restoreWeb = () => {
    for (const [language, code] of Object.entries(starter)) inputs[language].value = code;
    renderWeb();
    status.textContent = atelier.dataset.resetDone;
  };

  const bindTabs = (tablist, tabs, panels, keyFor) => {
    const activate = (tab, moveFocus = true) => {
      const selectedKey = keyFor(tab);
      for (const candidate of tabs) {
        const selected = candidate === tab;
        candidate.setAttribute('aria-selected', String(selected));
        candidate.tabIndex = selected ? 0 : -1;
      }
      for (const panel of panels) panel.hidden = keyFor(panel) !== selectedKey;
      tab.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      if (moveFocus) tab.focus();
    };

    tablist.addEventListener('click', (event) => {
      const tab = event.target.closest('[role="tab"]');
      if (tab && tabs.includes(tab)) activate(tab, false);
    });

    tablist.addEventListener('keydown', (event) => {
      const current = tabs.indexOf(event.target);
      if (current < 0) return;
      let next = current;
      if (event.key === 'ArrowRight') next = (current + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (current - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(tabs[next]);
    });
  };

  const labTabs = [...atelier.querySelectorAll('[data-lab-tab]')];
  const labPanels = [...atelier.querySelectorAll('[data-lab-panel]')];
  bindTabs(labTabs[0].parentElement, labTabs, labPanels, (element) => element.dataset.labTab || element.dataset.labPanel);

  const codeTablist = atelier.querySelector('[data-code-tabs]');
  const codeTabs = [...codeTablist.querySelectorAll('[role="tab"]')];
  const codePanels = [...atelier.querySelectorAll('.atelier-panel')];
  bindTabs(codeTablist, codeTabs, codePanels, (element) => element.dataset.language || element.id.replace('panel-', ''));

  for (const input of Object.values(inputs)) {
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        event.preventDefault();
        input.setRangeText('  ', input.selectionStart, input.selectionEnd, 'end');
      }
      if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        renderWeb();
      }
    });
  }

  const troiaForm = atelier.querySelector('[data-troia-form]');
  const troiaCode = atelier.querySelector('[data-troia-code]');
  const scenarioButtons = [...atelier.querySelectorAll('[data-scenario]')];
  const fieldRows = [...troiaForm.querySelectorAll('[data-field]')];
  const outputLabels = [...atelier.querySelectorAll('[data-output-label]')];
  const outputValues = [...atelier.querySelectorAll('[data-output-value]')];
  let activeScenario = 'production';

  const values = () => Object.fromEntries(new FormData(troiaForm).entries());

  const renderTroia = () => {
    const result = scenarios[activeScenario].result(values());
    result.labels.forEach((label, index) => { outputLabels[index].textContent = label; });
    result.values.forEach((value, index) => { outputValues[index].textContent = Number.isFinite(value) ? new Intl.NumberFormat(atelier.dataset.lang).format(value) : value; });
    outputValues[3].textContent = copy.status;
    troiaCode.textContent = scenarios[activeScenario].code(values());
    status.textContent = atelier.dataset.troiaUpdated;
  };

  const selectScenario = (name) => {
    activeScenario = name;
    const scenario = scenarios[name];
    scenarioButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.scenario === name)));
    fieldRows.forEach((row, index) => {
      const field = scenario.fields[index];
      row.hidden = !field;
      if (!field) return;
      const input = row.querySelector('input');
      row.querySelector('[data-field-label]').textContent = field.label;
      input.type = field.type;
      input.value = field.value;
    });
    renderTroia();
  };

  scenarioButtons.forEach((button) => button.addEventListener('click', () => selectScenario(button.dataset.scenario)));
  troiaForm.addEventListener('submit', (event) => { event.preventDefault(); renderTroia(); });
  atelier.querySelector('[data-run]').addEventListener('click', renderWeb);
  atelier.querySelector('[data-reset]').addEventListener('click', restoreWeb);

  restoreWeb();
  selectScenario('production');
}
