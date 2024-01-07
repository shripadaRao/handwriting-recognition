import requests
import csv
from nltk.corpus import words
import random
import pandas as pd
import Levenshtein
import nltk

# API URLs
GENERATE_INPUT_WORD_IMAGE_API_URL = "http://127.0.0.1:5000/generate_image/"
PREDICT_IMAGE_API_URL = "http://127.0.0.1:5000/predict_image"

# wordnet_words = words.words()

# def get_random_word():
#     return str(random.sample(wordnet_words, 1)[0])

# # Data structure to store results in memory
# data_in_memory = []

# # Number of iterations
# num_iterations = 100

# # Make API requests and store data in memory
# for _ in range(num_iterations):
#     print("iteration num: ",_)
#     # Call generate_image API
#     print(get_random_word())
#     generate_image_response = requests.get(GENERATE_INPUT_WORD_IMAGE_API_URL + get_random_word())
#     generate_image_data = generate_image_response.json()
#     true_label = generate_image_data["label"]
#     img_data = generate_image_data["image"]

#     # Call predict_image API
#     predict_image_data = {"imageData": img_data}
#     predict_image_response = requests.post(PREDICT_IMAGE_API_URL, json=predict_image_data)
#     predict_image_result = predict_image_response.json()
#     predicted_label = predict_image_result["predictedWord"]
#     autocorrected_label = predict_image_result["autocorrectedWord"]

#     # Store data in memory
#     data_in_memory.append({
#         "TrueLabel": true_label,
#         "PredictedLabel": predicted_label,
#         "AutocorrectedLabel": autocorrected_label
#     })

# # Save data from memory to CSV file
# csv_filename = "htr_benchmark_data_.csv"
# with open(csv_filename, mode="w", newline='') as csv_file:
#     fieldnames = ['TrueLabel', 'PredictedLabel', 'AutocorrectedLabel']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     # Write header
#     writer.writeheader()

#     # Write data
#     for data_point in data_in_memory:
#         writer.writerow(data_point)

# print(f"Data saved to {csv_filename}")

def calculate_cer( column1, column2, csv_path="htr_benchmark_data.csv",):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Extract the reference and hypothesis columns
    reference = df[column1].astype(str)
    hypothesis = df[column2].astype(str)

    total_cer = 0
    total_chars = 0

    # Calculate CER for each row
    for ref, hyp in zip(reference, hypothesis):
        cer = Levenshtein.distance(ref, hyp)
        total_cer += cer
        total_chars += len(ref)
    
    print("total_cer",total_cer)
    print("total_chars", total_chars)

    # Calculate the overall CER
    overall_cer = total_cer / total_chars if total_chars > 0 else 0

    return overall_cer

# print(calculate_cer("TrueLabel", "AutocorrectedLabel"))


def calculate_wer(column1, column2, csv_path="htr_benchmark_data.csv"):

    nltk.download('punkt')
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Extract the reference and hypothesis columns
    reference = df[column1].astype(str)
    hypothesis = df[column2].astype(str)

    total_wer = 0
    total_words = 0

    # Calculate WER for each row
    for ref, hyp in zip(reference, hypothesis):
        ref_tokens = nltk.word_tokenize(ref.lower())
        hyp_tokens = nltk.word_tokenize(hyp.lower())

        wer = nltk.edit_distance(ref_tokens, hyp_tokens)
        total_wer += wer
        total_words += len(ref_tokens)

    # Calculate the overall WER
    overall_wer = total_wer / total_words if total_words > 0 else 0

    return overall_wer

print(calculate_wer("TrueLabel", "PredictedLabel"))