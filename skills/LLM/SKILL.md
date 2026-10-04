---
name: LLM
version: "1.0.0"
category: "IA & Media"
tags:
  - LLM
description: Implémente des complétions de chat avec de grands modèles de langage (LLM) à l'aide du z-ai-web-dev-sdk. Utilisez ce skill lorsque l'utilisateur doit créer des applications d'IA conversationnelle, des chatbots, des assistants IA ou toute fonctionnalité de génération de texte. Prend en charge les conversations multi-tours, les prompts système et la gestion du contexte.
language: fr
license: MIT

read_when:
  - Déclencher quand la demande concerne : implémente des complétions de chat avec de grands modèles de langage (LLM) à l'aide du z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : implémente, complétions, chat
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Skill LLM (Large Language Model)

Ce skill guide l'implémentation de la fonctionnalité de complétions de chat à l'aide du package z-ai-web-dev-sdk, permettant des capacités puissantes d'IA conversationnelle et de génération de texte.

## Emplacement du skill

**Emplacement du skill** : `{project_path}/skills/llm`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/chat.ts` pour un exemple fonctionnel.

## Vue d'ensemble

Le skill LLM permet de créer des applications qui tirent parti des grands modèles de langage pour la compréhension et la génération de langage naturel : chatbots, assistants IA, génération de contenu, et plus encore.

**IMPORTANT** : le z-ai-web-dev-sdk doit être utilisé exclusivement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Utilisation du CLI (pour les tâches simples)

Pour des complétions de chat simples et ponctuelles, vous pouvez utiliser le CLI z-ai au lieu d'écrire du code. C'est idéal pour des tests rapides, des requêtes simples ou des scripts d'automatisation.

### Chat de base

```bash
# Simple question
z-ai chat --prompt "What is the capital of France?"

# Save response to file
z-ai chat -p "Explain quantum computing" -o response.json

# Stream the response
z-ai chat -p "Write a short poem" --stream
```

### Avec prompt système

```bash
# Custom system prompt for specific behavior
z-ai chat \
  --prompt "Review this code: function add(a,b) { return a+b; }" \
  --system "You are an expert code reviewer" \
  -o review.json
```

### Avec réflexion (Chain of Thought)

```bash
# Enable thinking for complex reasoning
z-ai chat \
  --prompt "Solve this math problem: If a train travels 120km in 2 hours, what's its speed?" \
  --thinking \
  -o solution.json
```

### Paramètres du CLI

- `--prompt, -p <text>` : **Obligatoire** - contenu du message utilisateur
- `--system, -s <text>` : Optionnel - prompt système pour un comportement personnalisé
- `--thinking, -t` : Optionnel - activer le raisonnement pas à pas (désactivé par défaut)
- `--output, -o <path>` : Optionnel - chemin du fichier de sortie (format JSON)
- `--stream` : Optionnel - streame la réponse en temps réel

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des questions ponctuelles rapides
- Des scripts d'automatisation simples
- Tester des prompts
- Des conversations à un seul tour

**Utilisez le SDK pour :**
- Des conversations multi-tours avec contexte
- Une gestion personnalisée des conversations
- L'intégration avec des applications web
- Des workflows de chat complexes
- Des applications de production

## Complétions de chat de base

### Question-réponse simple

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function askQuestion(question) {
  const zai = await ZAI.create();

  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: 'You are a helpful assistant.'
      },
      {
        role: 'user',
        content: question
      }
    ],
    thinking: { type: 'disabled' }
  });

  const response = completion.choices[0]?.message?.content;
  return response;
}

// Usage
const answer = await askQuestion('What is the capital of France?');
console.log('Answer:', answer);
```

### Prompt système personnalisé

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function customAssistant(systemPrompt, userMessage) {
  const zai = await ZAI.create();

  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: systemPrompt
      },
      {
        role: 'user',
        content: userMessage
      }
    ],
    thinking: { type: 'disabled' }
  });

  return completion.choices[0]?.message?.content;
}

// Usage - Code reviewer
const codeReview = await customAssistant(
  'You are an expert code reviewer. Analyze code for bugs, performance issues, and best practices.',
  'Review this function: function add(a, b) { return a + b; }'
);

// Usage - Creative writer
const story = await customAssistant(
  'You are a creative fiction writer who writes engaging short stories.',
  'Write a short story about a robot learning to paint.'
);

