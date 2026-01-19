import logging
from collections import Counter
from typing import Dict, List, Any


class ServerLogAnalyzer:
    """
    Stream-based analyzer that processes log files line-by-line.
    Designed to be memory efficient and resilient to malformed lines.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the log file and return aggregated results.

        Returns:
            dict: {
                "total_requests": int,
                "status_counts": Counter,
                "malformed_lines": list[dict],
            }
        """
        status_counts: Counter[int] = Counter()
        malformed_lines: List[Dict[str, Any]] = []
        total_requests = 0

        # Use context manager to ensure the file is closed properly.
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as log_file:
            for line_no, line in enumerate(log_file, start=1):
                # Strip trailing newlines for cleaner previews
                raw_line = line.rstrip("\n")
                if not raw_line:
                    continue

                try:
                    status_code = self._parse_status_code(raw_line)
                    status_counts[status_code] += 1
                    total_requests += 1
                except Exception as exc:
                    # Capture malformed line details but continue processing.
                    preview = raw_line[:80]
                    malformed_lines.append(
                        {"line_number": line_no, "preview": preview, "error": str(exc)}
                    )
                    self.logger.warning(
                        "Malformed line %s: %s | error: %s", line_no, preview, exc
                    )

        return {
            "total_requests": total_requests,
            "status_counts": status_counts,
            "malformed_lines": malformed_lines,
        }

    def _parse_status_code(self, line: str) -> int:
        """
        Extract the HTTP status code from a single log line.

        Expects Common Log Format or similar, where the status code
        typically appears as the penultimate token.
        """
        parts = line.split()
        if len(parts) < 2:
            raise ValueError("Not enough parts to extract status code")

        # In many server logs, status code is at index -2.
        status_token = parts[-2]
        status_code = int(status_token)  # Will raise ValueError if not int
        return status_code
