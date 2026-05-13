## 2024-05-24 - [CRITICAL] Prevent symlink-based path traversal bypass
**Vulnerability:** The `_sanitize_path` function used `os.path.abspath()` to resolve user-supplied paths, which does not resolve symlinks. This could allow an attacker to bypass directory containment checks by passing a symlink that points outside the allowed directory.
**Learning:** `os.path.abspath()` is insufficient for securely checking if a path resides within a given base directory because it doesn't resolve symlinks.
**Prevention:** Always use `os.path.realpath()` alongside `os.path.abspath()` to fully resolve symbolic links and determine the true canonical path before enforcing boundary checks.
