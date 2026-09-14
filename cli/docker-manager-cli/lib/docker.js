import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(exec);

export class DockerManager {
  constructor(composeFile = 'docker-compose.yml') {
    this.composeFile = composeFile;
    this.projects = {};
  }

  async runCommand(command, options = {}) {
    try {
      const { stdout, stderr } = await execAsync(command, options);
      if (stderr && !stderr.includes('WARN') && !stderr.includes('warning')) {
        console.error('⚠️', stderr);
      }
      return stdout;
    } catch (error) {
      throw new Error(error.message);
    }
  }

  async findProjects(directory = '.') {
    const files = fs.readdirSync(directory);
    const composeFiles = files.filter(f => 
      f === 'docker-compose.yml' || 
      f === 'docker-compose.yaml' ||
      f === 'compose.yml' ||
      f === 'compose.yaml'
    );

    const projects = [];
    for (const file of composeFiles) {
      const projectPath = path.join(directory, file);
      const dirName = path.basename(path.dirname(projectPath));
      
      // Check if it's a valid compose file
      try {
        const content = fs.readFileSync(projectPath, 'utf8');
        if (content.includes('services:') || content.includes('version:')) {
          projects.push({
            name: dirName,
            path: path.dirname(projectPath),
            composeFile: file
          });
        }
      } catch (error) {
        // Skip invalid files
      }
    }

    return projects;
  }

  async listServices(projectPath) {
    const command = `cd ${projectPath} && docker-compose config --services`;
    const output = await this.runCommand(command);
    return output.trim().split('\n').filter(Boolean);
  }

  async getStatus(projectPath) {
    try {
      const command = `cd ${projectPath} && docker-compose ps --format json`;
      const output = await this.runCommand(command);
      if (output.trim()) {
        const services = JSON.parse(output);
        return services.map(s => ({
          name: s.Service || s.Name,
          status: s.Status || s.State,
          ports: s.Ports || 'N/A',
          image: s.Image || 'N/A'
        }));
      }
      return [];
    } catch (error) {
      // Fallback to plain text
      const command = `cd ${projectPath} && docker-compose ps`;
      const output = await this.runCommand(command);
      const lines = output.split('\n').filter(Boolean);
      if (lines.length > 1) {
        const headers = lines[0].split(/\s{2,}/).map(h => h.trim());
        const services = lines.slice(1).map(line => {
          const parts = line.split(/\s{2,}/).map(p => p.trim());
          const status = parts[headers.indexOf('Status')] || parts[headers.indexOf('State')] || 'Unknown';
          return {
            name: parts[0] || 'Unknown',
            status: status,
            ports: parts[headers.indexOf('Ports')] || 'N/A'
          };
        });
        return services;
      }
      return [];
    }
  }

  async getContainerDetails(projectPath, service = '') {
    try {
      const command = service 
        ? `cd ${projectPath} && docker-compose ps ${service} --format json`
        : `cd ${projectPath} && docker-compose ps --format json`;
      const output = await this.runCommand(command);
      if (output.trim()) {
        return JSON.parse(output);
      }
      return [];
    } catch (error) {
      return [];
    }
  }

  async up(projectPath, service = '', options = {}) {
    const detached = options.detached !== false ? '-d' : '';
    const build = options.build ? '--build' : '';
    const command = `cd ${projectPath} && docker-compose up ${detached} ${build} ${service}`;
    console.log(`⏳ Starting services...`);
    const output = await this.runCommand(command);
    console.log(`✅ Services started`);
    return output;
  }

  async down(projectPath, options = {}) {
    const volumes = options.volumes ? '-v' : '';
    const command = `cd ${projectPath} && docker-compose down ${volumes}`;
    console.log(`⏳ Stopping services...`);
    const output = await this.runCommand(command);
    console.log(`✅ Services stopped`);
    return output;
  }

  async restart(projectPath, service = '') {
    const command = `cd ${projectPath} && docker-compose restart ${service}`;
    console.log(`⏳ Restarting services...`);
    const output = await this.runCommand(command);
    console.log(`✅ Services restarted`);
    return output;
  }

  async logs(projectPath, service = '', options = {}) {
    const follow = options.follow ? '-f' : '';
    const tail = options.tail ? `--tail=${options.tail}` : '';
    const command = `cd ${projectPath} && docker-compose logs ${follow} ${tail} ${service}`;
    const output = await this.runCommand(command);
    return output;
  }

  async pull(projectPath, service = '') {
    const command = `cd ${projectPath} && docker-compose pull ${service}`;
    console.log(`⏳ Pulling images...`);
    const output = await this.runCommand(command);
    console.log(`✅ Images pulled`);
    return output;
  }

  async build(projectPath, service = '', options = {}) {
    const noCache = options.noCache ? '--no-cache' : '';
    const command = `cd ${projectPath} && docker-compose build ${noCache} ${service}`;
    console.log(`⏳ Building services...`);
    const output = await this.runCommand(command);
    console.log(`✅ Services built`);
    return output;
  }

