"""Local chat history; no model or UI dependency and no cloud upload."""
import json
import os
from pathlib import Path
import tempfile


def default_history_path():
    """Desktop/console location; Android UI passes its private user_data_dir."""
    root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / "felix" / "chat_history.json"


class ChatHistoryStore:
    """Atomic replacement preserves the previous history if writing fails.

    An unreadable/invalid file raises an error, never silently overwrites it.
    Callers can continue chatting in memory and show a storage warning.
    """

    def __init__(self, path=None, max_turns=200):
        if max_turns < 1:
            raise ValueError("max_turns must be positive")
        self.path = Path(path) if path is not None else default_history_path()
        self.max_turns = max_turns

    def load(self):
        try:
            with self.path.open(encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            return []
        if not isinstance(data, dict) or data.get("version") != 1:
            raise ValueError("Formato de historial no compatible")
        turns = data.get("turns")
        if not isinstance(turns, list) or any(
            not isinstance(turn, list) or len(turn) != 2
            or not all(isinstance(text, str) for text in turn)
            for turn in turns
        ):
            raise ValueError("Historial de chat inválido")
        return [tuple(turn) for turn in turns[-self.max_turns:]]

    def save(self, turns):
        kept = list(turns)[-self.max_turns:]
        if any(len(turn) != 2 or not all(isinstance(text, str) for text in turn) for turn in kept):
            raise ValueError("Cada turno debe tener dos textos")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent,
                                             prefix=".history-", suffix=".tmp", delete=False) as handle:
                temporary = Path(handle.name)
                json.dump({"version": 1, "turns": kept}, handle, ensure_ascii=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


class PersistentChatHistory:
    """Shared app/console integration, keeping failures visible to the caller."""

    def init_history(self, path=None):
        self.history_store = ChatHistoryStore(path)
        self.history_error = None
        self._history_read_failed = False
        try:
            self.chat_history = self.history_store.load()
        except (OSError, ValueError) as exc:
            self.chat_history = []
            self._history_read_failed = True
            self.history_error = f"No se pudo cargar el historial; se conserva el archivo: {exc}"

    def remember_turn(self, message, response):
        self.chat_history.append((message, response))
        self.chat_history = self.chat_history[-self.history_store.max_turns:]
        if not self._history_read_failed:
            self._save_history()

    def _save_history(self):
        try:
            self.history_store.save(self.chat_history)
            self.history_error = None
        except (OSError, ValueError) as exc:
            self.history_error = f"No se pudo guardar el historial: {exc}"

    def forget_history(self):
        # An explicit clear may replace even an invalid history file.
        self.chat_history = []
        self._history_read_failed = False
        self._save_history()
