# Plotify - A Solution to Writer's Block

> __"Helping writers to get past writer's block: Providing inspiration for fresh ideas never before seen."__

Plotify is a project I worked on with 3 smart and energetic individuals as the final project during a 9 week data science bootcamp course at Le Wagon in London, December 2022.

The goal of the project was to address the paradoxical "writer's block". This is a condition experienced by writers, journalist, and authors everywhere: you can't think of the next thing to write!

So the idea that our team leader Phil McDonald came up with was that it would be helpful if a minimal input could inspire an extended output. By this, I mean that a small starting "prompt" could be used to generate a few additional lines with a novel - but relevant - feel.

The approach we used was:

- Identify a large body of text in the format of "summaries" which represent a story.
- Use this body of text to build a program that will take a few words or a sentence, and then output a few more sentences "in the style of" a summary.

## Architecture

The app consists of a frontend web application and a backend system where a Large Language model (GPT2) is loaded.

- The frontend is built in StreamLit which a framework to allow data apps to be rapidly built and deployed
- The backend consists of a Python codebase which utilises Hugging Face's pre-trained GPT2 (small) model and a set of API endpoints (via Fast API) to allow text generation.
- In addition, a call is made to a 3rd party API which allows us to include the output from a Stable Diffusion based Image generation model.

The frontend and backend are each built as Docker containers. The interaction between these Docker containers is coorindated by Docker Compose. This means it would be extremely straightforward to set the system up to run on new hardware (on the basis the Docker images are available on a publically available registry which they are not presently!).

## Data Sources

Data sources:

- IMDB movie summary data from Kaggle's [MPST: Movie Plot Synopses with Tags](https://www.kaggle.com/datasets/cryptexcode/mpst-movie-plot-synopses-with-tags). 14,828 movie summaries (in a 30MB CSV file)
- Wikipedia book summary data from Kaggle's [CMU Book Summary Dataset](https://www.kaggle.com/datasets/ymaricar/cmu-book-summary-dataset). 16,559 book summaries (in a 43.46MB plaintext file)

## Cleaning

- Reduced cardinality of Genres by grouping them together into generalised Genres.
- Dropped very long & short summaries. GPT only "recognises" the first 1024 tokens of input in any case.

## Training

Multiple issues were encountered in fine-tuning, of note:

- Issues with dependencies: The Hugging Face libraries didn't play ball with our more recent TensorFlow environment. We had to set up an environment with specific Transformers, Datasets, and TensorFlow library versions.
- The loss function needed to be switched for one specific to Hugging Face's implementation of GPT2.

Having overcome these, we fine-tuned the model using a Google Colab provided NVIDIA A100. The process took about 30 minutes until `val_loss` stabilised and training was stopped early.



## Resources

- [An excellent guide](https://data-dive.com/finetune-german-gpt2-on-tpu-transformers-tensorflow-for-text-generation-of-reviews/) which lead us through the process of fine-tuning. The guide was published in early 2021 using an older Hugging Face Transformers & TensorFlow library version and utilised "Eager Execution" as opposed to JIT so performance was poor. Not a problem for now, but room for improvement



