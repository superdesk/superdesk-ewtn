
import unittest
from ewt.macros import headline_capitalizer as macro


class HeadlineCapitalizerTest(unittest.TestCase):

    headlines = [
        # Actual headlines from CNA & NCR
        (
            "Pope Francis: St. Andrew Kim Taegon teaches us ‘we must not give up’",
            "Pope Francis: St. Andrew Kim Taegon Teaches Us ‘We Must Not Give Up’"
        ), (
            "Pope Francis: Pray that the Gospel can be freely shared in China",
            "Pope Francis: Pray That the Gospel Can Be Freely Shared in China"
        ), (
            "80-year-old man tries to kill archbishop after Mass in cathedral in Mexico",
            "80-Year-Old Man Tries to Kill Archbishop After Mass in Cathedral in Mexico"
        ), (
            "MiraVia maternity home brings hope and life to pregnant students in North Carolina",
            "MiraVia Maternity Home Brings Hope and Life to Pregnant Students in North Carolina"
        ), (
            "Supreme Court Justice Gorsuch blasts COVID lockdowns, closing of churches",
            "Supreme Court Justice Gorsuch Blasts COVID Lockdowns, Closing of Churches"
        ), (
            "PHOTOS: Thousands march in Italy’s national ‘Demonstration for Life’",
            "PHOTOS: Thousands March in Italy’s National ‘Demonstration for Life’"
        ), (
            "Pope Francis approves beatification of priest martyred in World War II",
            "Pope Francis Approves Beatification of Priest Martyred in World War II"
        ), (
            "Archdiocese in Mexico warns against attending SSPX Mass in newly built church",
            "Archdiocese in Mexico Warns Against Attending SSPX Mass in Newly Built Church"
        ), (
            "Cardinal Ladaria: Truth about humanity and sexuality doesn’t change because of changes in ideology",
            "Cardinal Ladaria: Truth About Humanity and Sexuality Doesn’t Change Because of Changes in Ideology"
        ), (
            "Pentecost Novena: Here’s how to pray the first novena",
            "Pentecost Novena: Here’s How to Pray the First Novena"
        ), (
            "Report gives voice to Canada’s Indigenous Christians, highlights need for religious freedom",
            "Report Gives Voice to Canada’s Indigenous Christians, Highlights Need for Religious Freedom"
        ), (
            "Blaze set at iconic Mexican church; Eucharist stolen from another",
            "Blaze Set at Iconic Mexican Church; Eucharist Stolen From Another"
        ), (
            "House of saints: Visiting St. Thérèse of Lisieux’s home has inspired conversions",
            "House of Saints: Visiting St. Thérèse of Lisieux’s Home Has Inspired Conversions"
        ), (
            "Texas becomes 18th state to ban sex changes for kids",
            "Texas Becomes 18th State to Ban Sex Changes for Kids"
        ),

        # My own tests
        (
            "mother-in-law",
            "Mother-in-Law"
        ), (
            " This headline has a leading space and a trailing dash-",
            " This Headline Has a Leading Space and a Trailing Dash-"
        ), (
            "The current temperature is 42deg outside",
            "The Current Temperature Is 42deg Outside"
        ), (
            'Someone said this is "a big deal"',
            'Someone Said This Is "a Big Deal"'
        ), (
            'This headline is decidedly "not a big deal"',
            'This Headline Is Decidedly "Not a Big Deal"'
        ), (
            "A tweet from @twitter_handle",
            "A Tweet From @twitter_handle"
        )
    ]

    def test_headline_capitalization(self):
        for (uncapitalized, expected) in self.headlines:
            item = {"headline": uncapitalized}
            macro.callback(item)
            self.assertEqual(expected, item["headline"])

    def test_uppercase_first_letter_ignoring_quotes(self):
        self.assertEqual("A", macro.uppercase_first_letter("a"))
        self.assertEqual("Blah", macro.uppercase_first_letter("blah"))
        self.assertEqual("'We", macro.uppercase_first_letter("'we"))
        self.assertEqual("We're", macro.uppercase_first_letter("we're"))
        self.assertEqual('"Who"', macro.uppercase_first_letter('"who"'))
        self.assertEqual('\u2018Who', macro.uppercase_first_letter('\u2018who'))
        self.assertEqual('\u201CWho', macro.uppercase_first_letter('\u201Cwho'))
