def skeyt(dictionary, value):
    keys = []
    def seek(key):
        if dictionary[key] == value:
            keys.append(key)
    list(map(seek, dictionary))
    return keys
