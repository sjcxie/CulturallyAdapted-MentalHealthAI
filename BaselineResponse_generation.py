import os
import openai
from utils.constants import ENG_BASE_PROMPT, ENG_CULTURAL_PROMPT, CHN_BASE_PROMPT, CHN_CULTURAL_PROMPT
from utils.tools import create_log_file, log_conversation, import_xlsx_data, convert_csv_to_xlsx, traslate_to_chinese

# Constants
MODEL_SELECTED = "gpt-4o"
TEMPERATURE_SELECTED = 0.5
versions = ['EngInput', 'TranslatedChnInput', 'EngResponse','EngResponse_with_CulturalPrompt','TranslateChnResponse','DirectChnResponse','TranslateChnResponse_with_CulturalPrompt','DirectChnResponse_with_CulturalPrompt']

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

def completions_multiple(eng_user_input):
    '''
    This function will generate multiple versions of responses based on the english user input
    '''
    try:
        eng_response = generate_response(eng_user_input, system_prompt=ENG_BASE_PROMPT)
        eng_response_w_cultural = generate_response(eng_user_input, system_prompt=ENG_CULTURAL_PROMPT+ENG_BASE_PROMPT)
        translated_chn_input = traslate_to_chinese(eng_user_input)
        translated_chn_response = traslate_to_chinese(eng_response)
        direct_chn_response = generate_response(translated_chn_input, system_prompt=CHN_BASE_PROMPT)
        translated_chn_response_w_cultural = traslate_to_chinese(eng_response_w_cultural)
        direct_chn_response_w_cultural = generate_response(translated_chn_input, system_prompt=CHN_CULTURAL_PROMPT + CHN_BASE_PROMPT)

        responses_list = [eng_user_input, translated_chn_input, eng_response, eng_response_w_cultural, translated_chn_response, direct_chn_response, translated_chn_response_w_cultural, direct_chn_response_w_cultural]

        log_conversation(log_filename, responses_list)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # import user input data
    data_file_path = "Example_inputs_data/Diary_data_eng_1_cleaned.xlsx"
    df = import_xlsx_data(data_file_path)
    
    # start log file
    log_filename = create_log_file(versions)
    # generate responses
    for i in range(df.shape[0]):
        completions_multiple(df['event'][i])
    
    csv_file_path = log_filename
    xlsx_file_path = "{}.xlsx".format(log_filename)
    convert_csv_to_xlsx(csv_file_path,xlsx_file_path)