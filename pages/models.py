from django.db import models

# Create your models here.


class PageBlock(models.Model):
    """
    Абстрактная Модель представляющая данные о блоках в футере и наве

    Поля:
        title(str) - имя блока
        icon_class(str) - класс иконки блока
        text(str) - текст блока
        url(str)- ссылка блока
    """
    title = models.CharField(verbose_name='Title', max_length=250, blank=True)
    icon_class = models.CharField(
        verbose_name='Icon', max_length=255, blank=True)
    text = models.TextField(verbose_name='Text', blank=True)
    url = models.CharField(verbose_name='Url', blank=True)

    class Meta:
        abstract = True


class FooterUsefulLink(PageBlock):
    """
    Модель наследуемая от PageBlock представляющая данные о  полезных ссылках в футере
    """
    class Meta:
        verbose_name = 'Footer Useful Link'
        verbose_name_plural = 'Footer Useful Links'

    def __str__(self):
        """
        Возвращает представляения полезной ссылки в виде его названия

        """
        return f"{self.title}"


class FooterSocial(PageBlock):
    """
    Модель наследуемая от PageBlock представляющая данные о соц медиях в футере
    """
    class Meta:
        verbose_name = 'Footer Social'
        verbose_name_plural = 'Footer Socials'

    def __str__(self):
        """
        Возвращает представляения соц медии в виде его названия

        """
        return f"{self.title}"


class NaviItem(PageBlock):
    """
    Модель наследуемая от PageBlock представляющая данные об элементах в наве в футере
    """
    class Meta:
        verbose_name = 'Navi Item'
        verbose_name_plural = 'Navi Items'

    def __str__(self):
        """
        Возвращает представляения элемента в наве в виде его названия

        """
        return f"{self.title}"
