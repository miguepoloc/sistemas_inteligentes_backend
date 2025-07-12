# traducir_espanol.py
import whisper
from sentence_transformers import SentenceTransformer, util

from translate.oraciones import oraciones, traducciones

# 1. Cargar modelos solo una vez
whisper_model = whisper.load_model("base")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def traducir_audio_espanol(audio_path):
    # Transcribir
    result = whisper_model.transcribe(audio_path, language="es")
    transcripcion = result["text"]

    # Embeddings
    frases_lista = list(traducciones.values())
    embeddings_frases = embedder.encode(frases_lista, convert_to_tensor=True)
    embedding_transcripcion = embedder.encode(transcripcion, convert_to_tensor=True)

    # Similitud
    scores = util.cos_sim(embedding_transcripcion, embeddings_frases)[0]
    idx = int(scores.argmax())
    score = float(scores[idx])

    return {
        "transcribe": transcripcion,
        "translate": oraciones[idx]
    }
