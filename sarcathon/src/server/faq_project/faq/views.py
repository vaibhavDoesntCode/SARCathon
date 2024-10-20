from django.shortcuts import render

# Create your views here.
# faq/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from .utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity

CLOUD_ID = 'f05504d71e7c4a308c6393fae548f768:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0ZDY5YjdhOTE4YzE0NmYwYWQ3NTAzMTEyYjZiZTNkMCQ1MzZiNjQ1Mzc1YzQ0ZWYxYjU3NzY3NjAwNTI0YWUzYg=='
USERNAME = 'elastic'
PASSWORD = 'eDh1RQbA3i6dMv2cEYNNcy2J'

es = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=(USERNAME, PASSWORD)
)
class FAQSearchView(APIView):
    def post(self, request):
        query = request.data.get('query', '')

        # Elasticsearch full-text search
        search_results = es.search(index="faq_index", body={
            "query": {
                "match": {"question": query}
            }
        })

        # BERT embedding for the query
        query_embedding = get_embedding(query)

        # Get FAQ embeddings and re-rank using cosine similarity
        faq_embeddings = [get_embedding(hit['_source']['question']) for hit in search_results['hits']['hits']]
        similarities = [cosine_similarity(query_embedding.reshape(1, -1), faq_emb.reshape(1, -1)).item() for faq_emb in faq_embeddings]
        ranked_results = sorted(zip(similarities, search_results['hits']['hits']), reverse=True, key=lambda x: x[0])

        # Get the top 3 ranked FAQs
        top_results = ranked_results[:3]

        # Format the response
        response_data = [{
            'question': faq['_source']['question'],
            'answer': faq['_source']['answer'],
            'similarity': sim
        } for sim, faq in top_results]

        return Response(response_data)
