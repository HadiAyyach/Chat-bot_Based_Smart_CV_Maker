import json
import re

# function that remove the start of the respond
def remove_until_star(input_string):
    if '*' in input_string:
        return input_string[input_string.index('*'):]
    elif ':' in input_string:
        output = input_string[input_string.index(':')+1:]
        match = re.search(r'"(.*?)"', output)
        if match:
            output = match.group(1)
        return output
    else :
        return input_string

# function that make an array of the responses
def turn_to_lines(input):
    
    lines = []
    for respond in input:
        if respond ["role"] != "user" :
            line = respond["content"]
            line = remove_until_star(line)
            lines.append(line)
    lines.pop(0)
    lines.pop(0)
    return lines

# function that make a txt CV 
def make_CV_txt(optimized_data):
    # cleaning the  data  
    exp_tit_lines = turn_to_lines(optimized_data["experience_title"])    
    exp_lines = turn_to_lines(optimized_data["experience"])  
    edu_lines = turn_to_lines(optimized_data["education"])
    skill_lines = turn_to_lines(optimized_data["skills"])
    add_info_lines = turn_to_lines(optimized_data["additional_info"])

    for i,v in enumerate(exp_tit_lines):
        exp_lines[i] = v +"\n\n" + exp_lines[i] 
    # save the cleaned data for future use
    optimized_data = {
        "experience":  exp_lines,
        "education":  edu_lines,
        "skills":  skill_lines,
        "additional_info":  add_info_lines
    }
    with open("optimized_data_unfinished.json", 'w') as file:
        json.dump(optimized_data, file)

    all =  [exp_lines, edu_lines, skill_lines, add_info_lines]
    titles = ["Experience : ", "Education : ", "Skills : ", "Additional information : "]
    
    # Open the file in write mode
    file = open("example.txt", "w")

    # Write some text to the file
    for index , value in enumerate(all):
        file.write(titles[index])
        file.write("\n")
        for i in value:
            file.write(i)
            file.write("\n")
        file.write("\n")
    file.close()
    print("the CV is ready as example.txt")


# with open('optimized_unprocessed_data.json', 'r') as file:
#     optimized_data = json.load(file)

    
# make_CV_txt(optimized_data)