import unittest

import text_utils
import object_detector
import model

class TestAlwaysOk(unittest.TestCase):
    def test_always_ok(self):
        # for test system test
        self.assertTrue(True)

class TestFindCapitalizeWordsInTextUtils(unittest.TestCase):
    def test_find_capitalized_should_return_empty_set(self):
        test_tokens = ['there', 'are', 'not', 'capitalized', 'words', 'here']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertFalse(capitalized)

    def test_find_capitalized_should_return_two_capitalized_words_from_begin_and_and_of_sentence(self):
        test_tokens = ['First', 'capitalized', 'word', 'and', 'Second']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertListEqual(capitalized, [('First',), ('Second',)])

    def test_find_capitalized_should_return_list_ofx_two_tuple_of_two_words_from_number_of_sentences(self):
        test_tokens = ['First', 'Proper', 'is', 'less',
                       'capitalized', 'word', 'then', 'Second', 'Proper']
        capitalized = text_utils.find_capitalize_words(test_tokens)
        self.assertListEqual(
            capitalized,
            [('First', 'Proper'), ('Second','Proper')]
        )

class TestFindPropersInTextUtils(unittest.TestCase):
    def test_find_proper_should_return_empty_set_of_propers(self):
        sents = []
        ret = text_utils.find_proper(sents)
        self.assertFalse(ret)

    def test_find_proper_should_ignore_first_proper_and_return_one_proper_as_tuple(self):
        sents = ['London is the capital of Great Britain']
        ret = text_utils.find_proper(sents)
        self.assertEqual(ret, {(0, ('Great', 'Britain',))})

    def test_find_proper_should_not_depend_on_count_of_sentences(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.']
        ret = text_utils.find_proper(sents)
        self.assertSetEqual(ret, {(0, ('Great', 'Britain',))})

    def test_find_proper_should_ignore_only_first_words_and_return_part_of_propers_ect(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.',
                 'Moscow is the biggest city in Europe.',
                 'Saint Petersburg is situated in the Neva River.',
                 'Saint Petersburg is the biggest city on the Baltic Sea.']
        ret = text_utils.find_proper(sents)
        self.assertSetEqual(set(ret), {
            (0, ('Great', 'Britain',)),
            (2, ('Europe',)),
            (3, ('Petersburg',)),
            (3, ('Neva', 'River'),),
            (4, ('Petersburg',)),
            (4, ('Baltic', 'Sea'))
        })

class TestGetWordBeforeInTextUtils(unittest.TestCase):
    def test_get_word_before_should_return_empty_string_if_input_word_is_the_first_in_sentence(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'London')
        self.assertFalse(word)

    def test_get_word_before_should_return_preposition(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'Great Britain')
        self.assertEqual(word, 'of')

    def test_get_word_before_should_return_empty_string_for_absence_input_word(self):
        sent = 'London is the capital of Great Britain.'
        word = text_utils.get_word_before(sent, 'the UK')
        self.assertFalse(word)

class TestFindPropersInSentsInObjectDetector(unittest.TestCase):
    def test_find_propers_should_return_empty_set(self):
        sents = []
        ret = object_detector.find_propers(sents)
        self.assertFalse(ret)

    def test_find_propers_should_return_one_two_wirds_proper(self):
        sents = ['London is the capital of Great Britain']
        ret = object_detector.find_propers(sents)
        self.assertEqual(
            ret, [model.NamedObject({0}, {('Great', 'Britain',)})])

    def test_find_propers_should_skip_propers_if_it_is_the_first_in_sentence(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.']
        ret = object_detector.find_propers(sents)
        self.assertEqual(ret, [model.NamedObject({0}, {('Great', 'Britain',)})])

    def test_find_propers_should_return_all_propers_from_the_end_of_number_of_sentences(self):
        sents = ['London is the capital of Great Britain.',
                 'Moscow is the port of five seas.',
                 'Moscow is the biggest city in Europe.',
                 'Saint Petersburg is situated in the Neva River.',
                 'Saint Petersburg is the biggest city on the Baltic Sea.']
        ret = object_detector.find_propers(sents)
        self.assertEqual(set(ret), {
            model.NamedObject({0}, {('Great', 'Britain',)}),
            model.NamedObject({2}, {('Europe',)}),
            model.NamedObject({3}, {('Petersburg',)}),
            model.NamedObject({3}, {('Neva', 'River')}),
            model.NamedObject({4}, {('Petersburg',)}),
            model.NamedObject({4}, {('Baltic', 'Sea',)})
        })

class TestReducePropersInObjectDetector(unittest.TestCase):
    def test_reduce_propers_should_not_join_different_propers(self):
        propers = [
            model.NamedObject({0}, {('Great', 'Britain',)}),
            model.NamedObject({2}, {('Europe',)})
        ]
        ret = object_detector.reduce_propers(propers)
        self.assertListEqual(ret, propers)

    def test_reduce_propers_should_join_on_two_same_propers(self):
        propers = [
            model.NamedObject({0}, {('Great', 'Britain',)}),
            model.NamedObject({2}, {('Britain',)})
        ]
        ret = object_detector.reduce_propers(propers)[0]
        self.assertEqual(
            model.NamedObject(
                {0, 2}, {('Great', 'Britain',),('Britain',)}),
            ret)