console.log(codeReview);
console.log(story);
```

## Conversations multi-tours

### Gestion de l'historique de conversation

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ConversationManager {
  constructor(systemPrompt = 'You are a helpful assistant.') {
    this.messages = [
      {
        role: 'assistant',
        content: systemPrompt
      }
    ];
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async sendMessage(userMessage) {
    // Add user message to history
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    // Get completion
    const completion = await this.zai.chat.completions.create({
      messages: this.messages,
      thinking: { type: 'disabled' }
    });

    const assistantResponse = completion.choices[0]?.message?.content;

    // Add assistant response to history
    this.messages.push({
      role: 'assistant',
      content: assistantResponse
    });

    return assistantResponse;
  }

  getHistory() {
    return this.messages;
  }

  clearHistory(systemPrompt = 'You are a helpful assistant.') {
    this.messages = [
      {
        role: 'assistant',
        content: systemPrompt
      }
    ];
  }

  getMessageCount() {
    // Subtract 1 for system message
    return this.messages.length - 1;
  }
}

// Usage
const conversation = new ConversationManager();
await conversation.initialize();

const response1 = await conversation.sendMessage('Hi, my name is John.');
console.log('AI:', response1);

const response2 = await conversation.sendMessage('What is my name?');
console.log('AI:', response2); // Should remember the name is John

console.log('Total messages:', conversation.getMessageCount());
```

### Conversations tenant compte du contexte

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ContextualChat {
  constructor() {
    this.messages = [];
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async startConversation(role, context) {
    // Set up system prompt with context
    const systemPrompt = `You are ${role}. Context: ${context}`;
    
    this.messages = [
      {
        role: 'assistant',
        content: systemPrompt
      }
    ];
  }

  async chat(userMessage) {
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    const completion = await this.zai.chat.completions.create({
      messages: this.messages,
      thinking: { type: 'disabled' }
    });

    const response = completion.choices[0]?.message?.content;

    this.messages.push({
      role: 'assistant',
      content: response
    });

    return response;
  }
}

// Usage - Customer support scenario
const support = new ContextualChat();
await support.initialize();

await support.startConversation(
  'a customer support agent for TechCorp',
  'The user has ordered product #12345 which is delayed due to shipping issues.'
);

const reply1 = await support.chat('Where is my order?');
console.log('Support:', reply1);

const reply2 = await support.chat('Can I get a refund?');
console.log('Support:', reply2);
```

## Cas d'usage avancés

### Génération de contenu

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ContentGenerator {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async generateBlogPost(topic, tone = 'professional') {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: `You are a professional content writer. Write in a ${tone} tone.`
        },
        {
          role: 'user',
          content: `Write a blog post about: ${topic}. Include an introduction, main points, and conclusion.`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }

  async generateProductDescription(productName, features) {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: 'You are an expert at writing compelling product descriptions for e-commerce.'
        },
        {
          role: 'user',
          content: `Write a product description for "${productName}". Key features: ${features.join(', ')}.`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }

  async generateEmailResponse(originalEmail, intent) {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: 'You are a professional email writer. Write clear, concise, and polite emails.'
        },
        {
          role: 'user',
          content: `Original email: "${originalEmail}"\n\nWrite a ${intent} response.`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }
}

// Usage
const generator = new ContentGenerator();
await generator.initialize();

const blogPost = await generator.generateBlogPost(
  'The Future of Artificial Intelligence',
  'informative'
);
console.log('Blog Post:', blogPost);

const productDesc = await generator.generateProductDescription(
  'Smart Watch Pro',
  ['Heart rate monitoring', 'GPS tracking', 'Waterproof', '7-day battery life']
);
console.log('Product Description:', productDesc);
```

### Analyse de données et résumé

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function analyzeData(data, analysisType) {
  const zai = await ZAI.create();

  const prompts = {
    summarize: 'You are a data analyst. Summarize the key insights from the data.',
    trend: 'You are a data analyst. Identify trends and patterns in the data.',
    recommendation: 'You are a business analyst. Provide actionable recommendations based on the data.'
  };

  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: prompts[analysisType] || prompts.summarize
      },
      {
        role: 'user',
        content: `Analyze this data:\n\n${JSON.stringify(data, null, 2)}`
      }
    ],
    thinking: { type: 'disabled' }
  });

  return completion.choices[0]?.message?.content;
}

// Usage
const salesData = {
  Q1: { revenue: 100000, customers: 250 },
  Q2: { revenue: 120000, customers: 280 },
  Q3: { revenue: 150000, customers: 320 },
  Q4: { revenue: 180000, customers: 380 }
};

