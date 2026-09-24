"""Regression tests for https://github.com/chapmanbe/pyConTextNLP/issues/18.

``get_items()`` used ``yaml.load_all(stream)`` without a ``Loader`` argument,
which raises ``TypeError: load_all() missing 1 required positional argument:
'Loader'`` on PyYAML >= 6.0, making it impossible to load any YAML knowledge
base. These tests are hermetic: they load the YAML files shipped with the
repo, no network and no external models required.
"""
import glob
import os
import unittest

from pyConTextNLP.itemData import get_items

KB_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "KB"))


class TestGetItems(unittest.TestCase):
    def test_get_items_loads_modifiers_kb(self):
        """A real modifiers KB must load into contextItem objects."""
        items = get_items(os.path.join(KB_DIR, "critical_modifiers.yml"))
        self.assertGreater(len(items), 0)
        first = items[0]
        self.assertEqual(first.getLiteral(), "bolus timing")
        self.assertEqual(first.getRule(), "bidirectional")
        self.assertIn("quality_feature", first.getCategory())

    def test_get_items_loads_targets_kb(self):
        """A real targets KB must load into contextItem objects."""
        items = get_items(os.path.join(KB_DIR, "critical_findings.yml"))
        self.assertGreater(len(items), 0)
        first = items[0]
        self.assertEqual(first.getLiteral(), "embolism")
        self.assertEqual(first.getRE(), r"\b(emboli|embolism|embolus)\b")

    def test_get_items_loads_every_shipped_kb(self):
        """Every YAML knowledge base shipped in KB/ must parse successfully."""
        yml_files = sorted(glob.glob(os.path.join(KB_DIR, "*.yml")))
        self.assertTrue(yml_files, "no .yml files found under KB/")
        failures = []
        for path in yml_files:
            try:
                items = get_items(path)
                self.assertGreater(len(items), 0, "loaded zero items")
            except Exception as exc:  # collect per-file failures
                failures.append("%s: %r" % (os.path.basename(path), exc))
        self.assertFalse(failures, "failed to load:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
