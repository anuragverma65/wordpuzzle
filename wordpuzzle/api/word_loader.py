import os


class WordLoader:
    """Class that provides access to the dictionary"""

    words = None

    @classmethod
    def load_words(cls):
        try:
            cls.words = set()
            app_dir = os.path.dirname(__file__)
            file_path = os.path.join(app_dir, "data", "words.txt")

            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip()
                    cls.words.add(word)
        except Exception as e:
            # Log the exception or print it for debugging
            print(f"Error loading words: {e}")

    @classmethod
    def get_word_set(cls):
        return cls.words
