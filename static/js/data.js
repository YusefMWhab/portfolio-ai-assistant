/* =========================================================================
   EDIT THIS FILE ONLY — it's where your info and projects live.
   You should not need to touch index.html, style.css or script.js at all.
   ========================================================================= */

const PROFILE = {
  name: "Youssef Mohamed",
  role: "AI & Python Backend Engineer",
  location: "New Cairo, Egypt",
  focus: "AI-Powered Systems & Scalable Automation",
  experience: "2+ years",
  about:
    "I am an Electronics and Communication Engineering graduate from Cairo University who found his true passion in bridging the gap between robust software architecture and Artificial Intelligence., " +
    "My expertise lies in building production-ready backend systems, scaling smart automation tools, and deploying Large Language Model (LLM) pipelines that turn unstructured business problems into highly efficient workflows.\n\n" +
    "Currently, I architect AI-driven internal solutions and data validation engines at IPSOS Egypt. " +
    "I thrive on designing secure, asynchronous multi-tenant architectures, optimizing API costs, and writing clean Python code. " +
    "Whether it's processing thousands of data points daily or building robust SaaS applications, I focus on delivering scalable, high-impact software.",
  skills: ["Python", "JavaScript", "SQL", "C/C++",
          "Django", "FastAPI", "REST APIs", "Celery", "Redis", "Nginx",
          "PostgreSQL", "Supabase",
          "OpenAI API", "Gemini API", "Prompt Engineering", "Embeddings",
          "Semantic Search", "Semantic Clustering", "NLP Pipelines",
          "Docker", "AWS", "Git", "Linux",
          "OOP", "Async Processing", "RBAC"],
  // social / contact links shown in the "Get in touch" section
  links: [
    { label: "Email",    url: "mailto:youssefmwhab@gmail.com" },
    { label: "GitHub",   url: "https://github.com/YusefMWhab" },
    { label: "LinkedIn", url: "https://linkedin.com/in/youssef-mohamed-5b71a422a" },
    { label: "Resume",   url: "/static/resume.pdf" }
  ]
};

/* -------------------------------------------------------------------------
   PROJECTS
   - description : short 1-line summary shown on the card
   - tech         : array of strings, used for the filter chips too
   - readme       : full write-up. Supports basic markdown:
                    # / ## headings, **bold**, *italic*, `code`,
                    ```code blocks```, - bullet lists, [text](url) links
   - images       : array of paths, put files in /static/images/
   - videos       : array of paths (mp4) or YouTube URLs, put files in /static/videos/
   - links        : { label, url } buttons shown at the top of the case study
                    (e.g. Live demo, GitHub repo)
   ------------------------------------------------------------------------- */

const PROJECTS = [
  {
    id: "NarrIQ",
    title: "NarrIQ | AI-Powered Market Research Automation Platform",
    description: "An AI-powered SaaS platform that automates open-ended coding, sentiment analysis, and qualitative text processing for market research workflows.",
    tech: ["Python", "Django", "PostgreSQL", "Celery", "Redis", "Nginx", "Docker", "AWS", "LLM APIs", "Embeddings", "Semantic Clustering", "JavaScript", "HTML", "CSS"],
    links: [
      { label: "Platform", url: "https://narriq.cloud" },
    ],
    images: [
      "/static/images/NarrIQ-1.png",
      "/static/images/NarrIQ-2.png",
      "/static/images/NarrIQ-3.png",
      "/static/images/NarrIQ-4.png",
      "/static/images/NarrIQ-5.png",
      "/static/images/NarrIQ-6.png",
      "/static/images/NarrIQ-7.png",
      "/static/images/NarrIQ-8.png",  
    ],
    videos: [
      "/static/videos/NarrIQ-demo-1.mp4",
      "/static/videos/NarrIQ-demo-2.mp4"
    ],
    readme: `
# NarrIQ

An AI-powered SaaS platform that automates open-ended coding, sentiment
analysis, and qualitative text processing for market research workflows.
The AI builds an initial codebook directly from the raw data using LLM
pipelines and semantic clustering, while coders keep full control — adding,
editing, deleting, or manually assigning codes on top of it.

## Highlights
- End-to-end LLM pipeline using LLM APIs, semantic embeddings, and
  clustering to automate qualitative text analysis
- 85%+ accuracy on AI-generated coding, 90%+ on sentiment classification
- Intelligent response-grouping algorithm that cuts LLM API calls and
  inference cost while keeping classification quality high
- Human-in-the-loop editing: add, edit, or delete codes in the AI-built
  codebook, or manually assign codes to individual rows
- Scalable asynchronous processing with Celery and Redis for concurrent
  analysis jobs across multiple users and projects
- Secure multi-tenant backend with RBAC, authentication, and subscription
  management for production deployment
- Containerized with Docker and deployed on AWS
- In production across market research projects in the MENA region,
  cutting coding time from days to hours

## Stack
Python and Django backend with PostgreSQL, Celery and Redis for
asynchronous job processing, LLM API for LLM-based analysis, containerized
with Docker and deployed on AWS.
`
  },
  {
    id: "DataWhisperer",
    title: "DataWhisperer | Internal Validation Management Platform",
    description: "An internal operations platform that centralized validation management, interviewer analytics, workflow automation, and operational reporting for market research teams.",
    tech: ["Python", "Django", "PostgreSQL", "Celery", "Redis", "Nginx", "JavaScript", "HTML", "CSS"],
    links: [
      //{ label: "Live demo", url: "https://example.com" },
      { label: "GitHub", url: "https://github.com/YusefMWhab/DataWhisperer-Web-App" }
    ],
    images: [
      "/static/images/DataWhisperer-1.png",
      "/static/images/DataWhisperer-2.png",
      "/static/images/DataWhisperer-3.png",
      "/static/images/DataWhisperer-4.png",
      "/static/images/DataWhisperer-5.png",
      "/static/images/DataWhisperer-6.png",
      "/static/images/DataWhisperer-7.png",
      "/static/images/DataWhisperer-8.png",
      "/static/images/DataWhisperer-9.png",
      "/static/images/DataWhisperer-10.png",
    ],
    videos: [
      // "/static/videos/DataWhisperer-demo.mp4"
    ],
    readme: `
# DataWhisperer

A validation management system that logs validation rounds and generates
performance dashboards — per project and per interviewer, across every
project running through the system. Paired with Time-Check, an automation
tool that validates interview time data.

## Highlights
- Logs and tracks validation rounds across multiple projects
- Performance dashboards broken down by project and by interviewer
- Validation Hub for running quality checks and reviewing results
- Time-Check tool for automated validation on interview time-row data,
  including:
  - LOI (length of interview) analysis
  - Out-of-hours interview detection
  - Daily reports on interview activity
  - Conflicting/overlapping interview time detection
  - Downloadable Excel report listing all flagged interviews
- Bulk dataset upload and processing pipeline

## Stack
Django backend with a Python-based processing pipeline, PostgreSQL database,
Celery and Redis for background/async task processing, served through
Nginx. Frontend built with HTML/CSS/JavaScript.

## What I'd do differently
Next time I'd add real-time collaboration and export options for the
performance dashboards from the start, instead of bolting them on after the
core validation pipeline was already built.

`
  },
];
