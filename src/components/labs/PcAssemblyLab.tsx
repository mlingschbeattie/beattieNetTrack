import { useEffect, useMemo, useState } from 'react';
import { setLastResult, setRequirementChecklist } from '../../lib/checksStore';

type Props = {
  labSlug?: string;
};

type BuildState = {
  cpu: string | null;
  mobo: string | null;
  ram: string | null;
  gpu: string | null;
  storage: string | null;
  cooler: string | null;
};

type ScenarioUseCase = {
  adjectives: string[];
  resolution: string | null;
  cpuTier: 'low' | 'mid' | 'high' | 'ultra';
  gpuTier: 'entry' | 'mid' | 'high' | 'ultra' | 'optional';
  ramMin: number;
  storageType: 'any' | 'NVMe';
  storageMin: number;
  budgetTier: 'ultraLow' | 'low' | 'mid' | 'high' | 'premium';
};

type ActiveScenario = {
  id: string;
  customer: string;
  adjective: string;
  useCase: string;
  budget: number;
  psuWattage: number;
  requirements: {
    cpuTier: ScenarioUseCase['cpuTier'];
    gpuTier: ScenarioUseCase['gpuTier'];
    ramMin: number;
    storageType: ScenarioUseCase['storageType'];
    storageMin: number;
    resolution: string | null;
  };
};

type FeedbackItem = {
  type: 'pass' | 'fail' | 'warn';
  text: string;
};

type EvalResult = {
  score: number;
  feedback: FeedbackItem[];
  passed: boolean;
};

type CompatibilityResult = {
  issues: string[];
  passes: string[];
};

type Cpu = { name: string; socket: string; ram: 'DDR4' | 'DDR5'; tdp: number; price: number; performance: number };

type Mobo = { name: string; socket: string; ram: 'DDR4' | 'DDR5'; formFactor: string; price: number };

type Ram = { name: string; type: 'DDR4' | 'DDR5'; capacity: number; speed: number; price: number };

type Gpu = { name: string; performance: number; suitable1080p: boolean; suitable1440p: boolean; price: number };

type Storage = { name: string; type: 'NVMe' | 'SATA'; capacity: number; price: number };

type Cooler = { name: string; type: 'Air' | 'Liquid'; maxTDP: number; price: number };

const scenarioTemplates: { useCases: Record<string, ScenarioUseCase>; customers: string[]; psuWattages: number[] } = {
  useCases: {
    'gaming-1080p': {
      adjectives: ['casual', 'budget-friendly', 'entry-level', 'basic'],
      resolution: '1080p',
      cpuTier: 'low',
      gpuTier: 'entry',
      ramMin: 8,
      storageType: 'any',
      storageMin: 500,
      budgetTier: 'low',
    },
    'gaming-1440p': {
      adjectives: ['mid-range', 'balanced', 'solid', 'capable'],
      resolution: '1440p',
      cpuTier: 'mid',
      gpuTier: 'mid',
      ramMin: 16,
      storageType: 'any',
      storageMin: 500,
      budgetTier: 'mid',
    },
    'gaming-premium': {
      adjectives: ['high-end', 'powerful', 'enthusiast', 'premium'],
      resolution: '1440p+',
      cpuTier: 'high',
      gpuTier: 'high',
      ramMin: 16,
      storageType: 'NVMe',
      storageMin: 1000,
      budgetTier: 'high',
    },
    'gaming-ultra': {
      adjectives: ['ultra-high-end', 'flagship', 'extreme', 'top-tier'],
      resolution: '4K',
      cpuTier: 'ultra',
      gpuTier: 'ultra',
      ramMin: 32,
      storageType: 'NVMe',
      storageMin: 1000,
      budgetTier: 'premium',
    },
    office: {
      adjectives: ['professional', 'business', 'office', 'productivity'],
      resolution: null,
      cpuTier: 'low',
      gpuTier: 'optional',
      ramMin: 8,
      storageType: 'any',
      storageMin: 250,
      budgetTier: 'ultraLow',
    },
    'content-creation': {
      adjectives: ['creative', 'content creation', 'multimedia', 'design'],
      resolution: null,
      cpuTier: 'high',
      gpuTier: 'mid',
      ramMin: 32,
      storageType: 'NVMe',
      storageMin: 1000,
      budgetTier: 'high',
    },
    workstation: {
      adjectives: ['professional', 'workstation', 'power-user', 'advanced'],
      resolution: null,
      cpuTier: 'ultra',
      gpuTier: 'high',
      ramMin: 32,
      storageType: 'NVMe',
      storageMin: 2000,
      budgetTier: 'premium',
    },
    'home-media': {
      adjectives: ['home media', 'HTPC', 'entertainment', 'streaming'],
      resolution: null,
      cpuTier: 'low',
      gpuTier: 'optional',
      ramMin: 8,
      storageType: 'any',
      storageMin: 1000,
      budgetTier: 'low',
    },
  },
  customers: [
    'A student',
    'A professional',
    'An enthusiast',
    'A small business owner',
    'A gamer',
    'A content creator',
    'A freelancer',
    'A home user',
    'An IT department',
    'A startup company',
  ],
  psuWattages: [450, 550, 650, 750, 850, 1000, 1200, 1500],
};

