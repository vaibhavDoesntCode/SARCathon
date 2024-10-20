from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
import json

class Command(BaseCommand):
    help = 'Loads FAQs from JSON into Elasticsearch'

    def handle(self, *args, **kwargs):
        # Initialize Elasticsearch client within the handle method
        CLOUD_ID = 'f05504d71e7c4a308c6393fae548f768:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0ZDY5YjdhOTE4YzE0NmYwYWQ3NTAzMTEyYjZiZTNkMCQ1MzZiNjQ1Mzc1YzQ0ZWYxYjU3NzY3NjAwNTI0YWUzYg=='
        USERNAME = 'elastic'
        PASSWORD = 'eDh1RQbA3i6dMv2cEYNNcy2J'

        es = Elasticsearch(
            cloud_id=CLOUD_ID,
            basic_auth=(USERNAME, PASSWORD)
        )

        # Check Elasticsearch connection
        try:
            if es.ping():
                self.stdout.write(self.style.SUCCESS("Elasticsearch is connected!"))
            else:
                self.stdout.write(self.style.ERROR("Elasticsearch is not connected."))
                return  # Exit if not connected
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error connecting to Elasticsearch: {e}"))
            return  # Exit if connection fails

        # Load FAQs from JSON file
        try:
            with open('faq/faq_data.json') as f:
                faqs = json.load(f)
                for faq in faqs:
                    es.index(index='faq_index', id=faq['id'], body=faq)
            self.stdout.write(self.style.SUCCESS('FAQs loaded successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading FAQs: {e}"))
