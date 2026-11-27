const productionDemo = document.querySelector('[data-production-demo]');

if (productionDemo) {
  const plan = productionDemo.elements.namedItem('plan');
  const actual = productionDemo.elements.namedItem('actual');
  const difference = productionDemo.querySelector('output');
  const formatter = new Intl.NumberFormat(document.documentElement.lang, { signDisplay: 'exceptZero' });

  const update = () => {
    for (const input of [plan, actual]) {
      productionDemo.querySelector(`[data-${input.name}]`).textContent = input.value;
      input.style.setProperty('--level', `${input.valueAsNumber / Number(input.max) * 100}%`);
    }
    const change = actual.valueAsNumber - plan.valueAsNumber;
    difference.value = formatter.format(change);
    difference.dataset.result = Math.sign(change);
  };

  productionDemo.addEventListener('input', update);
  productionDemo.addEventListener('reset', () => requestAnimationFrame(update));
  productionDemo.querySelector('fieldset').disabled = false;
  update();
}
