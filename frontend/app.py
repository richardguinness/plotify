import streamlit as st
from PIL import Image
from style import get_css
import requests
import yake
from io import BytesIO
import re

import replicate
from dotenv import load_dotenv, find_dotenv
import os

envpath = find_dotenv()
load_dotenv(envpath)

API_HOST = os.environ.get('API_HOST')
API_PORT = os.environ.get('API_PORT')
API_ENDPOINT = os.environ.get('API_ENDPOINT')

api_endpoint = f'http://{API_HOST}:{API_PORT}/{API_ENDPOINT}'


# function to return text keywords
def get_keywords(text):
    """
    Extracts keywords from text
    """
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.25
    numOfKeywords = 7
    custom_kw_extractor = yake.KeywordExtractor(
            lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
            top=numOfKeywords, features=None, stopwords=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    keyword_list = [x[0] for x in keywords]

    return keyword_list


def get_text_api():

    param = {
            'genre': input_genre,
            'prompt': input_prompt,
            'max_length': 40
            }

    output = requests.get(api_endpoint, params=param).json()
    output = output['generate_summary'][0]['generated_text']

    # Trim output to last occurance of full stop (if any)
    pos = output.rfind(".")  # find position of last full stop
    output = output[:pos+1] if pos != -1 else output

    # Trim token
    pos = output.rfind(">")  # find position of first >
    output = output[pos+1:] if pos != -1 else output
    output = output.strip()

    # Deal with occurences of floating letters
    output = output.replace(" s ", "'s ")
    output = output.replace(" t ", "'t ")
    output = output.replace(" ll ", "'ll ")
    output = output.replace(" ve ", "'ve ")
    output = output.replace(" nt ", "'nt ")
    output = output.replace(" re ", "'re ")

    # Remove space (from Sarah. Orig punct list: ?.!,")
    output = re.sub(r'\s([!?.,;-](?:\s|$))', r'\1', output)

    return output


# function to display images
def display_image(image_url):
    # Make a GET request to the URL to retrieve the image data
    response = requests.get(image_url[0])

    # Create an image object from the image data
    image = Image.open(BytesIO(response.content))

    # Display the image
    #   print('display image works')
    return image


def get_image_api(prompt):
    prompt = f'{output_topics}, realistic, digital illustration, no text'
    envpath = find_dotenv()
    load_dotenv(envpath)
    replicate.Client()
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get(
            "0827b64897df7b6e8c04625167bbb275b9db0f14ab09e2454b9824141963c966"
            )
    image_url = version.predict(prompt=prompt)
    print(image_url)
    print(image_url[0])
    return image_url

# SITE CONFIG


# set the config for the page. App themes in .streamlit/config.toml
st.set_page_config(
            page_title="Plotify - create your story",
            page_icon="streamlit_assets/plotify_logo_small.png",
            layout="wide",  # wide
            initial_sidebar_state="expanded")  # collapsed

st.markdown(get_css(), unsafe_allow_html=True)

# SIDEBAR

# Assets: Logo + headertext(plotify - create your story)
with st.sidebar.container():
    image = Image.open("streamlit_assets/plotify_logocomplete.png")
    st.image(image, use_column_width=True)


# User Input Generic: Start API to return story with no prompts
with st.sidebar.form("no_user_input_form"):
    submitted_lucky = st.sidebar.button("I'M FEELING LUCKY")


# User Input with prompts and selections:
with st.sidebar.form("user_input_form"):

    # Input 1: Text Box: prompt to input short text, limit
    input_prompt = st.text_area('got the start of an idea?', height=120, max_chars = 150)

    # Input 2: Radio buttons: choose genre
    opt_genre = st.radio('select your genre:',
                        ('Action 🤯',
                        'Comedy 🤣',
                        'Crime 👮🏽‍♀️',
                        'Drama 🎭',
                        'Fantasy 🚀',
                        'Horror 👻',
                        'Mystery 😵‍💫',
                        'Romance 😘'))

    genre_dict = {'Action 🤯': 'action',
              'Comedy 🤣': 'comedy',
              'Crime 👮🏽‍♀️': 'crime',
              'Drama 🎭': 'novel',
              'Fantasy 🚀': 'fantasy' ,
              'Horror 👻': 'horror',
              'Mystery 😵‍💫': 'mystery',
              'Romance 😘': 'romance'}

    if opt_genre:
        input_genre = genre_dict.get(opt_genre)

    # Button 2: Start API to return story with prompts + genre
    submitted_inputs = st.form_submit_button("GENERATE ME A STORY...")


# MAIN BODY

# Assets: borders top, right and bottom
# Assets: Headertext (your plotify-board)
image = Image.open("streamlit_assets/plotify_pageheadertext.png")
st.image(image,  use_column_width=None)

# Output 1: Summary Text
st.markdown(''' # ''')

with st.container():

    # button with inputs selected
    if submitted_inputs:

        # calls the first api to generate the output text
        with st.spinner("hold the pen, we're doing some plotting..."):
            output = get_text_api()
            if output:
                st.markdown(''' ##### your plotify story:  ''')
                st.write(''' ##''', output)
            else:
                st.error("Hmm, i'm stumped for a plot, awks!😬")

        st.markdown(''' # ''')
        st.markdown("##### your plot images & keywords:")

        # generates two more columns for keywords and image generation
        with st.container():
            if output:
                with st.container():
                    col1, col2, col3 = st.columns([1,3,3])
                with st.spinner("just grabbing a little extra inspiration..."):

                    # get keywords
                    output_topics = get_keywords(output)
                    col1.text('\n'.join(map(str, output_topics)))
                    # get images
                    col2.image(display_image(get_image_api(output_topics)),use_column_width=True)
                    col3.image(display_image(get_image_api(output_topics)),use_column_width=True)

    # lucky button selected
    if submitted_lucky:
        input_prompt = ''
        input_genre = ''

        # calls the first api to generate the output text
        with st.spinner("hold the pen, we're doing some plotting..."):
            output = get_text_api()
            if output:
                st.markdown(''' ##### your plotify story:  ''')
                st.write(''' ##''', output)
            else:
                st.error("Hmm, i'm stumped for a plot, awks!😬")

        st.markdown(''' # ''')
        st.markdown("##### your plot images & keywords:")

        # generates two more columns for keywords and image generation
        with st.container():
            if output:
                with st.container():
                    col1, col2, col3 = st.columns([1,3,3])
                with st.spinner("just grabbing a little extra inspiration..."):

                    # get keywords
                    output_topics = get_keywords(output)
                    col1.text('\n'.join(map(str, output_topics)))
                    # get images
                    col2.image(display_image(get_image_api(output_topics)),use_column_width=True)
                    col3.image(display_image(get_image_api(output_topics)),use_column_width=True)
