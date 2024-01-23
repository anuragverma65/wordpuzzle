from django.test import TestCase
from api.models import WordPuzzle


class WordPuzzleTestCase(TestCase):
    def test_shortest_sequence(self):
        # Create an instance of WordPuzzle
        word_puzzle = WordPuzzle()

        result_sequence = word_puzzle.shortest_sequence("mad", "dog")

        expected_response = ["mad", "dad", "dod", "dog"]

        self.assertEqual(result_sequence, expected_response)

    def test_shortest_sequence_not_found(self):
        word_puzzle = WordPuzzle()

        result_sequence = word_puzzle.shortest_sequence("abhode", "zurich")

        expected_response = []

        self.assertEqual(result_sequence, expected_response)

    def test_shortest_sequence_same_words(self):
        word_puzzle = WordPuzzle()

        result_sequence = word_puzzle.shortest_sequence("abhi", "abhi")

        expected_response = []

        self.assertEqual(result_sequence, expected_response)

    def test_generate_words(self):
        word_puzzle = WordPuzzle()

        # Check the generated words list length for a specific input word and position
        input_word = "cat"
        position = 1
        expected_length = 26
        result = word_puzzle.generate_words(input_word, position)
        self.assertEqual(len(result), expected_length)
