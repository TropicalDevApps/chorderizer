## 2024-05-18 - [Error Message Leakage]
**Vulnerability:** Raw exception messages were printed to user output, potentially leaking sensitive system information such as paths or OS details.
**Learning:** It is crucial to hide raw exception messages from users, providing only generic feedback, while logging the actual exception details securely for maintainers.
**Prevention:** Always use a logging module to track exact errors, and display sanitized messages to end users.

## 2024-05-20 - [Broad Exception Catching]
**Vulnerability:** Catching the base `Exception` class in file saving logic could mask unexpected errors (e.g., `KeyboardInterrupt`, memory issues, or logic bugs) and lead to unpredictable program state.
**Learning:** Catching specific exceptions (like `OSError` for file I/O) is essential for robust error handling and security, as it avoids swallowing unrelated system or logic failures.
**Prevention:** Always catch the most specific exceptions possible for a given operation.

## 2025-02-14 - Prevent Information Exposure in Exception Handling
**Vulnerability:** Raw exception strings (e.g. `except ValueError as e: print(f"...{e}")`) were directly exposed to end users via CLI output.
**Learning:** Returning or printing exact system exceptions to the user UI interface can unintentionally leak sensitive system paths, execution states, or dependency logic details.
**Prevention:** Catch the exception, securely log the detailed information using `logging.error(f"...{e}")` for internal monitoring, and display a safe, generalized error message to the end user.
## 2026-05-08 - Fixed Silent Exception Handling and Stack Trace Leakage
**Vulnerability:** Found `try-except-pass` blocks that silently ignored JSON configuration loading and saving failures (CWE-703, B110, S110). Also found unhandled exception stack traces being leaked to standard output on launch failures.
**Learning:** Silent exception handling hides configuration failure states and potentially malicious activity. Leaking stack traces by default exposes application internals to end users.
**Prevention:** Always log exceptions instead of silently passing them. Use feature flags (like `--debug`) to conditionally expose stack traces in production environments, displaying generic, safe error messages otherwise.
