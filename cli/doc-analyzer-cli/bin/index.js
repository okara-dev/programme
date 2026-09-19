#!/usr/bin/env node

import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, '..', '.env') });

import fs from 'fs';
import readline from 'readline';
import { extractText, prepareTextForAI } from '../lib/extractor.js';
import { analyzeWithGroq } from '../lib/groq.js';
import { getFileType, getSupportedExtensions } from '../lib/formats.js';

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
║              📄 Doc Analyzer - KI-gestützte Analyse               ║
║           PDF • Word • TXT • HTML → Zusammenfassung              ║
╚═══════════════════════════════════════════════════════════════════╝${c.reset}
`);
}

function showHelp() {
  console.log(`
${c.bold}Usage:${c.reset}
  ${c.green}docanalyze${c.reset} <datei> [optionen]

${c.bold}Optionen:${c.reset}
  ${c.cyan}--mode${c.reset} <mode>       Analysemodus (Standard: analyze)
  ${c.cyan}--lang${c.reset} <sprache>   Sprache (Standard: Deutsch)
  ${c.cyan}--output${c.reset} <datei>    Antwort in Datei speichern
  ${c.cyan}--prompt${c.reset} "<text>"   Eigener Prompt

${c.bold}Modi:${c.reset}
  ${c.green}summary${c.reset}       Kurze Zusammenfassung
  ${c.green}analyze${c.reset}       Volle Analyse (Standard)
  ${c.green}explain${c.reset}       Einfach erklärt
  ${c.green}keypoints${c.reset}     Wichtigste Punkte als Liste

${c.bold}Unterstützte Formate:${c.reset}
  ${c.dim}${getSupportedExtensions().join('  ')}${c.reset}

${c.bold}Beispiele:${c.reset}
  docanalyze vertrag.pdf
  docanalyze bewerbung.docx --mode summary
  docanalyze dokument.txt --mode keypoints
  docanalyze bericht.pdf --mode explain --output analyse.txt
  docanalyze brief.txt --prompt "Ist dieser Brief wichtig?"
