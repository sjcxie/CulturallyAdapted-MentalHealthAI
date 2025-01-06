import os
import openai
from utils.constants import ENG_BASE_PROMPT, CHN_BASE_PROMPT, MI_EXAMPLES, ENG_CULTURAL_PROMPT, CHN_CULTURAL_PROMPT
from utils.tools import convert_csv_to_xlsx, traslate_to_chinese, traslate_to_english, create_log_file, log_conversation, import_data


# Constants
MODEL_NAME = "chinese prompt model"

MODEL_SELECTED = "gpt-4o"
TEMPERATURE_SELECTED = 0.5

# Configurations
openai.api_key = os.environ.get("OPENAI_API_KEY")


# Function to call the OpenAI API
def generate_response(user_input, system_prompt, model=MODEL_SELECTED, temperature=TEMPERATURE_SELECTED):
    conversation_history = [{"role": "system", "content": system_prompt}]
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=temperature, 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def chat_completions(chn_user_input, eng_user_input):

    try:
        # # english user input -> baseline response 
        assistant_reply_1 = generate_response(eng_user_input, system_prompt=ENG_BASE_PROMPT)
        # print(f"NO Cultural Prompt Response:\n {assistant_reply_1}\n")
        # assistant_reply_1 = ""

        # # english user input -> response with cultural prompting
        assistant_reply_2 = generate_response(eng_user_input, system_prompt=ENG_CULTURAL_PROMPT + ENG_BASE_PROMPT)
        # print(f"WITH Cultural Prompt Response:\n {assistant_reply_2}\n")
        # assistant_reply_2 = ""

        # chinese user input -> baseline response 
        assistant_reply_3 = generate_response(chn_user_input, system_prompt=CHN_BASE_PROMPT)
        # print(f"NO Cultural Prompt Response:\n {assistant_reply_3}\n")
        
        # chinese user input -> response with cultural prompting
        assistant_reply_4 = generate_response(chn_user_input, system_prompt=CHN_CULTURAL_PROMPT + CHN_BASE_PROMPT)
        # print(f"WITH Cultural Prompt Response:\n {assistant_reply_4}\n")

        log_conversation(log_filename, eng_user_input, chn_user_input, assistant_reply_1, assistant_reply_2, assistant_reply_3, assistant_reply_4)


    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # # Specify the file path
    input_data_file_path = "Example_inputs_data/Ricky_persona1_df.csv"
    df = import_data(input_data_file_path)
    trial_id, log_filename = create_log_file()
    for i in range(len(df['Entry'])):
        chn_user_prompt = df['Entry'][i]
        eng_user_prompt = traslate_to_english(chn_user_prompt)
        # eng_user_prompt = ""
        chat_completions(chn_user_prompt, eng_user_prompt)
    
    csv_file_path = log_filename
    xlsx_file_path = "conversation_logs/log_{}.xlsx".format(trial_id)
    convert_csv_to_xlsx(csv_file_path,xlsx_file_path)
    