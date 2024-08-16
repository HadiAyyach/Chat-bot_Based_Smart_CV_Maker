import json
from gpt4all import GPT4All
from post_procesing import make_CV_txt, turn_to_lines
from make_docx import make_docx_CV

# opening the raw data
with open('raw_data.json', 'r') as file:
    raw_data = json.load(file)

# init the model 
model = GPT4All(model_name='mistral-7b-instruct-v0.1.Q4_0.gguf',model_path='A:/IUST/G PROJECT/chatbot/tamplet/models',allow_download=False)

# get each experience title 
with model.chat_session():
    response1 = model.generate(prompt="you are helping me to make a CV, so for every job experience I give, you will generate a job experience heading in the format '[job title] | [company name] | [date of work]'based on the information  with nothing more than that ,okay?", temp=0)
    for line in raw_data["experience"]:
        response2 = model.generate(prompt= line, temp=0)
    exp_tit = model.current_chat_session 
    
# optimize the experience
with model.chat_session():
    response1 = model.generate(prompt='you are helping me to make a CV, so for every job experience I give from now and on you will give me 3 lines that start with action verb, showing result and tasks, concise, impactful and quantified to write them in my CV and make sure to put them in a bulleted list with the name of the company,job title and date of working as a title,okay?', temp=0)
    for line in raw_data["experience"]:
        response2 = model.generate(prompt= line, temp=0)
    exp = model.current_chat_session
print("done optimizing the experience")

# optimize the education
with model.chat_session():
    response1 = model.generate(prompt='you are helping me to make a CV, so for every education details I give from now and on you will give me one line to write in my CV and make sure to put them in a bulleted list,okay?', temp=0)
    for line in raw_data["education"]:
        response2 = model.generate(prompt= line, temp=0)
    edu = model.current_chat_session
print("done optimizing the education")

# optimize the skills
with model.chat_session() as session :
    response1 = model.generate(prompt='you are helping me to make a CV, so I will give you all my skills and you will give them in an array with each skill individually in a better professional language and make sure to put them in a bulleted list, okay? ', temp=0)
    response = model.generate(prompt= raw_data["skills"], temp=0)
    skill = model.current_chat_session
print("done optimizing the skills")
    
# optimize the additional information
with model.chat_session():
    response1 = model.generate(prompt='you are helping me to make a CV, so i will give you my additional information and you will give me an array with the lines that i can add to my CV and make sure to put them in a bulleted list, okay?', temp=0)
    response2 = model.generate(prompt= raw_data["additional_info"], temp=0)
    add_info = model.current_chat_session
print("done optimizing the additional information")

# save the optimized information before sorting it 
optimized_data = {
    "experience_title": exp_tit,
    "experience":  exp,
    "education":  edu,
    "skills":  skill,
    "additional_info":  add_info
}
with open("optimized_unprocessed_data.json", 'w') as file:
    json.dump(optimized_data, file)

# make a txt CV
make_CV_txt(optimized_data)

# load the CV as a text 
with open("example.txt", "r") as file:
    text_content = file.read()

# generate a summary from the CV
with model.chat_session():
    response1 = model.generate(prompt='you are helping me to make a CV , so Based on the following information about my background and skills, please generate a 2-3 sentence professional summary that I can include at the top of my CV, okay?', temp=0)
    response2 = model.generate(prompt= text_content , temp=0)
    sum = model.current_chat_session
print("done generating the summary")

sum = turn_to_lines(sum)


with open('optimized_data_unfinished.json', 'r') as file:
    optimized_unfinished = json.load(file)


# save final information as json file
optimized_data = {
    "full_name": raw_data["full_name"],
    "email": raw_data["email"],
    "contact_info": raw_data["contact_info"],
    "experience":  optimized_unfinished["experience"],
    "education":  optimized_unfinished["education"],
    "skills":  optimized_unfinished["skills"],
    "additional_info":  optimized_unfinished["additional_info"],
    "summary": sum
}

with open("optimized_data.json", 'w') as file:
    json.dump(optimized_data, file)

# make_docx_CV(optimized_data)