from transformers import BertTokenizer, BertModel
import torch
import json

FILE_PATH = "faqs.json"

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def faq_embedding(text):
    inputs = tokenizer(text,  return_tensors='pt', max_length=512, truncation=True, padding=True)
    print(inputs)
    with torch.no_grad():
        outputs =  model(**inputs)
    return outputs.last_hidden_state.mean(dim=1) 


def read_data(file_path):
    with open(file_path, "r") as f:
        faq_data = json.load(f)
    return faq_data

query = "Can you tell me about scholarships?"

q_embedding = faq_embedding(query)

faq_embeddings_array = []

faqs_data = read_data(FILE_PATH)

for category, faqs in faqs_data.items():
    for faq in faqs:
        embedding1 = faq_embedding(faq["question"])
        faq_embeddings_array.append({
            "category": category,
            'question': faq["question"],
            'answer': faq["answer"],
            "embedding":embedding1
        })
    
def cosine_sim(a,b):
     return torch.nn.functional.cosine_similarity(a, b).item()

similarities = [
    (cosine_sim(q_embedding, faq['embedding']), faq)
    for faq in faq_embeddings_array
]


similarities.sort(key=lambda x: x[0], reverse=True)


most_similar_faq = similarities[0][1]
print(f"Q: {most_similar_faq['question']}")
print(f"A: {most_similar_faq['answer']}")