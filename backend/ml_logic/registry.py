from ml_logic.params import LOCAL_REGISTRY_PATH

import os

from colorama import Fore, Style

from transformers import TFGPT2LMHeadModel, GPT2Tokenizer, pipeline


def build_pipeline():
    """
    Load tokenizer & model
    Returns: built pipeline
    """

    path_model = os.path.join(LOCAL_REGISTRY_PATH, "model")
    path_tokenizer = os.path.join(LOCAL_REGISTRY_PATH, "tokenizer")

    try:
        print(Fore.BLUE + "\nLoad model from local disk..." + Style.RESET_ALL)

        model = TFGPT2LMHeadModel.from_pretrained(path_model)

    except:
        print("Exception while loading model")

    finally:
        print("\n✅ model loaded from disk")

    try:
        print(Fore.BLUE + "\nLoad tokenizer..." + Style.RESET_ALL)

        tokenizer = GPT2Tokenizer.from_pretrained(
            path_tokenizer
        )

    except:
        print("Exception while loading tokenizer")

    finally:
        print("\n✅ tokenizer loaded")

    try:
        print(Fore.BLUE + "\nInstantiating pipeline..." + Style.RESET_ALL)
        new_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )
        print("\n✅ pipeline instantiated")

    except:
        print("Exception while instantiating pipeline")

    return new_pipeline
