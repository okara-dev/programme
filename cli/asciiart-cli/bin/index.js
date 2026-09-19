#!/usr/bin/env node

import readline from 'readline';
import fs from 'fs';
import path from 'path';
import { textToAscii, getFonts } from '../lib/text.js';
import { imageToAscii } from '../lib/image.js';
import { colorize, rainbow, rainbowVertical, gradient, listColors } from '../lib/colors.js';
import { animate } from '../lib/animate.js';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const c = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
  bold: '\x1b[1m',
  dim: '\x1b[2m'
};

function showBanner() {
  console.log(`
${c.bold}${c.magenta}╔═══════════════════════════════════════════════════════════════════╗
║              🎨 ASCII Art Generator - Text wird Kunst!           ║
║        Text → ASCII • Bilder → ASCII • Regenbogen-Farben!        ║
╚═══════════════════════════════════════════════════════════════════╝${c.reset}
`);
}

function showHelp() {
  console.log(`
${c.bold}Commands:${c.reset}
  ${c.green}text${c.reset} "<Text>" [--font big]      - Text zu ASCII
  ${c.green}rainbow${c.reset} "<Text>" [--font big]   - 🌈 Regenbogen (jedes Zeichen andere Farbe)
  ${c.green}rainbow-v${c.reset} "<Text>"             - 🌈 Regenbogen vertikal (Farbverlauf links→rechts)
  ${c.green}gradient${c.reset} "<Text>" [--font big]  - Farbverlauf über Zeilen
  ${c.green}color${c.reset} "<Text>" <farbe>         - Text in einer Farbe
  ${c.green}image${c.reset} <pfad> [--width 80]      - Bild zu ASCII
  ${c.green}fonts${c.reset}                          - Alle Fonts anzeigen
  ${c.green}animate${c.reset} "<Text>" <style>       - Text animieren
  ${c.green}save${c.reset} "<Text>" <datei>          - ASCII in Datei speichern
  ${c.green}help${c.reset}                           - Hilfe
  ${c.green}exit${c.reset}                           - Beenden

${c.dim}Verfügbare Farben:${c.reset}
  red, green, yellow, blue, magenta, cyan, white

${c.dim}Animationen:${c.reset}
  typewriter, fade, slide

${c.dim}Regenbogen-Farben:${c.reset}
  ${c.red}R${c.yellow}E${c.green}G${c.cyan}E${c.blue}N${c.magenta}B${c.red}O${c.yellow}G${c.green}E${c.cyan}N${c.reset}

${c.dim}Beispiele:${c.reset}
  asciiart text "Hello"
  asciiart rainbow "Hallo Welt!" --font Big
  asciiart rainbow-v "ONUR"
  asciiart color "Warnung" red
  asciiart image logo.png --width 80
  asciiart animate "Loading" typewriter
`);
}

// ============================================================
// TEXT (ohne Farbe)
// ============================================================

