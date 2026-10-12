import json, os, glob, zipfile, urllib.request
import pandas as pd, numpy as np, networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

PINK, LILAC, DEEP = "#e8739b", "#c9b8e8", "#8d7bb0"
plt.rcParams["figure.dpi"] = 110

ZIP_URL = "https://raw.githubusercontent.com/3lza/JBS_biomedic-nask-rta/main/classroom_data.zip"
ALLOW_UPLOAD = False   

OK = False
SETUP_ERROR = None    


def _find():
    hits = glob.glob("**/edges_small.csv", recursive=True)
    return os.path.dirname(hits[0]) + "/" if hits else None


def _unzip_any():
    for z in sorted(glob.glob("**/*.zip", recursive=True), key=os.path.getsize, reverse=True):
        try:
            with zipfile.ZipFile(z) as f:
                f.extractall(".")
            return
        except zipfile.BadZipFile:
            continue


try:
    D = _find()

    if D is None:
        urllib.request.urlretrieve(ZIP_URL, "classroom_data.zip")
        _unzip_any()
        D = _find()

    if D is None and ALLOW_UPLOAD:
        from google.colab import files
        files.upload()
        _unzip_any()
        D = _find()

    if D is None:
        raise FileNotFoundError("data folder not found")

    edges   = pd.read_csv(D + "edges_small.csv")
    neurons = pd.read_csv(D + "neurons_small.csv")
    top     = pd.read_csv(D + "top_neurons.csv")
    hubs    = pd.read_csv(D + "hubs_all.csv")
    stats   = json.load(open(D + "stats.json"))

    top_lv = top.rename(columns={"id": "ID", "type": "Neirona veids",
                                 "class": "Klase", "total_weight": "Svars"})
    OK = True
    print("Viss labi, turpini darbu")

except Exception as e:
    SETUP_ERROR = repr(e)
    print("Pasauc kādu")
