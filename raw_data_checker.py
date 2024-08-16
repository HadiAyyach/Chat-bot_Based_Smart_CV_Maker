import json
from transformers import pipeline
def question_answering(data , Questions) :
    model_name = "deepset/roberta-base-squad2"
    model = pipeline('question-answering', model=model_name, tokenizer=model_name)

    all_results = []
    for i in data :  
        scores = []
        answers = []
        for question in Questions :
            input = {
                    'question': question,
                    'context': i }
            output = model(input)
            scores.append(output['score'])
            answers.append(output['answer'])
        result = {"scores": scores,
            "answers": answers}
        all_results.append(result) 
    return all_results

# this function make a json file with the answer and scores 
def get_answers():
    # opening the raw data
    with open('raw_data.json', 'r') as file:
        raw_data = json.load(file)
        
    # opening the questions
    with open('questions.json', 'r') as file:
        questions_data = json.load(file)
    
    # getting the answers from the function
    edu = question_answering(raw_data['education'],questions_data['education'])
    exp = question_answering(raw_data['experience'],questions_data['experience'])

    # initialize some variables
    edu_number = len(raw_data['education'])
    exp_number = len(raw_data['experience'])
    exps_data = [] 
    edus_data = [] 

    # a loop for the education questions and making the json data
    for j in range(edu_number):
        edu_data =[]
        for i,v in enumerate(edu[j]['scores']):
            edu_data.append({
                'info': questions_data['edu_info'][i],
                'question': questions_data['education'][i],
                'answer': edu[j]['answers'][i],
                'score': edu[j]['scores'][i]
            })
        edus_data.append(edu_data)
        
    # a loop for the experience questions and making the json data
    for j in range(exp_number):  
        exp_data =[]
        for i,v in enumerate(exp[j]['scores']):
            exp_data.append({
                'info': questions_data['exp_info'][i],
                'question': questions_data['experience'][i],
                'answer': exp[j]['answers'][i],
                'score': exp[j]['scores'][i]
            })
        exps_data.append(exp_data)
        
    # put it as one map
    new_data = {
            'education': edus_data ,
            'experience': exps_data 
            }

    # Write dictionary data to a new JSON file
    with open("question&answer_data.json", 'w') as file:
        json.dump(new_data, file)

def check_raw_data():
    get_answers()
    with open('question&answer_data.json', 'r') as file:
        check_file = json.load(file)

    edu = []
    for education in check_file['education']:
        sup_temp =""
        for question in education:
            if question['score'] < 0.0001 :
                sup_temp += " make sure the " + question['info'] + " included \n" 
        if sup_temp == "":
            sup_temp = "looking good"
        edu.append(sup_temp)      

    exp = []
    for experience in check_file['experience']:
        sup_temp =""
        for question in experience:
            if question['score'] < 0.004 :
                sup_temp += " make sure the " + question['info'] + " included \n"
        if sup_temp == "":
            sup_temp = "looking good"
        exp.append(sup_temp)

    result = {
    "education": exp,  
    "experience": edu,
    }

    with open("raw_data_checker.json", 'w') as file:
        json.dump(result, file)


check_raw_data()







