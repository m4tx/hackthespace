from django import template
from django.conf import settings

register = template.Library()

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id={0}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '{0}');
</script>
'''


@register.simple_tag
def google_analytics_tag():
    if not settings.GA_ID:
        return ''

    return GTAG.format(settings.GA_ID)
