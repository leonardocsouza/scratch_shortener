from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.db.models import F
from django.core.exceptions import ValidationError
from urlparse import urlparse

# Validator to check if url belongs to scratch.mit.edu
def validate_url(value):
    parsed_uri = urlparse(value)
    if parsed_uri.netloc != 'scratch.mit.edu':
        raise ValidationError('{0} is not a valid scratch.mit.edu URL'.format(value))

class Url(models.Model):
    # shorturl must allow blanks because for non-vanity URLs field is only populated after save
    shorturl = models.CharField(max_length=16, unique=True, db_index=True, verbose_name='Short URL', blank=True)
    httpurl = models.URLField(max_length=400, verbose_name='URL', validators=[validate_url])
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Update Date')
    is_vanity = models.BooleanField(default=False, verbose_name='Vanity URL?')

    def __unicode__(self):
        return self.httpurl

    @property
    def click_count(self):
        stats, created = UrlStats.objects.get_or_create(url = self)
        return stats.click_count

    # Defines how shorturl should be generated for non-vanity URLs
    def get_shorturl(self):
        return urlsafe_b64encode(str(self.pk))

    def increment_click_counter(self):
        stats, created = UrlStats.objects.get_or_create(url = self)
        stats.click_count = F('click_count') + 1
        stats.save()

    @staticmethod
    def resolve_url(shorturl, is_vanity):
        if is_vanity:
            # For vanity URLs, perform lookup using shorturl
            try:
                url = Url.objects.get(shorturl=shorturl, is_vanity=True)
                url.increment_click_counter()
                return url.httpurl
            except (Url.DoesNotExist, ValueError):
                return None
        else:
            # For non-vanity URLs, decode shorturl and perform lookup using PK
            pk = urlsafe_b64decode(shorturl)
            try:
                url = Url.objects.get(pk=pk, is_vanity=False)
                url.increment_click_counter()
                return url.httpurl
            except (Url.DoesNotExist, ValueError):
                return None

# Separate model to handle statistics for each URL
class UrlStats(models.Model):
    url = models.OneToOneField(Url, verbose_name='URL')
    click_count = models.BigIntegerField(verbose_name='Click Count', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Update Date')

# Necessary to use Django signals so we can leverage Url PK for shorturl creation
@receiver(post_save, sender=Url)
def create_shorturl(sender, instance, created, **kwargs):
    # only attempt to generate shorturl when url has just been created
    if created:
        # Only create if it isn't a vanit url and it doesn't already have a shorturl
        if not instance.is_vanity and not instance.shorturl:
            instance.shorturl = instance.get_shorturl()
            instance.save()
