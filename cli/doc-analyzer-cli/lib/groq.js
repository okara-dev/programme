const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';
const MODEL = 'groq/compound-mini';

/**
 * Sendet Text an Groq zur Analyse
 */
export async function analyzeWithGroq(text, options = {}) {
  const apiKey = process.env.GROQ_API_KEY;

  if (!apiKey) {
    throw new Error('GROQ_API_KEY ist nicht gesetzt');
  }

  const mode = options.mode || 'summary';
  const language = options.language || 'Deutsch';
  const customPrompt = options.prompt || null;

  // Prompt je nach Modus
  let systemPrompt;
  let userPrompt;

  if (customPrompt) {
    systemPrompt = `Du bist ein hilfreicher Assistent, der Dokumente analysiert. Antworte auf ${language}.`;
    userPrompt = `${customPrompt}\n\n--- DOKUMENT ---\n${text}`;
  } else {
    switch (mode) {
      case 'summary':
        systemPrompt = `Du bist ein Assistent, der Dokumente präzise zusammenfasst. Antworte auf ${language}. Sei klar und strukturiert.`;
        userPrompt = `Fasse das folgende Dokument zusammen. Gib eine kurze Übersicht und die wichtigsten Punkte:\n\n--- DOKUMENT ---\n${text}`;
        break;

      case 'explain':
        systemPrompt = `Du bist ein Assistent, der komplexe Dokumente einfach erklärt. Antworte auf ${language}.`;
        userPrompt = `Erkläre das folgende Dokument in einfachen Worten. Was steht drin? Was bedeutet es?\n\n--- DOKUMENT ---\n${text}`;
        break;

      case 'keypoints':
        systemPrompt = `Du bist ein Assistent, der die wichtigsten Punkte extrahiert. Antworte auf ${language}.`;
        userPrompt = `Extrahiere die wichtigsten Punkte aus dem folgenden Dokument als Liste:\n\n--- DOKUMENT ---\n${text}`;
        break;

      case 'analyze':
        systemPrompt = `Du bist ein Assistent, der Dokumente analysiert. Antworte auf ${language}.`;
        userPrompt = `Analysiere das folgende Dokument:\n- Was ist das für ein Dokument?\n- Was steht drin?\n- Was sind die wichtigsten Punkte?\n- Gibt es etwas Auffälliges?\n\n--- DOKUMENT ---\n${text}`;
        break;

      default:
        systemPrompt = `Du bist ein hilfreicher Assistent. Antworte auf ${language}.`;
        userPrompt = `${text}`;
    }
  }

  const body = {
    model: MODEL,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    temperature: 0.3,
    max_tokens: 2048
  };

  const response = await fetch(GROQ_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  const data = await response.json();

  if (!response.ok) {
    const errMsg = data.error?.message || JSON.stringify(data);
    throw new Error(`Groq API Fehler (${response.status}): ${errMsg}`);
  }

  return {
    result: data.choices[0].message.content,
    tokens: data.usage?.total_tokens || 0,
    model: data.model
  };
}

/**
 * Prüft ob der API Key gültig ist
 */
export async function checkApiKey() {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) return false;

  try {
    const response = await fetch(GROQ_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: 'OK' }],
        max_tokens: 5
      })
    });
    return response.ok;
  } catch {
    return false;
  }
}