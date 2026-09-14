import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import ignore from 'ignore';

export class Analyzer {
  constructor(targetPath) {
    this.targetPath = path.resolve(targetPath);
    this.ignorePatterns = [
      'node_modules/**',
      '.git/**',
      'dist/**',
      'build/**',
      '*.min.js',
      '*.bundle.js',
      '__pycache__/**',
      '*.pyc',
      '.venv/**',
      'venv/**',
      'env/**'
    ];
  }

  isCodeFile(ext) {
    const codeExtensions = [
      '.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.c', '.cpp', '.cc', '.cxx',
      '.h', '.hpp', '.cs', '.rb', '.go', '.rs', '.php', '.swift', '.kt', '.dart',
      '.lua', '.r', '.pl', '.pm', '.html', '.htm', '.css', '.scss', '.sass', '.less',
      '.vue', '.svelte', '.astro', '.json', '.xml', '.yaml', '.yml', '.toml',
      '.ini', '.cfg', '.conf', '.properties', '.env', '.sh', '.bash', '.zsh',
      '.ps1', '.bat', '.cmd', '.sql', '.sqlite', '.md', '.markdown', '.txt',
      '.graphql', '.gql', '.proto', '.thrift'
    ];
    return codeExtensions.includes(ext);
  }

  async getFiles() {
    const ig = ignore().add(this.ignorePatterns);
    const allFiles = await glob(path.join(this.targetPath, '**/*'), {
      nodir: true,
      dot: true,
      absolute: true
    });

    const files = [];
    for (const file of allFiles) {
      const relativePath = path.relative(process.cwd(), file);
      if (!ig.ignores(relativePath)) {
        const ext = path.extname(file);
        if (this.isCodeFile(ext)) {
          files.push(file);
        }
      }
    }
    return files;
  }

  getLanguage(ext) {
    const languages = {
      '.js': 'JavaScript', '.jsx': 'React', '.ts': 'TypeScript', '.tsx': 'React+TypeScript',
      '.py': 'Python', '.java': 'Java', '.c': 'C', '.cpp': 'C++', '.cs': 'C#',
      '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust', '.php': 'PHP', '.swift': 'Swift',
      '.kt': 'Kotlin', '.dart': 'Dart', '.html': 'HTML', '.css': 'CSS',
      '.scss': 'SCSS', '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML',
      '.md': 'Markdown', '.sh': 'Shell', '.sql': 'SQL', '.env': 'Environment'
    };
    return languages[ext] || ext || 'Unknown';
  }

