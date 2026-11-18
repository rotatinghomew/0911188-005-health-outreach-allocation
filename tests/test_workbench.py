import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.fixture = json.loads((ROOT / 'data/workbench.json').read_text())
        self.save()

    def save(self):
        (self.root / 'workbench.json').write_text(json.dumps(self.fixture))

    def run_action(self, action, key=None, succeeds=True):
        args = [sys.executable, '-m', 'app', action, '--data', str(self.root),
                '--ledger', str(self.root / 'receipts.sqlite3')]
        if key is not None:
            args.extend(['--key', key])
        proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=5)
        if succeeds:
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        return proc.stderr

    def test_late_report_does_not_consume_kit(self):
        self.assertEqual(self.run_action('coverage'), {'coast': 1, 'ridge': 2})
        self.assertEqual(self.run_action('allocation')['extra'], {'ridge': 4})
        self.fixture['contacts'][3]['reported'] = '2026-06-21'
        self.save()
        self.assertEqual(self.run_action('coverage'), {'coast': 1, 'ridge': 1})
        self.assertEqual(self.run_action('stock'), {'a1': 9, 'a2': 5})
        self.assertEqual(self.run_action('allocation')['extra'], {'coast': 4})
    def test_movement_can_stop_allocation(self):
        self.fixture['batches'][0]['received'] = 1
        self.save()
        self.assertIn('库存不足', self.run_action('allocation', succeeds=False))
