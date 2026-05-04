# import os
# import random
# import datetime
# import re
# # import google.generativeai as genai
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# # Client and Model initialization
# client = genai.Client(api_key=os.getenv("API_KEY"))
# MODEL_ID = "gemini-2.5-flash"

# # for m in client.models.list():
# #     print(m.name)

# OPERATIONS = {
#     "add": (["add", "sum", "+"], lambda x, y: x + y, "sum"),
#     "sub": (["subtract", "minus", "-"], lambda x, y: x - y, "difference"),
#     "mul": (["multiply", "*", "x"], lambda x, y: x * y, "product"),
#     "div": (["divide", "/"], lambda x, y: x / y if y != 0 else "Error: Division by zero", "quotient"),
# }

# def get_numbers(text, count=2):
#     nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
#     return nums[:count]

# def handle_gemini(prompt):
#     try:
#         # Updated method call for the new SDK
#         response = client.models.generate_content(
#             model=MODEL_ID,
#             contents=prompt
#         )
#         return response.text
#     except Exception as e:
#         return f"Error connecting to Gemini: {e}"

# def process_request(prompt):
#     prompt_lower = prompt.lower()

#     # Math Check
#     for key, (keywords, func, label) in OPERATIONS.items():
#         if any(word in prompt_lower for word in keywords):
#             nums = get_numbers(prompt_lower)
#             if len(nums) >= 2:
#                 return f"The {label} is: {func(nums[0], nums[1])}"

#     # Utility Checks
#     if any(w in prompt_lower for w in ["toss", "flip"]):
#         result = random.choice(["heads", "tails"])
#         print(f"The coin landed on: {result.upper()}!")
#         if 'heads' in result:
#             return "You win!"
#         if 'tails' in result:
#             return "You lose!"
               
#     if any(w in prompt_lower for w in ["roll", "dice"]):
#         result = random.randint(1, 6)
#         print(f"You rolled a {result} on the dice!")
#         if result >= 4:
#             return "You win!"
#         else:
#             return "You lose!"
            
            
#     if any(w in prompt_lower for w in ["date", "time", "now"]):
#         if "date" in prompt_lower and "time" in prompt_lower:            
#             return f"Current Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#         elif "date" in prompt_lower:
#             return f"Today's Date: {datetime.datetime.now().strftime('%Y-%m-%d')}"
#         elif "time" in prompt_lower:
#             return f"Current Time: {datetime.datetime.now().strftime('%H:%M:%S')}"

#     # Fallback to Gemini
#     return handle_gemini(prompt)



from email.mime import text
from multiprocessing import context
import os
import random
import datetime
import re
from google import genai
from dotenv import load_dotenv
import ollama # New import for Ollama

load_dotenv()

# Client and Model initialization for Gemini
client = genai.Client(api_key=os.getenv("API_KEY"))
GEMINI_MODEL_ID = "gemini-2.5-flash" # Renamed for clarity

# Ollama Model Initialization
OLLAMA_MODEL_ID = "llama3.2:1b" # Using 'llama3.2:1b' as a common variant for 'llama3.2:1b'
                             # User might need to pull this model first: ollama pull llama3.2:1b

OPERATIONS = {
    "add": (["add", "sum",'plus' "+"], lambda x, y: x + y, "sum"),
    "sub": (["subtract", "minus",'difference', "-"], lambda x, y: x - y, "difference"),
    "mul": (["multiply",'product', "*", "x"], lambda x, y: x * y, "product"),
    "div": (["divide",'quotient', "/"], lambda x, y: x / y if y != 0 else "Error: Division by zero", "quotient"),
}


def get_numbers(text, count=2):
    nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
    return nums[:count]

def handle_gemini(prompt):
    try:
        # Updated method call for the new SDK
        response = client.models.generate_content(
            model=GEMINI_MODEL_ID, # Use GEMINI_MODEL_ID
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {e}"




# New function for Ollama
def handle_ollama(prompt, model_id=OLLAMA_MODEL_ID):
    try:
        response = ollama.generate(model=model_id, prompt=prompt)
        return response['response']
    except Exception as e:
        return f"Error connecting to Ollama: {e}. Make sure Ollama server is running and model '{model_id}' is pulled."
    
s = [] 
info = {} # This will store extracted personal information for context
    
def process_request(prompt, llm_provider="ollama"): # Added llm_provider argument
    
    global info,s  # Declare as global to modify the outer variables
    storage_limit = 25  # Limit the number of past interactions stored in memory
    words_to_ignore = list(OPERATIONS.keys()) + ['date', 'time', 'now', 'toss', 'flip','roll','dice']  # Utility and math keywords to ignore
    prompt_lower = prompt.lower()
    
    if not any(word in prompt_lower for word in words_to_ignore):  # Only store prompts that are not utility or math related
        if len(s) >= storage_limit:  # Check if we exceed the storage limit
            s.pop(0)  # Remove the oldest entry

    if any(word in prompt_lower for word in ["name",'location', "phone", "email"]):  # Check for personal information keywords
        if "my name is" in prompt_lower:
            info['name'] = prompt_lower.split("my name is")[-1].strip()
        if "my location is" in prompt_lower:
            info['location'] = prompt_lower.split("my location is")[-1].strip()
        if "my phone no is" in prompt_lower:
            info['phone_no'] = prompt_lower.split("my phone no is")[-1].strip()
        if "my email id is" in prompt_lower:
            info['email_id'] = prompt_lower.split("my email id is")[-1].strip()

        print(f"Personal Information Updated: {info}")  # Debug print to show extracted personal information
        s.append(prompt_lower)  # Add the current prompt to memory
        print(f"Memory Updated: {s}")  # Debug print to show current memory

        regex = r'(what is|what\'s|tell me|show|give me|print) my (name|location|phone_no|email_id)\??'
        match = re.search(regex, prompt_lower)
        
        if match:
            field = match.group(2) # Extract the requested field (name, location, phone_no, or email_id)
            return f"Your {field} is: {info.get(field, 'not provided')}"
            
    # Math Check
    for key, (keywords, func, label) in OPERATIONS.items():
        if any(word in prompt_lower for word in keywords):
            nums = get_numbers(prompt_lower)
            if len(nums) >= 2:
                return f"The {label} is: {func(nums[0], nums[1])}"

    # Utility Checks
    if any(w in prompt_lower for w in ["toss", "flip"]):
        result = random.choice(["heads", "tails"])
        print(f"The coin landed on: {result.upper()}!")
        if 'heads' in result:
            return "You win!"
        if 'tails' in result:
            return "You lose!"
               
    if any(w in prompt_lower for w in ["roll", "dice"]):
        result = random.randint(1, 6)
        print(f"You rolled a {result} on the dice!")
        if result >= 4:
            return "You win!"
        else:
            return "You lose!"
            
            
    if any(w in prompt_lower for w in ["date", "time", "now"]):
        if "date" in prompt_lower and "time" in prompt_lower:            
            return f"Current Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif "date" in prompt_lower:
            return f"Today's Date: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        elif "time" in prompt_lower:
            return f"Current Time: {datetime.datetime.now().strftime('%H:%M:%S')}"

    # Fallback to chosen LLM
    if llm_provider == "gemini":
        return handle_gemini(prompt)
    elif llm_provider == "ollama":
        return handle_ollama(prompt)
    else:
        return "Invalid LLM provider specified. Choose 'gemini' or 'ollama'."

