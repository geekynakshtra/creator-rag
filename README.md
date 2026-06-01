# Creator RAG Analyzer

Creator RAG Analyzer is a full-stack RAG chatbot that compares two social media videos — one YouTube video and one Instagram Reel/short-form video — using transcript evidence and video-level metadata.

The goal of this project is not just to chat with transcripts. The system combines transcript chunks, creator metadata, engagement metrics, platform data, and retrieval-grounded LLM reasoning so a creator can ask useful questions like:

* Why did Video A get more engagement than Video B?
* What is the engagement rate of each video?
* Compare the hooks in the first 5 seconds.
* Who is the creator of Video B and what is their follower count?
* Suggest improvements for one video based on what worked in the other.

The app was built as a low-cost, dynamic RAG pipeline using FastAPI, Next.js, LangChain, open-source embeddings, ChromaDB, and Groq-hosted Llama.

---

## Demo Features

* Accepts two video URLs dynamically.
* Supports YouTube and Instagram-style short-form videos.
* Extracts video metadata:

  * title
  * creator
  * views
  * likes
  * comments
  * follower count, when exposed by the platform extractor
  * hashtags
  * upload date
  * duration
* Computes engagement rate:

```text
engagement_rate = (likes + comments) / views × 100
```

* Extracts transcripts using:

  * `youtube-transcript-api` for YouTube
  * `yt-dlp`
  * Whisper fallback for audio transcription
* Chunks transcript text.
* Embeds chunks using open-source embeddings.
* Stores chunks in ChromaDB.
* Tags every chunk with:

  * `video_id`
  * `comparison_label` such as Video A or Video B
  * title
  * creator
  * platform
  * engagement metrics
  * chunk index
* Provides a streaming RAG chat interface.
* Cites sources using Video A/B and chunk number.
* Maintains lightweight memory across turns during the active backend session.

---

## Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python
* Server-Sent Events for streaming responses

### RAG / AI

* LangChain
* Groq Llama model for chat generation
* Open-source BGE / sentence-transformer embeddings
* ChromaDB vector store

### Transcript and Metadata

* `yt-dlp`
* `youtube-transcript-api`
* Whisper fallback

---

## Architecture

```text
User enters Video A URL + Video B URL
        ↓
Next.js frontend
        ↓
FastAPI ingestion endpoint
        ↓
Platform detection
        ↓
yt-dlp metadata extraction
        ↓
YouTube transcript API / Whisper fallback
        ↓
Engagement rate calculation
        ↓
Transcript chunking
        ↓
Embedding generation
        ↓
ChromaDB vector storage
        ↓
FastAPI streaming chat endpoint
        ↓
LangChain prompt orchestration
        ↓
Groq Llama response stream
        ↓
Frontend renders answer + sources
```

---

## How the RAG Pipeline Works

Each video is processed dynamically after the user submits the URLs.

For every video, the backend extracts metadata and transcript text. The transcript is then chunked and embedded. Each chunk is stored in ChromaDB with metadata, including whether it belongs to Video A or Video B.

When a user asks a question, the system classifies the query mode:

* hook analysis
* engagement analysis
* creator analysis
* improvement analysis
* general analysis

The retriever fetches relevant chunks and metadata from ChromaDB. The response generator builds a grounded prompt using:

* retrieved transcript chunks
* video metadata
* recent conversation memory
* query-specific instructions

The LLM then streams a response back to the frontend.

---

## Source Citation

The assistant cites sources using the video label and chunk index.

Example:

```text
Video A uses "Learn Python for FREE in 2025" as a concise hook. (Video A, Chunk #0)
Video B mentions specific projects like a calculator and unit converter. (Video B, Chunk #0)
```

The frontend also displays source cards showing:

* Video A or Video B
* platform
* chunk number
* title
* creator
* retrieved transcript text

---

## Memory

The app maintains lightweight in-memory chat memory for the current backend session.

This allows follow-up questions such as:

```text
Which video performed better?
Why?
```

For production, I would move memory to Redis or Postgres with session IDs so it persists across users, browser refreshes, and server restarts.

---

## Why This Stack?

### Why ChromaDB?

I used ChromaDB because this is an MVP/screening project where fast local iteration and low cost matter. ChromaDB runs locally, is simple to integrate, and avoids managed vector database costs during development.

For production scale, I would consider:

* pgvector for simple Postgres-native vector search
* Qdrant for a dedicated open-source vector database
* Pinecone or Weaviate if managed scaling and operations are preferred

### Why open-source embeddings?

