import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("publication", ROOT / "scripts/verify_publication.py")
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def test_email_and_phone_detection(self):
        email = "person" + "@" + "example.org"
        phone = "138" + "0000" + "1234"
        self.assertIn("email_address", publication.text_issues(email))
        self.assertIn("phone_number", publication.text_issues(phone))

    def test_local_path_detection(self):
        path = "/" + "Users" + "/" + "example/notes"
        self.assertIn("machine_path", publication.text_issues(path))

    def test_private_marker_does_not_appear_in_report(self):
        marker = "synthetic" + "-private-person"
        result = publication.text_issues("contains " + marker, (marker,))
        self.assertIn("private_marker", result)
        self.assertNotIn(marker, str(result))

    def test_only_valid_whole_field_hash_is_exempt(self):
        value = "a" * 20 + "138" + "0000" + "1234" + "b" * 33
        self.assertEqual(len(value), 64)
        self.assertEqual(publication.json_issues({"sha256": value}), [])
        self.assertTrue(publication.json_issues({"note": value}))
        self.assertTrue(publication.json_issues({"sha256": "phone " + value}))

    def test_unexpected_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "unreviewed-attachment.txt").write_text("not public")
            self.assertTrue(any(x['category'] == 'not_allowlisted' for x in publication.audit(root)['issues']))

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").symlink_to(ROOT / "README.md")
            self.assertTrue(any(x['category'] == 'symbolic_link' for x in publication.audit(root)['issues']))

    def test_manifest_detects_changed_content(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in publication.PUBLIC_FILES:
                if name == publication.MANIFEST:
                    continue
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dest)
            self.assertTrue(publication.audit(root, write_manifest=True)['ok'])
            with (root / 'README.md').open('a') as out:
                out.write('\nA later unreviewed modification.\n')
            self.assertTrue(any(x['category'] == 'content_hash_mismatch' for x in publication.audit(root)['issues']))

    def test_current_publication(self):
        self.assertTrue(publication.audit()['ok'])


if __name__ == '__main__':
    unittest.main()
