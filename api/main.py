import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import string
import pandas as pd
import numpy as np
from fastapi import FastAPI
import json
import re
app = FastAPI()
con = sqlite3.connect('api/data/db.sqlite')
cur = con.cursor()

# config api
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://146.190.89.237",
    "http://192.168.1.10",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# load file result

subfields = ['SE', 'MM', 'CN']
labels = pd.read_json('api/data/label.json')


#
@app.get('/api')
async def base():
    return {"message": "oksiap"}


def query_db(query, args=(), one=False):
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    # cur.connection.close()
    return (r[0] if r else None) if one else r


@app.get('/api/classify-result')
async def read_rows(subfield, year: int, topic):
    topics = labels[labels['prefix'] == subfield]
    if topic == '1':
        topic_casted = topics.iloc[0]['code']
    else:
        topic_casted = topic

    docs = query_db(
        f"SELECT * FROM {subfield} WHERE {topic_casted} =1 AND year = {year}")
    if(len(docs) > 0):
        res = {
            "available_topics": json.loads(topics.to_json(orient="records")),
            "theses": json.loads(json.dumps(docs)),
            "chart": json.loads(pd.DataFrame(docs)[list(topics['code'])].sum().to_json()),
        }
    else:
        res = {
            "available_topics": json.loads(topics.to_json(orient="records")),
            "theses": [],
            "chart": [],
        }

    return {
        "message": "Load Classify Result",
        "status": "OK",
        "status_code": 200,
        "query": {"subfield": subfield, "year": year, "topic": topic_casted},
        "data": res,
    }


@app.get('/api/summary-result')
async def read_summary(subfield):
    topics = list(labels[labels['prefix'] == subfield]['code'])
    attr = ','.join([str(elem) for elem in topics])
    docs = query_db(
        f"SELECT {attr},year FROM {subfield} WHERE subfield = '{subfield}'")
    df_sum = pd.DataFrame(docs)

    # calclate best topic per year
    df_group = df_sum.groupby('year').sum(topics)
    df_top = df_group.idxmax(axis=1).reset_index(name='topic')
    df_top['total'] = df_group.max(axis=1).reset_index(name='total')['total']

    return {
        "message": "Load Summary Result",
        "status": "OK",
        "status_code": 200,
        "query": {"subfield": subfield, },
        "data": {
            "chart": json.loads(df_sum.groupby('year').sum().to_json()),
            "best_topic": json.loads(df_top.to_json(orient="records"))
        },
    }


@app.get('/api/thesis-detail')
async def read_theses(eprintid, subfield):
    doc = query_db(
        f"SELECT * FROM {subfield} WHERE eprintid = {eprintid}", one=True)
    
    # parsing multi label into array of multi label value
    topics: pd.DataFrame = labels[labels['prefix'] == subfield]
    l = []
    for k in doc:
        if(re.match(f'{subfield}_', k) and doc[k] == 1):
            l.append(k)
    doc['labels'] = list(topics[topics['code'].isin(l)]['name'])
    
    # parsing creators name into string
    c: str = doc['creators']
    c: str = re.sub('None', '"-"', c)
    doc['creators'] = " ".join(re.findall("[A-Z]\w+", c))

    return {
        "message": "Load Summary Result",
        "status": "OK",
        "status_code": 200,
        "query": {"subfield": subfield, },
        "data": json.loads(json.dumps(doc)),
    }
