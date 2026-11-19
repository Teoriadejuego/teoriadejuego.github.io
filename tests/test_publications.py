"""Publication output contracts, independent of the shared generated public tree."""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import build
from tools.content_contract import ContentError, load_content, validate_content


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = {}
        self.years = []
        self.current = None
        self.year_select = False
        self.title = False
        self.fields = []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'article' and a.get('class') == 'publication':
            self.current = {'attributes': a, 'title': '', 'links': [], 'order': []}
            self.articles[a['id']] = self.current
        if self.current:
            if tag == 'h2':
                self.title = True
                self.current['order'].append('title')
                self.current['title_lang'] = a.get('lang')
            if tag == 'p' and a.get('class') in {'authors', 'venue'}:
                self.current['order'].append(a['class'])
            if tag == 'div' and a.get('class') == 'pub-links':
                self.current['order'].append('links')
            if tag == 'a':
                self.current['links'].append(a)
        if tag == 'select' and a.get('id') == 'pub-year':
            self.year_select = True
        if self.year_select and tag == 'option' and a.get('value'):
            self.years.append(a['value'])
        if tag == 'fieldset':
            self.fields.append(a)

    def handle_data(self, text):
        if self.title and self.current:
            self.current['title'] += text

    def handle_endtag(self, tag):
        if tag == 'article':
            self.current = None
        if tag == 'h2':
            self.title = False
        if tag == 'select':
            self.year_select = False


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.content = load_content(Path(__file__).resolve().parents[1])

    def page(self, language='es', publications=None):
        pubs = self.content['publications'] if publications is None else publications
        with patch.multiple(build, PUBS=pubs, WORKING=self.content['working-papers'], BASE='https://example.org', OUT=Path('/render-fixture')), patch.object(build, 'shell') as shell:
            build.publication_page(language)
        body, schemas = shell.call_args.args[4], shell.call_args.args[6]
        parser = ArticleParser()
        parser.feed(body)
        return body, schemas, parser

    def test_year_options_follow_articles_including_future_fixture(self):
        pubs = deepcopy(self.content['publications'])
        pubs[0]['year'] = max(p['year'] for p in pubs) + 3
        for language in ('es', 'en'):
            _, _, page = self.page(language, pubs)
            self.assertEqual(page.years, [str(y) for y in sorted({p['year'] for p in pubs}, reverse=True)])
            self.assertEqual(page.articles[pubs[0]['id']]['attributes']['data-year'], str(pubs[0]['year']))

    def test_search_text_contains_topic_without_action_labels(self):
        for language, word in [('es', 'Redes'), ('en', 'Networks')]:
            _, _, page = self.page(language)
            text = page.articles['triadic']['attributes']['data-search']
            self.assertIn(word, text)
            self.assertIn('10.1073/pnas.2215041120', text)
            self.assertNotIn('BibTeX', text)
            self.assertNotIn('Citar', text)
            self.assertNotIn('Ficha institucional', text)

    def test_each_article_has_exactly_the_doi_and_selected_repository(self):
        for language in ('es', 'en'):
            body, _, page = self.page(language)
            for paper in self.content['publications']:
                article = page.articles[paper['id']]
                self.assertEqual([a['href'] for a in article['links']],
                                 ['https://doi.org/' + paper['doi'], paper['repository']['url']])
                for term in paper['keywords'][language]:
                    self.assertIn(term, article['attributes']['data-search'])
            self.assertNotIn('The development of rationality in games with hidden information', body)

    def test_venue_precedes_authors_and_actions_have_stable_dom_order(self):
        body, _, page = self.page()
        self.assertEqual(page.articles['private-solutions']['order'], ['title', 'venue', 'authors', 'links'])
        self.assertNotIn('Antonio Alfonso: autor 5 de 72.', body)
        self.assertEqual(page.articles['private-solutions']['title_lang'], 'en')
        self.assertEqual(len(page.fields), 1)
        self.assertIn('<legend>Filtrar artículos</legend>', body)

    def test_author_position_is_added_only_when_name_is_hidden(self):
        pubs = deepcopy(self.content['publications'])
        paper = next(p for p in pubs if p['id'] == 'private-solutions')
        for key in ('authors', 'author_parts'):
            paper[key][4], paper[key][-1] = paper[key][-1], paper[key][4]
        body, _, _ = self.page(publications=pubs)
        self.assertIn('Antonio Alfonso: autor 72 de 72.', body)

    def test_structured_year_and_verified_published_version(self):
        _, schemas, _ = self.page()
        for p, schema in zip(self.content['publications'], schemas):
            self.assertEqual(schema['datePublished'], str(p['year']))
            if p.get('open_access', {}).get('kind') == 'published':
                self.assertEqual(schema['encoding']['contentUrl'], p['open_access']['url'])
            else:
                self.assertNotIn('encoding', schema)

    def test_bibliography_has_each_doi_once_and_verified_urls_only(self):
        entries = build.bibliography_entries(self.content['publications'])
        bibliography = '\n\n'.join(entries)
        self.assertEqual(len(entries), len(self.content['publications']))
        for p, entry in zip(self.content['publications'], entries):
            self.assertEqual(bibliography.casefold().count('doi={' + p['doi'].casefold() + '}'), 1)
            if p.get('open_access'):
                self.assertIn('url={' + p['open_access']['url'] + '}', entry)
                if p['open_access']['kind'] != 'published':
                    self.assertIn('note={', entry)
            else:
                self.assertNotIn('url={', entry)

    def test_home_fragments_keep_article_identity_after_reordering(self):
        c = self.content
        globals = dict(PUBS=c['publications'], PROJECTS=c['projects'], PUB_BY_ID={p['id']:p for p in c['publications']},
                       PROJECT_BY_ID={p['id']:p for p in c['projects']}, HOME_RESEARCH=c['site']['home_publications'],
                       HOME_PROJECTS=c['site']['home_projects'], BASE='https://example.org', OUT=Path('/render-fixture'))
        with patch.multiple(build, **globals), patch.object(build, 'shell') as shell:
            build.home('es')
        homepage = shell.call_args.args[4]
        fragments = re.findall(r'href="publications/#([a-z0-9-]+)"', homepage)
        self.assertTrue(fragments)
        _, _, reversed_page = self.page(publications=list(reversed(c['publications'])))
        originals = {p['id']:p for p in c['publications']}
        for ident in fragments:
            self.assertEqual(reversed_page.articles[ident]['title'], originals[ident]['title'])

    def test_access_metadata_rejects_unsafe_or_untracked_values(self):
        for key, value in [('url', 'https://example.org/not-listed.pdf'), ('url', 'javascript:private'),
                           ('kind', 'unknown'), ('kind', True), ('checked', '2026-02-30'), ('checked', True)]:
            with self.subTest(field=key, value_type=type(value).__name__):
                content = deepcopy(self.content)
                paper = next(p for p in content['publications'] if p.get('open_access'))
                paper['open_access'][key] = value
                with self.assertRaises(ContentError):
                    validate_content(content)

    def test_later_publication_is_optional_and_uses_a_validated_id(self):
        for language in ('es', 'en'):
            body, _, _ = self.page(language)
            self.assertNotIn('Later publication:', body)
            self.assertNotIn('Publicación posterior:', body)
        self.content['working-papers'][0]['published_as'] = 'unknown-paper'
        with self.assertRaisesRegex(ContentError, 'published_as'):
            validate_content(self.content)


if __name__ == '__main__':
    unittest.main()
