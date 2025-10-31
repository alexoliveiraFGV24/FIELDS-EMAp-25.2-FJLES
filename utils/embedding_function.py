import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#modelo portugues
model_name = 'neuralmind/bert-base-portuguese-cased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.to(device)
model.eval()

#função por linha
def get_embedding(text, tokenizer=tokenizer, model=model):
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

#função por serie
def get_embeddings_series(text_series: pd.Series, tokenizer=tokenizer, model=model, device=None, batch_size=8):
    """
    Gera embeddings contextualizados para uma Series de textos.

    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.eval()
    embeddings = []


    texts = text_series.fillna("").astype(str).tolist()

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]

        inputs = tokenizer(
            batch_texts,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=512
        ).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        last_hidden_state = outputs.last_hidden_state
        attention_mask = inputs['attention_mask']


        mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * mask_expanded, 1)
        sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
        mean_pooled = sum_embeddings / sum_mask

        embeddings.append(mean_pooled.cpu().numpy())

    return np.vstack(embeddings)

#testes:

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

df['embedding'] = list(get_embeddings_series(df['texto_queixa'], tokenizer, model, device))

print(df["embedding"])

