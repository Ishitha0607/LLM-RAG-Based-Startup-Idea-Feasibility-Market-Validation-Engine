# Startup Validation Engine

An LLM + RAG powered tool that evaluates a startup idea against a knowledge
base of real, recurring market problems. It runs six specialized agents
(market, customer pain, competition, market gap, technical feasibility,
and an overall validation score) and produces a final evidence-based
report you can download as a PDF.

## How it works

1. You describe a startup idea on the **Home** page.
2. The **Dashboard** runs the multi-agent pipeline: each agent searches
   the ChromaDB vector store (built from `data/processed/startup_ideas.csv`)
   for semantically similar market problems, and reasons over what it finds.
3. The **Validation Score** agent combines the five dimension scores into
   one overall score (0–100) and a validation level.
4. The **Final Report** page asks Gemini to write a single, evidence-based
   report tying everything together, downloadable as a PDF.

The agents are intentionally conservative — they never invent competitor
names, market sizes, or customer numbers that aren't backed by retrieved
evidence.

## Project structure

```
app.py                     Streamlit entry point and page router
config/                    App-wide settings and page/icon config
data/                      Raw → processed startup-idea dataset + scripts
embeddings/                Sentence-transformer embedding generation
rag/                       ChromaDB vector store, retriever, RAG pipeline
agents/                    One file per validation agent
frontend/
  session_state.py         Initializes st.session_state defaults
  styles.py                The one place all CSS lives
  components/               Reusable UI: cards, charts, sidebar, navigation
  pages/                     One file per page, matching the sidebar
```

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Add your Gemini API key**

   Copy `.env.example` to `.env` and fill in your own key:

   ```bash
   cp .env.example .env   # on Windows: copy .env.example .env
   ```

   ```
   GOOGLE_API_KEY=your_key_here
   ```

   `.env` is git/zip-ignored on purpose — never commit or share your real key.

3. **Build the knowledge base** (only needed once, or after changing the
   raw data in `data/raw/`)

   ```bash
   python data/data_preprocessor.py     # markdown -> data/processed/startup_ideas.csv
   python data/data_validator.py        # optional: sanity-check the CSV
   python embeddings/embedding_generator.py   # generates embeddings/startup_embeddings.pkl
   python rag/vector_store.py           # loads embeddings into rag/chroma_db
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   On Windows you can also double-click `run.bat`.
   On macOS/Linux you can run `./run.sh`.

## Notes

- All validation scores are preliminary and evidence-based — they are not
  a guarantee of startup success.
- If `GOOGLE_API_KEY` is missing, the structured (non-LLM) analysis still
  works; only the final Gemini-written report is skipped.
