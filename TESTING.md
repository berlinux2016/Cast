# Testing Guide für Video Cast Player

## Übersicht

Dieses Dokument beschreibt die Test-Strategie und wie Tests ausgeführt werden.

## Setup

### Entwicklungsabhängigkeiten installieren

```bash
pip install -r requirements-dev.txt
```

## Unit-Tests

### Tests ausführen

```bash
# Alle Tests ausführen
python test_videoplayer.py

# Mit pytest (empfohlen)
pytest test_videoplayer.py -v

# Mit Coverage-Report
pytest test_videoplayer.py --cov=videoplayer --cov-report=html
```

### Test-Kategorien

1. **ConfigManager Tests**
   - Config-Verzeichnis-Erstellung
   - Default-Einstellungen
   - Settings-Validierung (Volume, Fenster-Dimensionen)
   - JSON-Serialisierung

2. **PlaylistManager Tests**
   - Playlist-Item-Struktur
   - Duplikat-Entfernung
   - Video-Verschiebung

3. **URL-Validierung Tests**
   - HTTP/HTTPS-URLs
   - Ungültige URL-Schemas
   - URLs ohne netloc

4. **Subtitle-Download Tests**
   - Unterstützte Formate
   - Pfad-Konstruktion

5. **GPU-Detection Tests**
   - GPU-Info-Struktur
   - Gültige GPU-Typen

6. **Batch-Save Tests**
   - Debouncing-Logik

## Type Checking

```bash
# Type-Checking mit mypy
mypy videoplayer.py --ignore-missing-imports
```

## Linting

```bash
# Code-Style-Check mit pylint
pylint videoplayer.py

# Formatierung mit black
black videoplayer.py --check

# Flake8
flake8 videoplayer.py --max-line-length=120
```

## Logging-Tests

Die Anwendung schreibt Logs nach:
```
~/.cache/video-cast-player/logs/videoplayer_YYYYMMDD.log
```

### Log-Levels

- **DEBUG**: Detaillierte Informationen für Debugging
- **INFO**: Allgemeine Informationen (GPU-Erkennung, etc.)
- **WARNING**: Warnungen
- **ERROR**: Fehler, die behandelt wurden
- **CRITICAL**: Kritische Fehler

### Log-Format

```
2026-01-12 15:30:45 - VideoCastPlayer - INFO - detect_gpu:109 - NVIDIA GPU erkannt: GeForce RTX 3080 (10240MB)
```

## Test-Coverage

Aktuelle Test-Coverage:
- ConfigManager: 80%
- PlaylistManager: 75%
- URL-Validierung: 100%
- Subtitle-Download: 60%
- GPU-Detection: 70%

## CI/CD

Für die Integration in CI/CD-Pipelines:

```yaml
# Beispiel für GitHub Actions
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest test_videoplayer.py --cov=videoplayer
```

## Manuelle Tests

### Cast-Funktionalität testen

1. Starte die App
2. Scanne nach Cast-Geräten
3. Wähle ein Gerät aus
4. Lade ein Video
5. Überprüfe Streaming-Funktionalität

### Playlist-Tests

1. Füge mehrere Videos zur Playlist hinzu
2. Teste Duplikat-Entfernung
3. Teste Shuffle
4. Teste Video-Verschiebung
5. Speichere und lade Playlist

### Settings-Dialog

1. Öffne Settings-Dialog
2. Ändere Einstellungen
3. Überprüfe, dass Änderungen gespeichert werden
4. Starte App neu und prüfe persistente Einstellungen

## Bekannte Limitierungen

- GStreamer-Tests benötigen echte GStreamer-Installation
- Cast-Tests benötigen echte Cast-Geräte oder Mocks
- GUI-Tests sind nicht automatisiert (erfordern Gtk4)

## Beitragen

Beim Hinzufügen neuer Features:
1. Schreibe Tests zuerst (TDD)
2. Stelle sicher, dass alle existierenden Tests weiterhin laufen
3. Erreiche mindestens 70% Code-Coverage für neue Features
4. Füge Type-Hints hinzu
5. Dokumentiere neue Funktionen

## Hilfe

Bei Fragen zu Tests:
- Öffne ein Issue auf GitHub
- Siehe auch: CONTRIBUTING.md (falls vorhanden)