const summary = await analyzeData(salesData, 'summarize');
const trends = await analyzeData(salesData, 'trend');
const recommendations = await analyzeData(salesData, 'recommendation');

console.log('Summary:', summary);
console.log('Trends:', trends);
console.log('Recommendations:', recommendations);
```

### Génération et débogage de code

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class CodeAssistant {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async generateCode(description, language) {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: `You are an expert ${language} programmer. Write clean, efficient, and well-commented code.`
        },
        {
          role: 'user',
          content: `Write ${language} code to: ${description}`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }

  async debugCode(code, issue) {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: 'You are an expert debugger. Identify bugs and suggest fixes.'
        },
        {
          role: 'user',
          content: `Code:\n${code}\n\nIssue: ${issue}\n\nFind the bug and suggest a fix.`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }

  async explainCode(code) {
    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'assistant',
          content: 'You are a programming teacher. Explain code clearly and simply.'
        },
        {
          role: 'user',
          content: `Explain what this code does:\n\n${code}`
        }
      ],
      thinking: { type: 'disabled' }
    });

    return completion.choices[0]?.message?.content;
  }
}

// Usage
const codeAssist = new CodeAssistant();
await codeAssist.initialize();

const newCode = await codeAssist.generateCode(
  'Create a function that sorts an array of objects by a specific property',
  'JavaScript'
);
console.log('Generated Code:', newCode);

const bugFix = await codeAssist.debugCode(
  'function add(a, b) { return a - b; }',
  'This function should add numbers but returns wrong results'
);
console.log('Debug Suggestion:', bugFix);
```

## Bonnes pratiques

### 1. Ingénierie des prompts

```javascript
// Bad: Vague prompt
const bad = await askQuestion('Tell me about AI');

// Good: Specific and structured prompt
async function askWithContext(topic, format, audience) {
  const zai = await ZAI.create();
  
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: `You are an expert educator. Explain topics clearly for ${audience}.`
      },
      {
        role: 'user',
        content: `Explain ${topic} in ${format} format. Include practical examples.`
      }
    ],
    thinking: { type: 'disabled' }
  });

  return completion.choices[0]?.message?.content;
}

const good = await askWithContext('artificial intelligence', 'bullet points', 'beginners');
```

### 2. Gestion des erreurs

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function safeCompletion(messages, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const zai = await ZAI.create();

      const completion = await zai.chat.completions.create({
        messages: messages,
        thinking: { type: 'disabled' }
      });

      const response = completion.choices[0]?.message?.content;

      if (!response || response.trim().length === 0) {
        throw new Error('Empty response from AI');
      }

      return {
        success: true,
        content: response,
        attempts: attempt
      };
    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt} failed:`, error.message);

      if (attempt < retries) {
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }
  }

  return {
    success: false,
    error: lastError.message,
    attempts: retries
  };
}
```

### 3. Gestion du contexte

```javascript
class ManagedConversation {
  constructor(maxMessages = 20) {
    this.maxMessages = maxMessages;
    this.systemPrompt = '';
    this.messages = [];
    this.zai = null;
  }

  async initialize(systemPrompt) {
    this.zai = await ZAI.create();
    this.systemPrompt = systemPrompt;
    this.messages = [
      {
        role: 'assistant',
        content: systemPrompt
      }
    ];
  }

  async chat(userMessage) {
    // Add user message
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    // Trim old messages if exceeding limit (keep system prompt)
    if (this.messages.length > this.maxMessages) {
      this.messages = [
        this.messages[0], // Keep system prompt
        ...this.messages.slice(-(this.maxMessages - 1))
      ];
    }

    const completion = await this.zai.chat.completions.create({
      messages: this.messages,
      thinking: { type: 'disabled' }
    });

    const response = completion.choices[0]?.message?.content;

    this.messages.push({
      role: 'assistant',
      content: response
    });

    return response;
  }

  getTokenEstimate() {
    // Rough estimate: ~4 characters per token
    const totalChars = this.messages
      .map(m => m.content.length)
      .reduce((a, b) => a + b, 0);
    return Math.ceil(totalChars / 4);
  }
}
```

### 4. Traitement des réponses

