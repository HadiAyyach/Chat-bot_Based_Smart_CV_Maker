import json 
from transformers import pipeline


def get_recommendations(job_title):
    with open('classes.json', 'r') as file:
        classes = json.load(file)
        
    with open("example.txt", "r") as file:
        text_content = file.read()

    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    candidate_labels = classes[job_title]

    output = classifier(text_content, candidate_labels, multi_label= True)

    skills = {
    "skill": output["labels"],  
    "score": output["scores"],
    }

    with open("skill_recomendation.json", 'w') as file:
        json.dump(skills, file)

get_recommendations('Finance')