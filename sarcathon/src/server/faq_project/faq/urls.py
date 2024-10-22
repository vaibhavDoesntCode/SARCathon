# faq/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('search/', FAQSearchView.as_view(), name='faq-search'),
    path('chat/',chat_bot_gem2.as_view(),name='chatbot')
]
