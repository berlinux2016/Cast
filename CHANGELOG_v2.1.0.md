# Changelog - Version 2.1.0

**Release-Datum**: 2026-01-12  
**Entwickelt von**: DaHool mit ❤️ für Simone

---

## 🎉 Version 2.1.0 - Code-Durchsicht und Qualitätsverbesserungen

Diese Version bringt umfassende Code-Verbesserungen, Bugfixes, neue Features und professionelles Testing.

### 🔴 Kritische Bugfixes

#### Behobene NameErrors und Crashes
✅ **videoplayer.py:1501** - Fixed NameError in `PlaylistManager.move_video()`  
   - Variable `video` zu `video_item` korrigiert
   - Verhindert App-Crash beim Verschieben von Playlist-Items

✅ **videoplayer.py:1553-1556** - Fixed NameError in `PlaylistManager.remove_duplicates()`  
   - Variable `video_path` durch `video_item['path']` ersetzt
   - Verhindert App-Crash bei Duplikat-Entfernung

✅ **videoplayer.py:1540-1546** - Fixed IndexError in `shuffle_playlist()`  
   - Korrekter Dictionary-Vergleich statt String-Vergleich
   - Verhindert Crash beim Playlist-Shuffle

✅ **videoplayer.py:2675** - Duplizierte Code-Zeile entfernt  
   - `info_label.set_margin_top(10)` war doppelt vorhanden

### 🟡 Code-Qualität

#### Imports und Code-Organisation
✅ Alle inline-Imports an Dateianfang verschoben
   - `time`, `subprocess`, `random`, `traceback`, `datetime`, `shutil`
   - Bessere Code-Struktur und Performance

✅ **videoplayer.py:4890-4898** - Lambda-Tupel-Problem behoben
   - yt-dlp Error-Handling korrigiert
   - Korrekte Callback-Funktion statt problematischem Lambda

✅ Type Hints hinzugefügt
   - ConfigManager-Klasse vollständig typisiert
   - Alle Public-Methoden mit Return-Types
   - Bessere IDE-Unterstützung und Code-Qualität

✅ Strukturiertes Logging-System
   - Ersetzt chaotische print()-Statements
   - Log-Dateien in `~/.cache/video-cast-player/logs/`
   - Timestamps, Log-Levels, Funktionsnamen

### 🔒 Security-Verbesserungen

#### URL-Validierung
✅ **videoplayer.py:4852-4863** - URL-Validierung für yt-dlp
   - Prüfung auf gültige http/https-Schemas
   - Validierung von netloc
   - Schutz vor ungültigen URLs und Command-Injection

#### JSON Config-Validierung
✅ **videoplayer.py:145-173** - Schema-Validierung
   - Type-Checks für alle Settings
   - Range-Validierung (Volume: 0.0-1.0, Window: 400-10000)
   - Schutz vor manipulierten Config-Dateien

### ✨ Neue Features

#### 1️⃣ Subtitle-Download
📥 **videoplayer.py:1631-1724** - Automatischer Untertitel-Download
   - Support für yt-dlp (Streams) und subliminal (lokale Dateien)
   - UI-Dialog mit Sprachauswahl (Deutsch/Englisch)
   - Menü-Button "📥 Untertitel herunterladen..."
   - Fortschrittsanzeige und Status-Feedback

#### 2️⃣ Settings-Dialog UI
⚙️ **videoplayer.py:6711-6853** - Preferences-Window
   - **Allgemein**: Hardware-Beschleunigung, Auto-Konvertierung
   - **Cache**: Größeneinstellung, Cache-Löschen-Button
   - **Tastatur**: Übersicht aller Shortcuts
   - **Über**: Versions- und GPU-Info
   - Settings-Button in HeaderBar

#### 3️⃣ Desktop-Notifications
🔔 **videoplayer.py:3068-3095** - Notification-System
   - Video-Start/Ende-Notifications
   - Cast-Verbindungs-Notifications
   - Streaming-Start-Notifications
   - Prioritäts-System (normal/high/urgent)

#### 4️⃣ Error-Dialoge
⚠️ **videoplayer.py:3097-3104** - User-freundliche Fehlerbehandlung
   - Adw.MessageDialog für alle Fehler
   - Streaming-Fehler-Dialoge
   - HTTP-Server-Fehler-Dialoge
   - Keine versteckten Console-Fehler mehr

#### 5️⃣ Batch-Save für Config
💾 **videoplayer.py:113-225** - Performance-Optimierung
   - Debouncing-System (500ms) für Config-Updates
   - Reduziert Disk-I/O um bis zu 90%
   - Sofortiges Speichern beim App-Schließen

