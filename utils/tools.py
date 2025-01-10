import openai
import os
from datetime import datetime
import csv
import pandas as pd

# Constants

MODEL_NAME = "EngChnReponses"
MODEL_SELECTED = "gpt-4o-mini"
TEMPERATURE_SELECTED = 0.5
LOG_DIRECTORY = "./conversation_logs"

# Configurations
openai.api_key = os.environ.get("OPENAI_API_KEY")

def traslate_to_chinese(eng_response, model=MODEL_SELECTED, temperature=TEMPERATURE_SELECTED):
    try:
        chn_response = openai.chat.completions.create(
            model=model,
            messages=[{
                "role": "user", 
                "content": "Translate the following text into Chinese:" + eng_response}],
            temperature=temperature, 
        )
        return chn_response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def traslate_to_english(chn_response, model=MODEL_SELECTED, temperature=TEMPERATURE_SELECTED):
    try:
        eng_response = openai.chat.completions.create(
            model=model,
            messages=[{
                "role": "user", 
                "content": "Translate the following text into English:" + chn_response}],
            temperature=temperature, 
        )
        return eng_response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def create_log_file(list_versions):
    """Creates a new log file for the conversation."""
    # TRIAL_ID = input("Trial ID is: ")
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    # log_filename = os.path.join(
    #     LOG_DIRECTORY, f"log_{MODEL_NAME}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    # )
    log_filename = os.path.join(
        LOG_DIRECTORY, f"log_{MODEL_NAME}_{datetime.now().strftime('%m%d_%H%M')}.csv"
    )
    # log_filename = os.path.join(
    #     LOG_DIRECTORY, f"log_{TRIAL_ID}.csv"
    # )
    with open(log_filename, mode="w", newline="", encoding="utf-8") as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(list_versions)

    return log_filename

def log_conversation(log_filename, generated_responses):
    """Logs a conversation turn to the specified log file."""
    # eng_user_input, chn_user_input, assistant_reply_1, assistant_reply_2, assistant_reply_3, assistant_reply_4
    with open(log_filename, mode="a", newline="", encoding="utf-8") as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(generated_responses)



def import_doc_data(file_path):

    # Read the file content
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Process the lines: remove empty lines and strip extra spaces
    entries = [line.strip() for line in lines if line.strip()]

    # Create a pandas DataFrame
    df = pd.DataFrame(entries, columns=["Entry"])

    return df


def import_xlsx_data(file_path):
    df = pd.read_excel(file_path, header=0)
    return df


# Function to convert CSV to XLSX
def convert_csv_to_xlsx(csv_file_path, xlsx_file_path):
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path, encoding="utf-8")
        
        # Save the DataFrame as an XLSX file
        df.to_excel(xlsx_file_path, index=False)
        print(f"CSV file has been successfully converted to XLSX and saved as '{xlsx_file_path}'.")
    except FileNotFoundError:
        print(f"The file '{csv_file_path}' does not exist. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")