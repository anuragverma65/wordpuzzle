from django.db import models
from collections import deque
from .word_loader import WordLoader


class WordPuzzle(models.Model):
    start_word = models.CharField(max_length=50)
    end_word = models.CharField(max_length=50)
    sequence = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_word} to {self.end_word} at {self.timestamp}"

    def shortest_sequence(self, start, target):
        """
        Find the shortest sequence of word transformations from a start word to a target word using breadth-first search.

        :param start: The starting word.
        :param target: The target word.
        :return: A list representing the shortest sequence of word transformations, or an empty list if no path exists.
        """
        if start == target:
            return []

        words = WordLoader.get_word_set()
        visited = set()
        wordLength = len(start)

        queue = deque()
        queue.append((start, [start]))

        while queue:
            current_word, path = queue.popleft()
            word = list(current_word)

            for pos in range(wordLength):
                orig_char = word[pos]
                for new_word in self.generate_words(word, pos):
                    if new_word == target:
                        return path + [target]

                    if new_word not in visited:
                        visited.add(new_word)
                        if new_word in words:
                            # TODO: Future improvements: Integrate A* algorithm with a heuristic function in case of API performance issues.
                            queue.append((new_word, path + [new_word]))
                word[pos] = orig_char
        return []

    def generate_words(self, word, pos):
        """
        Generate a list of words by changing the character at the specified position in the given word.

        :param word: The input word.
        :param pos: The position at which to change the character.
        :return: A list of words obtained by replacing the character at the specified position.
        """
        new_words = []

        for c in range(ord("a"), ord("z") + 1):
            new_word = "".join(list(word[:pos]) + [chr(c)] + list(word[pos + 1 :]))
            new_words.append(new_word)
        return new_words
