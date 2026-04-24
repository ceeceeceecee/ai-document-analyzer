# AI Document Analyzer

[![Python](https://img.shields.io/badge/python-3.11+-green?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)](https://www.docker.com)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude-supported-9945FF?logo=anthropic)](https://anthropic.com)

> PDF & DOCX Dokumente automatisch analysieren, zusammenfassen und klassifizieren — mit Claude, Gemini oder Ollama.

Automatically analyze, summarize and classify PDF & DOCX documents — with Claude, Gemini or Ollama.

---

## Screenshot

![Streamlit UI](screenshots/streamlit-ui.png)
*Upload-Bereich mit Live-Analyse: Klassifizierung, Zusammenfassung und Schlüsseldaten-Extraktion in Echtzeit.*

---

## Features

| Feature | Beschreibung |
|---------|-------------|
| PDF & DOCX Upload | Drag & Drop oder Dateiauswahl |
| KI-Zusammenfassung | Automatisch in max. 5 Sätzen (Deutsch/Englisch) |
| Dokumentklassifizierung | Rechnung, Vertrag, Angebot, Bericht, Sonstiges |
| Schlüsseldaten-Extraktion | Datum, Betrag, Parteien, Fristen als JSON |
| Multi-Provider | Claude, Gemini, Ollama (lokal) |
| Export | JSON & CSV |
| 100% lokal möglich | Mit Ollama keine Cloud-API nötig |

---

## 🚀 Schnellstart

### Voraussetzungen

| Komponente | Version | Zweck |
|---|---|---|
| Python | 3.11+ | Streamlit Web-App |
| Claude/Gemini API Key oder Ollama | aktuell | KI-Analyse |
| Docker (optional) | 20.10+ | Container-Deployment |

### Installation

```bash
git clone https://github.com/ceeceeceecee/ai-document-analyzer.git
cd ai-document-analyzer

# Abhängigkeiten installieren
pip install -r requirements.txt

# Konfiguration
cp .env.example .env
# API-Keys in .env eintragen
```

### Erste Schritte

1. **Lokal starten:** `streamlit run app.py` und [http://localhost:8501](http://localhost:8501) öffnen
2. **Oder mit Docker:** `docker compose up -d`
3. **Dokument hochladen** und KI-Analyse starten — unterstützt PDF & DOCX

---

## Projektstruktur

```
ai-document-analyzer/
├── app.py                      # Streamlit Web-App
├── analyzer/
│   ├── document_processor.py   # PDF/DOCX Verarbeitung
│   └── ai_analyzer.py          # KI-Analyse (Claude/Gemini/Ollama)
├── prompts/
│   ├── summarize.txt           # System-Prompt: Zusammenfassung
│   ├── classify.txt            # System-Prompt: Klassifizierung
│   └── extract.txt             # System-Prompt: Schlüsseldaten
├── docker-compose.yml
├── requirements.txt
└── docs/
    └── setup-guide.md          # Detaillierte Einrichtung
```

---

## Use Cases

| Zielgruppe | Szenario |
|------------|----------|
| Buchhaltung | Rechnungen: Beträge, Daten, Referenznummern extrahieren |
| Rechtsabteilung | Verträge: Art erkennen, Fristen & Parteien identifizieren |
| Assistenz | Posteingang: E-Mail-Anhänge automatisch klassifizieren |
| IT / DevOps | Dokumentation: Technische Docs zusammenfassen |

---

## Tech Stack

- **Streamlit** — Web-Interface
- **Claude / Gemini / Ollama** — KI-Analyse
- **PyPDF2 / python-docx** — Dokument-Verarbeitung
- **Docker** — Container-Deployment

---

## Roadmap

- [ ] Batch-Verarbeitung (Ordner)
- [ ] OCR für gescannte Dokumente
- [ ] RAG: Fragen an Dokumente stellen
- [ ] Multi-Sprachen-Erkennung

---

## Contributing

1. Fork → Feature-Branch → Commit → Push → Pull Request

---

## Lizenz

[MIT](LICENSE) — frei nutzbar.

## Author

[ceeceeceecee](https://github.com/ceeceeceecee)

## Weitere Projekte

- [Self-Hosted AI Chatbot](https://github.com/ceeceeceecee/self-hosted-ai-chatbot) — DSGVO-konformer Chatbot
- [AI Market Analysis Bot](https://github.com/ceeceeceecee/ai-market-analysis-bot) — Marktanalyse
