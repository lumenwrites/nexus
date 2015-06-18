# markdownify
from django import template
import markdown
import bleach

 
register = template.Library()
 
@register.filter
def markdownify(text, short = "False"):
    if short == "True":
        try:
            text = text.split("<!-- more -->")[0].strip()
        except:
            pass
        text = text[:512]
    html = markdown.markdown(text)

    # linkify_html = bleach.linkify(html)
    # tags = ['img', 'p', 'em', 'strong', 'a', 'span', 'b', 'i', 'blockquote', 'hr'] # bleach.ALLOWED_TAGS
    # attributes = {
    #     '*': ['class', 'style'],
    #     'a': ['href', 'rel'],
    #     'img': ['src', 'alt', 'style'],
    # }
    # styles = ['float','font-weight', 'width']
    
    # clean_html = bleach.clean(linkify_html, styles=styles, tags=tags, attributes=attributes, strip=True)
    return html #clean_html

