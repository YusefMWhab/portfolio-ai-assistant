# Project: AI Portfolio Assistant - Interactive Voice RAG Agent

## Overview
The AI Portfolio Assistant is an advanced, production-ready interactive agent designed to represent my professional profile, education, technical skills, and projects. Deployed live on AWS, the platform acts as an autonomous representative that users can chat with via text or natural voice. By integrating a full-stack Retrieval-Augmented Generation (RAG) pipeline, streaming APIs, and Voice-to-Voice capabilities, the assistant delivers accurate, context-aware answers about my career directly from verified documents.

---

## Problem
Traditional resumes, CVs, and personal portfolios are static, passive, and often tedious for recruiters and hiring managers to navigate. They require manual searching to find specific project details or technical competencies. On the other hand, generic AI chatbots lack specific context and are prone to "hallucinations"—making up facts about a candidate's experience.

The AI Portfolio Assistant solves this by providing a highly engaging, interactive, and reliable interface. It ensures 100% factual accuracy by grounding the AI's knowledge base in verified professional documents, allowing users to query my background naturally and receive instant, structured responses.

---

## AI & Voice Pipeline (RAG System)
The core of the assistant is an intelligent RAG and Audio processing pipeline designed for low-latency and high accuracy:

1. Document Ingestion & Chunking: Portfolio data (resumes, project details, FAQs) is parsed, split into optimized semantic chunks, and embedded using Gemini's embedding models (`gemini-embedding-2`).
2. Vector Database (Qdrant): Embeddings are stored in a Qdrant vector database. During a query, the system performs a semantic similarity search to retrieve the most relevant context chunks.
3. Generative LLM (Gemini API): The retrieved context is injected into a specialized system prompt, guiding `gemini-2.5-flash-lite` to generate factually grounded, tailored responses.
4. Real-time Streaming: To ensure a responsive user experience, the system utilizes FastAPI's Streaming Responses to stream the generated text to the frontend word-by-word.
5. Voice-to-Voice (STT & TTS): Integrated Speech-to-Text (STT) and Text-to-Speech (TTS) models allow users to speak directly to the assistant and receive natural spoken answers.

---

## Technical Architecture & System Design
The project is built using a modern, containerized, and secure microservices architecture:

* Backend Framework: FastAPI (chosen for its native asynchronous support, exceptional speed, and seamless streaming capabilities).
* Vector Database: Qdrant (running as a dedicated container, providing high-performance semantic vector search).
* Frontend: Responsive HTML, CSS, and vanilla JavaScript (handling real-time markdown rendering, audio recording/playback, and asynchronous API communication).
* Containerization: Docker & Docker Compose (orchestrating the `web` and `qdrant` services, ensuring identical environments in local development and cloud production).
* Reverse Proxy & SSL: Nginx (serving as a reverse proxy, routing traffic, and securing all communications with SSL/TLS HTTPS certificates via Certbot).
* Cloud Infrastructure: Hosted on an AWS EC2 instance, ensuring high availability and robust cloud performance.

---

## My Key Contributions
As the Sole Developer and Cloud Engineer, I built the entire system end-to-end:
* RAG Pipeline Engineering: Developed the document parser, custom chunking logic, and integrated Qdrant for semantic search.
* Asynchronous API Design: Built the FastAPI backend, implementing streaming endpoints for real-time text delivery.
* Voice Integration: Implemented the audio processing logic, enabling seamless voice input recording and dynamic TTS playback.
* DevOps & Dockerization: Created the Dockerfiles and Docker Compose configurations, linking the application services with secure networking.
* AWS & Nginx Deployment: Configured the AWS EC2 environment, set up Nginx to handle reverse proxy routing, and secured the custom domain `narriq.cloud/portfolio` using Let's Encrypt SSL.

---

## Key Impact & Metrics
* Zero Hallucinations: Secured 100% accurate responses by strictly grounding the LLM within the retrieved Qdrant context.
* Low-Latency Performance: Optimized streaming and lightweight voice processing to deliver near-instantaneous feedback.
* Interactive Experience: Transformed a traditional static CV into an engaging, voice-enabled, modern cloud application.