const components = {
  cpu: {
    'intel-i5-13600k': { name: 'Intel Core i5-13600K', socket: 'LGA1700', ram: 'DDR5', tdp: 125, price: 319, performance: 88 },
    'intel-i7-13700k': { name: 'Intel Core i7-13700K', socket: 'LGA1700', ram: 'DDR5', tdp: 190, price: 409, performance: 95 },
    'intel-i9-13900k': { name: 'Intel Core i9-13900K', socket: 'LGA1700', ram: 'DDR5', tdp: 253, price: 589, performance: 100 },
    'amd-r5-7600x': { name: 'AMD Ryzen 5 7600X', socket: 'AM5', ram: 'DDR5', tdp: 105, price: 299, performance: 86 },
    'amd-r7-7700x': { name: 'AMD Ryzen 7 7700X', socket: 'AM5', ram: 'DDR5', tdp: 105, price: 399, performance: 92 },
    'amd-r9-7900x': { name: 'AMD Ryzen 9 7900X', socket: 'AM5', ram: 'DDR5', tdp: 170, price: 549, performance: 98 },
    'intel-i5-12600k': { name: 'Intel Core i5-12600K', socket: 'LGA1700', ram: 'DDR4', tdp: 125, price: 289, performance: 80 },
    'amd-r5-5600x': { name: 'AMD Ryzen 5 5600X', socket: 'AM4', ram: 'DDR4', tdp: 65, price: 199, performance: 75 },
    'intel-i3-12100': { name: 'Intel Core i3-12100', socket: 'LGA1700', ram: 'DDR4', tdp: 60, price: 149, performance: 65 },
    'amd-r3-4100': { name: 'AMD Ryzen 3 4100', socket: 'AM4', ram: 'DDR4', tdp: 65, price: 99, performance: 55 },
  } as Record<string, Cpu>,
  mobo: {
    'asus-z790-ddr5': { name: 'ASUS ROG Z790', socket: 'LGA1700', ram: 'DDR5', formFactor: 'ATX', price: 329 },
    'msi-z790-ddr5': { name: 'MSI MPG Z790', socket: 'LGA1700', ram: 'DDR5', formFactor: 'ATX', price: 299 },
    'gigabyte-z790-ddr4': { name: 'Gigabyte Z790', socket: 'LGA1700', ram: 'DDR4', formFactor: 'ATX', price: 249 },
    'asus-b650-ddr5': { name: 'ASUS TUF B650', socket: 'AM5', ram: 'DDR5', formFactor: 'ATX', price: 189 },
    'msi-x670-ddr5': { name: 'MSI X670', socket: 'AM5', ram: 'DDR5', formFactor: 'ATX', price: 279 },
    'asus-b550-ddr4': { name: 'ASUS B550', socket: 'AM4', ram: 'DDR4', formFactor: 'ATX', price: 149 },
    'asrock-b660-ddr4': { name: 'ASRock B660M', socket: 'LGA1700', ram: 'DDR4', formFactor: 'mATX', price: 119 },
    'gigabyte-a520': { name: 'Gigabyte A520M', socket: 'AM4', ram: 'DDR4', formFactor: 'mATX', price: 79 },
  } as Record<string, Mobo>,
  ram: {
    'corsair-16gb-ddr5': { name: 'Corsair Vengeance 16GB DDR5-5600', type: 'DDR5', capacity: 16, speed: 5600, price: 109 },
    'gskill-32gb-ddr5': { name: 'G.Skill Trident 32GB DDR5-6000', type: 'DDR5', capacity: 32, speed: 6000, price: 179 },
    'kingston-16gb-ddr5': { name: 'Kingston Fury 16GB DDR5-5200', type: 'DDR5', capacity: 16, speed: 5200, price: 99 },
    'corsair-32gb-ddr4': { name: 'Corsair Vengeance 32GB DDR4-3200', type: 'DDR4', capacity: 32, speed: 3200, price: 89 },
    'gskill-16gb-ddr4': { name: 'G.Skill Ripjaws 16GB DDR4-3600', type: 'DDR4', capacity: 16, speed: 3600, price: 69 },
    'teamgroup-8gb-ddr4': { name: 'Team T-Force 8GB DDR4-3200', type: 'DDR4', capacity: 8, speed: 3200, price: 39 },
  } as Record<string, Ram>,
  gpu: {
    'rtx-4060': { name: 'NVIDIA RTX 4060 8GB', performance: 75, suitable1080p: true, suitable1440p: true, price: 299 },
    'rtx-4060ti': { name: 'NVIDIA RTX 4060 Ti 16GB', performance: 82, suitable1080p: true, suitable1440p: true, price: 499 },
    'rtx-4070': { name: 'NVIDIA RTX 4070 12GB', performance: 88, suitable1080p: true, suitable1440p: true, price: 599 },
    'rtx-4070ti': { name: 'NVIDIA RTX 4070 Ti 12GB', performance: 94, suitable1080p: true, suitable1440p: true, price: 799 },
    'rx-7600': { name: 'AMD Radeon RX 7600 8GB', performance: 72, suitable1080p: true, suitable1440p: false, price: 269 },
    'rx-7700xt': { name: 'AMD Radeon RX 7700 XT 12GB', performance: 84, suitable1080p: true, suitable1440p: true, price: 449 },
    'rx-7800xt': { name: 'AMD Radeon RX 7800 XT 16GB', performance: 90, suitable1080p: true, suitable1440p: true, price: 499 },
  } as Record<string, Gpu>,
  storage: {
    'samsung-500gb': { name: 'Samsung 980 Pro 500GB NVMe', type: 'NVMe', capacity: 500, price: 79 },
    'wd-1tb': { name: 'WD Black SN850X 1TB NVMe', type: 'NVMe', capacity: 1000, price: 129 },
    'samsung-1tb': { name: 'Samsung 990 Pro 1TB NVMe', type: 'NVMe', capacity: 1000, price: 149 },
    'crucial-2tb': { name: 'Crucial P5 Plus 2TB NVMe', type: 'NVMe', capacity: 2000, price: 179 },
    'wd-2tb-sata': { name: 'WD Blue 2TB SATA SSD', type: 'SATA', capacity: 2000, price: 159 },
    'kingston-500gb-sata': { name: 'Kingston A400 500GB SATA SSD', type: 'SATA', capacity: 500, price: 49 },
    'crucial-250gb-sata': { name: 'Crucial BX500 250GB SATA SSD', type: 'SATA', capacity: 250, price: 29 },
  } as Record<string, Storage>,
  cooler: {
    'noctua-nh-d15': { name: 'Noctua NH-D15', type: 'Air', maxTDP: 165, price: 109 },
    'arctic-34': { name: 'Arctic Freezer 34', type: 'Air', maxTDP: 150, price: 39 },
    'deepcool-gammaxx': { name: 'DeepCool GAMMAXX 400', type: 'Air', maxTDP: 130, price: 25 },
    'stock-cooler': { name: 'Stock Cooler', type: 'Air', maxTDP: 95, price: 0 },
    'corsair-h100i': { name: 'Corsair H100i 240mm AIO', type: 'Liquid', maxTDP: 250, price: 119 },
    'nzxt-x63': { name: 'NZXT Kraken X63 280mm AIO', type: 'Liquid', maxTDP: 300, price: 149 },
  } as Record<string, Cooler>,
};

