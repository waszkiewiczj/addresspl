def get_streets(adress:str, streets:str, n:int=5):
    scores = get_scores(address, streets)

    sorted_scores = sort_scores(scores)
    return sorted_scores[:n]

def get_scores(address, streets):
    scores = []

    for street in streets:
        if street in address:
            scores.append({'score': 1, 'name': street})
            continue

        r = fuzz.token_set_ratio(address, street) 
        scores.append({'score': r, 'name': street})
    return best_c, best_r

def sort_scores(scores):
    sortedLen = sorted(scores, key=lambda score: len(score['name']), reverse=True)
    sortedR = sorted(sortedLen, key=lambda score: score['score'], reverse=True)

    return sortedR