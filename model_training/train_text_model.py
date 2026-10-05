"""
train_text_model.py

Trains the job-posting TEXT model (TF-IDF + Logistic Regression) and saves it.
This repeats the steps that were done cell by cell in Google Colab.

Needs:   fake_job_postings.csv  (the Kaggle file with 17,880 rows)
Run:     python train_text_model.py
         python train_text_model.py path/to/fake_job_postings.csv

Output:  models/job_text_model.joblib
         models/versions.txt
         data/train.csv, data/test.csv

Use the same scikit-learn version that saved the model (1.6.1 in Colab).
"""

import os
import re
import sys
import html

import joblib
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else "fake_job_postings.csv"
DATA_DIR = "data"
MODEL_DIR = "models"


def clean_text(t):
    t = html.unescape(str(t))
    t = t.replace("\xa0", " ")
    t = re.sub(r"#(URL|EMAIL|PHONE)_[0-9a-f]+#", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def load_and_clean(path):
    df = pd.read_csv(path)

    # 1. Remove empty, conflicting and repeated descriptions
    df["desc_clean"] = (
        df["description"].fillna("").astype(str)
        .str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    )
    df = df[df["desc_clean"] != ""]
    n_labels = df.groupby("desc_clean")["fraudulent"].transform("nunique")
    df = df[n_labels == 1]
    df = df.drop_duplicates(subset="desc_clean", keep="first")

    # 2. Join the text fields into one column
    text_cols = ["title", "company_profile", "description",
                 "requirements", "benefits"]
    for c in text_cols:
        df[c] = df[c].fillna("").astype(str)
    df["text"] = (
        df["title"] + ". " + df["company_profile"] + " " +
        df["description"] + " " + df["requirements"] + " " + df["benefits"]
    ).str.strip()
    df["label"] = df["fraudulent"].astype(int)

    # 3. Clean the text (invisible spaces, HTML leftovers, placeholder tokens)
    df["text"] = df["text"].apply(clean_text)
    df = df[df["text"].str.len() > 0]
    return df[["text", "label"]].reset_index(drop=True)


def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2),
            min_df=3, max_features=20000, sublinear_tf=True)),
        ("model", LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42)),
    ])


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    clean = load_and_clean(DATA_FILE)
    print("Clean rows:", len(clean))
    print(clean["label"].value_counts())

    # Split BEFORE fitting TF-IDF, so the test rows never influence training
    train, test = train_test_split(
        clean, test_size=0.20, random_state=42, stratify=clean["label"]
    )
    train.to_csv(os.path.join(DATA_DIR, "train.csv"), index=False)
    test.to_csv(os.path.join(DATA_DIR, "test.csv"), index=False)

    model = build_model()
    model.fit(train["text"], train["label"])

    # Final test (the test rows were never used for training)
    pred = model.predict(test["text"])
    prob = model.predict_proba(test["text"])[:, 1]
    print()
    print("TEST RESULTS (Logistic Regression)")
    print(confusion_matrix(test["label"], pred))
    print(classification_report(
        test["label"], pred, target_names=["genuine", "fake"], digits=3))
    print("PR-AUC (fake class): %.3f" % average_precision_score(test["label"], prob))

    joblib.dump(model, os.path.join(MODEL_DIR, "job_text_model.joblib"))
    with open(os.path.join(MODEL_DIR, "versions.txt"), "w") as f:
        f.write("scikit-learn %s\n" % sklearn.__version__)
    print()
    print("Saved models/job_text_model.joblib")
    print("scikit-learn version used:", sklearn.__version__)


if __name__ == "__main__":
    main()
