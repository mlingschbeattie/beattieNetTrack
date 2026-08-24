import fs from 'node:fs';

const serverPath = 'c:/CustomApps/NexusPicker/server.ts';
const packageJsonPath = 'c:/CustomApps/NexusPicker/package.json';

const serverCode = `import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = 3000;

app.use(express.json());

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", app: "PC Build Simulator 3D (Nexus)", timestamp: new Date().toISOString() });
});

// Hardware Compatibility & PC Diagnostic AI Advisor (Corsair #2: gemma4:31b)
app.post("/api/ai/advisor", async (req, res) => {
  const { components, currentStep, userQuery } = req.body;
  const ollamaUrl = process.env.OLLAMA_API_URL || "http://10.45.0.40:11434/v1";
  const targetModel = process.env.OLLAMA_MODEL || "gemma4:31b";

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 12000);

    const prompt = \`You are an expert PC Hardware Technician and CompTIA A+ instructor.
Current Assembly Step: \${currentStep || "Component Selection"}
Installed Components: \${JSON.stringify(components || [])}
Student Question: "\${userQuery || "Check my build for compatibility and next wiring steps."}"

Provide concise, technical, and encouraging advice regarding pin connections, clearance, thermal paste application, or PSU wattage.\`;

    const response = await fetch(\`\${ollamaUrl}/chat/completions\`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        model: targetModel,
        messages: [
          { role: "system", content: "You are a master PC building engineer. Provide concise hardware guidance." },
          { role: "user", content: prompt }
        ],
        temperature: 0.5
      })
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data: any = await response.json();
      return res.json({ advice: data?.choices?.[0]?.message?.content || "Keep assembling according to motherboard manual." });
    }
  } catch (err: any) {
    console.warn("[Nexus AI] Offline fallback engaged:", err?.message);
  }

  res.json({
    advice: "Ensure motherboard standoffs are properly aligned, seat RAM firmly until both retention clips click, and verify 24-pin ATX power is locked."
  });
});

async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(\`Nexus PC Build Simulator server running on http://0.0.0.0:\${PORT}\`);
  });
}

startServer();
`;

fs.writeFileSync(serverPath, serverCode);

// Update package.json
let pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
pkg.scripts = {
  ...pkg.scripts,
  "dev": "tsx server.ts",
  "build": "vite build && esbuild server.ts --bundle --platform=node --format=cjs --packages=external --sourcemap --outfile=dist/server.cjs",
  "start": "node dist/server.cjs"
};
fs.writeFileSync(packageJsonPath, JSON.stringify(pkg, null, 2));

console.log('Created NexusPicker server.ts and updated package.json');
