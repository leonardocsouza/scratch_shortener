from django.shortcuts import render
from shortener.models import Url
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View

class RedirectShortURLView(View):
    is_vanity = False

    def get(self, request, **kwargs):
    	shorturl = str(self.kwargs['shorturl'])

    	redirect_url = Url.resolve_url(shorturl, self.is_vanity)
    	
    	if redirect_url:
    		return HttpResponseRedirect(redirect_url)
    	else:
        	return HttpResponseNotFound()

class RedirectVanityURLView(RedirectShortURLView):
    is_vanity = True