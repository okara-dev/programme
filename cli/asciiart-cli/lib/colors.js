// ANSI Farbcodes
const ANSI = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

// Zusätzliche Farben (256-Farben Modus)
const EXTENDED = {
  orange: '\x1b[38;5;208m',
  pink: '\x1b[38;5;213m',
  purple: '\x1b[38;5;93m',
  lime: '\x1b[38;5;118m',
  teal: '\x1b[38;5;30m',
  gold: '\x1b[38;5;220m'
};

// Regenbogen-Reihenfolge (7 Farben)
export const RAINBOW_COLORS = [
  ANSI.red,
  EXTENDED.orange,
  ANSI.yellow,
  ANSI.green,
  ANSI.cyan,
  ANSI.blue,
  ANSI.magenta
];

/**
 * Färbt den gesamten Text in einer Farbe
 */
export function colorize(text, color) {
  const code = ANSI[color.toLowerCase()] || EXTENDED[color.toLowerCase()] || ANSI.white;
  return `${code}${text}${ANSI.reset}`;
}

/**
 * 🌈 REGENBOGEN (horizontal)
 * JEDES ZEICHEN bekommt eine andere Regenbogenfarbe.
 *
 * H (rot) → a (orange) → l (gelb) → l (grün) → o (cyan) → ! (blau)
 */
export function rainbow(text) {
  let result = '';
  let colorIndex = 0;

  for (const char of text) {
    // Newline: kein Farbe, aber Farbindex weiterdrehen
    if (char === '\n') {
      result += char;
      continue;
    }

    // Leerzeichen: keine Farbe, aber Farbindex weiterdrehen
    if (char === ' ') {
      result += char;
      colorIndex = (colorIndex + 1) % RAINBOW_COLORS.length;
      continue;
    }

    const color = RAINBOW_COLORS[colorIndex % RAINBOW_COLORS.length];
    result += `${color}${char}${ANSI.reset}`;
    colorIndex++;
  }

  return result;
}

/**
 * 🌈 REGENBOGEN vertikal
 * Die Farbe richtet sich nach der Spaltenposition.
 * Links = rot, rechts = magenta → Verlauf über das ganze Bild.
 */
export function rainbowVertical(text) {
  const lines = text.split('\n');
  const maxLength = Math.max(...lines.map(l => l.length), 1);
  let result = '';

  for (const line of lines) {
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === ' ') {
        result += char;
        continue;
      }
      const colorIndex = Math.floor((i / maxLength) * RAINBOW_COLORS.length);
      const color = RAINBOW_COLORS[colorIndex % RAINBOW_COLORS.length];
      result += `${color}${char}${ANSI.reset}`;
    }
    result += '\n';
  }

  return result.replace(/\n$/, '');
}

/**
 * GRADIENT
 * Farbverlauf über die Zeilen (oben → unten).
 */
export function gradient(text) {
  const lines = text.split('\n');
  let result = '';

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const colorIndex = Math.floor((i / Math.max(lines.length, 1)) * RAINBOW_COLORS.length);
    const color = RAINBOW_COLORS[colorIndex % RAINBOW_COLORS.length];
    result += `${color}${line}${ANSI.reset}\n`;
  }

  return result.replace(/\n$/, '');
}

/**
 * Liste aller verfügbaren Farben (Namen)
 */
export function listColors() {
  return [
    ...Object.keys(ANSI).filter(k => k !== 'reset'),
    ...Object.keys(EXTENDED)
  ];
}