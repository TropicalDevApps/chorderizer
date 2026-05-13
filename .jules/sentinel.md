## 2025-02-27 - [Fix Symlink Path Traversal]
**Vulnerability:** Path traversal through symlinks in `_sanitize_path` method.
**Learning:** `os.path.abspath` does not resolve symlinks, which allows a user to point a symlink to an arbitrary location outside the base directory, bypassing the prefix check and potentially enabling them to write files anywhere on the system.
**Prevention:** Use `os.path.realpath` instead of `os.path.abspath` to ensure all symlinks are resolved before performing prefix validation for path containment checks.
