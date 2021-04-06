
# django
from django.views.generic import ListView
from django.views.generic.base import TemplateView

# django_weasyprint
from django_weasyprint import WeasyTemplateResponseMixin

# Users
from apps.users.models import User


class UserListView(ListView):
    model = User
    template_name = 'users/reports/user_list.html'

class UserListPDFView(WeasyTemplateResponseMixin, ListView):
    model = User
    template_name = 'users/reports/user_list.html'
    pdf_filename = 'User List.pdf'
    pdf_attachment = False


class TemplatePDFView(WeasyTemplateResponseMixin, TemplateView):
    model = User
    template_name = 'template_test.html'
    pdf_filename = 'User List.pdf'
    pdf_attachment = False
