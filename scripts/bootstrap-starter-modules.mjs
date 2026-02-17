import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const modulesRoot = path.join(projectRoot, 'src', 'content', 'modules', 'starter');

const map = [
  { track: 'pc-technician', moduleId: 'pct.foundations', title: 'PC Foundations', order: 1, description: 'Core computing concepts, units, and baseline workflows.' },
  { track: 'pc-technician', moduleId: 'pct.hardware', title: 'PC Hardware', order: 2, description: 'Components, form factors, compatibility, and peripherals.' },
  { track: 'pc-technician', moduleId: 'pct.os', title: 'PC Operating Systems', order: 3, description: 'Operating system installation, configuration, and recovery.' },
  { track: 'pc-technician', moduleId: 'pct.troubleshooting', title: 'PC Troubleshooting', order: 4, description: 'Methodical diagnosis, maintenance, and issue resolution.' },
  { track: 'pc-technician', moduleId: 'pct.network-basics', title: 'PC Network Basics', order: 5, description: 'Networking fundamentals needed for endpoint support.' },

  { track: 'network-engineer', moduleId: 'net.foundations', title: 'Network Foundations', order: 1, description: 'Standards, models, and protocol fundamentals.' },
  { track: 'network-engineer', moduleId: 'net.switching', title: 'Network Switching', order: 2, description: 'Layer 2 switching concepts and operations.' },
  { track: 'network-engineer', moduleId: 'net.routing', title: 'Network Routing', order: 3, description: 'Layer 3 routing design and operation basics.' },
  { track: 'network-engineer', moduleId: 'net.wireless', title: 'Network Wireless', order: 4, description: 'Wireless standards, security, and troubleshooting.' },
  { track: 'network-engineer', moduleId: 'net.services', title: 'Network Services', order: 5, description: 'Core services including DNS, DHCP, and NTP.' },

  { track: 'cybersecurity-engineer', moduleId: 'sec.foundations', title: 'Security Foundations', order: 1, description: 'Security principles, CIA triad, and core controls.' },
  { track: 'cybersecurity-engineer', moduleId: 'sec.threats', title: 'Security Threats', order: 2, description: 'Threat classes, adversary behavior, and risk context.' },
  { track: 'cybersecurity-engineer', moduleId: 'sec.defense', title: 'Security Defense', order: 3, description: 'Defensive controls, monitoring, and hardening fundamentals.' },
  { track: 'cybersecurity-engineer', moduleId: 'sec.identity', title: 'Security Identity', order: 4, description: 'Identity and access management principles.' },
  { track: 'cybersecurity-engineer', moduleId: 'sec.incident-response', title: 'Security Incident Response', order: 5, description: 'Incident response lifecycle and reporting essentials.' },

  { track: 'web-developer', moduleId: 'web.foundations', title: 'Web Foundations', order: 1, description: 'Core web platform concepts and tooling basics.' },
  { track: 'web-developer', moduleId: 'web.html-css', title: 'Web HTML/CSS', order: 2, description: 'Semantic HTML and responsive CSS foundations.' },
  { track: 'web-developer', moduleId: 'web.js', title: 'Web JavaScript', order: 3, description: 'JavaScript language and browser interaction basics.' },
  { track: 'web-developer', moduleId: 'web.frontend', title: 'Web Frontend', order: 4, description: 'Frontend architecture, components, and state basics.' },
  { track: 'web-developer', moduleId: 'web.backend', title: 'Web Backend', order: 5, description: 'Backend and API fundamentals for web systems.' },

  { track: 'python-developer', moduleId: 'py.foundations', title: 'Python Foundations', order: 1, description: 'Foundational Python concepts and coding practices.' },
  { track: 'python-developer', moduleId: 'py.syntax', title: 'Python Syntax', order: 2, description: 'Syntax, control flow, functions, and modules.' },
  { track: 'python-developer', moduleId: 'py.data', title: 'Python Data', order: 3, description: 'Data structures, transformation, and file formats.' },
  { track: 'python-developer', moduleId: 'py.scripting', title: 'Python Scripting', order: 4, description: 'Automation scripts, tooling, and environment usage.' },
  { track: 'python-developer', moduleId: 'py.projects', title: 'Python Projects', order: 5, description: 'Project organization and practical implementation patterns.' },

  { track: 'ai-ml', moduleId: 'ai.foundations', title: 'AI Foundations', order: 1, description: 'AI literacy and model behavior fundamentals.' },
  { track: 'ai-ml', moduleId: 'ai.prompting', title: 'AI Prompting', order: 2, description: 'Prompting patterns and evaluation basics.' },
  { track: 'ai-ml', moduleId: 'ai.data', title: 'AI Data', order: 3, description: 'Data quality, bias, and dataset lifecycle basics.' },
  { track: 'ai-ml', moduleId: 'ai.models', title: 'AI Models', order: 4, description: 'Model types, metrics, and performance concepts.' },
  { track: 'ai-ml', moduleId: 'ai.projects', title: 'AI Projects', order: 5, description: 'Responsible project planning and implementation.' },
];

const toMdx = (entry) => `---\ntitle: ${entry.title}\ndescription: ${entry.description}\nslug: ${entry.moduleId}\ntrack: ${entry.track}\nmoduleId: ${entry.moduleId}\norder: ${entry.order}\n---\n\nStarter module scaffold for ${entry.track}.\n`;

const run = async () => {
  await fs.mkdir(modulesRoot, { recursive: true });
  for (const entry of map) {
    const filePath = path.join(modulesRoot, `${entry.moduleId}.mdx`);
    await fs.writeFile(filePath, toMdx(entry), 'utf8');
  }
  console.log(`Generated ${map.length} starter module stubs at ${path.relative(projectRoot, modulesRoot)}`);
};

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
