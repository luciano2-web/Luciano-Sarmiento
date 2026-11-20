import json
import ast
from functools import partial
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from src.mobile.chat_history import ChatHistoryStore, PersistentChatHistory


class ChatHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "private" / "chat.json"

    def session(self):
        session = PersistentChatHistory()
        session.init_history(self.path)
        return session

    def test_restart_restores_unicode_and_clear_survives_restart(self):
        first = self.session()
        first.remember_turn("你好, Félix 🐱", "¡Hola!")
        second = self.session()
        self.assertEqual(second.chat_history, [("你好, Félix 🐱", "¡Hola!")])
        second.forget_history()
        self.assertEqual(self.session().chat_history, [])

    def test_failed_replace_preserves_old_file_and_removes_temporary(self):
        first = self.session()
        first.remember_turn("uno", "respuesta")
        with patch("src.mobile.chat_history.os.replace", side_effect=OSError("disk error")):
            first.remember_turn("dos", "respuesta")
        self.assertIn("guardar", first.history_error)
        self.assertEqual(self.session().chat_history, [("uno", "respuesta")])
        self.assertEqual(list(self.path.parent.glob(".history-*")), [])

    def test_corrupt_file_is_not_overwritten_by_chat(self):
        self.path.parent.mkdir()
        self.path.write_text("broken json", encoding="utf-8")
        session = self.session()
        self.assertIn("cargar", session.history_error)
        session.remember_turn("hola", "hola")
        self.assertEqual(self.path.read_text(), "broken json")
        session.forget_history()
        self.assertEqual(self.session().chat_history, [])

    def test_invalid_schema_is_not_used_as_model_history(self):
        self.path.parent.mkdir()
        for data in ({"version": 2, "turns": []}, {"version": 1, "turns": [["x", 1]]}):
            self.path.write_text(json.dumps(data))
            session = self.session()
            self.assertEqual(session.chat_history, [])
            self.assertIsNotNone(session.history_error)

    def test_retention_bounds_saved_and_loaded_history(self):
        store = ChatHistoryStore(self.path, max_turns=2)
        store.save([("a", "a"), ("b", "b"), ("c", "c")])
        self.assertEqual(store.load(), [("b", "b"), ("c", "c")])

    def test_mobile_clear_does_not_restore_in_flight_reply(self):
        # Execute real UI methods with deterministic worker/scheduler adapters.
        source = Path(__file__).resolve().parents[1] / "src/mobile/main.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                   and node.name == "FelixMobileApp")
        callbacks = []
        class ImmediateThread:
            def __init__(self, target, **kwargs):
                self.target = target
            def start(self):
                self.target()
        scope = {"PersistentChatHistory": PersistentChatHistory, "App": object,
                 "KIVY_AVAILABLE": False, "Thread": ImmediateThread, "partial": partial,
                 "Clock": SimpleNamespace(schedule_once=lambda callback, _: callbacks.append(callback))}
        exec(compile(ast.Module(body=[cls], type_ignores=[]), str(source), "exec"), scope)
        app = scope["FelixMobileApp"].__new__(scope["FelixMobileApp"])
        app.init_history(self.path)
        app._generation, app._busy, app._stopped = 0, False, False
        app.send_btn = SimpleNamespace(disabled=False, text="")
        app.chat_box = SimpleNamespace(clear_widgets=lambda: None)
        app.add_chat_bubble = lambda *args: None
        app._start_work("first", lambda: "answer")
        callbacks.pop()(0)
        self.assertEqual(self.session().chat_history, [("first", "answer")])
        app._start_work("late", lambda: "discard me")
        app.clear_chat(None)
        callbacks.pop()(0)
        self.assertEqual(self.session().chat_history, [])


if __name__ == "__main__":
    unittest.main()
