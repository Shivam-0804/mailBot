import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# nltk.download('punkt')

def summarize_extractive(text, num_sentences=2):
    sentences = nltk.sent_tokenize(text)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    sentence_scores = similarity_matrix.sum(axis=1)
    ranked_sentences = [sentences[i] for i in sentence_scores.argsort()[-num_sentences:][::-1]]
    
    summary = " ".join(ranked_sentences)
    return summary

# paragraph = """I hope this email finds you well. I am writing to request a meeting to discuss the current status of our ongoing project, “Client Project XYZ”. As the User Experience Director at ABC Company, Inc., I have been leading the UX design efforts and would like to provide an update on our progress.

# The meeting would be scheduled for [insert date and time] and would last approximately 30 minutes. I will be sharing a presentation outlining the key findings and recommendations for the project’s next phase.

# If this time does not work for you, please let me know and I will work with you to find an alternative. I look forward to discussing the project with you and exploring ways to move forward."""

# print("Output: ")
# print(summarize_extractive(paragraph))
