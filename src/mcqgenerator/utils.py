import os
import PyPDF2
import traceback


def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception('Error while reading PDF file')
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception('File type not supported')
    

def get_table(quiz):
    try:
        # Parse the questions, choices, and answers
        questions = []
        choices = []
        answers = []

        lines = quiz.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and line[0].isdigit():
                question = line.split(':')[0].strip()
                choice = ""
                i += 1
                while i < len(lines) and lines[i].strip().startswith("*"):
                    choice += lines[i].strip() + " | "
                    i += 1
                questions.append(question)
                choices.append(choice.strip(" | "))
            else:
                i += 1

        # Parse the answers
        if "The answers are:" in lines:
            answers_section = lines.index("The correct answers are:") + 1
            for line in lines[answers_section:]:
                if line.strip():
                    q_num, answer = line.strip().split(". ")
                    answers.append(answer)
        else:
            raise ValueError("'The answers are:' section not found in the text")

        questions = questions[:5]
        choices = choices[:5]

        data = {
            "MCQ": questions,
            "Choices": choices,
            "Answers": answers
        }

        return data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
