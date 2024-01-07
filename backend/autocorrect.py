import textdistance
from collections import Counter
from nltk.corpus import wordnet
import nltk
import google.generativeai as palm


# class AutocorrectModel:
#     def __init__(self, vocabulary):
#         self.V = set(vocabulary)
#         self.word_freq = Counter(vocabulary)
#         self.total_words = sum(self.word_freq.values())
#         self.probs = {k: v / self.total_words for k, v in self.word_freq.items()}

#     def autocorrect(self, input_word):
#         input_word = input_word.lower()

#         if input_word in self.V:
#             return input_word

#         sim_scores = [1 - textdistance.Jaccard(qval=2).distance(v, input_word) for v in self.word_freq.keys()]

#         # Combine similarity scores with probabilities
#         candidates = list(zip(self.word_freq.keys(), sim_scores, self.probs.values()))

#         # Sort by similarity and then by probability
#         sorted_candidates = sorted(candidates, key=lambda x: (x[1], x[2]), reverse=True)

#         # Return the top result
#         suggestion = sorted_candidates[0][0]
#         return suggestion

def generate_category_weights(context=None, no_of_words=100):
    try:
        if context is not None:
            API_KEY = 'AIzaSyDcJL64JpdSrZT5YNW1gF8vLvgdEI66dmA'
            palm.configure(api_key=API_KEY)
            model_id = 'models/text-bison-001'

            # prompt = f"Create a dictionary with {no_of_words} entries. Each entry should have the format '{{word}}: {{bias}}', where word is a word related to the context '{{context}}' and bias is a number between 5 and 50 representing its popularity of usage. The words should be generated with a bias towards those with higher popularity scores."
            prompt = 'Generate '+ str(no_of_words)+ ' words related to the context '+context+' with one space in between and dont repeat words'

            completion = palm.generate_text(
                model=model_id,
                prompt=prompt,
                temperature=0.5,
                max_output_tokens=800,
                candidate_count=1
            )
            contextual_words = (completion.result.split())
            contextual_words = {word:35 for word in contextual_words}
            print(contextual_words)
            return contextual_words
        else:
            raise ValueError("Context must be provided.")
    except Exception as e:
        print(f"Error in generate_category_weights: {e}")
        return {}


class AutocorrectModel:
    def __init__(self, vocabulary, category_weights=None):
        self.V = set(vocabulary)
        self.word_freq = Counter(vocabulary)
        self.total_words = sum(self.word_freq.values())
        self.probs = {k: v / self.total_words for k, v in self.word_freq.items()}
        self.category_weights = category_weights or {}

    def calculate_similarity_scores(self, input_word):
        input_word = input_word.lower()
        return [1 - textdistance.Jaccard(qval=2).distance(v, input_word) for v in self.word_freq.keys()]

    def apply_category_bias(self, similarity_scores):
        for category, weight in self.category_weights.items():
            if category in self.word_freq:
                # Get indices of words in the specified category
                category_indices = [i for i, word in enumerate(self.word_freq.keys()) if word == category]
                for idx in category_indices:
                    similarity_scores[idx] *= weight
        return similarity_scores
    
    def autocorrect(self, input_word,  context= None):
        if context is not None:
            self.category_weights = generate_category_weights(context)

        input_word = input_word.lower()

        if input_word in self.V:
            return input_word

        # Calculate Jaccard similarity scores
        sim_scores = self.calculate_similarity_scores(input_word)

        # Apply category-based bias
        sim_scores = self.apply_category_bias(sim_scores)

        # Combine similarity scores with probabilities
        candidates = list(zip(self.word_freq.keys(), sim_scores, self.probs.values()))

        # Sort by similarity and then by probability
        sorted_candidates = sorted(candidates, key=lambda x: (x[1], x[2]), reverse=True)

        # Return the top result
        suggestion = sorted_candidates[0][0]
        return suggestion

    
# category_weights = {"orange": 1.2}


# Read words from the "words.txt" file
with open("ScrabbleGAN/words.txt", 'r') as file:
    word_lines = file.readlines()

# Create a list of words from the file
word_list = [word.strip() for word in word_lines]


# get words from nltk word corpus too
nltk.download('wordnet')
all_synsets = list(wordnet.all_synsets())

# Extract words from synsets
all_nltk_words = set()
for synset in all_synsets:
    all_nltk_words.update(word.name() for word in synset.lemmas())

# Example usage
autocorrect_model = AutocorrectModel(word_list + list(all_nltk_words))
