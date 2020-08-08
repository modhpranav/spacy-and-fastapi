from typing import List, Any
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
import en_core_web_sm, pytextrank
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


nlp = en_core_web_sm.load()
app = FastAPI()
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
templates = Jinja2Templates(directory="app/templates/")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def get(request: Request):
    return templates.TemplateResponse('dashboard.html', context={"request": request})

@app.post("/")
def post(request: Request, article: str = Form(...), operation: str = Form(...)):
    labels = []
    phrases = []
    error_message = None
    if article:
        doc = nlp(article)
        if operation == "label":
            for ent in doc.ents:
                labels.append({"text": ent.text, "label": ent.label_})
        else:
            phrases = list(filter(lambda x: len(str(x).split()) > 2, doc._.phrases))
    else:
        error_message = "Please try something else!"
    return templates.TemplateResponse("result.html", context={"request": request , "labels": labels, "phrases": phrases, "error_message": error_message})