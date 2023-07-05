from unittest import TestCase
from ewt.macros import dumb_to_smart_quotes as macro

LS = macro.LS
RS = macro.RS
LD = macro.LD
RD = macro.RD


class DumbToSmartQuotesTest(TestCase):

    befores_and_afters = [
        (
            "\"Now that's interesting\", she said.",
            f"{LD}Now that{RS}s interesting{RD}, she said."
        ),
        (
            "According to Jane: \"I heard John say, 'My friend Joe exclaimed \"hooray!\"'\"",
            f"According to Jane: {LD}I heard John say, {LS}My friend Joe exclaimed {LD}hooray!{RD}{RS}{RD}"
        ),
        (
            # same as the one above, except inverted single and double quotes
            "According to Jane: 'I heard John say, \"My friend Joe exclaimed 'hooray!'\"'",
            f"According to Jane: {LS}I heard John say, {LD}My friend Joe exclaimed {LS}hooray!{RS}{RD}{RS}"
        ),
        (
            "This is a 'a direct quote'",
            f"This is a {LS}a direct quote{RS}"
        ),
        (
            # Note that the smart quote logic in the CNA RSS ingest logic (superdesk/server/ewt/cna/ingest/rss.py)
            # doesn't handle this case properly.  It's simply looking for opening and closing single quotes with
            # some characters in between, and then replacing the first single quote with {LS}.  In the case where
            # two contractions exist, they both should have {RS}.
            "We're celebrating Frank's birthday tomorrow",
            f"We{RS}re celebrating Frank{RS}s birthday tomorrow"
        ),
        (
            "Should preserve dumb quotes inside <a href=\"url\">html tags</a>",
            "Should preserve dumb quotes inside <a href=\"url\">html tags</a>"
        )
    ]

    def test_do_replacement(self):
        for (before, after) in self.befores_and_afters:
            item = {
                "headline": f"Headline: {before}",
                "abstract": f"<p>Abstract: {before}</p>"
            }
            macro.callback(item)
            self.assertEqual(f"Headline: {after}", item["headline"])
            self.assertEqual(f"<p>Abstract: {after}</p>", item["abstract"])