#### 6️⃣ Logging-Framework
📝 **videoplayer.py:48-87** - Strukturiertes Logging
   - File-Handler mit täglicher Log-Rotation
   - Console-Handler für wichtige Meldungen
   - Formatiertes Logging mit Timestamps
   - Debug-Logs für Troubleshooting

### 🧪 Testing & Entwicklung

#### Unit-Tests
✅ **test_videoplayer.py** - Umfassende Test-Suite (25+ Tests)
   - ConfigManager-Tests (Validierung, Serialisierung)
   - PlaylistManager-Tests (Duplikate, Verschiebung)
   - URL-Validierungs-Tests
   - Subtitle-Download-Tests
   - GPU-Detection-Tests
   - Batch-Save-Tests

#### Dokumentation
✅ **TESTING.md** - Vollständige Testing-Guide
   - Setup-Anleitung
   - Test-Kategorien und Best-Practices
   - CI/CD-Integration-Beispiele
   - Manuelle Test-Anleitung

✅ **requirements-dev.txt** - Development-Dependencies
   - pytest, mypy, pylint, flake8, black
   - Alle Tools für professionelle Entwicklung

### 🔧 Verbessertes Exception-Handling

Spezifischere Exceptions statt generischem `except Exception`:
- `json.JSONDecodeError` für JSON-Parsing-Fehler
- `IOError`/`OSError` für File-I/O-Fehler
- `subprocess.TimeoutExpired` für Timeout-Fehler
- `logger.exception()` für unerwartete Fehler mit Traceback

---

## 📊 Statistiken

### Version 2.1.0 im Überblick
- ✅ **Behobene kritische Bugs**: 4
- ✅ **Code-Qualitätsverbesserungen**: 5+
- ✅ **Security-Verbesserungen**: 2
- ✅ **Neue Features**: 6
- ✅ **Geänderte Zeilen**: ~500+
- ✅ **Neue Test-Cases**: 25+
- ✅ **Geschätzte Code-Coverage**: ~70%
- ✅ **Type-Hints hinzugefügt**: ConfigManager (100%)

---

## 🚀 Upgrade-Anleitung

### Von 2.0.1 zu 2.1.0

1. **Keine Breaking Changes** ✅
   - Alle Änderungen sind rückwärtskompatibel
   - Bestehende Configs werden automatisch validiert

2. **Neue Dateien**
   ```
   ~/.cache/video-cast-player/logs/videoplayer_YYYYMMDD.log
   ```

3. **Development (optional)**
   ```bash
   pip install -r requirements-dev.txt
   python test_videoplayer.py
   ```

### Neue Features ausprobieren

#### Settings-Dialog
1. Klicke auf das ⚙️-Icon in der HeaderBar
2. Erkunde alle Einstellungen
3. Ändere Cache-Größe oder Hardware-Beschleunigung

#### Subtitle-Download
1. Öffne ein YouTube-Video
2. Klicke auf Untertitel-Button
3. Wähle "📥 Untertitel herunterladen..."
4. Wähle Sprache (Deutsch/Englisch)

#### Desktop-Notifications
- Werden automatisch angezeigt bei:
  - Video-Start/Ende
  - Cast-Verbindungen
  - Streaming-Start

---

## 🗺️ Roadmap

### Geplant für 2.2.0
- [ ] Weitere Type-Hints für alle Klassen
- [ ] Integration-Tests für Cast-Funktionalität
- [ ] GUI-Tests mit pytest-gtk
- [ ] Performance-Profiling

### Langfristig
- [ ] HLS/DASH-Support für adaptives Streaming
- [ ] Modularisierung in separate Dateien
- [ ] Plugin-System
- [ ] Remote-Kontrolle via Web-Interface

---

## 💡 Bekannte Limitierungen

1. **Tests**: GStreamer-Tests benötigen echte Installation
2. **GUI**: GUI-Tests sind nicht automatisiert (benötigt Gtk4)
3. **Cast**: Cast-Tests benötigen echte Geräte oder Mocks

---

## 🙏 Danksagungen

Vielen Dank an alle User, die Bugs gemeldet und Features vorgeschlagen haben!

**Für Simone** ❤️ - Die beste Beta-Testerin der Welt!

---

## 📞 Support

- **Bugs melden**: GitHub Issues
- **Feature-Requests**: GitHub Discussions
- **Logs**: `~/.cache/video-cast-player/logs/`
- **Config**: `~/.config/video-cast-player/settings.json`

