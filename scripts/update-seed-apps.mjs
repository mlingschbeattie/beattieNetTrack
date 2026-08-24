import fs from 'node:fs';

const targetPath = 'c:/Users/mlingsch/cluster/packages/db/scripts/seed-apps.ts';
let file = fs.readFileSync(targetPath, 'utf8');

const newApps = `  {
    id: 'techsupport',
    title: 'Tech Support Simulator',
    description: 'Enterprise helpdesk, multi-OS troubleshooting, and AI user roleplay',
    url: 'https://techsupport.beattietech.local',
    icon: 'headphones',
    color: '#0ea5e9',
    navPosition: 13,
    status: 'active',
    eventTypes: ['techsupport.ticket_solved', 'techsupport.security_violation', 'techsupport.session_complete'],
  },
  {
    id: 'cyberlab',
    title: 'CyberLab: Ethical Hacker',
    description: 'Penetration testing sandbox, MITRE ATT&CK matrix, and AI mentor',
    url: 'https://cyberlab.beattietech.local',
    icon: 'shield-alert',
    color: '#ef4444',
    navPosition: 14,
    status: 'active',
    eventTypes: ['cyberlab.scenario_completed', 'cyberlab.quiz_passed', 'cyberlab.mitre_unlocked'],
  },
  {
    id: 'cyterm',
    title: 'CyberTerminal CIS',
    description: 'Interactive Linux security terminal simulator and attack scenarios',
    url: 'https://cyterm.beattietech.local',
    icon: 'terminal',
    color: '#10b981',
    navPosition: 15,
    status: 'active',
    eventTypes: ['cyterm.command_unlocked', 'cyterm.flag_captured', 'cyterm.scenario_completed'],
  },
  {
    id: 'nexus',
    title: 'PC Build Simulator 3D',
    description: 'Interactive 3D hardware assembly, cable management, and benchmarking',
    url: 'https://nexus.beattietech.local',
    icon: 'cpu',
    color: '#8b5cf6',
    navPosition: 16,
    status: 'active',
    eventTypes: ['nexus.build_complete', 'nexus.benchmark_passed', 'nexus.wire_connected'],
  },
];`;

if (!file.includes("id: 'techsupport'")) {
  file = file.replace(/\];\s*console\.log/, newApps + '\n\nconsole.log');
  fs.writeFileSync(targetPath, file);
  console.log('Appended 4 new apps before closing bracket');
} else {
  console.log('Already present');
}
