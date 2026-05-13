import sys
from unittest.mock import MagicMock

# Mock colorama
sys.modules["colorama"] = MagicMock()
sys.modules["colorama.Fore"] = MagicMock()
sys.modules["colorama.Style"] = MagicMock()

# Mock mido (needed by generators which is imported by chorderizer)
sys.modules["mido"] = MagicMock()

import os
import unittest

from chorderizer.chorderizer import _sanitize_midi_path


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath("safe_midi_exports")
        self.default_path = os.path.join(self.base_dir, "default.mid")

    def test_sanitize_empty_input(self):
        result = _sanitize_midi_path("", self.default_path, self.base_dir)
        self.assertEqual(result, self.default_path)

    def test_sanitize_normal_filename(self):
        result = _sanitize_midi_path("my_song.mid", self.default_path, self.base_dir)
        expected = os.path.join(self.base_dir, "my_song.mid")
        self.assertEqual(result, expected)

    def test_sanitize_path_traversal(self):
        # Should return default when path traversal detected
        result = _sanitize_midi_path("../../../etc/passwd", self.default_path, self.base_dir)
        self.assertEqual(result, self.default_path)

    def test_sanitize_absolute_path(self):
        # Absolute paths within base_dir should work
        result = _sanitize_midi_path("evil.mid", self.default_path, self.base_dir)
        expected = os.path.join(self.base_dir, "evil.mid")
        self.assertEqual(result, expected)

    def test_sanitize_nested_traversal(self):
        # Path traversal with directory separators should be blocked
        result = _sanitize_midi_path("subdir/../other.mid", self.default_path, self.base_dir)
        # Should resolve to base_dir/other.mid (valid) or default (if traversal detected)
        if result != self.default_path:
            self.assertTrue(result.endswith("other.mid"))
            self.assertTrue(result.startswith(self.base_dir))

    def test_sanitize_subdirectory_allowed(self):
        # Subdirectories within base_dir should be allowed
        result = _sanitize_midi_path("subdir/my_song.mid", self.default_path, self.base_dir)
        expected = os.path.join(self.base_dir, "subdir", "my_song.mid")
        self.assertEqual(result, expected)

    @unittest.skipIf(os.name == "nt", "Symlinks require admin privileges on Windows")
    def test_sanitize_symlink_traversal(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = os.path.join(temp_dir, "base")
            os.makedirs(base_dir)
            default_path = os.path.join(base_dir, "default.mid")

            external_dir = os.path.join(temp_dir, "external")
            os.makedirs(external_dir)

            symlink_path = os.path.join(base_dir, "link")
            os.symlink(external_dir, symlink_path)

            result = _sanitize_midi_path("link/secret.mid", default_path, base_dir)
            self.assertEqual(result, default_path, "Symlink path traversal bypass detected!")


if __name__ == "__main__":
    unittest.main()