async function handleText(args) {
  const { text, font } = parseTextArgs(args);

  if (!text) {
    console.log(`${c.yellow}Usage: text "Dein Text" [--font big]${c.reset}`);
    return;
  }

  try {
    const art = await textToAscii(text, font);
    console.log(`\n${art}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// REGENBOGEN (horizontal - jedes Zeichen andere Farbe)
// ============================================================

async function handleRainbow(args) {
  const { text, font } = parseTextArgs(args);

  if (!text) {
    console.log(`${c.yellow}Usage: rainbow "Dein Text" [--font big]${c.reset}`);
    return;
  }

  try {
    const art = await textToAscii(text, font);
    const rainbowArt = rainbow(art);
    console.log(`\n${rainbowArt}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// REGENBOGEN vertikal (Farbverlauf links → rechts)
// ============================================================

async function handleRainbowVertical(args) {
  const { text, font } = parseTextArgs(args);

  if (!text) {
    console.log(`${c.yellow}Usage: rainbow-v "Dein Text" [--font big]${c.reset}`);
    return;
  }

  try {
    const art = await textToAscii(text, font);
    const rainbowArt = rainbowVertical(art);
    console.log(`\n${rainbowArt}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// GRADIENT (Farbverlauf über Zeilen)
// ============================================================

async function handleGradient(args) {
  const { text, font } = parseTextArgs(args);

  if (!text) {
    console.log(`${c.yellow}Usage: gradient "Dein Text" [--font big]${c.reset}`);
    return;
  }

  try {
    const art = await textToAscii(text, font);
    const gradientArt = gradient(art);
    console.log(`\n${gradientArt}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// EINZELNE FARBE
// ============================================================

async function handleColor(args) {
  // Filtere --font raus
  const cleanArgs = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--font') {
      i++;
      continue;
    }
    cleanArgs.push(args[i]);
  }

  if (cleanArgs.length < 2) {
    console.log(`${c.yellow}Usage: color "Dein Text" <farbe>${c.reset}`);
    console.log(`${c.dim}Farben: ${listColors().join(', ')}${c.reset}`);
    return;
  }

  const color = cleanArgs[cleanArgs.length - 1].toLowerCase();
  const text = cleanArgs.slice(0, -1).join(' ');

  if (!listColors().includes(color)) {
    console.log(`${c.red}❌ Unbekannte Farbe: ${color}${c.reset}`);
    console.log(`${c.dim}Verfügbar: ${listColors().join(', ')}${c.reset}`);
    return;
  }

  try {
    const art = await textToAscii(text, 'Standard');
    const colored = colorize(art, color);
    console.log(`\n${colored}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// BILD ZU ASCII
// ============================================================

async function handleImage(args) {
  const cleanArgs = [];
  let width = 80;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--width') {
      width = parseInt(args[i + 1]) || 80;
      i++;
      continue;
    }
    cleanArgs.push(args[i]);
  }

  const imagePath = cleanArgs[0];

  if (!imagePath) {
    console.log(`${c.yellow}Usage: image <pfad> [--width 80]${c.reset}`);
    return;
  }

  if (!fs.existsSync(imagePath)) {
    console.log(`${c.red}❌ Datei nicht gefunden: ${imagePath}${c.reset}`);
    return;
  }

  console.log(`${c.dim}⏳ Lade Bild...${c.reset}`);

  try {
    const art = await imageToAscii(imagePath, width);
    console.log(`\n${art}\n`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
    console.log(`${c.dim}💡 Tipp: Installiere "sharp" mit: npm install sharp${c.reset}`);
  }
}

// ============================================================
// FONTS
// ============================================================

function handleFonts() {
  const fonts = getFonts();
  console.log(`\n${c.bold}📝 Verfügbare Fonts (${fonts.length}):${c.reset}`);
  console.log('='.repeat(50));
  fonts.forEach(f => console.log(`  ${c.cyan}•${c.reset} ${f}`));
  console.log(`\n${c.dim}Beispiel: asciiart text "Hi" --font Big${c.reset}`);
}

// ============================================================
// ANIMATION
// ============================================================

async function handleAnimate(args) {
  if (args.length < 2) {
    console.log(`${c.yellow}Usage: animate "Text" <typewriter|fade|slide>${c.reset}`);
    return;
  }

  const style = args[args.length - 1].toLowerCase();
  const text = args.slice(0, -1).join(' ');

  await animate(text, style);
}

// ============================================================
// SPEICHERN
// ============================================================

async function handleSave(args) {
  const cleanArgs = [];
  let font = 'Standard';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--font') {
      font = args[i + 1] || 'Standard';
      i++;
      continue;
    }
    cleanArgs.push(args[i]);
  }

  if (cleanArgs.length < 2) {
    console.log(`${c.yellow}Usage: save "Text" output.txt [--font Big]${c.reset}`);
    return;
  }

  const file = cleanArgs[cleanArgs.length - 1];
  const text = cleanArgs.slice(0, -1).join(' ');

  try {
    const art = await textToAscii(text, font);
    fs.writeFileSync(file, art, 'utf8');
    console.log(`${c.green}✅ Gespeichert in: ${path.resolve(file)}${c.reset}`);
  } catch (error) {
    console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
  }
}

// ============================================================
// HILFSFUNKTION: Argumente parsen
// ============================================================

function parseTextArgs(args) {
  let font = 'Standard';
  const textParts = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--font') {
      font = args[i + 1] || 'Standard';
      i++;
      continue;
    }
    textParts.push(args[i]);
  }

  return {
    text: textParts.join(' '),
    font
  };
}

// ============================================================
// MAIN
// ============================================================

async function main() {
  showBanner();
  showHelp();

  console.log(`\n${c.dim}💡 Tipp: 'rainbow "Hallo"' für Regenbogen-Text! 🌈${c.reset}`);
  console.log('─'.repeat(50));

  rl.on('line', async (input) => {
    // Anführungszeichen korrekt parsen
    const tokens = input.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
    const cleanTokens = tokens.map(t => t.replace(/^"|"$/g, ''));
    const cmd = cleanTokens[0]?.toLowerCase();
    const args = cleanTokens.slice(1);

    try {
      switch (cmd) {
        case 'text':
        case 't':
          await handleText(args);
          break;

        case 'rainbow':
        case 'r':
        case 'rb':
          await handleRainbow(args);
          break;

        case 'rainbow-v':
        case 'rb-v':
        case 'rainbow-v':
          await handleRainbowVertical(args);
          break;

        case 'gradient':
        case 'g':
          await handleGradient(args);
          break;

        case 'color':
        case 'c':
          await handleColor(args);
          break;

        case 'image':
        case 'img':
        case 'i':
          await handleImage(args);
          break;

        case 'fonts':
        case 'f':
          handleFonts();
          break;

        case 'animate':
        case 'a':
          await handleAnimate(args);
          break;

        case 'save':
        case 's':
          await handleSave(args);
          break;

        case 'help':
        case 'h':
          showHelp();
          break;

        case 'exit':
        case 'quit':
        case 'q':
          console.log(`\n${c.bold}👋 Tschüss!${c.reset}`);
          process.exit(0);
          break;

        default:
          if (cmd) {
            console.log(`${c.red}❌ Unbekannter Befehl: ${cmd}${c.reset}`);
            console.log(`${c.yellow}💡 Tippe 'help' für Hilfe${c.reset}`);
          }
      }
    } catch (error) {
      console.log(`${c.red}❌ Fehler: ${error.message}${c.reset}`);
    }
  });

  process.stdout.write(`\n${c.magenta}asciiart${c.reset}> `);
}

process.on('uncaughtException', (error) => {
  console.log(`${c.red}❌ Unerwarteter Fehler: ${error.message}${c.reset}`);
});

main();