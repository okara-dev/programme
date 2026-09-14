import path from 'path';

export class Reporter {
  constructor(analyzer) {
    this.analyzer = analyzer;
  }

  async generateFullReport(onProgress = null) {
    const report = [];
    const totalSteps = 4;
    let currentStep = 0;

    // Step 1: Metrics
    currentStep++;
    if (onProgress) {
      onProgress({
        current: currentStep,
        total: totalSteps,
        message: 'Collecting metrics...'
      });
    }
    const metrics = await this.analyzer.getMetrics();

    // Step 2: Complexity
    currentStep++;
    if (onProgress) {
      onProgress({
        current: currentStep,
        total: totalSteps,
        message: 'Analyzing complexity...'
      });
    }
    const complexity = await this.analyzer.getComplexity();

    // Step 3: Dependencies
    currentStep++;
    if (onProgress) {
      onProgress({
        current: currentStep,
        total: totalSteps,
        message: 'Analyzing dependencies...'
      });
    }
    const deps = await this.analyzer.getDependencies();

    // Step 4: Quality
    currentStep++;
    if (onProgress) {
      onProgress({
        current: currentStep,
        total: totalSteps,
        message: 'Calculating quality...'
      });
    }
    const quality = await this.analyzer.getQuality();

    // Build report
    report.push(this.generateHeader());
    report.push(this.generateMetricsSection(metrics));
    report.push(this.generateComplexitySection(complexity));
    report.push(this.generateDependenciesSection(deps));
    report.push(this.generateQualitySection(quality));
    report.push(this.generateFooter());

    return report.join('\n');
  }

  generateHeader() {
    return `# 📊 Code Analysis Report

**Generated:** ${new Date().toLocaleString()}
**Path:** ${this.analyzer.targetPath}

---
`;
  }

  generateMetricsSection(metrics) {
    let output = `## 📊 Code Metrics

| Metric | Value |
|--------|-------|
| **Total Files** | ${metrics.files} |
| **Total Lines** | ${metrics.totalLines.toLocaleString()} |
| **Code Lines** | ${metrics.codeLines.toLocaleString()} |
| **Comment Lines** | ${metrics.commentLines.toLocaleString()} |
| **Blank Lines** | ${metrics.blankLines.toLocaleString()} |
| **Functions** | ${metrics.functions.toLocaleString()} |
| **Classes** | ${metrics.classes.toLocaleString()} |
| **Imports** | ${metrics.imports.toLocaleString()} |

### Languages
`;

    if (metrics.languages) {
      const sorted = Object.entries(metrics.languages).sort((a, b) => b[1] - a[1]);
      sorted.forEach(([lang, count]) => {
        output += `- ${lang}: ${count} files\n`;
      });
    }

    output += `\n### Largest Files\n`;
    metrics.largestFiles.slice(0, 5).forEach((file, index) => {
      const size = (file.size / 1024).toFixed(2);
      output += `${index + 1}. **${path.basename(file.path)}** - ${size} KB (${file.lines} lines)\n`;
    });

    return output + '\n---\n';
  }

  generateComplexitySection(complexity) {
    let output = `## 🌀 Code Complexity

| Metric | Value |
|--------|-------|
| **Total Functions** | ${complexity.totalFunctions} |
| **Average Complexity** | ${complexity.average.toFixed(2)} |
| **Maximum Complexity** | ${complexity.max} |

`;

    if (complexity.complexFunctions && complexity.complexFunctions.length > 0) {
      output += `### Complex Functions (> 10)\n\n`;
      output += `| Function | File | Line | Complexity |\n`;
      output += `|----------|------|------|------------|\n`;

      complexity.complexFunctions.slice(0, 20).forEach(func => {
        const file = path.basename(func.file);
        output += `| ${func.name} | ${file} | ${func.line} | ${func.complexity} |\n`;
      });

      if (complexity.complexFunctions.length > 20) {
        output += `\n... and ${complexity.complexFunctions.length - 20} more complex functions\n`;
      }
    } else {
      output += `✅ No complex functions found.\n`;
    }

    return output + '\n---\n';
  }

  generateDependenciesSection(deps) {
    let output = `## 🔗 Dependencies

| Metric | Value |
|--------|-------|
| **Total Dependencies** | ${deps.total} |
| **Direct Dependencies** | ${deps.direct} |
| **Dev Dependencies** | ${deps.dev} |

`;

    if (deps.packages && deps.packages.length > 0) {
      output += `### Packages\n\n`;
      deps.packages.slice(0, 20).forEach(pkg => {
        const type = pkg.type === 'dev' ? ' (dev)' : '';
        output += `- ${pkg.name}@${pkg.version}${type}\n`;
      });

      if (deps.packages.length > 20) {
        output += `\n... and ${deps.packages.length - 20} more packages\n`;
      }
    }

    return output + '\n---\n';
  }

  generateQualitySection(quality) {
    let output = `## ⭐ Code Quality Score

**Overall Score:** ${quality.score}/100 (${quality.grade})

`;

    if (quality.details) {
      output += `### Breakdown\n\n`;
      Object.entries(quality.details).forEach(([key, value]) => {
        const icon = value >= 80 ? '✅' : value >= 60 ? '⚠️' : '❌';
        output += `- ${icon} **${key}**: ${value}/100\n`;
      });
    }

    if (quality.issues && quality.issues.length > 0) {
      output += `\n### Issues Found\n\n`;
      quality.issues.slice(0, 20).forEach(issue => {
        const icon = issue.severity === 'high' ? '🔴' : 
                    issue.severity === 'medium' ? '🟡' : '🔵';
        output += `- ${icon} ${issue.message}`;
        if (issue.file) {
          output += ` (${path.basename(issue.file)})`;
        }
        output += '\n';
      });

      if (quality.issues.length > 20) {
        output += `\n... and ${quality.issues.length - 20} more issues\n`;
      }
    } else {
      output += `\n✅ No issues found. Excellent code quality!\n`;
    }

    return output + '\n---\n';
  }

  generateFooter() {
    return `
## 📋 Summary

**Analysis Complete!** This report provides a comprehensive overview of your codebase.

### Recommendations

1. **Address Issues:** Review and fix the issues found above
2. **Reduce Complexity:** Simplify functions with high cyclomatic complexity
3. **Add Documentation:** Improve code documentation and comments
4. **Split Large Files:** Break down files with > 500 lines
5. **Review Dependencies:** Check for outdated or unused packages

---
*Report generated automatically by Code Analyzer CLI*
`;
  }
}

export default Reporter;