import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


print("Carregando modelo e tokenizador...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#modelo portugues
model_name = 'neuralmind/bert-base-portuguese-cased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.to(device)
model.eval()

def get_embedding(text, tokenizer, model):
    """Gera o embedding para um texto"""

    text = str(text) if text is not None else ""
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    
    last_hidden_state = outputs.last_hidden_state
    attention_mask = inputs['attention_mask']
    mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    sum_embeddings = torch.sum(last_hidden_state * mask_expanded, 1)
    sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
    mean_pooled = sum_embeddings / sum_mask
    
    return mean_pooled.squeeze().cpu().numpy()


data = {
    'id_queixa': [1, 2, 3, 4, 5,6,7,8,9,10],
    'texto_queixa': [
        "Dor de cabeca e febre",
        "Febre e dor de cabeca",
        "Dor de garganta",
        "Dor de ouvido e dor de garganta",
        "Joelho esfolado",
        "Corte no braco",
        "Queimadura leve",
        "Enxaqueca",
        "Dor de cabeca latejante",
        "Dor de ouvido"
        ""
    ]
}
df = pd.DataFrame(data)


print("\nGerando embeddings para cada queixa...")

df['embedding'] = df['texto_queixa'].apply(lambda text: get_embedding(text, tokenizer, model))

print("Embeddings gerados com sucesso!")
print(df)

query_text = "Cefaleia"
query_embedding = get_embedding(query_text, tokenizer, model)

all_embeddings = np.stack(df['embedding'].values)

# calcula a similaridade de cossenos entre a busca e todas as queixas
similarities = cosine_similarity([query_embedding], all_embeddings)[0]

# Adiciona a similaridade ao DataFrame
df['similaridade_com_busca'] = similarities

# Ordena o DataFrame pela similaridade e mostra os resultados
df_sorted = df.sort_values(by='similaridade_com_busca', ascending=False)

print(f"Buscando por queixas similares a: '{query_text}'\n")
print(df_sorted[['texto_queixa', 'similaridade_com_busca']])