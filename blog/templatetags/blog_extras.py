from django.contrib.auth import get_user_model
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django import template
from blog.models import Post
import logging


# Register the filters in the template library
register = template.Library()
logger = logging.getLogger(__name__)

user_model = get_user_model()

@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
      return format_html('<strong>me</strong>')

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""
    
    return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_class=''):
  return format_html('<div class="row {}">', extra_class)

@register.simple_tag
def endrow():
  return format_html('</div>')

@register.simple_tag
def col(extra_class=''):
  return format_html('<div class="col {}">', extra_class)

@register.simple_tag
def endcol():
  return format_html('</div>')

@register.inclusion_tag('blog/post-list.html')
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk).order_by('-published_at')[:5]
  logger.debug('Loaded %d recent posts for post %d', len(posts), post.id)
  return {'posts': posts,'title': 'Recent Posts'}