from flask_babel import lazy_gettext
import re
import logging
import superdesk.editor_utils as editor_utils

LS = "\u2018"  # left single quote
RS = "\u2019"  # right single quote
LD = "\u201C"  # left double quote
RD = "\u201D"  # right double quote

p = re.compile("(?i)(?<=[.?!])\\S+(?=[a-z])")
logger = logging.getLogger(__name__)


def dumb_to_smart_quotes(item):
    """
        Takes an item and returns it with dumb quotes, single and double,
        replaced by smart quotes in the headline and abstract
        Accounts for the possibility of HTML tags within the string.
    """

    for field in ["headline", "abstract"]:
        if item.get(field, None):
            original = item[field]
            quotes_replaced = do_replacement(original)

            editor_utils.replace_text(item, field, original, quotes_replaced, editor_utils.is_html(field))
            logger.info("Replaced quotes in %s:\nFrom: [ %s ]\nRepl: [ %s ]\nTo:   [ %s ]", field, original, quotes_replaced, item[field])

    return item


def do_replacement(text):
    """
        Takes a string and returns it with dumb quotes, single and double,
        replaced by smart quotes. Accounts for the possibility of HTML tags
        within the string.

        Adapted from: https://gist.github.com/davidtheclark/5521432
    """

    # Find dumb double quotes coming directly after letters or punctuation,
    # and replace them with right double quotes.
    text = re.sub(r'([a-zA-Z0-9.,?!;:\'\"’])"', r'\1{}'.format(RD), text)
    # Find any remaining dumb double quotes and replace them with
    # left double quotes.
    text = text.replace('"', LD)
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around HTML
    # attributes (following =) and replace them with dumb quotes.
    text = re.sub(r'={}(.*?){}'.format(LD, RD), r'="\1"', text)

    # Follow the same process with dumb/smart single quotes
    text = re.sub(r"([a-zA-Z0-9.,?!;:\"\'”])'", r'\1{}'.format(RS), text)
    text = text.replace("'", LS)
    text = re.sub(r'={}(.*?){}'.format(LS, RS), r"='\1'", text)
    return text


name = "dumb_to_smart_quotes"
label = lazy_gettext("Replace simple quotes with smart quotes")
order = 3
shortcut = "r"
callback = dumb_to_smart_quotes
access_type = "frontend"
action_type = "direct"
replace_type = "editor_state"
