"""AI Document Analyzer — Streamlit Web-App

KI-gestützte Analyse von PDF- und DOCX-Dokumenten.
Unterstützt Claude (Anthropic), Gemini (Google) und Ollama (lokal).
"""

import os
import json
import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

from analyzer.document_processor import DocumentProcessor
from analyzer.ai_analyzer import AIAnalyzer

# Seitenkonfiguration
st.set_page_config(
    page_title="AI Document Analyzer",
    page_icon="📄",
    layout="wide",
)

# KI-Anbieter Auswahloptionen
AI_PROVIDER = {
    "Claude (Anthropic)": "claude",
    "Gemini (Google)": "gemini",
    "Ollama (lokal)": "ollama",
}


def main():
    """Hauptfunktion der Streamlit-App."""
    st.title("📄 AI Document Analyzer")
    st.caption("PDF & DOCX Dokumente mit KI analysieren — Zusammenfassung, Klassifizierung, Schlüsseldaten")

    # Seitenleiste: Einstellungen
    with st.sidebar:
        st.header("⚙️ Einstellungen")

        provider_name = st.selectbox("KI-Anbieter", list(AI_PROVIDER.keys()))
        provider = AI_PROVIDER[provider_name]

        if provider == "ollama":
            ollama_host = st.text_input("Ollama Host", value=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
            model = st.text_input("Modell", value="llama3")
        else:
            ollama_host = None
            model = None

        st.divider()
        st.header("ℹ️ Info")
        st.markdown("""
        **Anwendung:**
        1. PDF oder DOCX hochladen
        2. Analyse starten
        3. Ergebnis ansehen & exportieren

        **Unterstützt:**
        - PDF-Dateien (.pdf)
        - Word-Dokumente (.docx)
        """)

    # Hauptbereich: Datei-Upload
    uploaded_file = st.file_uploader(
        "Dokument hochladen",
        type=["pdf", "docx"],
        help="PDF oder DOCX Datei auswählen",
    )

    if not uploaded_file:
        st.info("👆 Bitte ein Dokument hochladen, um zu beginnen.")
        return

    # Datei speichern
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
    except Exception as e:
        st.error(f"Fehler beim Speichern der Datei: {e}")
        return

    try:
        # Dokument verarbeiten
        processor = DocumentProcessor()
        with st.spinner("📄 Dokument wird gelesen..."):
            text = processor.extract_text(tmp_path)

        if not text.strip():
            st.warning("Das Dokument enthält keinen extrahierbaren Text.")
            os.unlink(tmp_path)
            return

        st.success(f"Dokument geladen: {len(text)} Zeichen")

        # Text-Vorschau
        with st.expander("📝 Text-Vorschau (erste 500 Zeichen)"):
            st.text(text[:500] + ("..." if len(text) > 500 else ""))

        # Analyse-Buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            do_summarize = st.button("📋 Zusammenfassen", use_container_width=True)
        with col2:
            do_classify = st.button("🏷️ Klassifizieren", use_container_width=True)
        with col3:
            do_extract = st.button("🔑 Schlüsseldaten", use_container_width=True)

        do_all = st.button("🚀 Alles analysieren", type="primary", use_container_width=True)

        if not (do_summarize or do_classify or do_extract or do_all):
            return

        # Analyzer initialisieren
        analyzer = AIAnalyzer(provider=provider, ollama_host=ollama_host, model=model)
        results = {}

        try:
            if do_summarize or do_all:
                with st.spinner("Generiere Zusammenfassung..."):
                    results["Zusammenfassung"] = analyzer.summarize(text)

            if do_classify or do_all:
                with st.spinner("Klassifiziere Dokument..."):
                    results["Klassifizierung"] = analyzer.classify(text)

            if do_extract or do_all:
                with st.spinner("Extrahiere Schlüsseldaten..."):
                    results["Schlüsseldaten"] = analyzer.extract_key_data(text)
        except Exception as e:
            st.error(f"Fehler bei der KI-Analyse: {e}")
            os.unlink(tmp_path)
            return

        # Ergebnisse anzeigen
        st.divider()
        st.header("📊 Ergebnisse")

        for key, value in results.items():
            st.subheader(key)
            if isinstance(value, dict):
                st.json(value)
            else:
                st.write(value)

        # Export-Buttons
        if results:
            st.divider()
            export_col1, export_col2 = st.columns(2)

            with export_col1:
                json_data = json.dumps(results, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Als JSON exportieren",
                    data=json_data,
                    file_name=f"analyse_{Path(uploaded_file.name).stem}.json",
                    mime="application/json",
                )

            with export_col2:
                df = pd.DataFrame(
                    [(k, str(v)) for k, v in results.items()],
                    columns=["Analyse", "Ergebnis"],
                )
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Als CSV exportieren",
                    data=csv_data,
                    file_name=f"analyse_{Path(uploaded_file.name).stem}.csv",
                    mime="text/csv",
                )

    finally:
        # Temporäre Datei aufräumen
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
