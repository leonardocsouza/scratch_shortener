from django.conf.urls import patterns, include, url
from shortener.views import RedirectShortURLView, RedirectVanityURLView

urlpatterns = patterns('shortener.views',
    url(r'^v/(?P<shorturl>.+)', RedirectVanityURLView.as_view(), name='redirect_vanity_url'),
    url(r'^(?P<shorturl>.+)', RedirectShortURLView.as_view(), name='redirect_non_vanity_url'),
)