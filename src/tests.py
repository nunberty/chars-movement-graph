import unittest

import text_utils
import object_detector

class TestAlwaysOk(unittest.TestCase):
    def setUp(self):
        pass
    def test_always_ok(self):
        self.assertTrue(True)

class TestFindCapitalizeWords(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty(self):
        test_tokens = ['there', 'are', 'not', 'capitalized', 'words', 'here']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertFalse(capitalized)

    def test_two_one_word_proper(self):
        test_tokens = ['First', 'capitalized', 'word', 'and', 'Second']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertListEqual(capitalized, [('First',), ('Second',)])

    def test_two_many_word_proper(self):
        test_tokens = ['First', 'Proper', 'is', 'less',
                       'capitalized', 'word', 'then', 'Second', 'Proper']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertListEqual(capitalized, [('First', 'Proper',), ('Second','Proper',)])

class TestFindPropers(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty(self):
        sents = []
        ret = text_utils.find_proper(sents)
        self.assertFalse(ret)

    def test_one_proper_one_sent(self):
        sents = ['London is the capital of Great Britain']
        ret = text_utils.find_proper(sents)
        self.assertSetEqual(ret, {(0, ('Great', 'Britain',))})

    def test_one_proper_many_sents(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.']
        ret = text_utils.find_proper(sents)
        self.assertSetEqual(ret, {(0, ('Great', 'Britain',))})

    def test_many_proper_many_sents(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.',
                 'Moscow is the biggest city in Europe.',
                 'Saint Petersburg is situated in the Neva River.',
                 'Saint Petersburg is the biggest city on the Baltic Sea.']
        ret = text_utils.find_proper(sents)
        self.assertSetEqual(ret, {
            (0, ('Great', 'Britain',)),
            (2, ('Europe',)),
            (3, ('Petersburg',)),
            (3, ('Neva', 'River'),),
            (4, ('Petersburg',)),
            (4, ('Baltic', 'Sea'))
        })

class TestGetWordBefore(unittest.TestCase):
    def setUp(self):
        pass

    def test_first_word(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'London')
        self.assertFalse(word)

    def test_word_before_two_words(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'Great Britain')
        self.assertEqual(word, 'of')

    def test_word_before_absence_word(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'the UK')
        self.assertFalse(word)

if __name__ == '__main__':
    unittest.main()
