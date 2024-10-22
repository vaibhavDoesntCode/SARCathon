# faq/urls.py
from django.urls import path
from .views import FAQSearchView, GeminiChatbotAPIView

urlpatterns = [
    path('search/', FAQSearchView.as_view(), name='faq-search'),
    path('chat/',GeminiChatbotAPIView.as_view(),name='chatbot')
]
