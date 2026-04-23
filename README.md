# AI Document Analyzer

> Python-Tool zur KI-gestützten Analyse von PDF- und DOCX-Dokumenten
> Python tool to analyze PDFs and DOCX files with AI (Claude / Gemini / Ollama)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Python](https://img.shields.io/badge/Python-3.11+-green.svg) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

## Features

- **PDF & DOCX Upload** — Dokumente per Drag & Drop oder Dateiauswahl hochladen
- **KI-Zusammenfassung** — Automatische Zusammenfassung in max. 5 Sätzen (Deutsch)
- **Dokumentklassifizierung** — Erkennung: Rechnung, Vertrag, Angebot, Bericht, Sonstiges
- **Schlüsseldaten-Extraktion** — Datum, Betrag, Parteien, Fristen, Referenznummer als JSON
- **Mehrere KI-Modelle** — Claude (Anthropic), Gemini (Google), Ollama (lokal)
- **Export** — Ergebnisse als JSON oder CSV exportieren
- **100% lokal möglich** — Mit Ollama keine Cloud-API nötig

## Use Cases für KMUs

| Use Case | Beschreibung |
|----------|-------------|
| Rechnungsverarbeitung | Beträge, Daten, Referenznummern automatisch extrahieren |
| Vertragsprüfung | Vertragsart erkennen, Fristen und Parteien identifizieren |
| Posteingangsortierung | E-Mail-Anhänge automatisch klassifizieren |
| Dokumentation | Technische Dokumente zusammenfassen |

## Schnellstart

```bash
# Lokal starten
pip install -r requirements.txt
cp .env.example .env   # API-Keys eintragen
streamlit run app.py

# Oder mit Docker
docker-compose up -d
```

Anschließend [http://localhost:8501](http://localhost:8501) öffnen.

## Projektstruktur

```
ai-document-analyzer/
  app.py                      # Streamlit Web-App
  analyzer/
    document_processor.py     # PDF/DOCX Verarbeitungs-Logik
    ai_analyzer.py            # KI-Analyse (Claude/Gemini/Ollama)
  prompts/
    summarize.txt             # System-Prompt: Zusammenfassung
    classify.txt              # System-Prompt: Klassifizierung
    extract.txt               # System-Prompt: Schlüsseldaten
  docs/
    setup-guide.md            # Detaillierte Einrichtungsanleitung
```

## Lizenz

MIT — siehe [LICENSE](LICENSE)
