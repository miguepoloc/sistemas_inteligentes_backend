# inference.py
import torch
from extract_embeddings import get_embedding

from translate.oraciones import oraciones, traducciones
from translate.train_model import SimpleClassifier

# Parámetros
input_dim = 768
num_classes = len(oraciones)

# Cargar modelo una sola vez
model = SimpleClassifier(input_dim, num_classes)
model.load_state_dict(torch.load("clasificador_audio.pt"))
model.eval()

def traducir_audio_arhuaco(audio_path):
    # Obtener embedding
    emb = get_embedding(audio_path)

    # Predecir
    with torch.inference_mode():
        logits = model(emb)
        predicted = torch.argmax(logits, dim=1).item()

    return {
        "transcribe": oraciones[predicted],
        "translate": traducciones[predicted]
    }