const emptyBuild = (): BuildState => ({
  cpu: null,
  mobo: null,
  ram: null,
  gpu: null,
  storage: null,
  cooler: null,
});

const randomChoice = <T,>(items: T[]): T => items[Math.floor(Math.random() * items.length)];

const randomInt = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1)) + min;

const randomBudget = (tier: ScenarioUseCase['budgetTier']) => {
  const budgetRanges: Record<ScenarioUseCase['budgetTier'], [number, number]> = {
    ultraLow: [600, 850],
    low: [850, 1200],
    mid: [1200, 1800],
    high: [1800, 2500],
    premium: [2500, 3500],
  };
  const [start, end] = budgetRanges[tier];
  return Math.round(randomInt(start, end) / 50) * 50;
};

const generateScenario = (): ActiveScenario => {
  const useCase = randomChoice(Object.keys(scenarioTemplates.useCases));
  const useCaseDef = scenarioTemplates.useCases[useCase];
  return {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
    customer: randomChoice(scenarioTemplates.customers),
    adjective: randomChoice(useCaseDef.adjectives),
    useCase,
    budget: randomBudget(useCaseDef.budgetTier),
    psuWattage: randomChoice(scenarioTemplates.psuWattages),
    requirements: {
      cpuTier: useCaseDef.cpuTier,
      gpuTier: useCaseDef.gpuTier,
      ramMin: useCaseDef.ramMin,
      storageType: useCaseDef.storageType,
      storageMin: useCaseDef.storageMin,
      resolution: useCaseDef.resolution,
    },
  };
};

