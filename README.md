# 🔬 Multi-Agent AI Research Pipeline

A LangGraph-powered multi-agent system that autonomously searches the web, scrapes content, writes structured research reports, and critically evaluates them — all in a single pipeline run.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agent Roles](#agent-roles)
- [Example Output](#example-output)

---

## Overview

This project implements a **4-step agentic research pipeline** using LangChain, LangGraph, and Groq's LLaMA 3.3 70B model. Given a research topic, the system:

1. Searches the web for relevant, recent information
2. Scrapes the most useful source for deeper content
3. Writes a full, structured research report
4. Critically reviews the report and scores it

---

## Features

- 🤖 **Multi-Agent Architecture** — Separate specialized agents for searching and reading
- 🌐 **Real-time Web Search** — Powered by Tavily Search API
- 📄 **Deep Content Scraping** — BeautifulSoup-based URL scraper
- ✍️ **Automated Report Writing** — Structured academic-style reports via LCEL chains
- 🧠 **Self-Critique Loop** — A critic chain scores and reviews the generated report
- ⚡ **Groq Inference** — Ultra-fast LLM responses with LLaMA 3.3 70B

---

## Architecture

```
User Input (Topic)
      │
      ▼
┌─────────────┐
│ Search Agent │  ──► web_search tool (Tavily)
└─────────────┘
      │
      ▼
┌─────────────┐
│ Reader Agent │  ──► scrape_url tool (BeautifulSoup)
└─────────────┘
      │
      ▼
┌──────────────┐
│ Writer Chain  │  ──► LCEL: Prompt | LLM | StrOutputParser
└──────────────┘
      │
      ▼
┌──────────────┐
│ Critic Chain  │  ──► LCEL: Prompt | LLM | StrOutputParser
└──────────────┘
      │
      ▼
  Final State Dict
  (search_results, scraped_content, report, feedback)
```

---

## Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com/)
- A [Tavily API key](https://tavily.com/)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/multi-agent-research-pipeline.git
cd multi-agent-research-pipeline

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### `requirements.txt`

```
langchain
langchain-groq
langgraph
tavily-python
requests
beautifulsoup4
rich
python-dotenv
```

---

## Configuration

Create a `.env` file in the root of the project:

```env
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

```bash
python pipeline.py
```

You will be prompted to enter a research topic:

```
Enter a research topic : Impact of AI on healthcare
```

The pipeline will run all 4 steps and print results to the console.

---

## Project Structure

```
├── tools.py          # Tool definitions: web_search, scrape_url
├── agents.py         # Agent builders + writer/critic chains
├── pipeline.py       # Main pipeline runner (run_research_pipeline)
├── .env              # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## Agent Roles

| Component | Type | Tool / Chain | Purpose |
|---|---|---|---|
| `build_search_agent()` | LangGraph Agent | `web_search` (Tavily) | Finds top 5 relevant web results |
| `build_reader_agent()` | LangGraph Agent | `scrape_url` (BS4) | Scrapes the most relevant URL |
| `writer_chain` | LCEL Chain | Prompt + LLM + Parser | Drafts a structured research report |
| `critic_chain` | LCEL Chain | Prompt + LLM + Parser | Scores and critiques the report |

---

## Example Output

```
step 1 - search agent is working ...
step 2 - reader agent is scraping top resources ...
step 3 - Writer is drafting the report ...
step 4 - critic is reviewing the report ...

Critic Report:
Score: 8/10

Strengths:
- Well-structured with clear sections
- Includes relevant and recent sources

Areas to Improve:
- Methodology section could be more detailed
- Some claims lack direct citation

One line verdict:
A solid, informative report with minor gaps in academic rigor.
```

---

## Notes

- The pipeline state is returned as a Python `dict` with keys: `search_results`, `scraped_content`, `report`, `feedback`
- The `scrape_url` tool strips scripts, styles, nav and footer tags for clean extraction
- Writer and Critic chains use `ChatPromptTemplate` with structured output formatting

---

## License

MIT License. Feel free to use, modify and extend.
