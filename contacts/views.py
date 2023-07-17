from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import ContactMessage, ContactPage
from .forms import ContactMessageForm
from django.contrib import messages
from icecream import ic
# Create your views here.


class ContactPageTemplateView(TemplateView):
    """
    Класс представления шаблона страницы контактов.

    Атрибуты:
        - template_name (str): Имя шаблона страницы контактов.
        - form_class (ContactMessageForm): Форма для сообщений.

    Методы:
        - get_context_data(**kwargs) -> dict: Возвращает контекст данных для шаблона.
        - post(request, *args, **kwargs) -> HttpResponse: Обрабатывает POST-запрос для отправки сообщения.
    """
    template_name = 'contacts/contact_page.html'
    form_class = ContactMessageForm

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст данных для шаблона.
        form(ContactMessageForm) - Форма для сообщений.
        contacts(ContactPage) - контакты об организации

        Аргументы:
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            dict: Контекст данных для шаблона.


        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['contacts'] = ContactPage.objects.get(pk=1)
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для отправки сообщения.

        Аргументы:
            - request (HttpRequest): Запрос.
            - *args: Дополнительные  аргументы.
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Ответ сервера.

        """
        template_name = 'contacts/contact_page.html'
        context = self.get_context_data()
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Message was successfully sent")
            return render(request, self.template_name, context=context)
        else:
            context['form'] = form
            return render(request, template_name, context)
