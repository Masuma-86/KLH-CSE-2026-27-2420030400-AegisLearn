# Aegis Learn

## Generative AI Framework for Personalized Learning

Aegis Learn is an AI-powered personalized learning framework that
transforms static academic textbooks into interactive, personalized
study support.

It uses **Retrieval-Augmented Generation (RAG)**, **vector similarity
search**, and **Bloom's Taxonomy** to generate grounded study guides,
quizzes, and learning recommendations based on a student's needs.

## Key Features

-   📚 **Textbook-Grounded Learning** -- Retrieves relevant textbook
    content before generating answers.
-   🧠 **Bloom's Taxonomy** -- Supports Remembering, Understanding,
    Applying, Analyzing, Evaluating, and Creating.
-   ✨ **Personalized Study Guides** -- Generates explanations and notes
    based on the selected cognitive level.
-   📝 **Interactive Quizzes** -- Creates quizzes from the selected
    learning corpus.
-   📊 **Performance Tracking** -- Measures student performance across
    Bloom's cognitive levels.
-   🎯 **Remedial Roadmaps** -- Identifies weak areas and suggests
    targeted re-study.
-   👨‍🏫 **Educator Dashboard** -- Supports custom syllabus/textbook
    corpus uploads and analysis.
-   ⚙️ **Admin Console** -- Provides usage, API, and corpus monitoring.

## Technology Stack

### AI & Machine Learning

-   Gemini 1.5 Flash
-   Retrieval-Augmented Generation (RAG)
-   Cosine Similarity Search
-   Bloom's Taxonomy Prompt Engineering

### Web Development

-   React.js
-   TypeScript
-   Vite
-   Tailwind CSS
-   Vanilla CSS
-   Lucide React

### Tools

-   VS Code
-   Git
-   GitHub

## System Workflow

``` text
Student / Educator Login
        ↓
Select or Upload Textbook Corpus
        ↓
Search Topic / Start Quiz
        ↓
Text Chunking & Indexing
        ↓
Vector Similarity Search
        ↓
Top-K Context Retrieval
        ↓
Bloom's Taxonomy Routing
        ↓
Prompt Synthesis
        ↓
Gemini API
        ↓
Personalized Notes / Quiz
        ↓
Student Evaluation
        ↓
Mastery Analysis & Remedial Roadmap
```

## Project Modules

### Student Portal

-   Topic search
-   Personalized study guides
-   Interactive quizzes
-   Performance tracking
-   Remedial learning roadmap

### Educator Portal

-   Upload textbook or syllabus data
-   View corpus statistics
-   Inspect indexed chunks
-   Test similarity matching

### Administrator Console

-   Usage analytics
-   Gemini API usage monitoring
-   Corpus and local index management

## Datasets

The framework uses reference academic content from:

-   OpenStax textbook corpus
-   NCERT textbook corpus
-   Khan Academy Algebra corpus

## Project Structure

``` text
Aegis Learn/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── data/
│   ├── utils/
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── package.json
├── vite.config.ts
└── README.md
```

## Getting Started

### 1. Clone the Repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Aegis-Learn
```

### 2. Install Dependencies

``` bash
npm install
```

### 3. Start the Development Server

``` bash
npm run dev
```

Open the local URL shown in the terminal, usually:

``` text
http://localhost:5173/
```

### 4. Configure Gemini API

Use the API key setup option in the application and provide your Gemini
API key to enable live AI-generated notes and quizzes.

## Evaluation Metrics

Aegis Learn evaluates the system using:

-   **Faithfulness** -- Checks whether generated content is supported by
    retrieved textbook context.
-   **Answer Relevance** -- Measures how well generated content
    addresses the student's query.
-   **Retrieval Precision & Recall** -- Evaluates the quality of
    retrieved textbook content.
-   **Student Mastery Score** -- Tracks performance across Bloom's
    cognitive levels.

## Team Members

  ID           Name
  ------------ ---------------------
  2420030400   Masuma Fathema
  2420030568   Avinash Yarukala
  2420030521   Madhav Ghattamaneni
  2420030467   K V S Jaswanth

## Supervisor

**Dr. K. Swanthana**

## Project Status

**Phase 4 -- Application Interface Development and RAG Model
Integration**

### Completed

-   Project architecture and objectives
-   Reference dataset selection
-   Vector similarity simulator
-   Text chunking
-   Bloom's Taxonomy prompt templates
-   Gemini API integration
-   Student login and core navigation

### In Progress

-   RAG analyzer
-   Bloom-based study notes
-   Interactive quiz system
-   Performance and mastery dashboard

### Upcoming

-   Educator corpus uploader
-   Validation and testing
-   Final documentation
-   Production deployment

## Project Outcome

Aegis Learn aims to make learning more **personalized, grounded,
adaptive, and measurable** by combining academic content with Generative
AI and RAG.
