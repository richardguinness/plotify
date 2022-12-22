from ml_logic.params import LOCAL_REGISTRY_PATH, REMOTE_MODEL_TARGET #, MODEL_REF

# import mlflow
# from mlflow.tracking import MlflowClient

import glob
import os
import subprocess
import time
import pickle

from colorama import Fore, Style

from transformers import TFGPT2LMHeadModel, GPT2Tokenizer, pipeline

# model_directory = LOCAL_REGISTRY_PATH #, MODEL_REF)
path_model = os.path.join(LOCAL_REGISTRY_PATH, "model")
path_tokenizer = os.path.join(LOCAL_REGISTRY_PATH, "tokenizer")


def load_tokenizer():
    # New Tokenizer effort based on https://data-dive.com/finetune-german-gpt2-on-tpu-transformers-tensorflow-for-text-generation-of-reviews

    try:
        tokenizer = GPT2Tokenizer.from_pretrained(
            path_tokenizer
        )

        return tokenizer
    except:
        print("Exception while loading tokenizer")
        return None


def build_pipeline():
    # Load model into memory
    # load tokenizer
    # build pipeline

    try:
        print(Fore.BLUE + "\nLoad model from local disk..." + Style.RESET_ALL)

        model = TFGPT2LMHeadModel.from_pretrained(path_model)

    except:
        print("Exception while loading model")

    finally:
        print("\n✅ model loaded from disk")

    try:
        print(Fore.BLUE + "\nLoad tokenizer..." + Style.RESET_ALL)
        tokenizer = load_tokenizer()

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

# def download_model():
#     # Load model from GCP bucket
#     # LOCAL_REGISTRY_PATH = "~/code/nitrobear95/plotify/model_hf2"
#     print(Fore.BLUE + "\nDownloading model from GCP Bucket: " + \
#         f"{REMOTE_MODEL_TARGET}... to " + \
#         f"{LOCAL_REGISTRY_PATH}/models/" + Style.RESET_ALL)
#     try:
#         subprocess.run([
#             "gsutil", "cp", "-r",
#             "gs://lewagon1050-rg/model_hf/model_hf",
#             # REMOTE_MODEL_TARGET + "/*",
#             "/home/rdzg/code/nitrobear95/plotify/model_hf2/models",
#             # LOCAL_REGISTRY_PATH + "/models/",
#             "-p", "52108777107"
#         ])
#         # check=True)
#         print("\n✅ model downloaded")
#         return None
#     except:
#         print(f"\n❌ Error downloading model")
#         return None

# def load_model(save_copy_locally=False) -> Model:
#     """
#     load the latest saved model, return None if no model found
#     """
#     if os.environ.get("MODEL_TARGET") == "mlflow":
#         stage = "Production"

#         print(Fore.BLUE + f"\nLoad model {stage} stage from mlflow..." + Style.RESET_ALL)

#         # load model from mlflow
#         mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

#         mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

#         model_uri = f"models:/{mlflow_model_name}/{stage}"
#         print(f"- uri: {model_uri}")

#         try:
#             model = mlflow.keras.load_model(model_uri=model_uri)
#             print("\n✅ model loaded from mlflow")
#         except:
#             print(f"\n❌ no model in stage {stage} on mlflow")
#             return None

#         if save_copy_locally:
#             from pathlib import Path

#             # Create the LOCAL_REGISTRY_PATH directory if it does exist
#             Path(LOCAL_REGISTRY_PATH).mkdir(parents=True, exist_ok=True)
#             timestamp = time.strftime("%Y%m%d-%H%M%S")
#             model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", timestamp)
#             model.save(model_path)

#         return model

#     print(Fore.BLUE + "\nLoad model from local disk..." + Style.RESET_ALL)

#     # get latest model version
#     model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")

#     results = glob.glob(f"{model_directory}/*")
#     if not results:
#         return None

#     model_path = sorted(results)[-1]
#     print(f"- path: {model_path}")

#     model = models.load_model(model_path)
#     print("\n✅ model loaded from disk")

#     return model
