from typing import List, Any
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
import en_core_web_md, pytextrank
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from string import punctuation


nlp = en_core_web_md.load()
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
    keywords = []
    error_message = None
    if article:
        doc = nlp(article)
        if operation == "label":
            for ent in doc.ents:
                labels.append({"text": ent.text, "label": ent.label_})
        elif operation == "keywords":
            keywords = get_hotwords(article)
        else:
            phrases = list(filter(lambda x: len(str(x).split()) > 2, doc._.phrases))
    else:
        error_message = "Please try something else!"
    return templates.TemplateResponse("result.html", context={"request": request , "labels": labels, "phrases": phrases, "keywords": keywords, "article": article, "error_message": error_message})


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))