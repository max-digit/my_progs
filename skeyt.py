def skeyt(dictionary, value):
"Function that returns a list of dictionary keys, if they match a given value "
    keys = []
    def seek(key):
        if dictionary[key] == value:
            keys.append(key)
    list(map(seek, dictionary))
    return keys
