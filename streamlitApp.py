import os
import json
import traceback
import pandas as pd

from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table

import streamlit as st
from src.mcqgenerator.mcqgenerator import generate_evaluation_chain
from src.mcqgenerator.logger import logging

# loading json file
with open('D:\\MCQ Generator Project\\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# creating title for the app
st.title("MCQ Creator Application with Langchain")

# create a form using st.form
with st.form("user_inputs"):
    # file uploaded
    uploaded_file = st.file_uploader("Upload a file")

    # input field
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    subject = st.text_input("Insert subject", max_chars=20)

    tone = st.text_input("Complexity level of the Question", max_chars=20, placeholder='Simple')

    button = st.form_submit_button('Create MCQs')

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading...."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluation_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    print(quiz)
                    if quiz is not None:
                        try:
                            table_data = get_table(quiz)
                            if table_data:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.table(df)
                                st.text_area(label="Review", value=response.get("review", ""))

                            else:
                                st.error("Error in the table data")

                        except Exception as e:
                            st.error(f"Error processing table data: {e}")
                            st.write(quiz)  # Debug output

                    else:
                        st.write(response)
                else:
                    st.error("Unexpected response format")
