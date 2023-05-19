# This test has been modified from https://raw.githubusercontent.com/huggingface/transformers/50a8ed3ee02a02550d7055d1539de5b12358cf26/tests/pipelines/test_pipelines_summarization.py

import unittest

from transformers import pipeline
from rouge_score import rouge_scorer


cnn_article = (
    " (CNN)The Palestinian Authority officially became the 123rd member of the International Criminal Court on"
    " Wednesday, a step that gives the court jurisdiction over alleged crimes in Palestinian territories. The"
    " formal accession was marked with a ceremony at The Hague, in the Netherlands, where the court is based."
    " The Palestinians signed the ICC's founding Rome Statute in January, when they also accepted its"
    ' jurisdiction over alleged crimes committed "in the occupied Palestinian territory, including East'
    ' Jerusalem, since June 13, 2014." Later that month, the ICC opened a preliminary examination into the'
    " situation in Palestinian territories, paving the way for possible war crimes investigations against"
    " Israelis. As members of the court, Palestinians may be subject to counter-charges as well. Israel and"
    " the United States, neither of which is an ICC member, opposed the Palestinians' efforts to join the"
    " body. But Palestinian Foreign Minister Riad al-Malki, speaking at Wednesday's ceremony, said it was a"
    ' move toward greater justice. "As Palestine formally becomes a State Party to the Rome Statute today, the'
    ' world is also a step closer to ending a long era of impunity and injustice," he said, according to an'
    ' ICC news release. "Indeed, today brings us closer to our shared goals of justice and peace." Judge'
    " Kuniko Ozaki, a vice president of the ICC, said acceding to the treaty was just the first step for the"
    ' Palestinians. "As the Rome Statute today enters into force for the State of Palestine, Palestine'
    " acquires all the rights as well as responsibilities that come with being a State Party to the Statute."
    ' These are substantive commitments, which cannot be taken lightly," she said. Rights group Human Rights'
    ' Watch welcomed the development. "Governments seeking to penalize Palestine for joining the ICC should'
    " immediately end their pressure, and countries that support universal acceptance of the court's treaty"
    ' should speak out to welcome its membership," said Balkees Jarrah, international justice counsel for the'
    " group. \"What's objectionable is the attempts to undermine international justice, not Palestine's"
    ' decision to join a treaty to which over 100 countries around the world are members." In January, when'
    " the preliminary ICC examination was opened, Israeli Prime Minister Benjamin Netanyahu described it as an"
    ' outrage, saying the court was overstepping its boundaries. The United States also said it "strongly"'
    " disagreed with the court's decision. \"As we have said repeatedly, we do not believe that Palestine is a"
    ' state and therefore we do not believe that it is eligible to join the ICC," the State Department said in'
    ' a statement. It urged the warring sides to resolve their differences through direct negotiations. "We'
    ' will continue to oppose actions against Israel at the ICC as counterproductive to the cause of peace,"'
    " it said. But the ICC begs to differ with the definition of a state for its purposes and refers to the"
    ' territories as "Palestine." While a preliminary examination is not a formal investigation, it allows the'
    " court to review evidence and determine whether to investigate suspects on both sides. Prosecutor Fatou"
    ' Bensouda said her office would "conduct its analysis in full independence and impartiality." The war'
    " between Israel and Hamas militants in Gaza last summer left more than 2,000 people dead. The inquiry"
    " will include alleged war crimes committed since June. The International Criminal Court was set up in"
    " 2002 to prosecute genocide, crimes against humanity and war crimes. CNN's Vasco Cotovio, Kareem Khadder"
    " and Faith Karimi contributed to this report."
)
cnn_summary = (
    " The Palestinian Authority becomes the 123rd member of the International Criminal Court . The move gives"
    " the court jurisdiction over alleged crimes in Palestinian territories . Israel and the United States"
    " opposed the Palestinians' efforts to join the court . Rights group Human Rights Watch welcomes the move,"
    " says governments seeking to penalize Palestine should end pressure ."
)

class SummarizationPipelineTests(unittest.TestCase):


    def test_integration_torch_summarization(self):
        summarizer = pipeline(task="summarization",
                              model='sshleifer/distilbart-cnn-12-6')
        result = summarizer(cnn_article)
        self.assertEqual(result[0]["summary_text"], cnn_summary)

    # Evaluating the model performance by comparing the two texts
    # https://huggingface.co/spaces/evaluate-metric/rouge
    def test_evaluate_rouge_score(self):
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        scores = scorer.score(cnn_article, cnn_summary)
        self.assertGreaterEqual(scores["rouge1"].precision, 0.8)
        self.assertGreaterEqual(scores["rouge2"].precision, 0.7)
        self.assertGreaterEqual(scores["rougeL"].precision, 0.8)
