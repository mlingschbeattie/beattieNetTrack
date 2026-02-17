// Scenario generation templates
      const scenarioTemplates = {
        useCases: {
          'gaming-1080p': {
            adjectives: ['casual', 'budget-friendly', 'entry-level', 'basic'],
            resolution: '1080p',
            cpuTier: 'low',
            gpuTier: 'entry',
            ramMin: 8,
            storageType: 'any',
            storageMin: 500,
            budgetTier: 'low'
          },
          'gaming-1440p': {
            adjectives: ['mid-range', 'balanced', 'solid', 'capable'],
            resolution: '1440p',
            cpuTier: 'mid',
            gpuTier: 'mid',
            ramMin: 16,
            storageType: 'any',
            storageMin: 500,
            budgetTier: 'mid'
          },
          'gaming-premium': {
            adjectives: ['high-end', 'powerful', 'enthusiast', 'premium'],
            resolution: '1440p+',
            cpuTier: 'high',
            gpuTier: 'high',
            ramMin: 16,
            storageType: 'NVMe',
            storageMin: 1000,
            budgetTier: 'high'
          },
          'gaming-ultra': {
            adjectives: ['ultra-high-end', 'flagship', 'extreme', 'top-tier'],
            resolution: '4K',
            cpuTier: 'ultra',
            gpuTier: 'ultra',
            ramMin: 32,
            storageType: 'NVMe',
            storageMin: 1000,
            budgetTier: 'premium'
          },
          'office': {
            adjectives: ['professional', 'business', 'office', 'productivity'],
            resolution: null,
            cpuTier: 'low',
            gpuTier: 'optional',
            ramMin: 8,
            storageType: 'any',
            storageMin: 250,
            budgetTier: 'ultraLow'
          },
          'content-creation': {
            adjectives: ['creative', 'content creation', 'multimedia', 'design'],
            resolution: null,
            cpuTier: 'high',
            gpuTier: 'mid',
            ramMin: 32,
            storageType: 'NVMe',
            storageMin: 1000,
            budgetTier: 'high'
          },
          'workstation': {
            adjectives: ['professional', 'workstation', 'power-user', 'advanced'],
            resolution: null,
            cpuTier: 'ultra',
            gpuTier: 'high',
            ramMin: 32,
            storageType: 'NVMe',
            storageMin: 2000,
            budgetTier: 'premium'
          },
          'home-media': {
            adjectives: ['home media', 'HTPC', 'entertainment', 'streaming'],
            resolution: null,
            cpuTier: 'low',
            gpuTier: 'optional',
            ramMin: 8,
            storageType: 'any',
            storageMin: 1000,
            budgetTier: 'low'
          }
        },
        customers: [
          'A student', 'A professional', 'An enthusiast', 'A small business owner',
          'A gamer', 'A content creator', 'A freelancer', 'A home user',
          'An IT department', 'A startup company'
        ],
        psuWattages: [450, 550, 650, 750, 850, 1000, 1200, 1500]
      };

      // Component database with specifications and prices
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
          'amd-r3-4100': { name: 'AMD Ryzen 3 4100', socket: 'AM4', ram: 'DDR4', tdp: 65, price: 99, performance: 55 }
        },
        mobo: {
          'asus-z790-ddr5': { name: 'ASUS ROG Z790', socket: 'LGA1700', ram: 'DDR5', formFactor: 'ATX', price: 329 },
          'msi-z790-ddr5': { name: 'MSI MPG Z790', socket: 'LGA1700', ram: 'DDR5', formFactor: 'ATX', price: 299 },
          'gigabyte-z790-ddr4': { name: 'Gigabyte Z790', socket: 'LGA1700', ram: 'DDR4', formFactor: 'ATX', price: 249 },
          'asus-b650-ddr5': { name: 'ASUS TUF B650', socket: 'AM5', ram: 'DDR5', formFactor: 'ATX', price: 189 },
          'msi-x670-ddr5': { name: 'MSI X670', socket: 'AM5', ram: 'DDR5', formFactor: 'ATX', price: 279 },
          'asus-b550-ddr4': { name: 'ASUS B550', socket: 'AM4', ram: 'DDR4', formFactor: 'ATX', price: 149 },
          'asrock-b660-ddr4': { name: 'ASRock B660M', socket: 'LGA1700', ram: 'DDR4', formFactor: 'mATX', price: 119 },
          'gigabyte-a520': { name: 'Gigabyte A520M', socket: 'AM4', ram: 'DDR4', formFactor: 'mATX', price: 79 }
        },
        ram: {
          'corsair-16gb-ddr5': { name: 'Corsair Vengeance 16GB DDR5-5600', type: 'DDR5', capacity: 16, speed: 5600, price: 109 },
          'gskill-32gb-ddr5': { name: 'G.Skill Trident 32GB DDR5-6000', type: 'DDR5', capacity: 32, speed: 6000, price: 179 },
          'kingston-16gb-ddr5': { name: 'Kingston Fury 16GB DDR5-5200', type: 'DDR5', capacity: 16, speed: 5200, price: 99 },
          'corsair-32gb-ddr4': { name: 'Corsair Vengeance 32GB DDR4-3200', type: 'DDR4', capacity: 32, speed: 3200, price: 89 },
          'gskill-16gb-ddr4': { name: 'G.Skill Ripjaws 16GB DDR4-3600', type: 'DDR4', capacity: 16, speed: 3600, price: 69 },
          'teamgroup-8gb-ddr4': { name: 'Team T-Force 8GB DDR4-3200', type: 'DDR4', capacity: 8, speed: 3200, price: 39 }
        },
        gpu: {
          'rtx-4060': { name: 'NVIDIA RTX 4060 8GB', performance: 75, suitable1080p: true, suitable1440p: true, price: 299 },
          'rtx-4060ti': { name: 'NVIDIA RTX 4060 Ti 16GB', performance: 82, suitable1080p: true, suitable1440p: true, price: 499 },
          'rtx-4070': { name: 'NVIDIA RTX 4070 12GB', performance: 88, suitable1080p: true, suitable1440p: true, price: 599 },
          'rtx-4070ti': { name: 'NVIDIA RTX 4070 Ti 12GB', performance: 94, suitable1080p: true, suitable1440p: true, price: 799 },
          'rx-7600': { name: 'AMD Radeon RX 7600 8GB', performance: 72, suitable1080p: true, suitable1440p: false, price: 269 },
          'rx-7700xt': { name: 'AMD Radeon RX 7700 XT 12GB', performance: 84, suitable1080p: true, suitable1440p: true, price: 449 },
          'rx-7800xt': { name: 'AMD Radeon RX 7800 XT 16GB', performance: 90, suitable1080p: true, suitable1440p: true, price: 499 }
        },
        storage: {
          'samsung-500gb': { name: 'Samsung 980 Pro 500GB NVMe', type: 'NVMe', capacity: 500, price: 79 },
          'wd-1tb': { name: 'WD Black SN850X 1TB NVMe', type: 'NVMe', capacity: 1000, price: 129 },
          'samsung-1tb': { name: 'Samsung 990 Pro 1TB NVMe', type: 'NVMe', capacity: 1000, price: 149 },
          'crucial-2tb': { name: 'Crucial P5 Plus 2TB NVMe', type: 'NVMe', capacity: 2000, price: 179 },
          'wd-2tb-sata': { name: 'WD Blue 2TB SATA SSD', type: 'SATA', capacity: 2000, price: 159 },
          'kingston-500gb-sata': { name: 'Kingston A400 500GB SATA SSD', type: 'SATA', capacity: 500, price: 49 },
          'crucial-250gb-sata': { name: 'Crucial BX500 250GB SATA SSD', type: 'SATA', capacity: 250, price: 29 }
        },
        cooler: {
          'noctua-nh-d15': { name: 'Noctua NH-D15', type: 'Air', maxTDP: 165, price: 109 },
          'arctic-34': { name: 'Arctic Freezer 34', type: 'Air', maxTDP: 150, price: 39 },
          'deepcool-gammaxx': { name: 'DeepCool GAMMAXX 400', type: 'Air', maxTDP: 130, price: 25 },
          'stock-cooler': { name: 'Stock Cooler', type: 'Air', maxTDP: 95, price: 0 },
          'corsair-h100i': { name: 'Corsair H100i 240mm AIO', type: 'Liquid', maxTDP: 250, price: 119 },
          'nzxt-x63': { name: 'NZXT Kraken X63 280mm AIO', type: 'Liquid', maxTDP: 300, price: 149 }
        }
      };

      let currentBuild = {
        cpu: null,
        mobo: null,
        ram: null,
        gpu: null,
        storage: null,
        cooler: null
      };

      let activeScenario = null;

      // Utility functions
      function randomChoice(array) {
        return array[Math.floor(Math.random() * array.length)];
      }

      function randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
      }

      function randomBudget(tier) {
        const budgetRanges = {
          ultraLow: [600, 850],
          low: [850, 1200],
          mid: [1200, 1800],
          high: [1800, 2500],
          premium: [2500, 3500]
        };
        const range = budgetRanges[tier];
        return Math.round(randomInt(range[0], range[1]) / 50) * 50;
      }

      // Scenario generation
      function generateScenario() {
        const useCaseKey = randomChoice(Object.keys(scenarioTemplates.useCases));
        const useCase = scenarioTemplates.useCases[useCaseKey];
        
        const adjective = randomChoice(useCase.adjectives);
        const customer = randomChoice(scenarioTemplates.customers);
        const budget = randomBudget(useCase.budgetTier);
        const psuWattage = randomChoice(scenarioTemplates.psuWattages);
        
        const scenario = {
          customer: customer,
          adjective: adjective,
          useCase: useCaseKey,
          budget: budget,
          psuWattage: psuWattage,
          requirements: {
            cpuTier: useCase.cpuTier,
            gpuTier: useCase.gpuTier,
            ramMin: useCase.ramMin,
            storageType: useCase.storageType,
            storageMin: useCase.storageMin,
            resolution: useCase.resolution
          }
        };
        
        return scenario;
      }

      function displayScenario() {
        const display = document.getElementById('scenario-display');
        const s = activeScenario;
        
        const useCaseName = s.useCase.replace(/-/g, ' ');
        const isGaming = s.useCase.startsWith('gaming');
        const resolutionText = s.requirements.resolution ? ` at ${s.requirements.resolution}` : '';
        
        let requirementsList = `
          <li><strong>CPU:</strong> Must support either DDR4 or DDR5</li>
          <li><strong>Motherboard:</strong> Must match CPU socket and support chosen RAM type</li>
          <li><strong>GPU:</strong> ${s.requirements.gpuTier === 'optional' ? 'Dedicated GPU optional (integrated graphics acceptable)' : `Suitable for ${s.requirements.resolution} gaming`}</li>
          <li><strong>RAM:</strong> Must be at least ${s.requirements.ramMin}GB</li>
          <li><strong>Storage:</strong> Must be at least ${s.requirements.storageMin}GB${s.requirements.storageType === 'NVMe' ? ' (NVMe required)' : ' (SATA or NVMe)'}</li>
          <li><strong>CPU Cooler:</strong> TDP rating must meet or exceed CPU TDP</li>
          <li><strong>Budget:</strong> Stay within the $${s.budget} budget</li>
        `;
        
        display.innerHTML = `
          <div style="border-left: 4px solid #00ff88; padding-left: 15px;">
            <h3 style="color: #00ff88; margin-bottom: 10px;">ðŸŽ¯ ${s.adjective.charAt(0).toUpperCase() + s.adjective.slice(1)} ${useCaseName.charAt(0).toUpperCase() + useCaseName.slice(1)} Setup</h3>
            <p style="margin-bottom: 15px; line-height: 1.6;">
              <strong>Objective:</strong> ${s.customer} needs a PC for ${useCaseName}${isGaming ? resolutionText : ''}. 
              Budget is <strong>$${s.budget}</strong>. They already own a case and ${s.psuWattage}W power supply.
            </p>
            <p style="color: #00d4ff; margin-bottom: 10px;"><strong>Requirements:</strong></p>
            <ul style="margin: 0 0 0 20px; line-height: 1.8;">
              ${requirementsList}
            </ul>
          </div>
        `;
      }

      // Component selection handlers
      function updateBuildDisplay() {
        const cpuData = currentBuild.cpu ? components.cpu[currentBuild.cpu] : null;
        const moboData = currentBuild.mobo ? components.mobo[currentBuild.mobo] : null;
        const ramData = currentBuild.ram ? components.ram[currentBuild.ram] : null;
        const gpuData = currentBuild.gpu ? components.gpu[currentBuild.gpu] : null;
        const storageData = currentBuild.storage ? components.storage[currentBuild.storage] : null;
        const coolerData = currentBuild.cooler ? components.cooler[currentBuild.cooler] : null;

        document.getElementById('build-cpu').innerHTML = cpuData ?
          `<div class="build-slot-label">âœ… CPU</div><div class="build-slot-content">${cpuData.name}<br><small>$${cpuData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² CPU</div><div class="build-slot-content"><span class="build-slot-empty">No CPU selected</span></div>`;

        document.getElementById('build-mobo').innerHTML = moboData ?
          `<div class="build-slot-label">âœ… Motherboard</div><div class="build-slot-content">${moboData.name}<br><small>$${moboData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² Motherboard</div><div class="build-slot-content"><span class="build-slot-empty">No motherboard selected</span></div>`;

        document.getElementById('build-ram').innerHTML = ramData ?
          `<div class="build-slot-label">âœ… RAM</div><div class="build-slot-content">${ramData.name}<br><small>$${ramData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² RAM</div><div class="build-slot-content"><span class="build-slot-empty">No RAM selected</span></div>`;

        document.getElementById('build-gpu').innerHTML = gpuData ?
          `<div class="build-slot-label">âœ… GPU</div><div class="build-slot-content">${gpuData.name}<br><small>$${gpuData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² GPU</div><div class="build-slot-content"><span class="build-slot-empty">No GPU selected</span></div>`;

        document.getElementById('build-storage').innerHTML = storageData ?
          `<div class="build-slot-label">âœ… Storage</div><div class="build-slot-content">${storageData.name}<br><small>$${storageData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² Storage</div><div class="build-slot-content"><span class="build-slot-empty">No storage selected</span></div>`;

        document.getElementById('build-cooler').innerHTML = coolerData ?
          `<div class="build-slot-label">âœ… CPU Cooler</div><div class="build-slot-content">${coolerData.name}<br><small>$${coolerData.price}</small></div>` :
          `<div class="build-slot-label">ðŸ”² CPU Cooler</div><div class="build-slot-content"><span class="build-slot-empty">No cooler selected</span></div>`;

        // Update budget
        const totalCost = (cpuData?.price || 0) + (moboData?.price || 0) + (ramData?.price || 0) + 
                          (gpuData?.price || 0) + (storageData?.price || 0) + (coolerData?.price || 0);
        const budget = activeScenario.budget;
        const percent = Math.min(100, (totalCost / budget) * 100);
        
        document.getElementById('budget-display').textContent = `$${totalCost} / $${budget}`;
        document.getElementById('budget-fill').style.width = `${percent}%`;
        document.getElementById('budget-percent').textContent = `${Math.round(percent)}%`;
        
        const budgetFill = document.getElementById('budget-fill');
        if (totalCost > budget) {
          budgetFill.classList.add('over');
        } else {
          budgetFill.classList.remove('over');
        }

        // Update slot styling
        ['cpu', 'mobo', 'ram', 'gpu', 'storage', 'cooler'].forEach(part => {
          const slot = document.getElementById(`build-${part}`);
          if (currentBuild[part]) {
            slot.classList.add('filled');
            slot.classList.remove('error');
          } else {
            slot.classList.remove('filled', 'error');
          }
        });

        checkRealTimeCompatibility();
      }

      function checkRealTimeCompatibility() {
        const compatList = document.getElementById('compat-list');
        const issues = [];
        const passes = [];
        
        const cpuData = currentBuild.cpu ? components.cpu[currentBuild.cpu] : null;
        const moboData = currentBuild.mobo ? components.mobo[currentBuild.mobo] : null;
        const ramData = currentBuild.ram ? components.ram[currentBuild.ram] : null;
        const coolerData = currentBuild.cooler ? components.cooler[currentBuild.cooler] : null;
        
        // Socket compatibility
        if (cpuData && moboData) {
          if (cpuData.socket === moboData.socket) {
            passes.push(`âœ… CPU socket matches motherboard (${cpuData.socket})`);
          } else {
            issues.push(`âŒ Socket mismatch: CPU is ${cpuData.socket}, motherboard is ${moboData.socket}`);
          }
        }
        
        // RAM compatibility
        if (cpuData && ramData) {
          if (cpuData.ram === ramData.type) {
            passes.push(`âœ… RAM type matches CPU (${cpuData.ram})`);
          } else {
            issues.push(`âŒ RAM type mismatch: CPU needs ${cpuData.ram}, selected ${ramData.type}`);
          }
        }
        
        if (moboData && ramData) {
          if (moboData.ram === ramData.type) {
            passes.push(`âœ… RAM type matches motherboard (${moboData.ram})`);
          } else {
            issues.push(`âŒ RAM type mismatch: Motherboard needs ${moboData.ram}, selected ${ramData.type}`);
          }
        }
        
        // TDP check
        if (cpuData && coolerData) {
          if (coolerData.maxTDP >= cpuData.tdp) {
            passes.push(`âœ… Cooler TDP adequate (${coolerData.maxTDP}W â‰¥ ${cpuData.tdp}W)`);
          } else {
            issues.push(`âŒ Cooler TDP insufficient: CPU needs ${cpuData.tdp}W, cooler rated for ${coolerData.maxTDP}W`);
          }
        }
        
        const html = [...issues.map(i => `<div class="compat-item compat-fail">${i}</div>`),
                       ...passes.map(p => `<div class="compat-item compat-pass">${p}</div>`)];
        
        compatList.innerHTML = html.length ? html.join('') : 
          '<div class="compat-item"><span class="compat-icon">âšª</span><span>Waiting for component selection...</span></div>';
        
        // Enable/disable submit
        const allSelected = currentBuild.cpu && currentBuild.mobo && currentBuild.ram && 
                            currentBuild.storage && currentBuild.cooler;
        document.getElementById('btn-submit').disabled = !allSelected || issues.length > 0;
      }

      // Grading function
      function evaluateLab() {
        const feedback = [];
        let score = 0;
        
        const cpuData = components.cpu[currentBuild.cpu];
        const moboData = components.mobo[currentBuild.mobo];
        const ramData = components.ram[currentBuild.ram];
        const gpuData = currentBuild.gpu ? components.gpu[currentBuild.gpu] : null;
        const storageData = components.storage[currentBuild.storage];
        const coolerData = components.cooler[currentBuild.cooler];
        
        const req = activeScenario.requirements;
        const totalCost = cpuData.price + moboData.price + ramData.price + 
                          (gpuData?.price || 0) + storageData.price + coolerData.price;
        
        // CPU (20 points)
        if (cpuData) {
          score += 20;
          feedback.push({ type: 'pass', text: `âœ“ CPU selected: ${cpuData.name} (+20 points)` });
        }
        
        // Socket compatibility (20 points)
        if (cpuData.socket === moboData.socket) {
          score += 20;
          feedback.push({ type: 'pass', text: `âœ“ CPU and motherboard sockets match (${cpuData.socket}) (+20 points)` });
        } else {
          feedback.push({ type: 'fail', text: `âœ— Socket mismatch: CPU ${cpuData.socket} â‰  Motherboard ${moboData.socket} (0 points)` });
        }
        
        // RAM compatibility (20 points)
        if (cpuData.ram === ramData.type && moboData.ram === ramData.type) {
          score += 20;
          feedback.push({ type: 'pass', text: `âœ“ RAM type (${ramData.type}) matches CPU and motherboard (+20 points)` });
        } else {
          feedback.push({ type: 'fail', text: `âœ— RAM type incompatible (0 points)` });
        }
        
        // GPU (15 points)
        if (req.gpuTier === 'optional') {
          score += 15;
          feedback.push({ type: 'pass', text: `âœ“ GPU is optional for this build (+15 points)` });
        } else if (gpuData) {
          if (req.resolution === '1440p' && gpuData.suitable1440p) {
            score += 15;
            feedback.push({ type: 'pass', text: `âœ“ GPU suitable for ${req.resolution} gaming (+15 points)` });
          } else if (req.resolution === '1080p' && gpuData.suitable1080p) {
            score += 15;
            feedback.push({ type: 'pass', text: `âœ“ GPU suitable for ${req.resolution} gaming (+15 points)` });
          } else if (req.resolution === '1440p+' || req.resolution === '4K') {
            score += Math.round((gpuData.performance / 100) * 15);
            feedback.push({ type: 'warn', text: `âš  GPU performance adequate but not optimal (+${Math.round((gpuData.performance / 100) * 15)} points)` });
          } else {
            feedback.push({ type: 'fail', text: `âœ— GPU not suitable for requirements (0 points)` });
          }
        } else {
          feedback.push({ type: 'fail', text: `âœ— GPU required but not selected (0 points)` });
        }
        
        // Storage (10 points)
        if (storageData.capacity >= req.storageMin) {
          if (req.storageType === 'NVMe' && storageData.type === 'NVMe') {
            score += 10;
            feedback.push({ type: 'pass', text: `âœ“ NVMe storage meets capacity requirement (${storageData.capacity}GB â‰¥ ${req.storageMin}GB) (+10 points)` });
          } else if (req.storageType === 'any') {
            score += 10;
            feedback.push({ type: 'pass', text: `âœ“ Storage meets capacity requirement (${storageData.capacity}GB â‰¥ ${req.storageMin}GB) (+10 points)` });
          } else {
            score += 5;
            feedback.push({ type: 'warn', text: `âš  Storage capacity OK but SATA instead of NVMe (+5 points)` });
          }
        } else {
          feedback.push({ type: 'fail', text: `âœ— Storage too small: ${storageData.capacity}GB < ${req.storageMin}GB (0 points)` });
        }
        
        // Cooler (10 points)
        if (coolerData.maxTDP >= cpuData.tdp) {
          score += 10;
          feedback.push({ type: 'pass', text: `âœ“ Cooler TDP adequate (${coolerData.maxTDP}W â‰¥ ${cpuData.tdp}W) (+10 points)` });
        } else {
          feedback.push({ type: 'fail', text: `âœ— Cooler TDP insufficient: ${coolerData.maxTDP}W < ${cpuData.tdp}W (0 points)` });
        }
        
        // Budget (5 points)
        if (totalCost <= activeScenario.budget) {
          score += 5;
          const saved = activeScenario.budget - totalCost;
          feedback.push({ type: 'pass', text: `âœ“ Within budget: $${totalCost} â‰¤ $${activeScenario.budget} (saved $${saved}) (+5 points)` });
        } else {
          const over = totalCost - activeScenario.budget;
          feedback.push({ type: 'fail', text: `âœ— Over budget by $${over} (0 points)` });
        }
        
        // RAM capacity check (bonus feedback)
        if (ramData.capacity >= req.ramMin) {
          feedback.push({ type: 'pass', text: `âœ“ RAM capacity meets requirement (${ramData.capacity}GB â‰¥ ${req.ramMin}GB)` });
        } else {
          feedback.push({ type: 'fail', text: `âœ— RAM capacity insufficient: ${ramData.capacity}GB < ${req.ramMin}GB` });
        }
        
        return { score, feedback };
      }

      // Event handlers
      document.getElementById('cpu-select').addEventListener('change', (e) => {
        currentBuild.cpu = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('mobo-select').addEventListener('change', (e) => {
        currentBuild.mobo = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('ram-select').addEventListener('change', (e) => {
        currentBuild.ram = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('gpu-select').addEventListener('change', (e) => {
        currentBuild.gpu = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('storage-select').addEventListener('change', (e) => {
        currentBuild.storage = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('cooler-select').addEventListener('change', (e) => {
        currentBuild.cooler = e.target.value || null;
        updateBuildDisplay();
      });

      document.getElementById('btn-validate').addEventListener('click', () => {
        checkRealTimeCompatibility();
        alert('Compatibility check complete. See results above.');
      });

      document.getElementById('btn-submit').addEventListener('click', () => {
        const results = evaluateLab();
        const resultsPanel = document.getElementById('results-panel');
        const scoreDisplay = document.getElementById('score-display');
        const feedbackList = document.getElementById('feedback-list');
        
        const passed = results.score >= 80;
        const grade = passed ? 'PASS' : 'FAIL';
        const gradeColor = passed ? '#00ff88' : '#ff4444';
        
        scoreDisplay.innerHTML = `<div style="color: ${gradeColor};">${grade}</div><div>Score: ${results.score}/100</div>`;
        
        feedbackList.innerHTML = results.feedback.map(f => 
          `<div class="feedback-item ${f.type}">${f.text}</div>`
        ).join('');
        
        resultsPanel.style.display = 'block';
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
      });

      document.getElementById('btn-reset').addEventListener('click', () => {
        currentBuild = { cpu: null, mobo: null, ram: null, gpu: null, storage: null, cooler: null };
        document.querySelectorAll('.component-select').forEach(select => select.value = '');
        document.getElementById('results-panel').style.display = 'none';
        document.getElementById('btn-submit').disabled = true;
        
        activeScenario = generateScenario();
        displayScenario();
        updateBuildDisplay();
      });

      // Initialize
      function initLab() {
        activeScenario = generateScenario();
        displayScenario();
        updateBuildDisplay();
      }

      initLab();
