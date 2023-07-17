from django import template
from contacts.models import ContactPage
from pages.models import(
    FooterSocial,
    FooterUsefulLink,
    NaviItem
)
from django.db.models import Q
from articles.models import Article

from icecream import ic
register = template.Library()

@register.filter(name='get_two_sentences')
def get_two_sentences(description):
    sentences = description.split('.')
    if len(sentences)>=1:
        result = sentences[0] + sentences[1]
    return result
        

@register.simple_tag(name='web_app_info')
def web_app_info():
    info = ContactPage.objects.get(pk = 1).info
    return f'{info}'


@register.inclusion_tag('tags/navi_items.html')
def navi_items():
    navi_items = NaviItem.objects.filter(pk__lte = 4)
    return {
        'navi_items' : navi_items
    }

@register.inclusion_tag('tags/dropdown_menu.html')
def dropdown_menu():
    query = Q(pk__gte = 5) & Q(pk__lte = 6)
    navi_items = NaviItem.objects.filter(query)

    return {
        'navi_items' : navi_items,
   
    }

@register.inclusion_tag('tags/dropdown_menu_staff.html')
def dropdown_menu_staff():
    staff_navi_items = NaviItem.objects.filter(pk__gte = 7)
    return {
        'staff_navi_items' : staff_navi_items
    }

@register.inclusion_tag('tags/footer_useful_links.html')
def footer_useful_links():
    footer_useful_links = FooterUsefulLink.objects.all()
    return {
        'footer_useful_links' : footer_useful_links
    }

@register.inclusion_tag('tags/latest_news.html')
def latest_news():
    latest_news = Article.objects.filter(approved = True).order_by('-updated_at')[:3]
    return {
        'latest_news' : latest_news
    }

@register.inclusion_tag('tags/footer_socials.html')
def footer_socials():
    footer_socials = FooterSocial.objects.all()
    return {
        'footer_socials' : footer_socials
    }