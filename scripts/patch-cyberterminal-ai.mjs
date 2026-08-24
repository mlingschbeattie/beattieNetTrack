import fs from 'node:fs';

const targetPath = 'c:/CustomApps/cyberTerminalCIS/server.ts';
let file = fs.readFileSync(targetPath, 'utf8');

// Ensure server defaults to in-house Ollama on Corsair #1
const defaultClusterCode = `
    const defaultClusterUrl = process.env.OLLAMA_API_URL || "http://10.45.0.46:11434/v1";
    const defaultClusterModel = process.env.OLLAMA_MODEL || "qwen3-coder-next:latest";
`;

if (!file.includes('defaultClusterUrl')) {
  file = file.replace('const requestedLevel = hintLevel || "Subtle Guide (Level 1)";', 'const requestedLevel = hintLevel || "Subtle Guide (Level 1)";\n' + defaultClusterCode);

  // Patch default cluster execution if no clusterConfig was passed
  const fallbackGeminiOld = '    // 2. Default to Gemini API if configured\n    const ai = getGeminiClient();';
  const fallbackGeminiNew = `    // 2. First try In-House GPU Node (Corsair #1: qwen3-coder-next:latest)
    try {
      const defaultEndpoint = formatOpenAIEndpoint(defaultClusterUrl);
      const cAbort = new AbortController();
      const cTimeout = setTimeout(() => cAbort.abort(), 12000);

      const promptInstructions = \`You are an expert Cybersecurity Instructor & Linux Mentor. 
STUDENT QUERY: "\${query || "I need guidance on solving this lab."}"
ACTIVE LAB: \${scenarioTitle} (\${scenarioCategory})
OBJECTIVE: \${scenarioObj}
DIRECTORY: \${currentDirectory || "/home/student"}
KNOWN FILES: \${scenarioFiles}
RECENT COMMANDS: \${JSON.stringify((commandHistory || []).slice(-5))}
HINT LEVEL: \${requestedLevel}

Provide an educational hint matching the requested level. 
Output strictly valid JSON with keys: hint, educationalContext, mitreTactic, suggestedCommand.\`;

      const cRes = await fetch(defaultEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: cAbort.signal,
        body: JSON.stringify({
          model: defaultClusterModel,
          messages: [
            { role: "system", content: "You are an expert cybersecurity advisor. Output strictly valid JSON." },
            { role: "user", content: promptInstructions }
          ],
          temperature: 0.3,
          response_format: { type: "json_object" }
        })
      });
      clearTimeout(cTimeout);

      if (cRes.ok) {
        const cData = await cRes.json();
        let content = cData?.choices?.[0]?.message?.content || "";
        if (content.startsWith("\`\`\`json")) content = content.replace(/^\`\`\`json\\s*/, "").replace(/\\s*\`\`\`$/, "");
        else if (content.startsWith("\`\`\`")) content = content.replace(/^\`\`\`\\s*/, "").replace(/\\s*\`\`\`$/, "");
        const parsed = JSON.parse(content);
        if (parsed.hint) {
          return res.json({
            hint: parsed.hint,
            educationalContext: parsed.educationalContext || \`Understanding Linux security and \${scenarioCategory}.\`,
            mitreTactic: parsed.mitreTactic || scenarioMitre,
            suggestedCommand: parsed.suggestedCommand || "ls -la",
            modelUsed: defaultClusterModel + " (Local GPU)"
          });
        }
      }
    } catch (cErr) {
      console.warn("[Cluster AI] Default cluster offline, proceeding to fallback");
    }

    // 2. Secondary fallback to Gemini API if configured
    const ai = getGeminiClient();`;

  file = file.replace(fallbackGeminiOld, fallbackGeminiNew);
  fs.writeFileSync(targetPath, file);
  console.log('Patched cyberTerminalCIS server.ts for default qwen3-coder-next inference');
} else {
  console.log('Already patched');
}
