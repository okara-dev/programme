const c = {
  reset: '\x1b[0m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
  bold: '\x1b[1m'
};

/**
 * Animiert Text im Terminal
 */
export async function animate(text, style = 'typewriter') {
  switch (style) {
    case 'typewriter':
      await typewriter(text);
      break;
    case 'fade':
      await fade(text);
      break;
    case 'slide':
      await slide(text);
      break;
    default:
      console.log(`❌ Unbekannter Stil: ${style}`);
      console.log('Verfügbar: typewriter, fade, slide');
  }
}

async function typewriter(text) {
  process.stdout.write('\n');
  for (const char of text) {
    process.stdout.write(c.cyan + char + c.reset);
    await sleep(80);
  }
  process.stdout.write('\n\n');
}

async function fade(text) {
  const steps = 4;
  process.stdout.write('\n');
  for (let i = 0; i < steps; i++) {
    process.stdout.write('\r' + ' '.repeat(text.length));
    await sleep(150);
    process.stdout.write('\r' + c.bold + c.magenta + text + c.reset);
    await sleep(150);
  }
  process.stdout.write('\n\n');
}

async function slide(text) {
  const width = process.stdout.columns || 80;
  for (let i = width; i >= 0; i -= 3) {
    process.stdout.write('\r' + ' '.repeat(i) + c.cyan + text + c.reset);
    await sleep(20);
  }
  process.stdout.write('\n\n');
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}