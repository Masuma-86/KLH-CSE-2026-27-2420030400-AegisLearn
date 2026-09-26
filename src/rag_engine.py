import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.models.schemas import RagChunk


class RagEngine:
    """
    Pedagogical Retrieval-Augmented Generation (RAG) Engine.
    Handles semantic chunking, vector indexing, and cosine similarity retrieval
    grounded in academic textbook corpora.
    """

    def __init__(self, stop_words: str = "english"):
        self.chunks: List[RagChunk] = []
        self.chunk_ids: List[str] = []
        self.vectorizer = TfidfVectorizer(
            stop_words=stop_words,
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True
        )
        self.tfidf_matrix = None
        self._is_fitted = False

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        title: str = "Textbook Passage",
        chapter_id: str = "custom",
        source_citation: str = "Source Document"
    ) -> List[RagChunk]:
        """
        Splits arbitrary long text into overlapping semantic windows.
        Preserves complete sentences whenever possible.
        """
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        chunks: List[RagChunk] = []
        current_sentences: List[str] = []
        current_len = 0
        chunk_counter = 1

        for sentence in sentences:
            sentence_clean = sentence.strip()
            if not sentence_clean:
                continue
            words_count = len(sentence_clean.split())
            if current_len + words_count > chunk_size and current_sentences:
                chunk_body = " ".join(current_sentences)
                chunk_id = f"{chapter_id}-chunk-{chunk_counter}"
                chunks.append(
                    RagChunk(
                        id=chunk_id,
                        chapter_id=chapter_id,
                        title=f"{title} (Part {chunk_counter})",
                        content=chunk_body,
                        source_citation=source_citation,
                        metadata={"word_count": len(chunk_body.split())}
                    )
                )
                chunk_counter += 1

                # Overlap: keep the last few sentences
                overlap_words = 0
                kept_sentences = []
                for s in reversed(current_sentences):
                    s_words = len(s.split())
                    if overlap_words + s_words <= chunk_overlap:
                        kept_sentences.insert(0, s)
                        overlap_words += s_words
                    else:
                        break
                current_sentences = kept_sentences
                current_len = sum(len(s.split()) for s in current_sentences)

            current_sentences.append(sentence_clean)
            current_len += words_count

        if current_sentences:
            chunk_body = " ".join(current_sentences)
            chunk_id = f"{chapter_id}-chunk-{chunk_counter}"
            chunks.append(
                RagChunk(
                    id=chunk_id,
                    chapter_id=chapter_id,
                    title=f"{title} (Part {chunk_counter})",
                    content=chunk_body,
                    source_citation=source_citation,
                    metadata={"word_count": len(chunk_body.split())}
                )
            )

        return chunks

    def add_chunks(self, new_chunks: List[RagChunk]) -> int:
        """
        Adds pre-chunked items to the vector store and re-indexes.
        """
        existing_ids = set(self.chunk_ids)
        added_count = 0
        for chunk in new_chunks:
            if chunk.id not in existing_ids:
                self.chunks.append(chunk)
                self.chunk_ids.append(chunk.id)
                existing_ids.add(chunk.id)
                added_count += 1

        if self.chunks:
            self._fit_index()
        return added_count

    def load_from_json(self, json_path: Path) -> int:
        """
        Loads textbook chapters and chunks from a JSON dataset.
        """
        if not json_path.exists():
            raise FileNotFoundError(f"Dataset not found at {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        new_chunks: List[RagChunk] = []
        for chapter in data:
            chap_id = chapter.get("id", "generic-chapter")
            chap_source = chapter.get("source", "Standard Textbook")
            for c in chapter.get("chunks", []):
                new_chunks.append(
                    RagChunk(
                        id=c.get("id", f"{chap_id}-chunk"),
                        chapter_id=chap_id,
                        title=c.get("title", chapter.get("title", "Passage")),
                        content=c.get("content", ""),
                        source_citation=f"{chap_source} - {c.get('title', '')}",
                        metadata={"keywords": c.get("keywords", [])}
                    )
                )

        return self.add_chunks(new_chunks)

    def _fit_index(self):
        """Builds TF-IDF vector matrix over all indexed text chunks."""
        corpus = [f"{c.title} {c.content} {' '.join(c.metadata.get('keywords', []))}" for c in self.chunks]
        if corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
            self._is_fitted = True

    def retrieve(
        self,
        query: str,
        chapter_id: Optional[str] = None,
        top_k: int = 3,
        min_similarity: float = 0.05
    ) -> List[RagChunk]:
        """
        Performs semantic vector search using cosine similarity.
        Returns Top-K relevant chunks with similarity score.
        """
        if not self._is_fitted or not self.chunks:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # Filter by chapter_id if provided
        indexed_scores = []
        for idx, score in enumerate(similarities):
            chunk = self.chunks[idx]
            if chapter_id and chunk.chapter_id != chapter_id:
                continue
            if score >= min_similarity:
                indexed_scores.append((idx, float(score)))

        # Sort descending by similarity
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = indexed_scores[:top_k]

        results: List[RagChunk] = []
        for idx, score in top_matches:
            original = self.chunks[idx]
            # Create a clone with similarity score populated
            chunk_copy = RagChunk(
                id=original.id,
                chapter_id=original.chapter_id,
                title=original.title,
                content=original.content,
                source_citation=original.source_citation,
                similarity_score=round(score, 4),
                metadata=original.metadata
            )
            results.append(chunk_copy)

        return results

    def build_grounded_context(self, chunks: List[RagChunk]) -> str:
        """
        Formats retrieved textbook chunks into a clean context block
        ready for the LLM prompt.
        """
        if not chunks:
            return "No verified textbook context retrieved."

        lines = ["--- VERIFIED TEXTBOOK CONTEXT (ACADEMIC GROUND TRUTH) ---"]
        for i, c in enumerate(chunks, 1):
            score_str = f" [Similarity: {c.similarity_score}]" if c.similarity_score is not None else ""
            lines.append(f"[{i}] SOURCE: {c.source_citation}{score_str}")
            lines.append(f"TITLE: {c.title}")
            lines.append(f"CONTENT: {c.content}")
            lines.append("")
        lines.append("---------------------------------------------------------")
        return "\n".join(lines)
