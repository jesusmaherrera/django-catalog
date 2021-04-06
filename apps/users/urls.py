"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# views
from apps.users.views import users as users_views
from apps.users.reports.users import UserListPDFView, UserListView, TemplatePDFView

router = DefaultRouter()
router.register(r'users', users_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/reports/list/', UserListPDFView.as_view()),
    path('users/page/list/', UserListView.as_view()),
    path('reports/template/', TemplatePDFView.as_view()),
]
