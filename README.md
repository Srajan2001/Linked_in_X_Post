# Multi-Agent Generative AI Content Pipeline

## Project Overview
This repository contains a multi-agent orchestration system designed to automate the lifecycle of professional content creation. The system integrates live web research, stylistic memory retrieval, agentic self-reflection, and multi-modal asset generation into a single Streamlit-based dashboard.

## System Architecture
The application utilizes a modular agent-based architecture to separate concerns and optimize for specific tasks:

1. Trend Agent: Handles real-time search queries and news extraction.
2. Profile Agent: Processes user identity and strategic content parameters.
3. Memory Agent: Manages a local Vector Database (ChromaDB) for stylistic RAG.
4. Writer Agent: Executes core drafting with dynamic model switching (GPT-4o vs GPT-4o-mini).
5. Critic Agent: Performs automated quality assurance and provides feedback loops.
6. Router Agent: Converts approved drafts into platform-specific formats (JSON).
7. Image Agent: Generates DALL-E style prompts and renders custom post graphics.

## Technical Stack
- Language: Python 3.10 or higher
- Orchestration: OpenAI API
- Database: ChromaDB (Vector Store)
- UI Framework: Streamlit
- Search Interface: DuckDuckGo Search API
- Visualization: Pillow, Requests

## Project Structure
- agents/: Specialized Python scripts for each AI agent.
- memory/: Local directory for ChromaDB persistence.
- outputs/: Directory for finalized content artifacts.
- app.py: Central Streamlit application and state management logic.
- requirements.txt: Python dependency manifest.
- .env: Environment variables (not included in repository).

## Installation

1. Clone the repository to your local machine:
   git clone https://github.com/Srajan2001/Linked_in_X_Post.git

2. Navigate into the project directory:
   cd Linked_in_X_Post

3. Create a isolated virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   # On Windows (PowerShell)
   .\venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate

5. Install all required Python packages:
   pip install -r requirements.txt

## Configuration

1. Create a file named .env in the root directory.
2. Add your OpenAI API credentials to the file:
   OPENAI_API_KEY=your_actual_api_key_here

## How to Run the Application

To start the local web server and launch the dashboard, execute the following command:

``streamlit run app.py``

Once the command is executed, a local URL (typically http://localhost:8501) will be displayed in the terminal and will automatically open in your default web browser.

## Operational Workflow

1. User Configuration: Input your name, role, and core skills in the sidebar.
2. Topic Definition: Enter the subject for your content and select the desired tone and audience.
3. Research Phase (Optional): 
   - Toggle "Fetch Live News" on to perform web scraping.
   - Curate the context by selecting up to 5 articles from the presented list.
4. Content Generation:
   - Click "Generate Post". 
   - If Research was toggled off, the system routes the task to GPT-4o with a 700-token limit.
   - If Research was toggled on, the system uses GPT-4o-mini for cost-effective synthesis.
5. Review and Edit: 
   - Modify the draft manually in the text area.
   - Use AI Quick Action buttons for immediate stylistic adjustments (Shorter, Technical, or CTA).
6. Final Distribution:
   - Click "Approve & Route".
   - The system saves the post to local memory for future style cloning.
   - Use the provided Web Intent links to copy text directly to LinkedIn and X (Twitter).
   - Download the AI-generated graphic for visual attachment.

## Security and Best Practices
The .env file and the memory/ directory are excluded from version control via .gitignore. Ensure that API keys are never hardcoded into the agent files.