const computeCompatibility = (build: BuildState): CompatibilityResult => {
  const issues: string[] = [];
  const passes: string[] = [];

  const cpu = build.cpu ? components.cpu[build.cpu] : null;
  const mobo = build.mobo ? components.mobo[build.mobo] : null;
  const ram = build.ram ? components.ram[build.ram] : null;
  const cooler = build.cooler ? components.cooler[build.cooler] : null;

  if (cpu && mobo) {
    if (cpu.socket === mobo.socket) passes.push(`CPU socket matches motherboard (${cpu.socket})`);
    else issues.push(`Socket mismatch: CPU ${cpu.socket} vs motherboard ${mobo.socket}`);
  }

  if (cpu && ram) {
    if (cpu.ram === ram.type) passes.push(`RAM type matches CPU (${cpu.ram})`);
    else issues.push(`RAM mismatch: CPU needs ${cpu.ram}, selected ${ram.type}`);
  }

  if (mobo && ram) {
    if (mobo.ram === ram.type) passes.push(`RAM type matches motherboard (${mobo.ram})`);
    else issues.push(`RAM mismatch: motherboard needs ${mobo.ram}, selected ${ram.type}`);
  }

  if (cpu && cooler) {
    if (cooler.maxTDP >= cpu.tdp) passes.push(`Cooler TDP is adequate (${cooler.maxTDP}W ≥ ${cpu.tdp}W)`);
    else issues.push(`Cooler TDP insufficient (${cooler.maxTDP}W < ${cpu.tdp}W)`);
  }

  return { issues, passes };
};

const evaluateLab = (build: BuildState, scenario: ActiveScenario): EvalResult => {
  if (!build.cpu || !build.mobo || !build.ram || !build.storage || !build.cooler) {
    return {
      score: 0,
      passed: false,
      feedback: [{ type: 'fail', text: 'Select all required components before submitting.' }],
    };
  }

  const cpu = components.cpu[build.cpu];
  const mobo = components.mobo[build.mobo];
  const ram = components.ram[build.ram];
  const gpu = build.gpu ? components.gpu[build.gpu] : null;
  const storage = components.storage[build.storage];
  const cooler = components.cooler[build.cooler];

  const req = scenario.requirements;
  const feedback: FeedbackItem[] = [];
  let score = 0;

  const totalCost = cpu.price + mobo.price + ram.price + (gpu?.price ?? 0) + storage.price + cooler.price;

  score += 20;
  feedback.push({ type: 'pass', text: `CPU selected: ${cpu.name} (+20)` });

  if (cpu.socket === mobo.socket) {
    score += 20;
    feedback.push({ type: 'pass', text: `CPU/motherboard socket match (${cpu.socket}) (+20)` });
  } else {
    feedback.push({ type: 'fail', text: `Socket mismatch: ${cpu.socket} vs ${mobo.socket} (+0)` });
  }

  if (cpu.ram === ram.type && mobo.ram === ram.type) {
    score += 20;
    feedback.push({ type: 'pass', text: `RAM type compatible (${ram.type}) (+20)` });
  } else {
    feedback.push({ type: 'fail', text: 'RAM type is not compatible with CPU/motherboard (+0)' });
  }

  if (req.gpuTier === 'optional') {
    score += 15;
    feedback.push({ type: 'pass', text: 'Dedicated GPU optional for this scenario (+15)' });
  } else if (!gpu) {
    feedback.push({ type: 'fail', text: 'GPU required by scenario but not selected (+0)' });
  } else if (req.resolution === '1440p' && gpu.suitable1440p) {
    score += 15;
    feedback.push({ type: 'pass', text: 'GPU suitable for 1440p target (+15)' });
  } else if (req.resolution === '1080p' && gpu.suitable1080p) {
    score += 15;
    feedback.push({ type: 'pass', text: 'GPU suitable for 1080p target (+15)' });
  } else if (req.resolution === '4K' || req.resolution === '1440p+') {
    const partial = Math.round((gpu.performance / 100) * 15);
    score += partial;
    feedback.push({ type: 'warn', text: `GPU partially meets high-end target (+${partial})` });
  } else {
    feedback.push({ type: 'fail', text: 'GPU does not meet scenario target (+0)' });
  }

  if (storage.capacity >= req.storageMin) {
    if (req.storageType === 'NVMe' && storage.type === 'NVMe') {
      score += 10;
      feedback.push({ type: 'pass', text: `Storage meets NVMe requirement (${storage.capacity}GB) (+10)` });
    } else if (req.storageType === 'any') {
      score += 10;
      feedback.push({ type: 'pass', text: `Storage capacity meets requirement (${storage.capacity}GB) (+10)` });
    } else {
      score += 5;
      feedback.push({ type: 'warn', text: 'Storage capacity is good but NVMe was requested (+5)' });
    }
  } else {
    feedback.push({ type: 'fail', text: `Storage too small (${storage.capacity}GB < ${req.storageMin}GB) (+0)` });
  }

  if (cooler.maxTDP >= cpu.tdp) {
    score += 10;
    feedback.push({ type: 'pass', text: `Cooler TDP is sufficient (${cooler.maxTDP}W ≥ ${cpu.tdp}W) (+10)` });
  } else {
    feedback.push({ type: 'fail', text: `Cooler TDP too low (${cooler.maxTDP}W < ${cpu.tdp}W) (+0)` });
  }

  if (totalCost <= scenario.budget) {
    score += 5;
    feedback.push({ type: 'pass', text: `Within budget ($${totalCost} ≤ $${scenario.budget}) (+5)` });
  } else {
    feedback.push({ type: 'fail', text: `Over budget by $${totalCost - scenario.budget} (+0)` });
  }

  if (ram.capacity >= req.ramMin) {
    feedback.push({ type: 'pass', text: `RAM capacity meets requirement (${ram.capacity}GB ≥ ${req.ramMin}GB)` });
  } else {
    feedback.push({ type: 'fail', text: `RAM capacity too low (${ram.capacity}GB < ${req.ramMin}GB)` });
  }

  return { score, feedback, passed: score >= 80 };
};

