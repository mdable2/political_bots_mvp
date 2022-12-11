import pickle
from typing import List, Set
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import numpy as np
import dotmap
from transformers import (
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from sentence_transformers import SentenceTransformer, util
from common import logging
from common.data_models import TranscriptObject, TranscriptPage
import __main__

__main__.TranscriptPage = TranscriptPage
__main__.TranscriptObject = TranscriptObject

app = FastAPI()
origins = [
    'http://localhost:3000',
    'localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

biden_model = None
trump_model = None
tokenizer = None
args = dotmap.DotMap()
args.biden_model_name_or_path = "./models/biden_80000"
args.trump_model_name_or_path = "./models/trump_70000"
args.prompt = ''
args.padding_text = ''
args.length = 128
args.num_samples = 1
args.temperature = 1
args.num_beams = 5
args.repetition_penalty = 1
args.top_k = 0
args.top_p = 0.5
args.no_cuda = False
args.seed = 2022
args.stop_token = '<|endoftext|>'
args.n_gpu = 1
args.device = 'cuda:0'

class ChatQuery(BaseModel):
    person: str
    query: str

class ExplainabilityObject(BaseModel):
    location: str
    text: str

class ChatResponse(BaseModel):
    response: str
    explainability: List[ExplainabilityObject]

try:
    logging.log("Biden model loading.")
    biden_config = AutoConfig.from_pretrained(args.biden_model_name_or_path)
    biden_model = AutoModelForSeq2SeqLM.from_pretrained(
            args.biden_model_name_or_path,
            from_tf=bool(".ckpt" in args.model_name_or_path),
            config=biden_config,
            )
    biden_model = biden_model.to(args.device)
    biden_tokenizer = AutoTokenizer.from_pretrained(
            args.biden_model_name_or_path, use_fast=not args.use_slow_tokenizer)
    logging.log("Biden model loaded.")

    logging.log("Trump model loading.")
    trump_config = AutoConfig.from_pretrained(args.trump_model_name_or_path)
    trump_model = AutoModelForSeq2SeqLM.from_pretrained(
            args.trump_model_name_or_path,
            from_tf=bool(".ckpt" in args.model_name_or_path),
            config=trump_config,
            )
    trump_model = trump_model.to(args.device)
    trump_tokenizer = AutoTokenizer.from_pretrained(
            args.trump_model_name_or_path, use_fast=not args.use_slow_tokenizer)
    logging.log("Trump model loaded.")

    logging.log("Trump transcripts loading.")
    with open('./data/trump_transcripts.pkl', 'rb') as f:
        trump_data: List[TranscriptPage] = pickle.load(f)

    trump_convo_texts = []
    trump_convo_speeches = []

    for data in trump_data:
        for objs in data.transcript_objects:
            if len(objs.keywords) > 0 and objs.speaker == "Donald Trump":
                trump_convo_texts.append(objs.text)
                trump_convo_speeches.append(data.title)
    keywords = set()

    for data in trump_data:
        for kw in data.keywords:
            keywords.add(kw)
    logging.log("Trump transcripts loaded.")

    logging.log("Biden transcripts loading.")
    with open("./data/biden_transcripts.pkl", "rb") as f:
        biden_data: List[TranscriptPage] = pickle.load(f)

    biden_convo_texts = []
    biden_convo_speeches = []
    for transcript_page in biden_data:
        for transcript_object in transcript_page.transcript_objects:
            for word in transcript_object.text.split(" "):
                if word in keywords:
                    transcript_page.keywords.add(word)
                    transcript_object.keywords.add(word)
    for data in biden_data:
        for objs in data.transcript_objects:
            if len(objs.keywords) > 0 and objs.speaker == "Joe Biden":
                biden_convo_texts.append(objs.text)
                biden_convo_speeches.append(data.title)
    logging.log("Biden transcripts loaded.")

    logging.log("Creating embeddings.")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    trump_embeddings = model.encode(trump_convo_texts, convert_to_tensor=True)
    biden_embeddings = model.encode(biden_convo_texts, convert_to_tensor=True)
    logging.log("Embeddings are done.")

    logging.log("Good to start chatting...")
except Exception as e:
    logging.error(e)

@app.get("/health")
def health() -> str:
    return {"health": "Service is online!"}

@app.post("/chat")
def chat(chat_query: ChatQuery) -> ChatResponse:
    logging.log(f"Got new request! {chat_query.person} | {chat_query.query}")
    explainability_objects = []
    gen_kwargs = {
        # 'num_beams': args.num_beams,
        'max_length': args.length,
        'min_length': 32,
        'top_k': 10,
        'no_repeat_ngram_size': 4

    }
    if chat_query.person == "Biden":
        input_ids = biden_tokenizer(chat_query.query + ' <|knowledge|> ' + "" +
                          ' =>', return_tensors="pt").input_ids.to(args.device)
        output_sequences = biden_model.generate(input_ids, **gen_kwargs)
        output_sequences = biden_tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
        query = model.encode([chat_query.query], convert_to_tensor=True)
        cosine_scores = util.cos_sim(biden_embeddings, query)
        indexes = torch.topk(cosine_scores.flatten(), 5).indices
        for index in indexes:
            loc = biden_convo_speeches[index]
            txt = biden_convo_texts[index]
            explainability_objects.append(ExplainabilityObject(location=loc, text=txt))
    elif chat_query.person == "Trump":
        input_ids = trump_tokenizer(chat_query.query + ' <|knowledge|> ' + "" +
                          ' =>', return_tensors="pt").input_ids.to(args.device)
        output_sequences = trump_model.generate(input_ids, **gen_kwargs)
        output_sequences = trump_tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
        query = model.encode([chat_query.query], convert_to_tensor=True)
        cosine_scores = util.cos_sim(trump_embeddings, query)
        indexes = torch.topk(cosine_scores.flatten(), 5).indices
        for index in indexes:
            loc = trump_convo_speeches[index]
            txt = trump_convo_texts[index]
            explainability_objects.append(ExplainabilityObject(location=loc, text=txt))

    return ChatResponse(response=output_sequences[0], explainability=explainability_objects)