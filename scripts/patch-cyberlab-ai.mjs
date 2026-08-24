import fs from 'node:fs';

const targetPath = 'c:/CustomApps/cyberLabEthicalHacker/server.ts';
let file = fs.readFileSync(targetPath, 'utf8');

const clusterHelper = `
// Query In-House Cluster Ollama Node (Corsair #1: qwen3-coder-next:latest)
async function queryClusterInference(systemPrompt: string, userPrompt: string, model: string = 'qwen3-coder-next:latest', jsonMode: boolean = false): Promise<string | null> {
  const ollamaUrl = process.env.OLLAMA_API_URL || 'http://10.45.0.46:11434/v1';
  const targetModel = process.env.OLLAMA_MODEL || model;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  try {
    const messages = [
      ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
      { role: 'user', content: userPrompt }
    ];

    const bodyPayload: any = {
      model: targetModel,
      messages,
      temperature: 0.4,
    };
    if (jsonMode) {
      bodyPayload.response_format = { type: 'json_object' };
    }

    const res = await fetch(\`\${ollamaUrl}/chat/completions\`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(bodyPayload),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      console.warn(\`[Cluster AI] \${ollamaUrl} returned \${res.status}\`);
      return null;
    }

    const data: any = await res.json();
    return data?.choices?.[0]?.message?.content || null;
  } catch (err: any) {
    clearTimeout(timeoutId);
    console.warn(\`[Cluster AI] Offline/Timeout (\${ollamaUrl}):\`, err?.message);
    return null;
  }
}
`;

if (!file.includes('queryClusterInference')) {
  file = file.replace('const app = express();', 'const app = express();\n' + clusterHelper);

  // Patch mentor endpoint
  const mentorOld = '    const ai = getGeminiClient();\n    if (!ai) {';
  const mentorNew = `    // 1. Try In-House GPU Node (qwen3-coder-next on Corsair #1)
    const clusterAnswer = await queryClusterInference(
      \`You are a distinguished Senior Cybersecurity Instructor and Certified Ethical Hacker (CEH/OSCP/Security+ certified) mentor. Format answers with clear headings, code snippets, and MITRE technique references when applicable.\`,
      \`User Question: \${question}\${context ? \`\\n\\nContext: \${context}\` : ''}\`,
      'qwen3-coder-next:latest',
      false
    );
    if (clusterAnswer) {
      return res.json({ answer: clusterAnswer, model: 'qwen3-coder-next (Local GPU)' });
    }

    const ai = getGeminiClient();
    if (!ai) {`;
  file = file.replace(mentorOld, mentorNew);

  // Patch generate-question endpoint
  const questionOld = '    const ai = getGeminiClient();\n\n    if (!ai) {';
  const questionNew = `    // 1. Try In-House GPU Node (qwen3-coder-next on Corsair #1)
    const clusterQuestion = await queryClusterInference(
      'You are a cybersecurity exam author. Output valid JSON adhering to the requested question schema.',
      \`Generate a realistic multiple-choice question for an Ethical Hacker / Cybersecurity certification in domain: "\${domain || 'Web Application Security'}" with difficulty "\${difficulty || 'Medium'}". Include question, 4 options (A, B, C, D), correctAnswer, explanation, mitreRef, remediation, and domain as valid JSON.\`,
      'qwen3-coder-next:latest',
      true
    );
    if (clusterQuestion) {
      try {
        let clean = clusterQuestion.trim();
        if (clean.startsWith('\`\`\`json')) clean = clean.replace(/^\`\`\`json\\s*/, '').replace(/\\s*\`\`\`$/, '');
        else if (clean.startsWith('\`\`\`')) clean = clean.replace(/^\`\`\`\\s*/, '').replace(/\\s*\`\`\`$/, '');
        return res.json(JSON.parse(clean));
      } catch (pe) {
        console.warn('Cluster JSON parse error, trying fallback');
      }
    }

    const ai = getGeminiClient();

    if (!ai) {`;
  file = file.replace(questionOld, questionNew);

  fs.writeFileSync(targetPath, file);
  console.log('Patched cyberLabEthicalHacker server.ts for qwen3-coder-next inference');
} else {
  console.log('Already patched');
}
