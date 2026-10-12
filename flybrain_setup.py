import json, os, glob, zipfile, urllib.request
import pandas as pd, numpy as np, networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

PINK, LILAC, DEEP = "#e8739b", "#c9b8e8", "#8d7bb0"
plt.rcParams["figure.dpi"] = 110

# Teacher: the RAW link to the zip on GitHub
ZIP_URL = "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/classroom_data.zip"


def _find():
    hits = glob.glob("**/edges_small.csv", recursive=True)
    return os.path.dirname(hits[0]) + "/" if hits else None


def _unzip_any():
    # tries the biggest zip first, skips broken ones
    for z in sorted(glob.glob("**/*.zip", recursive=True), key=os.path.getsize, reverse=True):
        try:
            with zipfile.ZipFile(z) as f:
                f.extractall(".")
            return
        except zipfile.BadZipFile:
            continue


D = _find()

if D is None:                       # 1) download from GitHub
    try:
        urllib.request.urlretrieve(ZIP_URL, "classroom_data.zip")
    except Exception as e:
        print("Lejupielāde neizdevās:", e)
    _unzip_any()
    D = _find()

if D is None:                       # 2) last resort: upload by hand
    from google.colab import files
    print("Augšupielādē classroom_data.zip:")
    files.upload()
    _unzip_any()
    D = _find()

assert D, "Datu faili nav atrasti. Pasauc skolotāju!"

edges   = pd.read_csv(D + "edges_small.csv")
neurons = pd.read_csv(D + "neurons_small.csv")
top     = pd.read_csv(D + "top_neurons.csv")
hubs    = pd.read_csv(D + "hubs_all.csv")
stats   = json.load(open(D + "stats.json"))

# Latvian-named copy of the table, for Q2
top_lv = top.rename(columns={"id": "ID", "type": "Neirona veids",
                             "class": "Klase", "total_weight": "Svars"})

print("Gatavs! Izmantoto datu mape:", D)
