from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Union, Optional

# import pydantic import BaseModel
import pandas as pd

import re

# from plotify_model.interface.main import preprocess_features
from ml_logic.registry import build_pipeline
from interface.main import generate_summary

app = FastAPI()
# download model
app.state.model = build_pipeline()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/generate_summary")
def generate_summary(
    genre: str = "",
    prompt: str = "", # for optional params
    max_length: int = 10
):
    """
    we use type hinting to indicate the data types expected
    for the parameters of the function
    FastAPI uses this information in order to hand errors
    to the developpers providing incompatible parameters
    FastAPI also provides variables of the expected data type to use
    without type hinting we need to manually convert
    the parameters of the functions which are all received as strings
    """
    # genre = f"<|{genre}|>" if genre else None
    # lead_sequence = genre + prompt if prompt else genre
    # output = app.state.model(lead_sequence, max_length=max_length)


    # Trim white space from both ends of each
    prompt = prompt.strip()
    genre = genre.strip()

    if genre:
        genre = f"<|{genre}|>"

    # Trim unwanted white space
    lead_sequence = " ".join([genre, prompt]).strip()

    # Generate sequence
    output = app.state.model(lead_sequence, max_length=max_length)
    output = output[0]['generated_text']
    # print('type(output)', type(output[0]['generated_text']))
    # Trim output to last occurance of full stop (if any)
    pos = output.rfind(".") # find position of last full stop
    output = output[:pos+1] if pos != -1 else output

    # Trim token
    pos = output.rfind(">") # find position of first >
    output = output[pos+1:] if pos != -1 else output
    output= output.strip()

    # Deal with occurences of floating letters
    output = output.replace(" s ", "'s ")
    output = output.replace(" t ", "'t ")
    output = output.replace(" ve ", "'ve ")
    output = output.replace(" nt ", "'nt ")
    output = output.replace(" re ", "'re ")

    # Remove space (from Sarah. Orig punct list: ?.!,")
    output = re.sub(r'\s([!?.,;-](?:\s|$))', r'\1', output)

    output = [{'generated_text':output}]

    return {
        'generate_summary': output
    }

@app.get("/")
def root():
    return {
        'greeting': 'Hello'
    }
