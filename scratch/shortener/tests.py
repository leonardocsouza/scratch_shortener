from django.test import TestCase
from shortener.models import Url
from django.forms.models import modelform_factory

class ShortenerTest(TestCase):

	def test_create_non_vanity_url(self):
		url = Url.objects.create(httpurl='https://scratch.mit.edu/projects/57264876/')

		# For non-vanity urls the shorturl must be auto-generated
		self.assertTrue(url.shorturl)

	def test_create_vanity_url(self):
		original_url = 'https://scratch.mit.edu/projects/57264876/'
		shorturl = 'cool'
		url = Url.objects.create(httpurl=original_url, shorturl=shorturl, is_vanity=True)

		# For vanity urls the shorturl must be the same as the specified shorturl
		self.assertEqual(url.shorturl, shorturl)

	def test_non_vanity_url_resolution(self):
		original_url = 'https://scratch.mit.edu/projects/57264876/'
		url = Url.objects.create(httpurl=original_url)

		# Check that short URL resolves to original URL
		self.assertEqual(Url.resolve_url(url.shorturl, url.is_vanity), original_url)

	def test_vanity_url_resolution(self):
		original_url = 'https://scratch.mit.edu/projects/57264876/'
		shorturl = 'cool'
		url = Url.objects.create(httpurl=original_url, shorturl=shorturl, is_vanity=True)

		# Check that short URL resolves to original URL
		self.assertEqual(Url.resolve_url(url.shorturl, url.is_vanity), original_url)

	def test_non_vanity_url_click_count(self):
		original_url = 'https://scratch.mit.edu/projects/57264876/'
		total_clicks = 10
		url = Url.objects.create(httpurl=original_url)

		for c in range(0, total_clicks):
			Url.resolve_url(url.shorturl, url.is_vanity)

		self.assertEqual(url.click_count, total_clicks)

	def test_vanity_url_click_count(self):
		original_url = 'https://scratch.mit.edu/projects/57264876/'
		shorturl = 'cool'
		total_clicks = 10
		url = Url.objects.create(httpurl=original_url, shorturl=shorturl, is_vanity=True)

		for c in range(0, total_clicks):
			Url.resolve_url(url.shorturl, url.is_vanity)

		self.assertEqual(url.click_count, total_clicks)

	def test_form_with_invalid_url(self):
		UrlForm = modelform_factory(Url, fields=('httpurl',))
		form_data = {'httpurl': 'http://google.com'}
		form = UrlForm(data=form_data)

		self.assertFalse(form.is_valid())
