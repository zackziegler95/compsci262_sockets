def replace_punc(sentence):
    sentence = sentence.replace(',', ' ,')
    sentence = sentence.replace('.', ' .')
    sentence = sentence.replace('!', ' !')
    sentence = sentence.replace('?', ' ?')
    return sentence

def rereplace_punc(sentence):
    sentence = sentence.replace(' ,', ',')
    sentence = sentence.replace(' .', '.')
    sentence = sentence.replace(' !', '!')
    sentence = sentence.replace(' ?', '?')
    return sentence

# Convert to pig latin, modified from https://stackoverflow.com/questions/23177250/converting-a-sentence-to-piglatin-in-python

lst = ['sh', 'gl', 'ch', 'ph', 'tr', 'br', 'fr', 'bl', 'gr', 'st', 'sl', 'cl', 'pl', 'fl']
def to_piglatin(sentence):
    # Converts the sentence string into a pig latin string
    sentence = replace_punc(sentence)
    words = sentence.split()

    output_words = []
    for k in range(len(words)):
        word = words[k]
        if word[0] in ['a', 'e', 'i', 'o', 'u']:
            output_words.append(word+'ay')
        elif word[:2] in lst:
            output_words.append(word[2:]+word[:2]+'ay')
        elif word.isalpha() == False:
            output_words.append(word)
        else:
            output_words.append(word[1:]+word[0]+'ay')

    sentence = rereplace_punc(' '.join(output_words))
    return sentence
