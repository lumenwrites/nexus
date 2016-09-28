# markdownify
from django import template
import markdown
import bleach

 
register = template.Library()
 
@register.filter
def markdownify(post, short = "False"):
    text = post.body
    if short == "True":
        try:
            text = text.split("<!-- more -->")[0].strip()
        except:
            pass
        text = text[:1024]

    html = markdown.markdown(text)

    if short == "True":
        try:
            sep = '</p>'
            firstparagraphs = html.split(sep, 2)[:2]
            html = ''.join(firstparagraphs)
        except:
            pass
        
    

    if short == "True":    
        html += "<div class='clearfix'></div><a href='"+post.get_absolute_url()+"' class='readmore'> read more >>>> </a>"

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
