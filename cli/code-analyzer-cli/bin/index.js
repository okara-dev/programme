#!/usr/bin/env node

import readline from 'readline';
import fs from 'fs';
import path from 'path';
import { Analyzer } from '../lib/analyzer.js';
import { Reporter } from '../lib/reporter.js';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const colors = {
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

let analyzer = null;

function showBanner() {
  console.log(`
${colors.bold}${colors.cyan}╔═══════════════════════════════════════════════════════════════════╗
║              🔍 Code Analyzer - Understand Your Code!            ║
║       Analyze metrics, complexity, dependencies and quality       ║
╚═══════════════════════════════════════════════════════════════════╝${colors.reset}
`);
}

function showHelp() {
  console.log(`
${colors.bold}Commands:${colors.reset}
  ${colors.green}metrics${colors.reset} [path]              - Show code metrics
  ${colors.green}complexity${colors.reset} [path]          - Analyze code complexity
  ${colors.green}dependencies${colors.reset} [path]        - Analyze dependencies
  ${colors.green}quality${colors.reset} [path]             - Calculate code quality score
  ${colors.green}report${colors.reset} [path]              - Generate full report
  ${colors.green}help${colors.reset}                       - Show this help
  ${colors.green}exit${colors.reset}                       - Exit

${colors.dim}Examples:${colors.reset}
  code-analyzer metrics ./src
  code-analyzer complexity ./src
  code-analyzer dependencies ./src
  code-analyzer quality ./src
  code-analyzer report ./src --output report.md
`);
}

function showProgress(current, total, message = '') {
  const percentage = Math.round((current / total) * 100);
  const barLength = 30;
  const filled = Math.round((percentage / 100) * barLength);
  const empty = barLength - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);
  
  process.stdout.write(`\r${colors.dim}[${bar}] ${percentage}% ${message}${colors.reset}`);
  if (percentage === 100) {
    process.stdout.write('\n');
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function displayMetrics(metricsData) {
  console.log(`\n${colors.bold}📊 Code Metrics${colors.reset}`);
  console.log('='.repeat(50));
  
  console.log(`  ${colors.blue}Files:${colors.reset} ${metricsData.files}`);
  console.log(`  ${colors.blue}Total Lines:${colors.reset} ${metricsData.totalLines}`);
  console.log(`  ${colors.blue}Code Lines:${colors.reset} ${metricsData.codeLines}`);
  console.log(`  ${colors.blue}Comment Lines:${colors.reset} ${metricsData.commentLines}`);
  console.log(`  ${colors.blue}Blank Lines:${colors.reset} ${metricsData.blankLines}`);
  console.log(`  ${colors.blue}Functions:${colors.reset} ${metricsData.functions}`);
  console.log(`  ${colors.blue}Classes:${colors.reset} ${metricsData.classes}`);
  console.log(`  ${colors.blue}Imports:${colors.reset} ${metricsData.imports}`);
  
  if (metricsData.languages && Object.keys(metricsData.languages).length > 0) {
    console.log(`\n  ${colors.bold}Languages:${colors.reset}`);
    const sorted = Object.entries(metricsData.languages).sort((a, b) => b[1] - a[1]);
    sorted.forEach(([lang, count]) => {
      console.log(`    ${lang}: ${count} files`);
    });
  }

  if (metricsData.largestFiles && metricsData.largestFiles.length > 0) {
    console.log(`\n  ${colors.bold}Largest Files:${colors.reset}`);
    metricsData.largestFiles.slice(0, 5).forEach((file, i) => {
      console.log(`    ${i+1}. ${path.basename(file.path)} (${formatFileSize(file.size)})`);
    });
  }
}

function displayComplexity(complexity) {
  console.log(`\n${colors.bold}🌀 Code Complexity Report${colors.reset}`);
  console.log('='.repeat(50));

  const total = complexity.totalFunctions || 0;
  const avg = complexity.average || 0;
  const max = complexity.max || 0;

  console.log(`  ${colors.blue}Total Functions:${colors.reset} ${total}`);
  console.log(`  ${colors.blue}Average Complexity:${colors.reset} ${avg.toFixed(2)}`);
  console.log(`  ${colors.blue}Maximum Complexity:${colors.reset} ${max}`);
  
  if (complexity.complexFunctions && complexity.complexFunctions.length > 0) {
    console.log(`\n  ${colors.bold}Complex Functions (> 10):${colors.reset}`);
    complexity.complexFunctions.slice(0, 10).forEach(func => {
      const level = func.complexity > 20 ? colors.red : colors.yellow;
      console.log(`    ${level}${func.name}${colors.reset}: ${func.complexity} (${path.basename(func.file)}:${func.line})`);
    });
    if (complexity.complexFunctions.length > 10) {
      console.log(`    ${colors.dim}... and ${complexity.complexFunctions.length - 10} more${colors.reset}`);
    }
  } else {
    console.log(`\n  ${colors.green}✅ No complex functions found!${colors.reset}`);
  }
}

function displayDependencies(deps) {
  console.log(`\n${colors.bold}🔗 Dependencies Analysis${colors.reset}`);
  console.log('='.repeat(50));

  console.log(`  ${colors.blue}Total dependencies:${colors.reset} ${deps.total}`);
  console.log(`  ${colors.blue}Direct dependencies:${colors.reset} ${deps.direct}`);
  console.log(`  ${colors.blue}Dev dependencies:${colors.reset} ${deps.dev}`);

  if (deps.packages && deps.packages.length > 0) {
    console.log(`\n  ${colors.bold}Packages:${colors.reset}`);
    deps.packages.slice(0, 20).forEach(pkg => {
      const type = pkg.type === 'dev' ? colors.dim + '(dev)' : '';
      console.log(`    ${pkg.name}${colors.dim}@${pkg.version}${colors.reset} ${type}`);
    });
    if (deps.packages.length > 20) {
      console.log(`    ${colors.dim}... and ${deps.packages.length - 20} more${colors.reset}`);
    }
  }
}

function displayQuality(quality) {
  console.log(`\n${colors.bold}⭐ Code Quality Score${colors.reset}`);
  console.log('='.repeat(50));

  const score = quality.score || 0;
  const grade = quality.grade || 'F';
  
  const color = score >= 80 ? colors.green : score >= 60 ? colors.yellow : colors.red;
  
  console.log(`  ${colors.blue}Overall Score:${colors.reset} ${color}${score}/100${colors.reset} (${grade})`);
  
  if (quality.details) {
    console.log(`\n  ${colors.bold}Breakdown:${colors.reset}`);
    Object.entries(quality.details).forEach(([key, value]) => {
      const color2 = value >= 80 ? colors.green : value >= 60 ? colors.yellow : colors.red;
      console.log(`    ${key}: ${color2}${value}${colors.reset}`);
    });
  }

  if (quality.issues && quality.issues.length > 0) {
    console.log(`\n  ${colors.bold}Issues Found:${colors.reset}`);
    quality.issues.slice(0, 10).forEach(issue => {
      const color3 = issue.severity === 'high' ? colors.red : 
                    issue.severity === 'medium' ? colors.yellow : colors.blue;
      console.log(`    ${color3}• ${issue.message}${colors.reset}`);
      if (issue.file) {
        console.log(`      ${colors.dim}${path.basename(issue.file)}${colors.reset}`);
      }
    });
    if (quality.issues.length > 10) {
      console.log(`    ${colors.dim}... and ${quality.issues.length - 10} more issues${colors.reset}`);
    }
  } else {
    console.log(`\n  ${colors.green}✅ No issues found! Excellent code quality!${colors.reset}`);
  }
}

function displayReport(report) {
  console.log(`\n${report}`);
}

async function handleMetrics(args) {
  try {
    const targetPath = args[0] || '.';
    const absolutePath = path.resolve(targetPath);
    
    console.log(`\n${colors.bold}${colors.cyan}📊 Analyzing metrics for: ${absolutePath}${colors.reset}`);
    console.log('='.repeat(50));

    if (!fs.existsSync(absolutePath)) {
      console.log(`${colors.red}❌ Path does not exist: ${absolutePath}${colors.reset}`);
      return;
    }

    if (!fs.statSync(absolutePath).isDirectory()) {
      console.log(`${colors.red}❌ Not a directory: ${absolutePath}${colors.reset}`);
      return;
    }

    analyzer = new Analyzer(absolutePath);
    const metricsData = await analyzer.getMetrics((progress) => {
      showProgress(progress.current, progress.total, `Analyzing files...`);
    });

    if (metricsData.files === 0) {
      console.log(`\n${colors.yellow}⚠️ No code files found in: ${absolutePath}${colors.reset}`);
      console.log(`\n${colors.cyan}📁 Files in this directory:${colors.reset}`);
      const files = fs.readdirSync(absolutePath);
      files.forEach(file => {
        const filePath = path.join(absolutePath, file);
        const isDir = fs.statSync(filePath).isDirectory();
        console.log(`  ${isDir ? '📁' : '📄'} ${file}`);
      });
      return;
    }

    displayMetrics(metricsData);

  } catch (error) {
    console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
  }
}

async function handleComplexity(args) {
  try {
    const targetPath = args[0] || '.';
    const absolutePath = path.resolve(targetPath);
    
    console.log(`\n${colors.bold}${colors.cyan}🌀 Analyzing code complexity for: ${absolutePath}${colors.reset}`);
    console.log('='.repeat(50));

    if (!fs.existsSync(absolutePath)) {
      console.log(`${colors.red}❌ Path does not exist: ${absolutePath}${colors.reset}`);
      return;
    }

    if (!fs.statSync(absolutePath).isDirectory()) {
      console.log(`${colors.red}❌ Not a directory: ${absolutePath}${colors.reset}`);
      return;
    }

    analyzer = new Analyzer(absolutePath);
    const complexity = await analyzer.getComplexity((progress) => {
      showProgress(progress.current, progress.total, `Analyzing functions...`);
    });

    displayComplexity(complexity);

  } catch (error) {
    console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
  }
}

async function handleDependencies(args) {
  try {
    const targetPath = args[0] || '.';
    const absolutePath = path.resolve(targetPath);
    
    console.log(`\n${colors.bold}${colors.cyan}🔗 Analyzing dependencies for: ${absolutePath}${colors.reset}`);
    console.log('='.repeat(50));

    if (!fs.existsSync(absolutePath)) {
      console.log(`${colors.red}❌ Path does not exist: ${absolutePath}${colors.reset}`);
      return;
    }

    if (!fs.statSync(absolutePath).isDirectory()) {
      console.log(`${colors.red}❌ Not a directory: ${absolutePath}${colors.reset}`);
      return;
    }

    analyzer = new Analyzer(absolutePath);
    const deps = await analyzer.getDependencies();

    displayDependencies(deps);

  } catch (error) {
    console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
  }
}

async function handleQuality(args) {
  try {
    const targetPath = args[0] || '.';
    const absolutePath = path.resolve(targetPath);
    
    console.log(`\n${colors.bold}${colors.cyan}⭐ Calculating code quality score for: ${absolutePath}${colors.reset}`);
    console.log('='.repeat(50));

    if (!fs.existsSync(absolutePath)) {
      console.log(`${colors.red}❌ Path does not exist: ${absolutePath}${colors.reset}`);
      return;
    }

    if (!fs.statSync(absolutePath).isDirectory()) {
      console.log(`${colors.red}❌ Not a directory: ${absolutePath}${colors.reset}`);
      return;
    }

    analyzer = new Analyzer(absolutePath);
    const quality = await analyzer.getQuality((progress) => {
      showProgress(progress.current, progress.total, `Analyzing quality...`);
    });

    displayQuality(quality);

  } catch (error) {
    console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
  }
}

async function handleReport(args) {
  try {
    const targetPath = args[0] || '.';
    const absolutePath = path.resolve(targetPath);
    let outputFile = null;
    
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--output' && args[i+1]) {
        outputFile = args[i+1];
        i++;
      }
    }

    console.log(`\n${colors.bold}${colors.cyan}📊 Generating full report for: ${absolutePath}${colors.reset}`);
    console.log('='.repeat(50));

    if (!fs.existsSync(absolutePath)) {
      console.log(`${colors.red}❌ Path does not exist: ${absolutePath}${colors.reset}`);
      return;
    }

    if (!fs.statSync(absolutePath).isDirectory()) {
      console.log(`${colors.red}❌ Not a directory: ${absolutePath}${colors.reset}`);
      return;
    }

    analyzer = new Analyzer(absolutePath);
    const reporter = new Reporter(analyzer);
    const report = await reporter.generateFullReport((progress) => {
      showProgress(progress.current, progress.total, progress.message);
    });

    if (outputFile) {
      fs.writeFileSync(outputFile, report);
      console.log(`\n${colors.green}✅ Report saved to: ${outputFile}${colors.reset}`);
    } else {
      displayReport(report);
    }

  } catch (error) {
    console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
  }
}