  async exec(projectPath, service, command) {
    const cmd = `cd ${projectPath} && docker-compose exec ${service} ${command}`;
    return this.runCommand(cmd);
  }

  async getProjectConfig(projectPath) {
    const command = `cd ${projectPath} && docker-compose config`;
    const output = await this.runCommand(command);
    try {
      return JSON.parse(output);
    } catch (error) {
      return output;
    }
  }

  async getServices(projectPath) {
    const services = await this.listServices(projectPath);
    const statuses = await this.getStatus(projectPath);
    
    return services.map(service => {
      const status = statuses.find(s => s.name === service);
      return {
        name: service,
        status: status ? status.status : 'unknown',
        ports: status ? status.ports : 'N/A'
      };
    });
  }

  async getRunningServices(projectPath) {
    const statuses = await this.getStatus(projectPath);
    return statuses.filter(s => s.status.includes('Up'));
  }

  async getStoppedServices(projectPath) {
    const statuses = await this.getStatus(projectPath);
    return statuses.filter(s => !s.status.includes('Up'));
  }

  async scale(projectPath, service, replicas) {
    const command = `cd ${projectPath} && docker-compose up -d --scale ${service}=${replicas}`;
    console.log(`⏳ Scaling ${service} to ${replicas} replicas...`);
    const output = await this.runCommand(command);
    console.log(`✅ ${service} scaled to ${replicas} replicas`);
    return output;
  }

  async getLogsBetween(projectPath, service, from, to) {
    const command = `cd ${projectPath} && docker-compose logs --since="${from}" --until="${to}" ${service}`;
    return this.runCommand(command);
  }

  async getResourceUsage(projectPath) {
    const command = `cd ${projectPath} && docker-compose ps --format json`;
    const output = await this.runCommand(command);
    if (output.trim()) {
      const containers = JSON.parse(output);
      const results = [];
      for (const container of containers) {
        try {
          const statsCmd = `docker stats ${container.ID || container.Name} --no-stream --format json`;
          const statsOutput = await execAsync(statsCmd);
          if (statsOutput.stdout.trim()) {
            const stats = JSON.parse(statsOutput.stdout);
            results.push({
              container: container.Name || container.Service,
              cpu: stats.CPUPerc || 'N/A',
              memory: stats.MemUsage || 'N/A',
              network: stats.NetIO || 'N/A'
            });
          }
        } catch (error) {
          // Skip containers that can't be monitored
        }
      }
      return results;
    }
    return [];
  }

  async isServiceHealthy(projectPath, service) {
    try {
      const command = `cd ${projectPath} && docker-compose ps ${service} --format json`;
      const output = await this.runCommand(command);
      if (output.trim()) {
        const containers = JSON.parse(output);
        if (containers.length > 0) {
          const container = containers[0];
          const health = container.Health || container.Status;
          return health && health.includes('healthy');
        }
      }
      return false;
    } catch (error) {
      return false;
    }
  }

  async getPorts(projectPath, service) {
    const command = `cd ${projectPath} && docker-compose port ${service} 80`;
    try {
      const output = await this.runCommand(command);
      return output.trim();
    } catch (error) {
      return 'No port mapping found';
    }
  }

  async getNetworks(projectPath) {
    const command = `cd ${projectPath} && docker-compose config --networks`;
    try {
      const output = await this.runCommand(command);
      return output.trim().split('\n').filter(Boolean);
    } catch (error) {
      return [];
    }
  }

  async getVolumes(projectPath) {
    const command = `cd ${projectPath} && docker-compose config --volumes`;
    try {
      const output = await this.runCommand(command);
      return output.trim().split('\n').filter(Boolean);
    } catch (error) {
      return [];
    }
  }

  async getTotalContainerCount(projectPath) {
    const services = await this.listServices(projectPath);
    return services.length;
  }

  async getCPUUsage(projectPath) {
    const usage = await this.getResourceUsage(projectPath);
    return usage.reduce((total, container) => {
      const cpu = parseFloat(container.cpu);
      return total + (isNaN(cpu) ? 0 : cpu);
    }, 0);
  }

  async getMemoryUsage(projectPath) {
    const usage = await this.getResourceUsage(projectPath);
    let totalMemory = 0;
    for (const container of usage) {
      const match = container.memory.match(/([\d.]+)\s*([KMGT]?B)/);
      if (match) {
        const value = parseFloat(match[1]);
        const unit = match[2];
        switch (unit) {
          case 'KB': totalMemory += value / 1024; break;
          case 'MB': totalMemory += value; break;
          case 'GB': totalMemory += value * 1024; break;
          default: totalMemory += value / 1024 / 1024;
        }
      }
    }
    return totalMemory;
  }
}