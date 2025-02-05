import os

from dotenv import dotenv_values

from gpyt.free_assistant import FreeAssistant
from gpyt.palm_assistant import PalmAssistant
from gpyt.lite_assistant import LiteAssistant

from .app import gpyt
from .args import USE_EXPERIMENTAL_FREE_MODEL
from .assistant import Assistant
from .config import MODEL, PROMPT


# check for environment variable first
API_KEY = os.getenv("OPENAI_API_KEY")
PALM_API_KEY = os.getenv("PALM_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
DOTENV_PATH = os.path.expanduser("~/.env")

if API_KEY is None or (isinstance(API_KEY, str) and not len(API_KEY)):
    result = dotenv_values(DOTENV_PATH)
    API_KEY = result.get("OPENAI_API_KEY", None)
    PALM_API_KEY = result.get("PALM_API_KEY", None)
    ANTHROPIC_API_KEY = result.get("ANTHROPIC_API_KEY", None)
    COHERE_API_KEY = result.get("COHERE_API_KEY", None)
    REPLICATE_API_KEY = result.get("REPLICATE_API_KEY", None)


assert (
    API_KEY is not None and len(API_KEY)
) or USE_EXPERIMENTAL_FREE_MODEL, """

❗Missing OpenAI API Key ❗

Steps to fix this issue:

    1) Get an OpenAI Key from https://platform.openai.com/account/api-keys
    2) Create a `.env` file located in your $HOME directory.
    3) add `OPENAI_API_KEY="your_api_key"` to the `.env` file.
    4) or, you can run `$ EXPORT OPENAI_API_KEY="your_api_key"` to set a key
    for the active shell session.
    5) rerun this program with `$ gpyt` or `$ python -m gpyt`

💡 OR 💡

Use the new **experimental** free model feature.

$ gpyt --free

💭 This may break sometimes and is often times slower. It is recommended to
generate your own OpenAI API key (see above)

"""
model_keys = {}
if ANTHROPIC_API_KEY:
    model_keys["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
if COHERE_API_KEY:
    model_keys["COHERE_API_KEY"] = COHERE_API_KEY
if REPLICATE_API_KEY:
    model_keys["REPLICATE_API_KEY"] = REPLICATE_API_KEY

gpt = Assistant(api_key=API_KEY or "", model=MODEL, prompt=PROMPT)
gpt4 = Assistant(api_key=API_KEY or "", model="gpt-4", prompt=PROMPT)
free_gpt = FreeAssistant()
palm = PalmAssistant(api_key=PALM_API_KEY)
litellm = LiteAssistant(model_keys=model_keys, model=MODEL, prompt=PROMPT)
app = gpyt(assistant=gpt, free_assistant=free_gpt, palm=palm, gpt4=gpt4, lite_assistant = litellm)
