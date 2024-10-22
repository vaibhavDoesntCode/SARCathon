from django.shortcuts import render



from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from .utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from rest_framework.decorators import api_view
import google.generativeai as genai
import json
import os
from django.contrib.sessions.models import Session
import requests
from django.conf import settings
from genai import GenerativeModel



CLOUD_ID = 'f05504d71e7c4a308c6393fae548f768:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0ZDY5YjdhOTE4YzE0NmYwYWQ3NTAzMTEyYjZiZTNkMCQ1MzZiNjQ1Mzc1YzQ0ZWYxYjU3NzY3NjAwNTI0YWUzYg=='
USERNAME = 'elastic'
PASSWORD = 'eDh1RQbA3i6dMv2cEYNNcy2J'


GEMINI_API_ENDPOINT = "https://api.gemini.ai/v1/generate"
GEMINI_API_KEY = "AIzaSyDAh7Ug0TKtRuq6w7RAjekLlvy8SRLza1M"

FAQ_PATH = os.path.join(os.path.dirname(__file__), 'faq_data.json')

with open(FAQ_PATH, "r") as f:
    faq_data = json.load(f)







    


es = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=(USERNAME, PASSWORD)
)
class FAQSearchView(APIView):
    def post(self, request):
        query = request.data.get('query', '')

        
        search_results = es.search(index="faq_index", body={
            "query": {
                "match": {"question": query}
            }
        })

        
        query_embedding = get_embedding(query)

        
        faq_embeddings = [get_embedding(hit['_source']['question']) for hit in search_results['hits']['hits']]
        similarities = [cosine_similarity(query_embedding.reshape(1, -1), faq_emb.reshape(1, -1)).item() for faq_emb in faq_embeddings]
        ranked_results = sorted(zip(similarities, search_results['hits']['hits']), reverse=True, key=lambda x: x[0])

        
        top_results = ranked_results[:3]

        
        response_data = [{
            'question': faq['_source']['question'],
            'answer': faq['_source']['answer'],
            'similarity': sim
        } for sim, faq in top_results]

        return Response(response_data)

























    








































































class GeminiChatbotAPIView(APIView):

    def post(self, request):
        
        prompt = request.data.get('prompt')

        
        history = request.session.get('chat_history', [])

        
        history.append({"user": prompt})

        
        context = faq_data

        
        model = GenerativeModel('gemini-pro')

        
        model_input = {
            'prompt': prompt,
            'context': context,
            'history': history
        }

        try:
            
            gemini_response = model.generate(model_input)

            
            bot_response = gemini_response.get('response', 'No response from Gemini model.')

            
            history.append({"bot": bot_response})

            
            request.session['chat_history'] = history

            
            return JsonResponse({
                'response': bot_response,
                'history': history
            })

        except Exception as e:
            return JsonResponse({
                'error': 'Failed to communicate with Gemini model.',
                'details': str(e)
            }, status=500)