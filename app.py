import streamlit as st
from PIL import Image
from style import get_css
import time
import requests
import yake
import requests
from io import BytesIO

import replicate
from dotenv import load_dotenv, find_dotenv
import os


def get_image_api(prompt):
    prompt = f'{output_topics}, illustration, book cover, no text'
    #envpath = find_dotenv()
    #load_dotenv(envpath)
    replicate.Client(api_token=os.getenv("REPLICATE_API_KEY"))
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("0827b64897df7b6e8c04625167bbb275b9db0f14ab09e2454b9824141963c966")
    image_url = version.predict(prompt=prompt)
    print(image_url)
    print(image_url[0])
    return image_url





def get_keywords():

    kw_extractor = yake.KeywordExtractor()
    text = output
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.15
    numOfKeywords = 6
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None, stopwords=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    keyword_list = [x[0] for x in keywords]
    # print('get keywords works')
    return keyword_list



def display_image(image_url):
  # Make a GET request to the URL to retrieve the image data
  response = requests.get(image_url[0])

  # Create an image object from the image data
  image = Image.open(BytesIO(response.content))

  # Display the image
#   print('display image works')
  return image


def get_text_api():


    url = "https://plotifymodel-b4p33xwhra-ez.a.run.app/generate_summary?"

    param = {'genre': input2.lower(),
                'prompt': input1,
                'max_length': 150}

    x = requests.get(url, params=param).json()
    # print('get text api works')
    return x['generate_summary'][0]['generated_text'].split('|>',1)[1]




## SITE CONFIG

# set the config for the page. App themes in .streamlit/config.toml
st.set_page_config(
            page_title="Plotify - create your story", # => Quick reference - Streamlit
            page_icon="streamlit_assets/plotify_logo_small.png",
            layout="wide", # wide
            initial_sidebar_state="expanded") # collapsed


st.markdown(get_css(), unsafe_allow_html=True)



## SIDEBAR

# Assets: Logo + headertext(plotify - create your story)
with st.sidebar.container():
    image = Image.open("streamlit_assets/plotify_logocomplete.png")
    st.image(image, use_column_width=True) #, caption ='Plotify - create your story'


# User Input Generic: Start API to return story with no prompts
if st.sidebar.button("I'M FEELING LUCKY"):
    # print is visible in the server output, not in the page
    st.write('lucky_story_selected')


## User Input with prompts and selections:
with st.sidebar.form("user_input_form"):

    # Input 1: Text Box: prompt to input short text, limit
    input1 = st.text_area('got the start of an idea?', height=150, max_chars = 1000)

    # Input 2: Radio buttons: choose genre
    input2 = st.radio('select your genre:',
                        ('Action 🤯',
                        'Comedy 🤣',
                        'Crime 👮🏽‍♀️',
                        'Drama 🎭',
                        'Fantasy 🚀',
                        'Horror 👻',
                        'Mystery 😵‍💫',
                        'Romance 😘',
                        'Young Adult 😎'))

    # Button 2: Start API to return story with prompts + genre
    submitted = st.form_submit_button("GENERATE ME A STORY...")



## MAIN BODY

# Assets: borders top, right and bottom
# Assets: Headertext (your plotify-board)
image = Image.open("streamlit_assets/plotify_pageheadertext.png")
st.image(image,  use_column_width=None)



# Output 1: Summary Text
st.markdown(''' # ''')


with st.container():

    # button selected
    if submitted:
        # calls the first api to generate the output text
        with st.spinner("hold the pen, we're doing some plotting..."):
            output = get_text_api()
            if output:
                st.markdown(''' #### 🎉👀 YIPPPEEE!''')
                st.markdown(''' ##### plotify has got a story for you:  ''')
                st.write(output)
            else:
                st.error("Hmm, i'm stumped for a plot, awks!😬")

        st.markdown(''' # ''')

        # generates two more columns for keywords and image generation
        with st.container():
            col1, col2 = st.columns([1,4])

            # keyword generation
            with col1:
                if output:
                    st.markdown(''' ##### your plot keywords: ''')
                    output_topics = get_keywords()
                    st.markdown(output_topics)

            # image generation
            with col2:
                if output:
                    st.markdown("##### your plot images:")
                    st.image(display_image(get_image_api(output_topics)), use_column_width=True)
