import unittest
import gensent
import nltk

class TestSentenceGenerator(unittest.TestCase):
    sentence_list = [
        'I am Sam, Sam-I-am.', 
        'That Sam-I-am.', 
        'That Sam-I-am.', 
        'I do not like that Sam-I-am.',
        'Do you like green eggs and ham?'    
    ]
    
    def test_generator_unprepared(self):
        """Make sure an unprepared sentence generator throws an error."""
        sentences = gensent.SentenceGenerator()
        self.assertRaises(Exception, sentences._gen_sentences())

    def test_two_passes(self):
        """Make sure we can make two passes over the sentence generator iterator."""
        sentences = gensent.SentenceGenerator()
        sentences.read_sentence_list(self.sentence_list)
        #the list() function makes one pass over an iterator, so just do it 2x
        self.assertEqual(list(sentences), list(sentences))

    def test_process_sentence(self):
        sentences = gensent.SentenceGenerator()
        result = sentences._process_sentence(self.sentence_list[0])
        correct = ['i', 'am', 'sam', 'sam-i-am']
        self.assertEqual(result, correct)

    def test_process_sentence_russian(self):
        sentences = gensent.SentenceGenerator(language='russian')
        result = sentences._process_sentence("Три девицы под окном Пряли поздно вечерком.")
        correct = ['три', 'девицы', 'под', 'окном', 'пряли', 'поздно', 'вечерком']
        self.assertEqual(result, correct)

    def test_process_US_money(self):
        sentences = gensent.SentenceGenerator()
        result = sentences._process_sentence("Breakfast cost me $5.60")
        correct = ['breakfast', 'cost', 'me', sentences.NUM]
        self.assertEqual(result, correct)

    def test_process_EU_money(self):
        sentences = gensent.SentenceGenerator()
        result = sentences._process_sentence("Breakfast cost me €5.60")
        correct = ['breakfast', 'cost', 'me', sentences.NUM]
        self.assertEqual(result, correct)
    
    def test_process_numbers(self):
        sentences = gensent.SentenceGenerator()
        result = sentences._process_sentence("Pi is 3.14159")
        correct = ['pi', 'is', sentences.NUM]
        self.assertEqual(result, correct)

if __name__ == '__main__':
    unittest.main()