const pickTotalCost = (build: BuildState) => {
  const cpu = build.cpu ? components.cpu[build.cpu] : null;
  const mobo = build.mobo ? components.mobo[build.mobo] : null;
  const ram = build.ram ? components.ram[build.ram] : null;
  const gpu = build.gpu ? components.gpu[build.gpu] : null;
  const storage = build.storage ? components.storage[build.storage] : null;
  const cooler = build.cooler ? components.cooler[build.cooler] : null;
  return (cpu?.price ?? 0) + (mobo?.price ?? 0) + (ram?.price ?? 0) + (gpu?.price ?? 0) + (storage?.price ?? 0) + (cooler?.price ?? 0);
};

const estimatePowerDraw = (build: BuildState) => {
  const cpu = build.cpu ? components.cpu[build.cpu] : null;
  const gpu = build.gpu ? components.gpu[build.gpu] : null;
  const storage = build.storage ? components.storage[build.storage] : null;
  const ram = build.ram ? components.ram[build.ram] : null;

  const cpuWatts = cpu?.tdp ?? 0;
  const gpuWatts = gpu ? 60 + Math.round(gpu.performance * 2.2) : 0;
  const storageWatts = storage ? (storage.type === 'NVMe' ? 8 : 6) : 0;
  const ramWatts = ram ? Math.max(6, Math.round(ram.capacity / 4)) : 0;
  const motherboardReserve = build.mobo ? 45 : 0;
  return cpuWatts + gpuWatts + storageWatts + ramWatts + motherboardReserve;
};

const fmtCurrency = (value: number) => `$${value.toLocaleString()}`;

const normalizeWord = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');

const buildScenarioTitle = (adjective: string, useCaseName: string) => {
  const adjectiveWords = adjective.split(/\s+/).filter(Boolean);
  const useCaseWords = useCaseName.split(/\s+/).filter(Boolean);

  if (!adjectiveWords.length) return useCaseName;

  const adjectiveTokens = new Set(adjectiveWords.map(normalizeWord).filter(Boolean));
  const filteredUseCase = useCaseWords.filter((word, index) => {
    const token = normalizeWord(word);
    if (!token) return false;
    const prevToken = index > 0 ? normalizeWord(useCaseWords[index - 1]) : '';
    if (token === prevToken) return false;
    return !adjectiveTokens.has(token);
  });

  const combined = [...adjectiveWords, ...filteredUseCase];
  const deduped = combined.filter((word, index) => {
    const token = normalizeWord(word);
    if (!token) return false;
    const prevToken = index > 0 ? normalizeWord(combined[index - 1]) : '';
    return token !== prevToken;
  });

  return deduped.join(' ') || adjective || useCaseName;
};

