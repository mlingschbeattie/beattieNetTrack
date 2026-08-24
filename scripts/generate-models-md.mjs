import fs from 'node:fs';
import path from 'node:path';

const content = `# Cluster Model Fleet & Inference Strategy

## Active Ollama Inference Nodes

### Corsair AI #1 (\`10.45.0.46\` / \`100.x.x.x\`)
- **Primary Role:** Active Workstation & Primary Coding Agent
- **Hardware:** AMD Ryzen AI 9 HX 370, 128GB LPDDR5X (111GB VRAM pool), gfx1151 ROCm
- **Active Model:**
  - \`qwen3-coder-next:latest\` (79.7B Q4, ~54GB VRAM) — Primary coding / Aider (\`aq\`)

---

### Corsair AI #2 (\`10.45.0.40\` / \`100.105.115.8\`)
- **Primary Role:** Dedicated Multi-Model Inference Server
- **Hardware:** AMD Ryzen AI 9 HX 370, 128GB LPDDR5X (111GB VRAM pool), gfx1151 ROCm
- **Active Models:**
  - \`qwen3-coder-next:latest\` — Aider / Coding fallback (\`aq\`)
  - \`gemma4:31b\` — General inference & conversational roleplay (\`ag\`)
  - \`gemma4:latest\` — Lightweight general inference
  - \`deepseek-r1:32b\` — Deep technical reasoning & architecture (\`ads\`)
  - \`deepseek-r1-32b-16k:latest\` — Complex reasoning with 16k context window

---

## App Model Allocation & Recommendations

| Application | Primary Model | Node | Fallback Model | Role & Use Case |
|---|---|---|---|---|
| **CyberLab Ethical Hacker** | \`qwen3-coder-next:latest\` | Corsair #1 (\`10.45.0.46\`) | \`deepseek-r1:32b\` | Cybersecurity mentor, MITRE ATT&CK mapping, defensive detection rules |
| **CyberTerminal CIS** | \`qwen3-coder-next:latest\` | Corsair #1 (\`10.45.0.46\`) | \`deepseek-r1:32b\` | Linux security advisor, command deconstruction, custom CTF generator |
| **Tech Support Simulator** | \`gemma4:31b\` | Corsair #2 (\`10.45.0.40\`) | \`qwen3-coder-next\` | Corporate employee dialogue roleplay, mood simulation, bedside-manner evaluation |
| **PC Build Simulator 3D** | \`gemma4:31b\` | Corsair #2 (\`10.45.0.40\`) | \`qwen3-coder-next\` | Hardware compatibility advisor, diagnostic coaching, benchmark analysis |

---

## Unified Local Inference Endpoint

Each ecosystem app connects to local inference via:
\`\`\`bash
# Direct Ollama API
OLLAMA_API_URL="http://10.45.0.40:11434/v1"

# Or Cluster Proxy via API Gateway
AI_CLUSTER_URL="https://api.beattietech.local/api/chat"
\`\`\`
`;

fs.writeFileSync('c:/Users/mlingsch/cluster/models.md', content);
console.log('models.md created successfully');
