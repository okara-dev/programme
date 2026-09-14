#!/usr/bin/env node

import readline from 'readline';
import { DockerManager } from '../lib/docker.js';
import path from 'path';
import fs from 'fs';

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
  bold: '\x1b[1m',
  dim: '\x1b[2m'
};

const manager = new DockerManager();
let projects = [];

function showHelp() {
  console.log(`
${colors.bold}🐳 Docker Compose Manager${colors.reset}
${colors.dim}Commands:${colors.reset}

  ${colors.green}list${colors.reset}                   - Find and list all Docker Compose projects
  ${colors.green}status${colors.reset} [project]       - Show status of services
  ${colors.green}start${colors.reset} [project]        - Start services (up -d)
  ${colors.green}stop${colors.reset} [project]         - Stop services (down)
  ${colors.green}restart${colors.reset} [project]      - Restart services
  ${colors.green}logs${colors.reset} [project]         - Show logs
  ${colors.green}pull${colors.reset} [project]         - Pull latest images
  ${colors.green}build${colors.reset} [project]        - Build services
  ${colors.green}scale${colors.reset} [project] [service] [count] - Scale service
  ${colors.green}health${colors.reset} [project]       - Check service health
  ${colors.green}stats${colors.reset} [project]        - Show resource usage
  ${colors.green}help${colors.reset}                   - Show this help
  ${colors.green}exit${colors.reset}                   - Exit

${colors.dim}Example:${colors.reset}
  docker-manager list
  docker-manager status my-project
  docker-manager start my-project
`);
}

async function findProjects() {
  console.log(`${colors.dim}🔍 Scanning for Docker Compose projects...${colors.reset}`);
  projects = await manager.findProjects('.');
  
  if (projects.length > 0) {
    console.log(`\n${colors.green}Found ${projects.length} project(s):${colors.reset}`);
    projects.forEach((p, i) => {
      console.log(`  ${i+1}. ${colors.bold}${p.name}${colors.reset} (${p.path})`);
    });
    console.log('');
  } else {
    console.log(`${colors.yellow}No Docker Compose projects found.${colors.reset}`);
  }
  return projects;
}

async function main() {
  console.log(`${colors.bold}🐳 Docker Compose Manager CLI${colors.reset}`);
  console.log('='.repeat(50));

  await findProjects();
  showHelp();

  rl.on('line', async (input) => {
    const parts = input.trim().split(/\s+/);
    const cmd = parts[0]?.toLowerCase();

    try {
      switch (cmd) {
        case 'list': {
          await findProjects();
          break;
        }

        case 'status':
        case 'ps': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified. Use 'list' to see available projects.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          console.log(`\n${colors.bold}📊 Status for ${projectName}${colors.reset}`);
          console.log('='.repeat(50));
          const status = await manager.getStatus(project.path);
          if (status.length > 0) {
            status.forEach(s => {
              const statusColor = s.status.includes('Up') ? colors.green : 
                                s.status.includes('Exited') ? colors.yellow : colors.red;
              console.log(`  ${s.name}: ${statusColor}${s.status}${colors.reset}`);
              if (s.ports && s.ports !== 'N/A') {
                console.log(`    ${colors.dim}Ports: ${s.ports}${colors.reset}`);
              }
            });
          } else {
            console.log(`${colors.yellow}No services running${colors.reset}`);
          }
          break;
        }

        case 'start':
        case 'up': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.up(project.path);
          break;
        }

        case 'stop':
        case 'down': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.down(project.path);
          break;
        }

        case 'restart': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.restart(project.path);
          break;
        }

        case 'logs': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          const logs = await manager.logs(project.path);
          console.log(logs);
          break;
        }

        case 'pull': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.pull(project.path);
          break;
        }

        case 'build': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.build(project.path);
          break;
        }

        case 'scale': {
          if (parts.length < 4) {
            console.log(`${colors.yellow}Usage: scale <project> <service> <count>${colors.reset}`);
            break;
          }
          const projectName = parts[1];
          const service = parts[2];
          const count = parseInt(parts[3]);
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          await manager.scale(project.path, service, count);
          break;
        }

        case 'health': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          const services = await manager.listServices(project.path);
          console.log(`\n${colors.bold}🏥 Health Status for ${projectName}${colors.reset}`);
          console.log('='.repeat(50));
          for (const service of services) {
            const healthy = await manager.isServiceHealthy(project.path, service);
            const status = healthy ? `${colors.green}✅ healthy${colors.reset}` : `${colors.yellow}⚠️ unknown${colors.reset}`;
            console.log(`  ${service}: ${status}`);
          }
          break;
        }

        case 'stats': {
          const projectName = parts[1] || projects[0]?.name;
          if (!projectName) {
            console.log(`${colors.yellow}No project specified.${colors.reset}`);
            break;
          }
          const project = projects.find(p => p.name === projectName);
          if (!project) {
            console.log(`${colors.red}Project '${projectName}' not found.${colors.reset}`);
            break;
          }
          const usage = await manager.getResourceUsage(project.path);
          if (usage.length > 0) {
            console.log(`\n${colors.bold}📊 Resource Usage${colors.reset}`);
            console.log('='.repeat(50));
            usage.forEach(container => {
              console.log(`  ${container.container}:`);
              console.log(`    CPU: ${container.cpu}`);
              console.log(`    Memory: ${container.memory}`);
              if (container.network) {
                console.log(`    Network: ${container.network}`);
              }
            });
          } else {
            console.log(`${colors.yellow}No resource usage data available${colors.reset}`);
          }
          break;
        }

        case 'help':
          showHelp();
          break;

        case 'exit':
        case 'quit':
          console.log(`${colors.bold}👋 Goodbye!${colors.reset}`);
          process.exit(0);
          break;

        default:
          if (cmd) {
            console.log(`${colors.red}Unknown command: ${cmd}${colors.reset}`);
            showHelp();
          }
      }
    } catch (error) {
      console.log(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
    }
  });

  process.stdout.write(`\n${colors.cyan}docker-manager${colors.reset}> `);
}

main();