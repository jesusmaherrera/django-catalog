import functools

from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import CONTENT_TYPE_PNG, WeasyTemplateResponse

from apps.users.models import User

# class UserReport(WeasyTemplateResponseMixin, DetailView):
#     model = User
#     template_name = 'mymodel.html'
#     # output of MyModelView rendered as PDF with hardcoded CSS
#     pdf_stylesheets = [
#         settings.STATIC_ROOT + 'css/app.css',
#     ]
#     # show pdf in-line (default: True, show download dialog)
#     pdf_attachment = False
#     # custom response class to configure url-fetcher
#     response_class = CustomWeasyTemplateResponse