(() => {
  const article = document.querySelector('.md-text');
  if (!article) return;

  const STORAGE_KEY = 'stellar-reader-font-size';

  const presets = [
    {
      label: 'A−',
      fontSize: '18px',
      mathZoom: 1.24,
      title: '较小：18px'
    },
    {
      label: 'A',
      fontSize: '20px',
      mathZoom: 1.32,
      title: '标准：20px'
    },
    {
      label: 'A+',
      fontSize: '22px',
      mathZoom: 1.40,
      title: '推荐：22px'
    },
    {
      label: 'A++',
      fontSize: '24px',
      mathZoom: 1.48,
      title: '较大：24px'
    },
    {
      label: 'A+++',
      fontSize: '26px',
      mathZoom: 1.56,
      title: '最大：26px'
    }
  ];

  const saved = localStorage.getItem(STORAGE_KEY);

  /*
   * 旧版保存的是 rem。
   * 自动迁移到最接近的新档位。
   */
  const legacyMap = {
    '1rem': '18px',
    '1.125rem': '20px',
    '1.25rem': '22px'
  };

  const normalizedSaved = legacyMap[saved] || saved;

  const current =
    presets.find(item => item.fontSize === normalizedSaved) ||
    presets[2];

  function applyPreset(item) {
    document.documentElement.style.setProperty(
      '--article-font-size',
      item.fontSize
    );

    document.documentElement.style.setProperty(
      '--inline-math-zoom',
      item.mathZoom
    );
  }

  applyPreset(current);

  const control = document.createElement('div');
  control.className = 'reader-size-control';
  control.setAttribute('aria-label', '文章字号');

  presets.forEach(item => {
    const button = document.createElement('button');

    button.type = 'button';
    button.textContent = item.label;
    button.title = item.title;

    if (item.fontSize === current.fontSize) {
      button.classList.add('active');
    }

    button.addEventListener('click', () => {
      applyPreset(item);

      localStorage.setItem(
        STORAGE_KEY,
        item.fontSize
      );

      control
        .querySelectorAll('button')
        .forEach(btn => btn.classList.remove('active'));

      button.classList.add('active');
    });

    control.appendChild(button);
  });

  document.body.appendChild(control);
})();