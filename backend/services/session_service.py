"""
SatQuery AI — Session Service

Manages user sessions: tracks uploaded images, query history,
and generated results per session.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from backend.config import MAX_SESSIONS, SESSION_TIMEOUT_MINUTES


class SessionService:
    """
    In-memory session manager.

    For the prototype, sessions are stored in memory. This is sufficient
    for a single-user demo. For production, replace with Redis/SQLite.
    """

    def __init__(self):
        self._sessions: dict[str, dict[str, Any]] = {}

    def create_session(self) -> str:
        """Create a new session and return its ID."""
        self._cleanup_expired()

        if len(self._sessions) >= MAX_SESSIONS:
            # Remove oldest session
            oldest_id = min(
                self._sessions,
                key=lambda sid: self._sessions[sid]["created_at"],
            )
            del self._sessions[oldest_id]

        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow(),
            "images": [],
            "queries": [],
            "results": [],
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get a session by ID, updating last_accessed."""
        session = self._sessions.get(session_id)
        if session:
            session["last_accessed"] = datetime.utcnow()
        return session

    def add_image(self, session_id: str, image_info: dict[str, Any]) -> None:
        """Register an uploaded image in the session."""
        session = self.get_session(session_id)
        if session:
            session["images"].append(image_info)

    def add_query(self, session_id: str, query: str) -> None:
        """Record a query in the session history."""
        session = self.get_session(session_id)
        if session:
            session["queries"].append({
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
            })

    def _cleanup_expired(self) -> None:
        """Remove sessions that have exceeded the timeout."""
        cutoff = datetime.utcnow() - timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        expired = [
            sid for sid, data in self._sessions.items()
            if data["last_accessed"] < cutoff
        ]
        for sid in expired:
            del self._sessions[sid]


# Singleton instance
session_service = SessionService()
