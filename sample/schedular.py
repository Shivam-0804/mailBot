import spacy
from dateparser.search import search_dates
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

def extract_event_info(paragraph):
    doc = nlp(paragraph)
    
    matcher = Matcher(nlp.vocab)
    reschedule_patterns = [
        [{"LOWER": {"IN": ["rescheduled", "moved", "postponed", "changed", "pushed"]}}],
        [{"LOWER": "from"}, {"IS_DIGIT": True, "OP": "?"}, {"LIKE_NUM": True}, {"LOWER": "to"}, {"IS_DIGIT": True, "OP": "?"}, {"LIKE_NUM": True}],
        [{"LOWER": "to"}, {"IS_DIGIT": True, "OP": "?"}, {"LIKE_NUM": True}]
    ]

    matcher.add("RESCHEDULE", reschedule_patterns)
    matches = matcher(doc)

    tasks = [chunk.text for chunk in doc.noun_chunks if "event" in chunk.text.lower() or "meeting" in chunk.text.lower()]

    date_time_info = search_dates(paragraph)

    is_rescheduled = False
    new_date = None

    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text.lower().split()[0] in ["rescheduled", "moved", "postponed", "changed", "pushed"]:
            is_rescheduled = True
        elif "from" in span.text.lower() and "to" in span.text.lower():
            from_index = span.text.lower().split().index("from")
            to_index = span.text.lower().split().index("to")
            if to_index > from_index + 1:
                new_date = date_time_info[-1][1] if date_time_info else None
        elif "to" in span.text.lower():
            new_date = date_time_info[-1][1] if date_time_info else None  

    if is_rescheduled and new_date is None and date_time_info:
        new_date = date_time_info[-1][1]

    return {
        "tasks": tasks,
        "date_time": new_date
    }

# Example usage with a single paragraph
paragraph = """I hope this email finds you well. I am writing to request a meeting to discuss the current status of our ongoing project, “Client Project XYZ”. As the User Experience Director at ABC Company, Inc., I have been leading the UX design efforts and would like to provide an update on our progress.

The meeting would be rescheduled from 25th of March to 27th of March and would last approximately 30 minutes. I will be sharing a presentation outlining the key findings and recommendations for the project’s next phase.

If this time does not work for you, please let me know and I will work with you to find an alternative. I look forward to discussing the project with you and exploring ways to move forward."""
paragraph=""""The meeting is rescheduled on 30th of march is cancelled now."""
event_info = extract_event_info(paragraph)
print(f"Extracted Info: {event_info}")