Embedding every transcript chunk through a paid API can become expensive at scale. Open-source embeddings keep ingestion cost low and make the system easier to run locally.

This matters because ingestion happens for every video pair, while LLM reasoning only happens when the user asks questions.

### Why Groq?

I initially tested local LLM inference, but small local models were weaker at following RAG instructions and avoiding hallucinations. Groq provided much better response quality and very fast streaming while staying low-cost for the demo.

The final architecture keeps expensive reasoning limited to chat-time, while transcript processing and embedding remain low-cost.

---

## Cost and Scalability Reasoning

The current implementation is designed as a low-cost MVP. For a workload like 1000 creators per day, I would scale it like this:

### 1. Cache video metadata and transcripts

Many creators may analyze the same popular videos. I would cache extracted metadata and transcripts by `video_id` so the system does not repeatedly call extractors or transcribe the same audio.

### 2. Use asynchronous ingestion jobs

Video extraction and Whisper transcription can be slow. At scale, ingestion should run through a background queue such as:

* Celery
* RQ
* Dramatiq
* cloud-native queue workers

The frontend would submit a job and poll or subscribe for completion.

### 3. Store structured metadata in Postgres

Video metadata such as views, likes, comments, upload date, duration, follower count, and engagement rate should live in Postgres.

The vector DB should store transcript chunks and embeddings, not act as the main analytics database.

### 4. Move vector storage depending on scale

For the MVP, ChromaDB is enough.

For 1000 creators/day:

* pgvector is a good low-cost production option if the team already uses Postgres.
* Qdrant is a strong option if vector search becomes a core workload.
* Pinecone is useful if managed infrastructure is preferred.

### 5. Use official or paid enrichment APIs where needed

`yt-dlp` is useful for prototyping, but follower counts and Instagram metadata are not always reliable.

For production:

* YouTube follower/subscriber count should come from YouTube Data API.
* Instagram follower count should come from Instagram Graph API, Apify, or a reliable third-party provider.

### 6. Keep LLM usage selective

The system should not call the LLM during ingestion. It should only call the LLM when a creator asks a question.

This keeps cost lower because transcript extraction, embedding, and metadata calculation are deterministic and do not require generative AI.

---

## Known Limitations

### Follower count availability

Follower count is included in the metadata schema and works when the platform extractor exposes it.

However, public extractors like `yt-dlp` do not reliably expose follower or subscriber count for every platform or video. When unavailable, the app returns:

```text
Follower count data unavailable from platform metadata.
```

This is intentional. The system avoids hallucinating fake follower numbers.

### Instagram reliability

Instagram metadata and transcript extraction are less reliable than YouTube. Whisper fallback helps recover transcript text from audio, but metadata such as follower count may still require official or paid APIs in production.

### Local memory

Conversation memory is currently in-memory for the active backend session. Production memory should use Redis or Postgres with user/session IDs.

### Local vector DB

ChromaDB is good for local MVP development. For multi-user production workloads, I would move to pgvector, Qdrant, Pinecone, or Weaviate.

---

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## Environment Variables

Example file:

```text
backend/.env.example
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Example Questions

After analyzing two videos, try:

```text
Compare the hooks in the first 5 seconds.
```

```text
What is the engagement rate of each video?
```

```text
Why did Video B get more engagement than Video A?
```

```text
Who is the creator of Video B and what is their follower count?
```

```text
Suggest improvements for Video A based on what worked in Video B.
```

---

## Engineering Tradeoffs

This project was built with a practical engineering mindset:

* I chose ChromaDB for fast local development and zero vector DB cost.
* I used open-source embeddings to avoid embedding API cost.
* I used Groq-hosted Llama for better quality than small local models while keeping inference low-cost.
* I kept ingestion deterministic and avoided LLM calls during ingestion.
* I added safe fallbacks for missing metadata instead of hallucinating.
* I used streaming responses because the user experience is much better for RAG chat.
* I tagged chunks with Video A/B metadata because comparison tasks fail if video identity is inferred from platform alone.

The main production upgrade would be replacing local state with managed/persistent services:

```text
ChromaDB → pgvector or Qdrant
in-memory memory → Redis/Postgres
yt-dlp-only metadata → official APIs / Apify enrichment
local Whisper → queued transcription workers
```

---

## Submission Notes

This project demonstrates:

* full-stack product implementation
* RAG architecture
* vector retrieval
* streaming responses
* metadata-aware reasoning
* source-cited answers
* engineering tradeoff thinking
* cost-conscious scaling design

The goal was to build something that works dynamically end-to-end, not a hard-coded demo.


# Author
Nakshatra Tyagi