  async getMetrics(onProgress = null) {
    const files = await this.getFiles();
    const metrics = {
      files: 0,
      totalLines: 0,
      codeLines: 0,
      commentLines: 0,
      blankLines: 0,
      functions: 0,
      classes: 0,
      imports: 0,
      languages: {},
      largestFiles: []
    };

    const fileStats = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        const content = fs.readFileSync(file, 'utf8');
        const stats = fs.statSync(file);
        const lines = content.split('\n');
        const fileMetrics = this.analyzeFile(content);

        metrics.files++;
        metrics.totalLines += lines.length;
        metrics.codeLines += fileMetrics.codeLines;
        metrics.commentLines += fileMetrics.commentLines;
        metrics.blankLines += fileMetrics.blankLines;
        metrics.functions += fileMetrics.functions;
        metrics.classes += fileMetrics.classes;
        metrics.imports += fileMetrics.imports;

        const ext = path.extname(file);
        const lang = this.getLanguage(ext);
        metrics.languages[lang] = (metrics.languages[lang] || 0) + 1;

        fileStats.push({
          path: file,
          size: stats.size,
          lines: lines.length
        });

        if (onProgress) {
          onProgress({
            current: i + 1,
            total: files.length
          });
        }
      } catch (error) {
        // Skip unreadable files
      }
    }

    metrics.largestFiles = fileStats
      .sort((a, b) => b.size - a.size)
      .slice(0, 10);

    return metrics;
  }

  analyzeFile(content) {
    const lines = content.split('\n');
    let codeLines = 0, commentLines = 0, blankLines = 0;
    let functions = 0, classes = 0, imports = 0;

    for (const line of lines) {
      const trimmed = line.trim();

      // Comments
      if (trimmed.startsWith('//') || trimmed.startsWith('#') || 
          trimmed.startsWith('/*') || trimmed.startsWith('*') ||
          trimmed.startsWith('<!--') || trimmed.startsWith('--')) {
        commentLines++;
        continue;
      }

      // Empty lines
      if (!trimmed) {
        blankLines++;
        continue;
      }

      codeLines++;

      // Functions
      if (/function\s+|def\s+|fn\s+|func\s+/.test(trimmed)) functions++;
      
      // Classes
      if (/class\s+|interface\s+|struct\s+|enum\s+/.test(trimmed)) classes++;
      
      // Imports
      if (/import\s+|from\s+.*import|require\s*\(|#include\s+/.test(trimmed)) imports++;
    }

    return { codeLines, commentLines, blankLines, functions, classes, imports };
  }

  async getComplexity(onProgress = null) {
    const files = await this.getFiles();
    const functions = [];
    let totalComplexity = 0;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        const content = fs.readFileSync(file, 'utf8');
        const fileFunctions = this.extractFunctions(content);
        
        fileFunctions.forEach(func => {
          const complexity = this.calculateComplexity(func.code);
          functions.push({
            name: func.name,
            file: file,
            line: func.line,
            complexity: complexity
          });
          totalComplexity += complexity;
        });

        if (onProgress) {
          onProgress({
            current: i + 1,
            total: files.length
          });
        }
      } catch (error) {
        // Skip unreadable files
      }
    }

    const totalFunctions = functions.length;
    const average = totalFunctions > 0 ? totalComplexity / totalFunctions : 0;
    const max = functions.length > 0 ? Math.max(...functions.map(f => f.complexity)) : 0;
    const complexFunctions = functions.filter(f => f.complexity > 10);

    return {
      totalFunctions,
      average,
      max,
      complexFunctions: complexFunctions.sort((a, b) => b.complexity - a.complexity)
    };
  }

  extractFunctions(content) {
    const functions = [];
    const lines = content.split('\n');
    let currentFunction = null;
    let braceCount = 0;
    let inFunction = false;

    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();

      if (trimmed.startsWith('//') || trimmed.startsWith('#') || trimmed.startsWith('/*')) {
        continue;
      }

      if (!inFunction) {
        const match = trimmed.match(/(function|def|fn|func)\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
        if (match) {
          currentFunction = {
            name: match[2] || 'anonymous',
            line: i + 1,
            code: [lines[i]]
          };
          braceCount = this.countBraces(lines[i]);
          inFunction = true;
          if (braceCount === 0) {
            functions.push(currentFunction);
            currentFunction = null;
            inFunction = false;
          }
        }
      } else {
        currentFunction.code.push(lines[i]);
        braceCount += this.countBraces(lines[i]);
        if (braceCount === 0) {
          functions.push(currentFunction);
          currentFunction = null;
          inFunction = false;
        }
      }
    }

    return functions;
  }

  countBraces(line) {
    let count = 0;
    for (const char of line) {
      if (char === '{') count++;
      if (char === '}') count--;
    }
    return count;
  }

  calculateComplexity(code) {
    const patterns = [/if\s*\(/g, /else\s+if\s*\(/g, /for\s*\(/g, /while\s*\(/g,
                       /do\s*\{/g, /case\s+/g, /\?/g, /\|\|/g, /&&/g, /catch\s*\(/g];
    let complexity = 1;
    for (const pattern of patterns) {
      const matches = code.match(pattern);
      if (matches) complexity += matches.length;
    }
    return complexity;
  }

  async getDependencies() {
    const deps = { total: 0, direct: 0, dev: 0, packages: [] };
    const packageFiles = await glob(path.join(this.targetPath, '**/package.json'), {
      ignore: ['**/node_modules/**']
    });

    for (const file of packageFiles) {
      try {
        const content = JSON.parse(fs.readFileSync(file, 'utf8'));
        const dependencies = content.dependencies || {};
        const devDependencies = content.devDependencies || {};

        deps.direct += Object.keys(dependencies).length;
        deps.dev += Object.keys(devDependencies).length;

        Object.entries(dependencies).forEach(([name, version]) => {
          deps.packages.push({ name, version, type: 'direct' });
        });
        Object.entries(devDependencies).forEach(([name, version]) => {
          deps.packages.push({ name, version, type: 'dev' });
        });
      } catch (error) {
        // Skip invalid package.json
      }
    }

    deps.total = deps.direct + deps.dev;
    return deps;
  }

  async getQuality(onProgress = null) {
    const metrics = await this.getMetrics(onProgress);
    const complexity = await this.getComplexity(onProgress);
    const issues = [];
    let score = 100;

    // Check file size
    for (const file of metrics.largestFiles) {
      if (file.lines > 500) {
        issues.push({
          severity: 'medium',
          message: `File ${path.basename(file.path)} has ${file.lines} lines (consider splitting)`,
          file: file.path
        });
        score -= 2;
      }
      if (file.lines > 1000) {
        issues.push({
          severity: 'high',
          message: `File ${path.basename(file.path)} is very large (${file.lines} lines)`,
          file: file.path
        });
        score -= 5;
      }
    }

    // Check comments
    if (metrics.totalLines > 0) {
      const commentRatio = metrics.commentLines / metrics.totalLines;
      if (commentRatio < 0.05) {
        issues.push({
          severity: 'medium',
          message: 'Low comment ratio (< 5%) - consider adding more documentation'
        });
        score -= 5;
      }
    }

    // Check complexity
    for (const func of complexity.complexFunctions) {
      if (func.complexity > 20) {
        issues.push({
          severity: 'high',
          message: `Function ${func.name} has high complexity (${func.complexity})`,
          file: func.file
        });
        score -= 3;
      }
    }

    let grade;
    if (score >= 80) grade = 'A';
    else if (score >= 70) grade = 'B';
    else if (score >= 60) grade = 'C';
    else if (score >= 50) grade = 'D';
    else grade = 'F';

    score = Math.max(0, Math.min(100, score));

    return {
      score: Math.round(score),
      grade: grade,
      issues: issues,
      details: {
        'File Size': Math.max(0, 100 - (metrics.largestFiles.filter(f => f.lines > 500).length * 5)),
        'Comments': Math.round(Math.min(100, (metrics.commentLines / metrics.totalLines) * 100 * 5)),
        'Complexity': Math.max(0, 100 - (complexity.complexFunctions.length * 5)),
        'Documentation': Math.max(0, 100 - (issues.filter(i => i.message.includes('comment')).length * 10))
      }
    };
  }
}

export default Analyzer;