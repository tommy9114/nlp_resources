import unittest
from unittest import TestCase

import torch

from nlp_models.bert_wrappers import BertSentencePredictionWrapper, BertTokeniserWrapper, BertWrapper, BertNames


class BertTester(TestCase):

    def test_bert_sentence_prediction_output(self):
        bert_model = BertSentencePredictionWrapper("bert-base-multilingual-cased", "cuda")
        out = bert_model([("this is a sentence.", "the computer are nice persons!")])
        self.assertEqual(out.shape, torch.Size([1, 2]))
        cls = torch.argmax(out, -1)[0].item()
        self.assertEqual(cls, 1)
        print(out.tolist())

        out = bert_model([("this is a sentence", "and this is its consequence")])
        self.assertEqual(out.shape, torch.Size([1, 2]))
        cls = torch.argmax(out, -1)[0].item()
        self.assertEqual(cls, 0)
        print(out.tolist())

    def test_bert_tokeniser(self):
        test_sentence = "this is a stupid test for the tokeniser"
        tokeniser = BertTokeniserWrapper("bert-base-multilingual-cased", "cuda")

        tokens, indexed_tokens, segment_ids, attention_masks = tokeniser.tokenise([test_sentence])
        correct_token_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(tokens[0][0], "[CLS]")
        self.assertTrue(len([x for x in tokens[0] if x == "[SEP]"]) == 1)
        self.assertEqual(segment_ids.tolist()[0], correct_token_class)

        # print(tokens)
        # print(indexed_tokens.tolist())
        # print(segment_ids.tolist())
        # print(attention_masks.tolist())
        test_pair = (test_sentence, "another stupid sentence")

        tokens, indexed_tokens, segment_ids, attention_masks = tokeniser.tokenise([test_pair])
        correct_token_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

        self.assertEqual(tokens[0][0], "[CLS]")
        self.assertTrue(len([x for x in tokens[0] if x == "[SEP]"]) == 2)
        self.assertEqual(segment_ids.tolist()[0], correct_token_class)
        # TODO test batched sentences and limit cases (empty strings) and test strings longer than max tok size.
        # print(tokens)
        # print(indexed_tokens.tolist())
        # print(segment_ids.tolist())
        # print(attention_masks.tolist())

    def test_word_merging(self):
        bert = BertWrapper(BertNames.BERT_BASE_MULTILINGUAL_CASED.value, "cuda")
        bert.eval()
        test_sentence = "this is a stupid test for the tokeniser"
        with torch.no_grad():
            outputs, token_inputs = bert([test_sentence])
        hidde_states = outputs["hidden_states"]
        words, mapping = bert.bert_tokeniser.merge_words(token_inputs["str_tokens"][0])
        word_hidden_states = bert.get_word_hidden_states(hidde_states[0], mapping)
        assert len(words) == word_hidden_states.shape[0]




# if __name__ == "__main__":
#     BertTester().test_bert_sentence_prediction_output()
if __name__ == '__main__':
    BertTester().test_word_merging()
    unittest.main()
