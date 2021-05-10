from fuzzywuzzy import fuzz, process

def get_streets(address:str, streets, n:int=5):
    scores = get_scores(address, streets)

    sorted_scores = sort_scores(scores)
    return sorted_scores[:n]

def get_scores(address, streets):
    scores = []

    for street in streets:
        if street in address:
            scores.append({'score': 1, 'name': street})
            continue

        r = fuzz.token_set_ratio(address, street) / 100
        scores.append({'score': r, 'name': street})
    return scores

def sort_scores(scores):
    sortedLen = sorted(scores, key=lambda score: len(score['name']), reverse=True)
    sortedR = sorted(sortedLen, key=lambda score: score['score'], reverse=True)

    return sortedR