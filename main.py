
import nltk

from fastapi import FastAPI, Query


from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List

from typing import Optional

from ParaphrasationModule import DefaultParaphrasationAlgorithm, Rephraser

DefaultMethod = DefaultParaphrasationAlgorithm()
Rephraser = Rephraser()

app = FastAPI()




@app.get("/paraphrase")
def paraphrase(tree: str = Query(..., min_length=2), limit: Optional[int] = Query(20, gt=0)):
    t = nltk.Tree.fromstring(tree)

    Rephraser.SetLimit(limit)
    Rephraser.SetParaphrasationMethod(DefaultMethod)
    res: List[nltk.Tree] = Rephraser.ExecuteMethod(t)

    paraphrases = [{"tree": str(el)} for el in res]
    to_json = {"paraphrases": paraphrases}

    json_data = jsonable_encoder(to_json)

    return JSONResponse(content=json_data)
