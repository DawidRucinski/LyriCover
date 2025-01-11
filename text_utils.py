import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import logging

def preprocess_text(text):
     # Convert to lowercase
    text = text.lower()

    # Replace multiple dots with a single dot
    text = re.sub(r'\.{2,}', '.', text)

    # Remove unnecessary punctuation
    text = re.sub(r'[^\w\s.]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def compute_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer(ngram_range=(3, 3))
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0, 0]


def generate_lyrics(file_path, model, instrumental_threshold):
    logging.info(f"Generating lyrics for: {file_path}")
    try:
        transcription = preprocess_text(model.transcribe(file_path)['text'].strip())
        is_instrumental = len(transcription.split()) < instrumental_threshold
        return transcription, is_instrumental
    except ValueError as e:
        logging.error(f"Value error when processing {file_path}: {e}")
        return np.zeros(12)
    except RuntimeError as e:
        logging.error(f"Failed to process file {file_path}: {e}")
    except NotImplementedError as e:
        logging.error(f"Using not implemented feature of Whisper: {e}")