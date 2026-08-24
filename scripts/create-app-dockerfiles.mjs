import fs from 'node:fs';

const dockerfileContent = `FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "start"]
`;

const apps = [
  'c:/CustomApps/techSupportSim',
  'c:/CustomApps/cyberLabEthicalHacker',
  'c:/CustomApps/cyberTerminalCIS',
  'c:/CustomApps/NexusPicker'
];

for (const app of apps) {
  fs.writeFileSync(`${app}/Dockerfile`, dockerfileContent);
  console.log(`Created Dockerfile in ${app}`);
}
