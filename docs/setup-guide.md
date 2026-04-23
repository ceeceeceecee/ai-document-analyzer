# Einrichtungsanleitung — AI Document Analyzer

## Voraussetzungen

- Python 3.11 oder neuer
- pip (Python Package Manager)
- Git

## Lokale Installation

### 1. Repository klonen

```bash
git clone https://github.com/ceeceeceecee/ai-document-analyzer.git
cd ai-document-analyzer
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren

```bash
cp .env.example .env
```

Die `.env` Datei bearbeiten und mindestens einen API-Key eintragen:

- **Claude:** [console.anthropic.com](https://console.anthropic.com/) — API-Key erstellen
- **Gemini:** [aistudio.google.com](https://aistudio.google.com/) — API-Key erstellen
- **Ollama:** Kein API-Key nötig — [ollama.ai](https://ollama.ai/) installieren

### 5. Anwendung starten

```bash
streamlit run app.py
```

Die App ist unter [http://localhost:8501](http://localhost:8501) erreichbar.

## Docker-Installation

### 1. `.env` Datei erstellen

```bash
cp .env.example .env
# API-Keys eintragen
```

### 2. Container starten

```bash
docker-compose up -d
```

### 3. Logs anzeigen

```bash
docker-compose logs -f
```

## Ollama (lokale KI)

Für den komplett lokalen Betrieb ohne Cloud-API:

```bash
# Ollama installieren (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Modell herunterladen
ollama pull llama3

# Ollama starten
ollama serve
```

Anschließend in der App "Ollama (lokal)" als KI-Anbieter auswählen.

## Troubleshooting

### "PyPDF2 ImportError"
```bash
pip install PyPDF2
```

### "ANTHROPIC_API_KEY nicht gesetzt"
`.env` Datei erstellen und API-Key eintragen. Siehe Schritt 4.

### "Ollama Connection refused"
Prüfen ob Ollama läuft: `curl http://localhost:11434/api/tags`
Ollama starten mit: `ollama serve`

### Leerer Text nach PDF-Upload
Einige PDFs sind als Bilder gescannt (kein OCR). In diesem Fall wird kein Text extrahiert.
Lösung: PDF vorher mit einem OCR-Tool (z.B. Tesseract) verarbeiten.
