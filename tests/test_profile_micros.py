"""Profile/lab editorial regressions without writing the shared build."""
import copy
import unittest
from unittest.mock import patch

import build
from tools.content_contract import ContentError, load_content, validate_content


class ProfileMicroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = load_content(build.ROOT)

    def body(self, function, lang):
        values = dict(BASE='https://example.org', DATE='2026-11-19', OUT=build.ROOT / 'public',
                      RESOURCES=self.content['resources'], SOFTWARE=self.content['software'],
                      PROJECT_BY_ID={p['id']: p for p in self.content['projects']})
        with patch.multiple(build, **values), patch.object(build, 'shell') as shell:
            function(lang)
            return shell.call_args.args[4]

    def test_resource_language_is_optional_and_restricted(self):
        for language in ('es', 'en'):
            content = copy.deepcopy(self.content)
            content['resources'][0]['language'] = language
            validate_content(content)
        content['resources'][0].pop('language')
        validate_content(content)
        for invalid in ('', 'fr', None, [], {}, 2):
            content['resources'][0]['language'] = invalid
            with self.subTest(language=invalid), self.assertRaises(ContentError):
                validate_content(content)

    def test_profile_identity_periods_and_thesis(self):
        for lang in ('es', 'en'):
            html = self.body(build.profile, lang)
            self.assertIn('<h1>Antonio Alfonso Costillo</h1>', html)
            for period in ('2024–2025', '2023–2024', '2022–2023', '2020–2022'):
                self.assertIn('<time>' + period + '</time>', html)
            self.assertIn('https://hdl.handle.net/10433/14568', html)
            self.assertIn('for-teams/', html)
            self.assertIn('CNEAI)', html)
            self.assertNotIn('Python, R, JavaScript, HTML, Stata', html)

    def test_work_samples_precede_qualifications_and_email_is_a_draft(self):
        for lang in ('es', 'en'):
            html = self.body(build.teams_page, lang)
            self.assertLess(html.index('class="fit-grid"'), html.index('class="hiring-facts"'))
            self.assertIn('mailto:aalfonsoc@gmail.com?subject=', html)
            self.assertNotIn('Evidence status', html)
            self.assertNotIn('Estado de la evidencia', html)

    def test_resources_are_complete_and_grouped_without_duplicates(self):
        for lang in ('es', 'en'):
            html = self.body(build.lab_page, lang)
            self.assertEqual(html.count('class="resource-group"'), 3)
            for item in self.content['resources']:
                self.assertEqual(html.count('href="' + item['url'] + '"'), 1)
                # Escaped URL still retains the same prefix and unique record ID.
                self.assertIn(item['url'].rsplit('/', 1)[-1], html)
            self.assertEqual(html.count(' · en inglés'), 4 if lang == 'es' else 0)
            self.assertEqual(html.count(' · in Spanish'), 10 if lang == 'en' else 0)

    def test_lab_help_and_table_groups(self):
        for lang in ('es', 'en'):
            html = self.body(build.lab_page, lang)
            for identifier in ('lab-scale-note', 'lab-reset-values', 'lab-lower', 'lab-upper'):
                self.assertIn('id="' + identifier + '"', html)
            self.assertIn('aria-describedby="lab-reset-values"', html)
            self.assertIn('class="lab-inputs"', html)
            self.assertIn('class="lab-calculated"', html)
            self.assertEqual(html.count('role="status"'), 1)


if __name__ == '__main__':
    unittest.main()