async function main() {
  showBanner();
  showHelp();

  const currentDir = process.cwd();
  console.log(`\n${colors.dim}💡 Current directory: ${currentDir}${colors.reset}`);
  console.log(`${colors.dim}💡 Type 'metrics ./src' to analyze your code${colors.reset}`);
  console.log(`${colors.dim}💡 Type 'help' for available commands${colors.reset}`);

  console.log('\n' + '─'.repeat(50));

  rl.on('line', async (input) => {
    const parts = input.trim().split(/\s+/);
    const cmd = parts[0]?.toLowerCase();
    const args = parts.slice(1);

    try {
      switch (cmd) {
        case 'metrics':
        case 'm':
          await handleMetrics(args);
          break;

        case 'complexity':
        case 'c':
          await handleComplexity(args);
          break;

        case 'dependencies':
        case 'dep':
        case 'd':
          await handleDependencies(args);
          break;

        case 'quality':
        case 'q':
          await handleQuality(args);
          break;

        case 'report':
        case 'r':
          await handleReport(args);
          break;

        case 'help':
        case 'h':
          showHelp();
          break;

        case 'exit':
        case 'quit':
        case 'e':
          console.log(`\n${colors.bold}👋 Goodbye!${colors.reset}`);
          process.exit(0);
          break;

        default:
          if (cmd) {
            console.log(`${colors.red}❌ Unknown command: ${cmd}${colors.reset}`);
            console.log(`${colors.yellow}💡 Type 'help' for available commands${colors.reset}`);
          }
      }
    } catch (error) {
      console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
    }
  });

  process.stdout.write(`\n${colors.cyan}code-analyzer${colors.reset}> `);
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.log(`${colors.red}❌ Unexpected error: ${error.message}${colors.reset}`);
  console.log(`${colors.dim}${error.stack}${colors.reset}`);
});

main();