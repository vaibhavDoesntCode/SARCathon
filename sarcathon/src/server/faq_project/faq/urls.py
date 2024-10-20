# faq/urls.py
from django.urls import path
from .views import FAQSearchView

urlpatterns = [
    path('search/', FAQSearchView.as_view(), name='faq-search'),
]
