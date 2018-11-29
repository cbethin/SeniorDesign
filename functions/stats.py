def normalize(array=[]):
    return [(x - min(array)) / (max(array) - min(array)) for x in array]