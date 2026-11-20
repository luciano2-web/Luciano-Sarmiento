import copy
import importlib.util
import os
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("levels", Path(__file__).parents[1] / "scripts/update_levels.py")
levels = importlib.util.module_from_spec(spec)
spec.loader.exec_module(levels)


class LevelsTests(unittest.TestCase):
    def setUp(self):
        self.data = {"contributors": []}
        self.today = datetime(2026, 11, 20, tzinfo=timezone.utc)
        self.clock = patch.object(levels, "now", return_value=self.today)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        levels.enforce_reserved_roles(self.data)

    def event(self, number="1", login="alice", **extra):
        env = {"EVENT_NAME": "pull_request_target", "PR_MERGED": "true",
               "PR_AUTHOR": login, "PR_NUMBER": number}
        env.update(extra)
        with patch.dict(os.environ, env, clear=True):
            return levels.process_event(self.data)

    def test_duplicate_event_is_noop(self):
        self.event()
        before = copy.deepcopy(self.data)
        self.assertEqual(self.event(), [])
        self.assertEqual(before, self.data)

    def test_promotion_thresholds_and_history(self):
        for n in range(1, 6):
            self.event(str(n))
        c = levels.get_contributor(self.data, "ALICE")
        self.assertEqual((c["prs_merged"], c["level"], len(c["history"])), (5, 3, 5))
        self.assertEqual(c["history"][-1]["issue_number"], 5)

    def test_owner_never_promoted_or_demoted(self):
        for n in range(1, 6):
            self.event(str(n), "Luciano2-Web")
        c = levels.get_contributor(self.data, levels.OWNER_LOGIN)
        c["last_contribution"] = "2020-01-01"
        levels.demote_inactive(self.data)
        self.assertEqual((c["level"], c["rank"], c["prs_merged"]), (0, "Kitten", 5))
        self.assertIn("Kitten", levels.badge_line(c))

    def test_reserved_roles_repaired(self):
        self.data["reserved_roles"]["fenix"]["assigned_to"] = "alice"
        c = levels.get_contributor(self.data, "alice")
        c.update(role="owner", rank="Fénix", level=8)
        levels.enforce_reserved_roles(self.data)
        self.assertIsNone(self.data["reserved_roles"]["fenix"]["assigned_to"])
        self.assertEqual(c["role"], "contributor")
        self.assertNotIn("rank", c)
        self.assertEqual(c["level"], 7)

    def test_demotion_interval_and_recovery(self):
        for n in range(1, 6):
            self.event(str(n))
        c = levels.get_contributor(self.data, "alice")
        c["last_contribution"] = (self.today - timedelta(days=90)).date().isoformat()
        self.assertEqual(len(levels.demote_inactive(self.data)), 1)
        self.assertEqual(c["level"], 2)
        self.assertEqual(levels.demote_inactive(self.data), [])
        with patch.object(levels, "now", return_value=self.today + timedelta(days=89)):
            self.assertEqual(levels.demote_inactive(self.data), [])
        with patch.object(levels, "now", return_value=self.today + timedelta(days=90)):
            self.assertEqual(len(levels.demote_inactive(self.data)), 1)
        self.event("6")
        self.assertEqual(c["level"], 3)

    def test_manual_level_preserved_but_activity_remembered(self):
        c = levels.get_contributor(self.data, "alice")
        c.update(manual=True, level=6, last_contribution="2020-01-01")
        self.assertEqual(levels.demote_inactive(self.data), [])
        self.event()
        self.assertEqual((c["level"], c["prs_merged"]), (6, 1))

    def test_completed_issue_is_activity_not_promotion(self):
        self.event(EVENT_NAME="issues", ISSUE_AUTHOR="alice", ISSUE_NUMBER="2", ISSUE_REASON="completed")
        c = levels.get_contributor(self.data, "alice")
        self.assertEqual((c["issues_closed"], c["level"]), (1, 0))
        before = copy.deepcopy(self.data)
        self.event(EVENT_NAME="issues", ISSUE_AUTHOR="alice", ISSUE_NUMBER="2", ISSUE_REASON="completed")
        self.assertEqual(self.data, before)

    def test_unmerged_or_missing_number_ignored(self):
        before = copy.deepcopy(self.data)
        self.event(PR_MERGED="false")
        self.event(number="")
        self.event(EVENT_NAME="issues", ISSUE_AUTHOR="alice", ISSUE_NUMBER="4", ISSUE_REASON="not_planned")
        self.assertEqual(self.data, before)


if __name__ == "__main__":
    unittest.main()