`);
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function parseArgs(args) {
  const opts = {
    file: null,
    mode: 'analyze',
    language: 'Deutsch',
    output: null,
    prompt: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--mode') {
      opts.mode = args[i + 1] || 'analyze';
      i++;
    } else if (arg === '--lang') {
      opts.language = args[i + 1] || 'Deutsch';
      i++;
    } else if (arg === '--output') {
      opts.output = args[i + 1];
      i++;
    } else if (arg === '--prompt') {
      opts.prompt = args[i + 1];
      i++;
    } else if (!arg.startsWith('--')) {
      if (!opts.file) opts.file = arg;
    }
  }

  return opts;
}

function loadingAnimation(text) {
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  let i = 0;
  process.stdout.write(`\r${c.cyan}${frames[0]} ${text}${c.reset}`);
  return setInterval(() => {
    i = (i + 1) % frames.length;
    process.stdout.write(`\r${c.cyan}${frames[i]} ${text}${c.reset}`);
  }, 80);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showBanner();
    showHelp();
    process.exit(0);
  }

  // API Key prüfen
  if (!process.env.GROQ_API_KEY) {
    console.log(`${c.red}❌ GROQ_API_KEY ist nicht gesetzt!${c.reset}`);
    console.log(`\n${c.yellow}So setzt du den Key:${c.reset}`);
    console.log(`  ${c.dim}Windows PowerShell:${c.reset}`);
    console.log(`    $env:GROQ_API_KEY = "gsk_..."`);
    console.log(`  ${c.dim}Windows CMD:${c.reset}`);
    console.log(`    set GROQ_API_KEY=gsk_...`);
    console.log(`  ${c.dim}Linux/Mac:${c.reset}`);
    console.log(`    export GROQ_API_KEY="gsk_..."`);
    process.exit(1);
  }

  const opts = parseArgs(args);

  if (!opts.file) {
    console.log(`${c.red}❌ Keine Datei angegeben!${c.reset}`);
    console.log(`${c.dim}Usage: docanalyze <datei> [--mode analyze]${c.reset}`);
    process.exit(1);
  }

  showBanner();

  const filePath = path.resolve(opts.file);

  // Existiert?
  if (!fs.existsSync(filePath)) {
    console.log(`${c.red}❌ Datei nicht gefunden: ${filePath}${c.reset}`);
    process.exit(1);
  }

  const stats = fs.statSync(filePath);
  if (stats.isDirectory()) {
    console.log(`${c.red}❌ "${opts.file}" ist ein Ordner, keine Datei!${c.reset}`);
    process.exit(1);
  }

  // Format prüfen
  const fileType = getFileType(filePath);
  if (!fileType) {
    console.log(`${c.red}❌ Nicht unterstütztes Format: ${path.extname(filePath)}${c.reset}`);
    console.log(`${c.dim}Unterstützt: ${getSupportedExtensions().join(', ')}${c.reset}`);
    process.exit(1);
  }

  // Header
  console.log(`${c.bold}📄 Datei:${c.reset}     ${path.basename(filePath)}`);
  console.log(`${c.bold}📏 Größe:${c.reset}     ${formatBytes(stats.size)}`);
  console.log(`${c.bold}📋 Format:${c.reset}    ${fileType.toUpperCase()}`);
  console.log(`${c.bold}🔍 Modus:${c.reset}     ${opts.mode}`);
  console.log('─'.repeat(60));

  // 1. Text extrahieren
  console.log(`\n${c.dim}📖 Lese Datei...${c.reset}`);
  let extracted;

  try {
    extracted = await extractText(filePath);
  } catch (error) {
    console.log(`${c.red}❌ Fehler beim Lesen: ${error.message}${c.reset}`);
    process.exit(1);
  }

  if (!extracted.text || extracted.text.trim().length === 0) {
    console.log(`${c.red}❌ Kein Text in der Datei gefunden!${c.reset}`);
    console.log(`${c.dim}Tipp: Bei gescannten PDFs wird OCR benötigt.${c.reset}`);
    process.exit(1);
  }

  console.log(`  ${c.green}✅ Text extrahiert:${c.reset} ${extracted.text.length.toLocaleString()} Zeichen`);
  if (extracted.pages) {
    console.log(`  ${c.green}✅ Seiten:${c.reset} ${extracted.pages}`);
  }

  // 2. Text für KI vorbereiten
  const { text: preparedText, truncated } = prepareTextForAI(extracted.text);

  if (truncated) {
    console.log(`  ${c.yellow}⚠️  Text gekürzt auf ${preparedText.length.toLocaleString()} Zeichen (zu lang)${c.reset}`);
  }

  // 3. KI-Analyse
  console.log(`\n${c.dim}🤖 Sende an Groq KI...${c.reset}`);
  const spinner = loadingAnimation('Analysiere mit groq/compound-mini...');

  let result;
  try {
    result = await analyzeWithGroq(preparedText, {
      mode: opts.mode,
      language: opts.language,
      prompt: opts.prompt
    });
  } catch (error) {
    clearInterval(spinner);
    process.stdout.write('\r' + ' '.repeat(60) + '\r');
    console.log(`${c.red}❌ KI-Fehler: ${error.message}${c.reset}`);
    process.exit(1);
  }

  clearInterval(spinner);
  process.stdout.write('\r' + ' '.repeat(60) + '\r');

  // 4. Ergebnis anzeigen
  console.log(`\n${c.bold}${c.green}📊 Ergebnis:${c.reset}`);
  console.log('='.repeat(60));
  console.log('');
  console.log(result.result);
  console.log('');
  console.log('='.repeat(60));
  console.log(`${c.dim}Tokens: ${result.tokens} | Modell: ${result.model}${c.reset}`);

  // 5. Optional: Speichern
  if (opts.output) {
    const outputPath = path.resolve(opts.output);
    const content = `# Analyse: ${path.basename(filePath)}\n\n` +
                    `**Datum:** ${new Date().toLocaleString()}\n` +
                    `**Modus:** ${opts.mode}\n` +
                    `**Tokens:** ${result.tokens}\n\n` +
                    `---\n\n${result.result}\n`;
    fs.writeFileSync(outputPath, content, 'utf8');
    console.log(`\n${c.green}💾 Gespeichert: ${outputPath}${c.reset}`);
  }

  console.log('');
  rl.close();
}

main().catch(error => {
  console.log(`${c.red}❌ Unerwarteter Fehler: ${error.message}${c.reset}`);
  process.exit(1);
});