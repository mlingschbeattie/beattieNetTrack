import fs from 'node:fs';

const artifactPath = 'C:/Users/mlingsch/.gemini/antigravity-ide/brain/a9eff248-c065-470c-bb31-93ba4a528fda/rack_server_upgrade_proposal.md';
const destPath = 'c:/Users/mlingsch/cluster/rack-server-upgrade.md';

const content = fs.readFileSync(artifactPath, 'utf8');
fs.writeFileSync(destPath, content);
console.log('Copied proposal to cluster repository');
