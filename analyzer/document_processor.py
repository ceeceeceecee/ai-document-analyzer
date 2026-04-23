"""Dokumentverarbeitung — PDF und DOCX

Lädt PDF-Dateien (PyPDF2) und DOCX-Dateien (python-docx),
extrahiert den Text und bereitet ihn für die KI-Analyse vor.
"""

import re
from pathlib import Path
from typing import Optional


class DocumentProcessor:
    """Verarbeitet PDF- und DOCX-Dokumente und extrahiert Text."""

    def __init__(self, max_chunk_size: int = 8000):
        """
        Args:
            max_chunk_size: Maximale Zeichenanzahl pro Text-Chunk.
        """
        self.max_chunk_size = max_chunk_size

    def load_pdf(self, file_path: str) -> str:
        """Lädt eine PDF-Datei und gibt den extrahierten Text zurück.

        Args:
            file_path: Pfad zur PDF-Datei.

        Returns:
            Extrahierter Text als String.

        Raises:
            ImportError: Wenn PyPDF2 nicht installiert ist.
            FileNotFoundError: Wenn die Datei nicht existiert.
            ValueError: Wenn die Datei keine lesbaren Seiten enthält.
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError(
                "PyPDF2 ist erforderlich für PDF-Verarbeitung. "
                "Installieren mit: pip install PyPDF2"
            )

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

        reader = PdfReader(str(path))
        if not reader.pages:
            raise ValueError("PDF enthält keine lesbaren Seiten.")

        text_parts = []
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
            except Exception as e:
                text_parts.append(f"[Seite {i + 1}: Fehler bei der Textextraktion]")

        full_text = "\n\n".join(text_parts)
        return self._clean_text(full_text)

    def load_docx(self, file_path: str) -> str:
        """Lädt eine DOCX-Datei und gibt den extrahierten Text zurück.

        Args:
            file_path: Pfad zur DOCX-Datei.

        Returns:
            Extrahierter Text als String.

        Raises:
            ImportError: Wenn python-docx nicht installiert ist.
            FileNotFoundError: Wenn die Datei nicht existiert.
            ValueError: Wenn das Dokument keinen Text enthält.
        """
        try:
            from docx import Document
        except ImportError:
            raise ImportError(
                "python-docx ist erforderlich für DOCX-Verarbeitung. "
                "Installieren mit: pip install python-docx"
            )

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

        doc = Document(str(path))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        if not paragraphs:
            raise ValueError("DOCX-Dokument enthält keinen Text.")

        return self._clean_text("\n\n".join(paragraphs))

    def extract_text(self, file_path: str) -> str:
        """Erkennt den Dateityp automatisch und extrahiert den Text.

        Args:
            file_path: Pfad zur Datei.

        Returns:
            Extrahierter Text als String.

        Raises:
            ValueError: Wenn der Dateityp nicht unterstützt wird.
        """
        suffix = Path(file_path).suffix.lower()

        if suffix == ".pdf":
            return self.load_pdf(file_path)
        elif suffix == ".docx":
            return self.load_docx(file_path)
        else:
            raise ValueError(f"Dateityp '{suffix}' wird nicht unterstützt. Nur .pdf und .docx.")

    def chunk_text(self, text: str) -> list[str]:
        """Teilt einen langen Text in handhabbare Chunks auf.

        Trennt bevorzugt an Absatzgrenzen, fällt zurück auf Satzgrenzen.

        Args:
            text: Der zu teilende Text.

        Returns:
            Liste von Text-Chunks.
        """
        if len(text) <= self.max_chunk_size:
            return [text]

        chunks = []
        paragraphs = text.split("\n\n")
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk = current_chunk + "\n\n" + para if current_chunk else para

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _clean_text(self, text: str) -> str:
        """Bereinigt extrahierten Text: überflüssige Leerzeichen, Tabs etc."""
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