```javascript
async function getStructuredResponse(query, format = 'json') {
  const zai = await ZAI.create();

  const formatInstructions = {
    json: 'Respond with valid JSON only. No additional text.',
    list: 'Respond with a numbered list.',
    markdown: 'Respond in Markdown format.'
  };

  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: `You are a helpful assistant. ${formatInstructions[format]}`
      },
      {
        role: 'user',
        content: query
      }
    ],
    thinking: { type: 'disabled' }
  });

  const response = completion.choices[0]?.message?.content;

  // Parse JSON if requested
  if (format === 'json') {
    try {
      return JSON.parse(response);
    } catch (e) {
      console.error('Failed to parse JSON response');
      return { raw: response };
    }
  }

  return response;
}

// Usage
const jsonData = await getStructuredResponse(
  'List three programming languages with their primary use cases',
  'json'
);
console.log(jsonData);
```

## Cas d'usage courants

1. **Chatbots et assistants virtuels** : créer des interfaces conversationnelles pour le support client
2. **Génération de contenu** : créer des articles, des descriptions de produits, des textes marketing
3. **Assistance au code** : générer, expliquer et déboguer du code
4. **Analyse de données** : analyser et résumer des jeux de données complexes
5. **Traduction de langues** : traduire du texte d'une langue à l'autre
6. **Outils éducatifs** : créer des applications de tutorat et d'apprentissage
7. **Automatisation des e-mails** : générer des réponses d'e-mails professionnelles
8. **Écriture créative** : génération d'histoires, de poésie et de contenu créatif

## Exemples d'intégration

### API de chatbot Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';

const app = express();
app.use(express.json());

// Store conversations in memory (use database in production)
const conversations = new Map();

let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

app.post('/api/chat', async (req, res) => {
  try {
    const { sessionId, message, systemPrompt } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Get or create conversation history
    let history = conversations.get(sessionId) || [
      {
        role: 'assistant',
        content: systemPrompt || 'You are a helpful assistant.'
      }
    ];

    // Add user message
    history.push({
      role: 'user',
      content: message
    });

    // Get completion
    const completion = await zaiInstance.chat.completions.create({
      messages: history,
      thinking: { type: 'disabled' }
    });

    const aiResponse = completion.choices[0]?.message?.content;

    // Add AI response to history
    history.push({
      role: 'assistant',
      content: aiResponse
    });

    // Save updated history
    conversations.set(sessionId, history);

    res.json({
      success: true,
      response: aiResponse,
      messageCount: history.length - 1
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.delete('/api/chat/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  conversations.delete(sessionId);
  res.json({ success: true, message: 'Conversation cleared' });
});

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('Chatbot API running on port 3000');
  });
});
```

## Dépannage

**Problème** : « le SDK doit être utilisé côté backend »
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur

**Problème** : réponses vides ou incomplètes
- **Solution** : vérifiez que completion.choices[0]?.message?.content existe et n'est pas vide

**Problème** : contexte de conversation trop long
- **Solution** : implémentez un rognage des messages pour ne conserver que les plus récents

**Problème** : réponses incohérentes
- **Solution** : utilisez des prompts système plus spécifiques et donnez des instructions claires

**Problème** : erreurs de limitation de débit
- **Solution** : implémentez une logique de nouvelle tentative avec backoff exponentiel

## Conseils de performance

1. **Réutilisez l'instance du SDK** : créez l'instance ZAI une seule fois et réutilisez-la entre les requêtes
2. **Gérez la longueur du contexte** : rognez les anciens messages pour éviter les limites de tokens
3. **Implémentez un cache** : mettez en cache les réponses des requêtes courantes
4. **Utilisez des prompts spécifiques** : des prompts clairs donnent des réponses plus rapides et meilleures
5. **Gérez les erreurs avec soin** : implémentez une logique de nouvelle tentative et des réponses de repli

## Considérations de sécurité

1. **Validation des entrées** : validez et assainissez toujours les entrées utilisateur
2. **Limitation de débit** : implémentez des limites de débit pour prévenir les abus
3. **Protection des clés API** : n'exposez jamais les identifiants du SDK dans du code côté client
4. **Filtrage de contenu** : filtrez les contenus sensibles ou inappropriés
5. **Gestion des sessions** : implémentez une gestion et un nettoyage appropriés des sessions

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé - importez-le comme montré dans les exemples
- Utilisez le rôle 'assistant' pour les prompts système
- Définissez thinking sur { type: 'disabled' } pour les complétions standard
- Implémentez une gestion d'erreurs et des nouvelles tentatives appropriées en production
- Gérez l'historique de conversation pour éviter les limites de tokens
- Des prompts clairs et spécifiques donnent de meilleurs résultats
- Consultez `scripts/chat.ts` pour un exemple de démarrage rapide
