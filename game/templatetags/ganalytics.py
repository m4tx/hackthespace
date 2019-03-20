from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id={0}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{0}');
</script>
'''


@register.simple_tag
def google_analytics_tag():
    if not settings.GA_ID:
        return ''

    return mark_safe(GTAG.format(settings.GA_ID))