export default function PcAssemblyLab({ labSlug = 'pc-assembly' }: Props) {
  const [activeScenario, setActiveScenario] = useState<ActiveScenario | null>(null);
  const [build, setBuild] = useState<BuildState>(() => emptyBuild());
  const [results, setResults] = useState<EvalResult | null>(null);

  useEffect(() => {
    setActiveScenario(generateScenario());
  }, []);

  const compatibility = useMemo(() => computeCompatibility(build), [build]);
  const totalCost = useMemo(() => pickTotalCost(build), [build]);
  const estimatedDraw = useMemo(() => estimatePowerDraw(build), [build]);
  const budgetPercent = activeScenario
    ? Math.min(100, Math.round((totalCost / activeScenario.budget) * 100))
    : 0;

  const isComplete = Boolean(build.cpu && build.mobo && build.ram && build.storage && build.cooler);
  const cpu = build.cpu ? components.cpu[build.cpu] : null;
  const mobo = build.mobo ? components.mobo[build.mobo] : null;
  const ram = build.ram ? components.ram[build.ram] : null;
  const storage = build.storage ? components.storage[build.storage] : null;
  const gpu = build.gpu ? components.gpu[build.gpu] : null;

  const requirements = activeScenario
    ? [
        {
          id: 'required-parts',
          label: 'Required parts selected',
          pass: isComplete,
          message: isComplete ? 'All required components selected' : 'CPU, motherboard, RAM, storage, and cooler are required',
        },
        {
          id: 'socket-match',
          label: 'CPU and motherboard socket match',
          pass: Boolean(cpu && mobo && cpu.socket === mobo.socket),
          message: cpu && mobo ? `${cpu.socket} vs ${mobo.socket}` : 'Select CPU and motherboard',
        },
        {
          id: 'ram-requirements',
          label: `RAM type and capacity (${activeScenario.requirements.ramMin}GB+)`,
          pass: Boolean(cpu && mobo && ram && cpu.ram === ram.type && mobo.ram === ram.type && ram.capacity >= activeScenario.requirements.ramMin),
          message: ram ? `${ram.type} · ${ram.capacity}GB` : 'Select RAM',
        },
        {
          id: 'storage-requirements',
          label: `Storage requirement (${activeScenario.requirements.storageMin}GB ${activeScenario.requirements.storageType})`,
          pass: Boolean(
            storage &&
            storage.capacity >= activeScenario.requirements.storageMin &&
            (activeScenario.requirements.storageType === 'any' || storage.type === activeScenario.requirements.storageType)
          ),
          message: storage ? `${storage.type} · ${storage.capacity}GB` : 'Select storage',
        },
        {
          id: 'gpu-requirement',
          label: activeScenario.requirements.gpuTier === 'optional' ? 'GPU optional for this scenario' : 'GPU required for this scenario',
          pass: activeScenario.requirements.gpuTier === 'optional' ? true : Boolean(gpu),
          message: gpu ? gpu.name : 'No GPU selected',
        },
        {
          id: 'budget-check',
          label: 'Within budget',
          pass: totalCost <= activeScenario.budget,
          message: `${fmtCurrency(totalCost)} / ${fmtCurrency(activeScenario.budget)}`,
        },
        {
          id: 'psu-check',
          label: 'PSU wattage headroom',
          pass: estimatedDraw <= activeScenario.psuWattage,
          message: `${estimatedDraw}W / ${activeScenario.psuWattage}W available`,
        },
      ]
    : [];

  const emitWorkspaceResult = (action: 'check' | 'submit' | 'reset', passed: boolean, progress: number, message: string) => {
    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: labSlug,
          action,
          passed,
          progress,
          message,
          difficulty: 'Intermediate',
          estMinutes: 20,
        },
      })
    );
  };

  const resetBuild = () => {
    setBuild(emptyBuild());
    setResults(null);
  };

  const validateBuild = () => {
    const passed = compatibility.issues.length === 0 && isComplete;
    setLastResult(labSlug, {
      passed,
      score: null,
      checks: requirements,
      timestamp: Date.now(),
      action: 'check',
      message: passed ? 'Compatibility check passed' : 'Resolve compatibility issues',
    });
    emitWorkspaceResult('check', passed, passed ? 70 : 40, passed ? 'Compatibility check passed' : 'Resolve compatibility issues');
  };

  const gradeBuild = () => {
    if (!activeScenario) return;
    const evaluated = evaluateLab(build, activeScenario);
    setResults(evaluated);
    setLastResult(labSlug, {
      passed: evaluated.passed,
      score: evaluated.score,
      checks: requirements,
      timestamp: Date.now(),
      action: 'submit',
      message: evaluated.passed ? 'Build passed grading' : `Build score ${evaluated.score}/100`,
    });
    emitWorkspaceResult(
      'submit',
      evaluated.passed,
      evaluated.passed ? 100 : Math.max(40, evaluated.score),
      evaluated.passed ? 'Build passed grading' : `Build score ${evaluated.score}/100`,
    );
  };

  const handleReset = () => {
    resetBuild();
    emitWorkspaceResult('reset', false, 0, 'Build reset');
  };

  const handleRun = () => {
    validateBuild();
  };

  const handleSubmit = () => {
    gradeBuild();
  };

  const handleNewScenario = () => {
    setActiveScenario(generateScenario());
    resetBuild();
    emitWorkspaceResult('reset', false, 0, 'New scenario generated');
  };

  useEffect(() => {
    if (!activeScenario) return;
    setRequirementChecklist(labSlug, requirements);
  }, [labSlug, activeScenario?.id, requirements]);

  useEffect(() => {
    const onAction = (event: Event) => {
      const detail = (event as CustomEvent<{ action?: string; slug?: string }>).detail;
      if (!detail || detail.slug !== labSlug) return;
      if (detail.action === 'run' || detail.action === 'check') handleRun();
      if (detail.action === 'submit') handleSubmit();
      if (detail.action === 'reset') handleReset();
    };

    window.addEventListener('workspace:action', onAction);
    return () => window.removeEventListener('workspace:action', onAction);
  }, [labSlug, build, compatibility, isComplete, activeScenario]);

  if (!activeScenario) {
    return (
      <div className="pc-lab" data-testid="pc-lab-root">
        <article className="card pc-lab__panel">
          <p className="pc-lab__muted">Loading scenario…</p>
        </article>
      </div>
    );
  }

  const useCaseName = activeScenario.useCase.replace(/-/g, ' ');
  const scenarioTitle = buildScenarioTitle(activeScenario.adjective, useCaseName);

  return (
    <div className="pc-lab" data-testid="pc-lab-root">
      <article className="card pc-lab__scenario">
        <div className="pc-lab__scenario-head">
          <h3 data-testid="pc-scenario-title">Scenario: {scenarioTitle}</h3>
          <span className="badge badge--muted">Budget {fmtCurrency(activeScenario.budget)}</span>
          <span data-testid="pc-scenario-id" className="pc-lab__muted">ID: {activeScenario.id}</span>
        </div>
        <p>
          {activeScenario.customer} needs a system for {useCaseName}
          {activeScenario.requirements.resolution ? ` at ${activeScenario.requirements.resolution}` : ''}. PSU available: {activeScenario.psuWattage}W.
        </p>
        <ul className="pc-lab__requirements">
          <li>RAM minimum: {activeScenario.requirements.ramMin}GB</li>
          <li>Storage minimum: {activeScenario.requirements.storageMin}GB ({activeScenario.requirements.storageType})</li>
          <li>GPU: {activeScenario.requirements.gpuTier === 'optional' ? 'Optional' : 'Required for target workload'}</li>
        </ul>
      </article>

      <div className="pc-lab__grid">
        <article className="card pc-lab__panel">
          <h3>Component Selection</h3>
          <div className="pc-lab__fields">
            {([
              ['cpu', 'CPU', components.cpu],
              ['mobo', 'Motherboard', components.mobo],
              ['ram', 'RAM', components.ram],
              ['gpu', 'GPU (optional)', components.gpu],
              ['storage', 'Storage', components.storage],
              ['cooler', 'CPU Cooler', components.cooler],
            ] as const).map(([key, label, catalog]) => (
              <label className="pc-lab__field" key={key} htmlFor={`${labSlug}-${key}-select`}>
                <span>{label}</span>
                <select
                  id={`${labSlug}-${key}-select`}
                  className="pc-lab__select"
                  value={build[key] ?? ''}
                  onChange={(event) => {
                    const value = event.target.value || null;
                    setBuild((prev) => ({ ...prev, [key]: value }));
                    setResults(null);
                  }}
                  data-testid={`pc-select-${key}`}
                >
                  <option value="">Select {label}</option>
                  {Object.entries(catalog).map(([value, meta]) => (
                    <option key={value} value={value}>
                      {meta.name} - ${meta.price}
                    </option>
                  ))}
                </select>
              </label>
            ))}
          </div>
        </article>

        <article className="card pc-lab__panel">
          <h3>Your Build</h3>
          <div className="pc-lab__slots">
            {([
              ['cpu', 'CPU', components.cpu],
              ['mobo', 'Motherboard', components.mobo],
              ['ram', 'RAM', components.ram],
              ['gpu', 'GPU', components.gpu],
              ['storage', 'Storage', components.storage],
              ['cooler', 'CPU Cooler', components.cooler],
            ] as const).map(([key, label, catalog]) => {
              const selected = build[key] ? catalog[build[key] as keyof typeof catalog] : null;
              return (
                <div className={`pc-lab__slot ${selected ? 'pc-lab__slot--filled' : ''}`} key={key} data-testid={`pc-slot-${key}`}>
                  <div className="pc-lab__slot-label">{label}</div>
                  <div className="pc-lab__slot-value">{selected ? selected.name : `No ${label} selected`}</div>
                </div>
              );
            })}
          </div>

          <div className="pc-lab__budget" data-testid="pc-budget">
            <div className="pc-lab__budget-head">
              <span>Budget</span>
              <strong>{fmtCurrency(totalCost)} / {fmtCurrency(activeScenario.budget)}</strong>
            </div>
            <div className="pc-lab__budget-bar">
              <div
                className={`pc-lab__budget-fill ${
                  totalCost > activeScenario.budget ? 'is-over' : budgetPercent >= 90 ? 'is-warning' : 'is-safe'
                }`}
                style={{ width: `${budgetPercent}%` }}
              />
            </div>
            <p className="pc-lab__muted">Remaining: {fmtCurrency(activeScenario.budget - totalCost)}</p>
          </div>

          <div className="pc-lab__compat" data-testid="pc-compatibility">
            <h4>Compatibility</h4>
            {compatibility.issues.length === 0 && compatibility.passes.length === 0 && <p className="pc-lab__muted">Waiting for component selection…</p>}
            {compatibility.issues.map((item) => (
              <p className="pc-lab__compat-item pc-lab__compat-item--fail" key={`issue-${item}`}>✖ {item}</p>
            ))}
            {compatibility.passes.map((item) => (
              <p className="pc-lab__compat-item pc-lab__compat-item--pass" key={`pass-${item}`}>✔ {item}</p>
            ))}
          </div>

          <div className="pc-lab__compat" data-testid="pc-requirements-checklist">
            <h4>Requirements</h4>
            {requirements.map((entry) => (
              <p key={entry.id} className={`pc-lab__compat-item ${entry.pass ? 'pc-lab__compat-item--pass' : 'pc-lab__compat-item--fail'}`}>
                {entry.pass ? '✔' : '✖'} {entry.label} {entry.message ? `— ${entry.message}` : ''}
              </p>
            ))}
          </div>
        </article>
      </div>

      <article className="card pc-lab__panel">
        <div className="pc-lab__controls">
          <button className="btn-secondary" type="button" onClick={handleRun} data-testid="pc-run">Run</button>
          <button className="btn-secondary" type="button" onClick={handleReset} data-testid="pc-reset">Reset</button>
          <button
            className={`btn-primary ${!isComplete ? 'btn-is-disabled' : ''}`}
            type="button"
            onClick={handleSubmit}
            disabled={!isComplete}
            aria-disabled={!isComplete ? 'true' : 'false'}
            data-testid="pc-submit"
          >
            Submit for Grading
          </button>
          <button className="btn-ghost" type="button" onClick={handleNewScenario} data-testid="pc-new-scenario">New Scenario</button>
        </div>

        {results && (
          <div className="pc-lab__results" data-testid="pc-results">
            <div className={`pc-lab__score ${results.passed ? 'is-pass' : 'is-fail'}`}>
              {results.passed ? 'PASS' : 'FAIL'} · {results.score}/100
            </div>
            <div className="pc-lab__feedback">
              {results.feedback.map((entry, index) => (
                <p key={`${entry.text}-${index}`} className={`pc-lab__feedback-item pc-lab__feedback-item--${entry.type}`}>{entry.text}</p>
              ))}
            </div>
          </div>
        )}
      </article>
    </div>
  );
}
