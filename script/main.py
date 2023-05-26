import os
import openai
import asyncio
import whisper
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from script.utils.instructions import instructions
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from script.utils.pushover import Client

# Import the logging module
import logging

# Configure logging settings
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Add a log message at the beginning of the script
logging.info("Starting the application")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


pushover_client = Client(user_key=os.getenv(
    "PUSHOVER_USER_KEY"), api_token=os.getenv("PUSHOVER_API_TOKEN"))


app = FastAPI()
data_folder = os.path.dirname(os.path.abspath(__file__))
tmp_folder = os.path.join(data_folder, "user_data/tmp")
out_folder = os.path.join(data_folder, "user_data/transcriptions")
out_fixed_folder = os.path.join(data_folder, "user_data/gpted")

# Check if directories exist, create them if not
for folder in [tmp_folder, out_folder, out_fixed_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

user = 'brt-'
security = HTTPBasic()
templates_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)
static_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("USERNAME")
    correct_password = os.getenv("PASSWORD")
    if not (credentials.username == correct_username and credentials.password == correct_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return True


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request, secure: bool = Depends(auth)):
    gpted_files = sorted(os.listdir(out_fixed_folder), reverse=True)
    gpted_data = [{"filename": file, "content": open(os.path.join(
        out_fixed_folder, file)).read()} for file in gpted_files]
    return templates.TemplateResponse("index.html", {"request": request, "gpted_data": gpted_data})


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "audio/x-m4a":
        return {"error": "Only m4a recordings are supported"}

    os.makedirs(tmp_folder, exist_ok=True)
    file_name = f"{user}{datetime.now().strftime('%Y%m%d%H%M%S')}.m4a"

    if os.path.exists(os.path.join(tmp_folder, file_name)):
        return {"error": "File already exists"}

    with open(os.path.join(tmp_folder, file_name), "wb") as f:
        f.write(await file.read())

    asyncio.create_task(transcribe_background(file_name))
    return True


async def transcribe_background(file):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, transcribe, file)


def transcribe(file_name):
    model = whisper.load_model("small")
    content = os.path.join(tmp_folder, file_name)
    transcript_text = model.transcribe(content)['text']
    chat = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
    messages = [SystemMessage(content=instructions),
                HumanMessage(content=transcript_text)]
    reply = chat(messages)
    pushover_client.send_message("Done!")

    os.makedirs(out_folder, exist_ok=True)
    os.makedirs(out_fixed_folder, exist_ok=True)

    with open(os.path.join(out_folder, file_name.split('.')[0] + ".md"), "w") as f:
        f.write(transcript_text)

    with open(os.path.join(out_fixed_folder, file_name.split('.')[0] + ".md"), "w") as f:
        f.write(reply.content)
