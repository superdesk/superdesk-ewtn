import itertools
import logging
import superdesk.editor_utils as editor_utils


logger = logging.getLogger(__name__)
do_not_capitalize = "a an the and but for at by in to of".split()


def capitalize(item, **kwargs):
    """
        Properly capitalize the headline per National Catholic Register conventions.
        This approximates the Associated Press style guidelines (words with 4 or more letters should
        be capitalized).  However, in practice, an implementation more consistent with the Register's conventions is
        simply to have a whitelist of non-capitalized words, and everything else gets capitalized.
    """

    if item.get("headline", None):
        old_headline = item["headline"]
        capitalized_headline = capitalize_headline(item["headline"])
        editor_utils.replace_text(item, "headline", old_headline, capitalized_headline)
        item["headline"] = capitalized_headline
        logger.info("Capitalized headline:\nFrom: [ %s ]\nTo:   [ %s ]", old_headline, capitalized_headline)

    return item


def capitalize_headline(headline):
    words = []
    splitters = []
    word = ""
    for char in headline:
        if char in [' ', '-']:
            splitters.append(char)
            words.append(word)
            word = ""
        else:
            word = word + char
    words.append(word)

    capitalized = []
    for word in words:
        if ''.join(filter(str.isalpha, word)) in do_not_capitalize:  # filtering non-alphabet chars from the word
            capitalized.append(word)
        else:
            capitalized.append(uppercase_first_letter(word))

    zip_result = itertools.zip_longest(capitalized, splitters, fillvalue="")
    ordered_bits = [item for sublist in zip_result for item in sublist]
    return "".join(ordered_bits)


def uppercase_first_letter(word):
    for i in range(len(word)):
        '''
            The input "word" may contain opening quotation marks, so ignore those / skip past them to find the first
            non-quotation-mark character to capitalize.

            \u2018 = left single quote
            \u201C = left double quote
        '''
        if word[i] not in ['"', "'", "\u2018", "\u201C"]:
            return word[0:i] + word[i].capitalize() + word[i + 1:]
    return word


name = "headline_capitalizer"
label = "Capitalize Headline"
order = 3
shortcut = "c"
callback = capitalize
access_type = "frontend"
action_type = "direct"
replace_type = "editor_state"
