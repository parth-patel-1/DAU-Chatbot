# DAU-Chatbot • RAG over Dhirubhai Ambani University website

An interactive Streamlit chatbot that answers questions about the Dhirubhai Ambani University (DAU) website using Retrieval-Augmented Generation (RAG) with real-time response streaming.
Live demo: https://dau-chatbot.streamlit.app/
Github Repository: https://github.com/parth-patel-1/DAU-Chatbot
 
## Features

- Ask DAU anything — conversational Q&A grounded on DAU website pages.
- RAG pipeline — retrieves the most relevant page chunks before generating answers.
- An agentic capability can access a web page if the available information is insufficient.
- Vector database storage with Supabase
- Semantic search using OpenAI embeddings
- Streaming replies — token-by-token updates for a responsive chat feel.

## Prerequisites

- Python 3.11+
- Supabase account and database
- OpenAI API key
- Streamlit (for web interface)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/parth-patel-1/DAU-Chatbot.git
cd DAU-Chatbot
```

2. Install dependencies (recommended to use a Python virtual environment):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
   - Edit `.streamlit/secrets.toml` file with your API keys:
   ```secrets.toml
   SUPABASE_URL = your_supabase_url
   SUPABASE_SERVICE_KEY = your_supabase_service_key
   OPENAI_API_KEY= your_openai_api_key
   LOGFIRE_TOKEN= your logfire token for logging
   ```

## Usage

### Database Setup

Execute the SQL commands in `site_pages.sql` to:
1. Create the necessary tables
2. Enable vector similarity search
3. Set up Row Level Security policies

In Supabase, do this by going to the "SQL Editor" tab and pasting in the SQL into the editor there. Then click "Run".

### Crawl Documentation

To crawl and store documentation in the vector database:

```bash
python crawl_dau.py
```

This will:
1. Fetch URLs from the documentation sitemap
2. Crawl each page and split into chunks
3. Generate embeddings and store in Supabase

### Streamlit Web Interface

For an interactive web interface to query the documentation:

```bash
streamlit run slit.py
```

## Configuration

### Database Schema

The Supabase database uses the following schema:
```sql
CREATE TABLE site_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url TEXT,
    chunk_number INTEGER,
    title TEXT,
    summary TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);
```

### Chunking Configuration

You can configure chunking parameters in `crawl_dau.py`:
```python
chunk_size = 10000  # Characters per chunk
```

The chunker intelligently preserves:
- Code blocks
- Paragraph boundaries
- Sentence boundaries

## Project Structure

- `crawl_dau.py`: Documentation crawler and processor
- `pydantic_ai_expert.py`: RAG agent implementation
- `slit.py`: Web interface
- `site_pages.sql`: Database setup commands
- `requirements.txt`: Project dependencies

## Live Demo

If you're interested in live demo of this chatbot , [click here](https://dau-chatbot.streamlit.app/)


## Error Handling

The system includes robust error handling for:
- Network failures during crawling
- Database connection issues
- Embedding generation errors
- Invalid URLs or content

