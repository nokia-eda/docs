# Ask EDA

**Ask EDA** is the conversational (chat) interface built into the Nokia Event-Driven Automation (EDA) platform. It  allows you to interact with Nokia EDA using natural-language chat, enabling quick queries, AIOps assistance, dashboard creation, and context-specific help.

## Overview

The AIOps implementation for Nokia EDA is built around a conversational chat interface, **Ask EDA**, that lets you interact with the platform using natural-language dialogue. **Ask EDA** provides the following high-level features:

- Chat interface with history: you can ask follow-up questions without re-entering the full context, and the conversation history is displayed inline.
- Multiple persistent conversations per user: you can create, delete, or rename a conversation. Persistence is maintained during a session; a restart of Nokia EDA may clear the data (transient persistence).
- Chart generation: The chat can produce and display charts such as line charts, pie charts, bar charts, counters, and tables. You can link directly to the query view from a generated table.
- Resource linking: Agents can embed links to referenced resources, allowing you to navigate to those resources easily.
- Workflow triggering: you can start workflows from the chat, receive links to generated artifacts, and see a summary of the results.
- Model-type control for queries: for more information, see [Model selection options](#model-selection-options).
- Support for LLM providers with OpenAI-style API: for more information, see [LLM providers](#llm-providers).

### Key concepts

- Agentic AI: the main agent that orchestrates interactions with lower-level agents for task-specific purposes. Agents combine prompt engineering with additional resources such as workflows, APIs, and other agents.

- Tool: functionality that can be added to an agent through the common  `Manifest` resource; the tools can be as workflows.

- LLM provider: a configuration object that registers an external large-language-model service (for example, OpenAI, Google) with endpoint, API key, and model metadata. Nokia EDA supports LLM providers that expose an OpenAI-compatible API endpoint (`chat`/`completions` or `responses` APIs)

Nokia EDA follows an extensible, agent-centric model. A main agent is always present, alongside a number of other agents with task-specific purposes. The list of agents is outlined in [Agents](#agents).

**Ask EDA** extends the functionality provided in native query language (NQL) to be more context aware, and to allow follow up or iterative questions to refine information. The chat interface is equivalent to **show** commands on the CLI, where you can easily look back at previous results. It supports a alarm root cause and transaction detail analysis.

### LLM providers

The `Provider` resource adds OpenAI-style API LLM providers to Nokia EDA. This resource defines:

- The endpoint URL where the provider is can be reached; this can be the model's host or an LLM gateway.
- The API Key
- A list of models:
  
      - The model name, as defined by the LLM host
      - An optional description of the model
      - The API type (chat/completions, responses or embeddings )
      - The intended use of the model: chat, routing, or reasoning 
      - Various model behavior tuning, such as priority and temperature 
  
/// details | Example of a `Provider` resource
      type: code-example

    ```yaml
    apiVersion: ai.core.eda.nokia.com/v1
    kind: Provider
    metadata:
    name: openai
    namespace: eda-system
    spec:
    endpoint:
        url: https://api.openai.com/v1/responses
        apiKey: <your-openai-api-key>
    models:
        - name: gpt-4.1
        description: Balanced GPT-4.1 for chat and tool calls
        type: Responses
        usage: [Chat]
        priority: Priority
        temperature: "0"
        supportNestedResponses: true
        - name: gpt-5-mini
        description: Fast lightweight model for routing/classification
        type: Responses
        usage: [Routing]
        priority: Priority
        supportNestedResponses: true
        - name: gpt-5.1
        description: Flagship reasoning model
        type: Responses
        usage: [Reasoning]
        priority: Priority
        reasoningLevel: [Low, Medium, High]
        supportNestedResponses: true
    ```

///

### Agents

The following agents currently exist:

| Agent | Primary function | Typical invocation |
| --- | --- | --- |
| Main | Orchestrates all user-initiated flows. | Default entry point for most queries. |
| Alarms | Root-cause analysis for alarms.| "Diagnose alarm InterfaceDown-leaf-1" or "What just happened ?"|
| Query | Executes NQL → EQL translations. | “Can you show the subinterface names and their corresponding operational down reasons on `leaf-1`?” |
| Resources | Looks up network resources and their attributes. | “Is my fabric healthy ?” |
| NetOps | Runs network related operations | "Ping leaf-1 from leaf-2 | 
| Charts | Converts data queries into dashlets. | “Build a donut chart showing active alarms by severity.” |

### Model selection options

When you send a query, you can choose how the agent selects the underlying model:

- **Auto**: the tool or prompt selects whether to use a reasoning model or not.
- **Standard**: the called tool or prompt uses a non-reasoning model, if available. This model is for data retrieval or command execution.
- **Reasoning**: the called tool or prompt uses a reasoning model, if available. The reasoning model is typically used for analysis, synthesis, or explanation.

## Using Ask EDA

To access Ask EDA, click on the **Ask EDA** icon (a chat-bubble) in the top-right corner of any EDA UI screen.

-{{image(url="graphics/ask-eda-gui.png", title="Ask EDA icon", shadow=true, padding=20)}}-

When you click the **Ask EDA** icon, a chat panel opens, docked to the right of the screen.

-{{image(url="graphics/new-ask-eda-window.png", title="New Ask EDA window", shadow=true, padding=20)}}-

Table: Elements of the Ask EDA window

|\#|Name|Function|
|:---:|----|--------|
|1|Input bar|Enter queries here and press **Enter** on your keyboard.|
|2|**Start new conversation** icon|Click to start an new conversation.|
|3|Model type drop-down list|Select from **Auto**, **Reasoning**, or **Standard**.|
|4|**Full screen** toggle|When the panel is docked, the **Full screen** icon is a left arrow. Click it to make the chat overlay the main view. In this mode, the **Full screen** icon is a right arrow; click it to dock the ASK EDA window.|
|5|**X**|Click to close the chat window.|

You can set up the **Ask EDA** chat window to display in one of the following modes:

- Docked mode: The chat occupies a pane on the right, leaving most of the EDA workspace available for other tasks.
- Full screen mode: Click the **Full screen** toggle to cover the main UI view with the chat.

### Managing conversations

When you first open Ask EDA, a new conversation is automatically created. When you make a query, Nokia EDA provides a default title for your conversation and the **Open conversation history** icon becomes visible; click it to display the conversation list.

 -{{image(url="graphics/open-conversation-history-icon.png", title="Open conversations history", shadow=true, padding=20)}}-

All active and completed conversations appear in the side-bar, ordered by most recent activity. Click a conversation to load its full chat history.

 -{{image(url="graphics/conversation-list.png", title="Conversation list", shadow=true, padding=20)}}-

Conversations persist for the duration of the Nokia EDA session. If Nokia EDA is restarted, transient conversations are cleared unless the administrator has enabled permanent storage.

You can rename a conversation or delete it entirely.

 -{{image(url="graphics/conversation-options.png", title="Conversation action menu", shadow=true, padding=20)}}-

Click the action menu for a conversation and select one of the following actions:

- Click **Rename** to provide a new title. Then, click the check icon when you are finished.
- Click **Delete** to remove the conversation from the list.

### Contextual help

Currently, **Ask EDA** provides contextual help for transactions and alarms.

- For alarms, a sparkle icon appears in the **Alarm Details** view. Click it to open **Ask EDA** with the alarm ID pre-populated.
**Ask EDA** returns a root-cause analysis, suggested remediation steps, and links to related resources.

- For transactions, a sparkle icon appears in the **Transactions**>**Details** view. When you click the sparkle icon, the **Ask EDA** panel displays the summary of changes, success/failure status, and, if failed, an explanation of error messages for the selected transaction.
 -{{image(url="graphics/transaction-ask-eda-help.png", title="Transaction ASK EDA contextual help", shadow=true, padding=20)}}-

### Dashboard generation

**Ask EDA** can help create dashboards by generating individual dashlets based on prompts that you provide; it can create the following types of dashlets:

- Pie chart
- Line chart
- Table
- Counter

**Ask EDA** can generate multiple types of dashlets from your prompt. If you do not provide a dashlet type, **Ask EDA** infers the most appropriate type of dashlet based based on your requested data. If it cannot infer the dashlet type, it asks you to select one.

Once the dashlet is generated, you can drag and drop it in an opened dashboard designer view. For more information about how to build dashboards, see [Dashboards](dashboards.md).