import fs from 'node:fs';

const targetPath = 'c:/CustomApps/techSupportSim/server.ts';
let file = fs.readFileSync(targetPath, 'utf8');

const localInferenceCode = `
// Query In-House Cluster Ollama Node (Corsair #2: gemma4:31b)
async function queryClusterInference(systemPrompt: string, userPrompt: string, model: string = 'gemma4:31b', jsonMode: boolean = true): Promise<string | null> {
  const ollamaUrl = process.env.OLLAMA_API_URL || 'http://10.45.0.40:11434/v1';
  const targetModel = process.env.OLLAMA_MODEL || model;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 12000);

  try {
    const messages = [
      ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
      { role: 'user', content: userPrompt }
    ];

    const bodyPayload: any = {
      model: targetModel,
      messages,
      temperature: 0.7,
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
  file = file.replace("const attemptsStore: any[] = [];", "const attemptsStore: any[] = [];\n" + localInferenceCode);
  
  // Replace chat Gemini call with cluster first
  const chatCallOld = "      try {\n        const systemPrompt = `You are roleplaying as ${userName}";
  const chatCallNew = `      try {
        const systemPrompt = \`You are roleplaying as \${userName}, a \${userRole} in \${userDept} at a corporate enterprise in an IT support training simulator.
Personality & Background: \${scenario?.user?.personalityNotes || 'Busy professional trying to get work done'}.
Current Sentiment: \${currentUserMood}.
The problem you reported: "\${issueSummary}".
Current Technical State: IP is \${currentOsState?.ipAddress || 'APIPA'}, Account Locked: \${currentOsState?.accountLocked}, Display: \${currentOsState?.displayCableConnected}, Printer: \${currentOsState?.printerStatus}.

Realistic Behavioral Guidelines:
1. Speak in first-person as \${userName} in an authentic corporate chat style (Slack / Teams).
2. If the technician is accusatory, rude, or asks "what did you do?!?!", react realistically! Defend yourself calmly or with surprise (e.g., explain that facilities moved the desk or that you didn't touch any settings, and you're just trying to do payroll/work). Do NOT say "Thank you" to an insult or accusation.
3. If the technician is empathetic and polite, appreciate their reassurance.
4. If they give instructions (like running a command, checking a cable, or asking for Employee ID), respond cooperatively with the simulated result.
5. If the issue is fixed, express genuine relief.
6. Keep your response concise (1-3 sentences).

Reply with a JSON object format:
{
  "reply": "Your message as \${userName}",
  "mood": "anxious" | "frustrated" | "neutral" | "relieved" | "delighted"
}\`;

        const userPrompt = \`Conversation history:\\n\${conversationHistory.map((m: any) => \`\${m.sender.toUpperCase()}: \${m.text}\`).join('\\n')}\\n\\nTECHNICIAN: \${userMessage}\\n\\nRespond as \${userName}:\`;

        // 1. Try In-House GPU Node (gemma4:31b on Corsair #2)
        const clusterOutput = await queryClusterInference(systemPrompt, userPrompt, 'gemma4:31b', true);
        if (clusterOutput) {
          try {
            let cleanJson = clusterOutput.trim();
            if (cleanJson.startsWith('\`\`\`json')) cleanJson = cleanJson.replace(/^\`\`\`json\\s*/, '').replace(/\\s*\`\`\`$/, '');
            else if (cleanJson.startsWith('\`\`\`')) cleanJson = cleanJson.replace(/^\`\`\`\\s*/, '').replace(/\\s*\`\`\`$/, '');
            const parsed = JSON.parse(cleanJson);
            if (parsed.reply) {
              aiReplyText = parsed.reply;
              if (parsed.mood) updatedMood = parsed.mood;
            }
          } catch (pe) {
            aiReplyText = clusterOutput;
          }
        }
`;
  file = file.replace(chatCallOld, chatCallNew);
  fs.writeFileSync(targetPath, file);
  console.log('Patched techSupportSim server.ts for in-house gemma4:31b inference');
} else {
  console.log('Already patched');
}
