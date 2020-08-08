from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import en_core_web_sm

nlp = en_core_web_sm.load()
app = FastAPI()


class Response(BaseModel):
    article_text: str = None


@app.post("/")
def main(input_data: Response):
    result = []
    if input_data.article_text:
        doc = nlp(input_data.article_text)
        for ent in doc.ents:
            result.append({"text": ent.text, "label": ent.label_})
    return result
