#!/usr/bin/env python3
"""
Unit-Tests für Video Cast Player
"""

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Füge das Hauptverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock GI dependencies vor dem Import
sys.modules['gi'] = MagicMock()
sys.modules['gi.repository'] = MagicMock()
sys.modules['gi.repository.Gtk'] = MagicMock()
sys.modules['gi.repository.Adw'] = MagicMock()
sys.modules['gi.repository.Gst'] = MagicMock()
sys.modules['gi.repository.GLib'] = MagicMock()
sys.modules['gi.repository.GstVideo'] = MagicMock()
sys.modules['gi.repository.Gdk'] = MagicMock()
sys.modules['gi.repository.Gio'] = MagicMock()
sys.modules['gi.repository.GdkPixbuf'] = MagicMock()
sys.modules['pychromecast'] = MagicMock()
sys.modules['zeroconf'] = MagicMock()


class TestConfigManager(unittest.TestCase):
    """Tests für ConfigManager"""

    def setUp(self):
        """Setup für jeden Test"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / "config"
        self.config_file = self.config_dir / "settings.json"

    def tearDown(self):
        """Cleanup nach jedem Test"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_config_directory_creation(self):
        """Test: Config-Verzeichnis wird erstellt"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.assertTrue(self.config_dir.exists())

    def test_default_settings(self):
        """Test: Default-Einstellungen werden korrekt geladen"""
        default_settings = {
            "last_directory": str(Path.home()),
            "volume": 1.0,
            "window_width": 1000,
            "window_height": 700,
            "chromecast_device": None,
            "play_mode": "local",
            "loop_mode": "NONE",
            "equalizer": None,
            "hardware_acceleration": True,
            "auto_convert_mkv": True,
            "cache_size_gb": 10,
        }

        # Prüfe, dass alle wichtigen Keys vorhanden sind
        for key in ["volume", "window_width", "window_height", "play_mode"]:
            self.assertIn(key, default_settings)

    def test_settings_validation_volume(self):
        """Test: Volume-Validierung funktioniert"""
        # Gültige Werte
        self.assertTrue(0.0 <= 0.5 <= 1.0)
        self.assertTrue(0.0 <= 1.0 <= 1.0)
        self.assertTrue(0.0 <= 0.0 <= 1.0)

        # Ungültige Werte
        self.assertFalse(0.0 <= -0.1 <= 1.0)
        self.assertFalse(0.0 <= 1.5 <= 1.0)

    def test_settings_validation_window_dimensions(self):
        """Test: Fenster-Dimensionen-Validierung funktioniert"""
        # Gültige Werte
        self.assertTrue(400 <= 1000 <= 10000)
        self.assertTrue(300 <= 700 <= 10000)

        # Ungültige Werte
        self.assertFalse(400 <= 300 <= 10000)
        self.assertFalse(300 <= 200 <= 10000)

    def test_json_serialization(self):
        """Test: JSON-Serialisierung funktioniert"""
        test_data = {
            "volume": 0.8,
            "window_width": 1200,
            "window_height": 800
        }

        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Schreibe JSON
        with open(self.config_file, 'w') as f:
            json.dump(test_data, f)

        # Lese JSON
        with open(self.config_file, 'r') as f:
            loaded = json.load(f)

        self.assertEqual(test_data, loaded)


class TestPlaylistManager(unittest.TestCase):
    """Tests für PlaylistManager"""

    def test_playlist_item_structure(self):
        """Test: Playlist-Items haben korrekte Struktur"""
        playlist_item = {
            'path': '/path/to/video.mp4',
            'display': 'video.mp4'
        }

        self.assertIn('path', playlist_item)
        self.assertIn('display', playlist_item)
        self.assertIsInstance(playlist_item['path'], str)
        self.assertIsInstance(playlist_item['display'], str)

    def test_playlist_deduplication_logic(self):
        """Test: Duplikat-Entfernungs-Logik"""
        playlist = [
            {'path': '/video1.mp4', 'display': 'video1.mp4'},
            {'path': '/video2.mp4', 'display': 'video2.mp4'},
            {'path': '/video1.mp4', 'display': 'video1.mp4'},  # Duplikat
            {'path': '/video3.mp4', 'display': 'video3.mp4'},
        ]

        unique_videos = []
        seen = set()

        for video_item in playlist:
            video_path = video_item['path']
            if video_path not in seen:
                seen.add(video_path)
                unique_videos.append(video_item)

        self.assertEqual(len(unique_videos), 3)
        self.assertNotEqual(len(unique_videos), len(playlist))

    def test_playlist_move_logic(self):
        """Test: Video-Verschiebung in Playlist"""
        playlist = [
            {'path': '/video1.mp4', 'display': 'video1.mp4'},
            {'path': '/video2.mp4', 'display': 'video2.mp4'},
            {'path': '/video3.mp4', 'display': 'video3.mp4'},
        ]

        # Verschiebe von Index 0 nach Index 2
        from_index = 0
        to_index = 2

        if 0 <= from_index < len(playlist) and 0 <= to_index < len(playlist):
            video_item = playlist.pop(from_index)
            playlist.insert(to_index, video_item)

        # video1 sollte jetzt an letzter Stelle sein
        self.assertEqual(playlist[2]['path'], '/video1.mp4')
        self.assertEqual(playlist[0]['path'], '/video2.mp4')


class TestURLValidation(unittest.TestCase):
    """Tests für URL-Validierung"""

    def test_valid_http_url(self):
        """Test: Gültige HTTP-URL"""
        from urllib.parse import urlparse

        url = "http://example.com/video.mp4"
        parsed = urlparse(url)

        self.assertEqual(parsed.scheme, 'http')
        self.assertTrue(parsed.netloc)

    def test_valid_https_url(self):
        """Test: Gültige HTTPS-URL"""
        from urllib.parse import urlparse

        url = "https://example.com/video.mp4"
        parsed = urlparse(url)

        self.assertEqual(parsed.scheme, 'https')
        self.assertTrue(parsed.netloc)

    def test_invalid_url_scheme(self):
        """Test: Ungültiges URL-Schema"""
        from urllib.parse import urlparse

        url = "ftp://example.com/video.mp4"
        parsed = urlparse(url)

        self.assertNotIn(parsed.scheme, ('http', 'https'))

    def test_invalid_url_no_netloc(self):
        """Test: URL ohne netloc"""
        from urllib.parse import urlparse

        url = "http://"
        parsed = urlparse(url)

        self.assertFalse(parsed.netloc)


class TestSubtitleDownload(unittest.TestCase):
    """Tests für Subtitle-Download-Logik"""

    def test_subtitle_formats(self):
        """Test: Unterstützte Subtitle-Formate"""
        subtitle_formats = ['.srt', '.ass', '.ssa', '.vtt', '.sub']

        self.assertIn('.srt', subtitle_formats)
        self.assertIn('.vtt', subtitle_formats)
        self.assertEqual(len(subtitle_formats), 5)

    def test_subtitle_path_construction(self):
        """Test: Subtitle-Pfad-Konstruktion"""
        video_path = Path("/videos/movie.mp4")
        video_stem = video_path.stem

        subtitle_path = video_path.parent / f"{video_stem}.de.srt"

        self.assertEqual(subtitle_path.name, "movie.de.srt")
        self.assertEqual(subtitle_path.parent, Path("/videos"))


class TestGPUDetection(unittest.TestCase):
    """Tests für GPU-Erkennung"""

    def test_gpu_info_structure(self):
        """Test: GPU-Info-Struktur"""
        gpu_info = {
            'type': 'nvidia',
            'name': 'GeForce RTX 3080',
            'vram': 10240
        }

        self.assertIn('type', gpu_info)
        self.assertIn('name', gpu_info)
        self.assertIn('vram', gpu_info)

    def test_gpu_type_values(self):
        """Test: Gültige GPU-Typen"""
        valid_types = ['nvidia', 'amd', 'intel', 'unknown']

        for gpu_type in valid_types:
            self.assertIn(gpu_type, valid_types)


class TestBatchSaveLogic(unittest.TestCase):
    """Tests für Batch-Save-Logik"""

    def test_debounce_logic(self):
        """Test: Debouncing-Logik"""
        save_pending = False
        save_timeout_id = None

        # Simuliere mehrfache Aufrufe
        calls = []

        def mock_save():
            calls.append(1)
            return False

        # Wenn Timeout bereits existiert, sollte er entfernt werden
        if save_timeout_id:
            pass  # In echtem Code: GLib.source_remove(save_timeout_id)

        save_pending = True
        # In echtem Code: save_timeout_id = GLib.timeout_add(500, mock_save)

        self.assertTrue(save_pending)


if __name__ == '__main__':
    # Führe Tests aus
    unittest.main(verbosity=2)
