"""KI-Analyse — Claude, Gemini, Ollama

Bietet Zusammenfassung, Klassifizierung und Schlüsseldaten-Extraktion
für Dokumenttexte. Unterstützt drei KI-Anbieter mit automatischer
Retry-Logik.
"""

import json
import os
import time
from pathlib import Path
from typing import Optional


class AIAnalyzer:
    """KI-gestützte Dokumentanalyse mit mehreren Anbietern."""

    MAX_RETRIES = 3
    RETRY_DELAY = 2  # Sekunden

    def __init__(self, provider: str = "claude", ollama_host: Optional[str] = None, model: Optional[str] = None):
        """
        Args:
            provider: 'claude', 'gemini' oder 'ollama'
            ollama_host: URL des Ollama-Servers (nur für provider='ollama')
            model: Modellname (nur für Ollama)
        """
        self.provider = provider
        self.ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or "llama3"
        self._client = None
        self.prompt_dir = Path(__file__).parent.parent / "prompts"

    def _load_prompt(self, name: str) -> str:
        """Lädt einen System-Prompt aus der prompts/ Textdatei."""
        path = self.prompt_dir / f"{name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Prompt-Datei nicht gefunden: {path}")
        return path.read_text(encoding="utf-8").strip()

    def _get_client(self):
        """Initialisiert und gibt den KI-Client zurück."""
        if self._client is not None:
            return self._client

        if self.provider == "claude":
            import anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY nicht gesetzt. Bitte in .env eintragen.")
            self._client = anthropic.Anthropic(api_key=api_key)

        elif self.provider == "gemini":
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY nicht gesetzt. Bitte in .env eintragen.")
            genai.configure(api_key=api_key)
            self._client = genai.GenerativeModel("gemini-pro")

        elif self.provider == "ollama":
            import requests
            self._client = requests.Session()
            self._client.headers.update({"Content-Type": "application/json"})

        else:
            raise ValueError(f"Unbekannter Anbieter: {self.provider}. Verwende 'claude', 'gemini' oder 'ollama'.")

        return self._client

    def _call_claude(self, system_prompt: str, user_text: str) -> str:
        """Aufruf der Claude API."""
        client = self._get_client()
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )
        return response.content[0].text

    def _call_gemini(self, system_prompt: str, user_text: str) -> str:
        """Aufruf der Gemini API."""
        client = self._get_client()
        response = client.generate_content(
            f"{system_prompt}\n\n---\n\n{user_text}"
        )
        return response.text

    def _call_ollama(self, system_prompt: str, user_text: str) -> str:
        """Aufruf der lokalen Ollama API."""
        client = self._get_client()
        url = f"{self.ollama_host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n---\n\n{user_text}",
            "stream": False,
        }
        response = client.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")

    def _analyze(self, prompt_name: str, text: str) -> str:
        """Führt eine KI-Analyse mit Retry-Logik durch."""
        system_prompt = self._load_prompt(prompt_name)

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                if self.provider == "claude":
                    return self._call_claude(system_prompt, text)
                elif self.provider == "gemini":
                    return self._call_gemini(system_prompt, text)
                elif self.provider == "ollama":
                    return self._call_ollama(system_prompt, text)
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_DELAY * attempt)

        raise RuntimeError(f"KI-Analyse nach {self.MAX_RETRIES} Versuchen fehlgeschlagen: {last_error}")

    def summarize(self, text: str) -> str:
        """Erstellt eine Zusammenfassung des Dokumenttexts."""
        return self._analyze("summarize", text)

    def classify(self, text: str) -> str:
        """Klassifiziert das Dokument."""
        return self._analyze("classify", text)

    def extract_key_data(self, text: str) -> dict:
        """Extrahiert Schlüsseldaten aus dem Dokument."""
        raw = self._analyze("extract", text)
        try:
            json_match = raw[raw.find("{"):raw.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"rohdaten": raw, "hinweis": "Konnte nicht als JSON parsen"}
