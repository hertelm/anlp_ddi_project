from corpus_reader import read_dataset
from word_extraction import get_word_lists_from_sentence
from naive_bayes import NaiveBayes

def n_grams(word, n = 3, padding = True):
    if padding:
        pads = "#" * (n - 1)
        word = pads + word + pads
    ngrams = []
    for i in range(0, len(word) - n + 1):
        ngrams.append(word[i:(i+n)])
    return ngrams

def starts_with_uppercase(word):
    return word[0].lower() != word[0]

def trained_naive_bayes(dataset):
    nb = NaiveBayes([True, False])
    ngram_feature_name = "3gram"
    nb.register_feature(ngram_feature_name)
    length_feature_name = "word_length"
    nb.register_feature(length_feature_name)
    uppercase_feature_name = "uppercase_start"
    nb.register_feature(uppercase_feature_name)
    for doc in dataset:
        for s in doc.sentences:
            drug_words, neutral_words = get_word_lists_from_sentence(s)
            for dw in drug_words:
                nb.count_class(True)
                nb.count_feature(length_feature_name, len(dw), True)
                nb.count_feature(uppercase_feature_name, starts_with_uppercase(dw), True)
                ngrams = n_grams(dw)
                for ngram in ngrams:
                    nb.count_feature(ngram_feature_name, ngram, True)
            for nw in neutral_words:
                nb.count_class(False)
                nb.count_feature(length_feature_name, len(nw), False)
                nb.count_feature(uppercase_feature_name, starts_with_uppercase(nw), False)
                ngrams = n_grams(nw)
                for ngram in ngrams:
                    nb.count_feature(ngram_feature_name, ngram, False)
    return nb

def extract_features_and_classify(word, nb):
    features = []
    features.append(("word_length", len(word)))
    features.append(("uppercase_start", starts_with_uppercase(word)))
    ngrams = n_grams(word)
    for ngram in ngrams:
        features.append(("3gram", ngram))
    label = nb.classify(features)
    return label

if __name__ == "__main__":
    dataset = read_dataset()
    nb = trained_naive_bayes(dataset)
    while True:
        print("enter example:")
        example = input()
        label = extract_features_and_classify(example, nb)
        print(label)
