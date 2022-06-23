import time
from typing import List, Tuple, Dict
import re
import random
import csv
from lxml import etree
import json
# import lxml.etree as ET


class Joke:
    """The Joke object contains the joke, and some metadata on that joke. One can compare the jokes by upvotes"""
    def __init__(self, raw_joke):
        self.raw_joke = raw_joke
        self.author = self.raw_joke[0]
        self.link = self.raw_joke[1]
        self.joke = self.raw_joke[2]
        self.rating = self.raw_joke[3]
        self.time = self.raw_joke[4]

        self.sentences_joke = self.split_into_sentences()
        self.tokenized_joke = self._tokenize()
        self.filtered_joke = self.filter_profanity()[0]
        self.num_profanities = self.filter_profanity()[1]

        # TODO: Save representations in xml and json
        self.joke_xml = self._get_xml_repr()
        self.joke_json = self._get_json_repr()

    def split_into_sentences(self) -> List[str]:
        """Split text into sentences"""
        output = re.findall(r' ?([^.!?\n]+[.?!]*|\n)', self.joke)
        return output

    def _tokenize(self) -> List[List[str]]:
        """Tokenize all the words in the sentences"""
        output = []
        for sentence in self.sentences_joke:
            tokenized_sentence = re.findall(r'([\w\']+|\?|\.|\n|,|!)', sentence)
            output.append(tokenized_sentence)
        return output

    def filter_profanity(self, filename="profanities.txt") -> Tuple[List[List[str]], int]:
        """Filter out all the profanity"""

        output = []

        # Count number of profanities
        num_profanities = 0

        # Read in profanity file
        with open(filename, "r")as file:
            profanities = file.read().split("\n")

        for sentence in self.tokenized_joke:
            no_profanity = True
            text_sentence = " ".join(sentence)
            for profanity in profanities:

                # Check if there is profanity in the sentence
                if profanity in text_sentence:
                    profanity_in_text = True
                else:
                    profanity_in_text = False

                while profanity_in_text:
                    num_profanities += 1
                    no_profanity = False

                    # Find the index of the profanity
                    index = text_sentence.index(profanity)
                    front = text_sentence[:index - 1]

                    # Find the words that need to be replaced
                    num_words_before_profanity = len(front.split(" "))
                    num_profanity_words = len(profanity.split(" "))
                    profanity_in_sentence = sentence[num_words_before_profanity: num_words_before_profanity + num_profanity_words]

                    # Replace the profanity with '#'
                    replacement = ["#" * len(word) for word in profanity_in_sentence]

                    # Construct new sentence composed of the parts with and without profanity
                    new_sent = []
                    new_sent.extend(sentence[:num_words_before_profanity])
                    new_sent.extend(replacement)
                    new_sent.extend(sentence[num_words_before_profanity + len(replacement):])
                    text_sentence = " ".join(new_sent)
                    sentence = new_sent

                    # Check if there is still profanity in the sentence
                    if profanity in text_sentence:
                        profanity_in_text = True

                    else:
                        profanity_in_text = False
                        output.append(new_sent)

            # Add sentence immediately if there are no profanities in the sentence
            if no_profanity:
                output.append(sentence)
        return output, num_profanities

    def tell_joke(self):
        if len(self.filtered_joke) > 1:
            build_up = self.filtered_joke[:-1]
            punch_line = self.filtered_joke[-1:]

            print(self.pretty_print(build_up))
            time.sleep(1)
            print(self.pretty_print(punch_line))
        else:
            print(self.pretty_print(self.filtered_joke))

    @staticmethod
    def pretty_print(joke) -> str:
        """Print in a humanly readable way"""
        output = ""
        for sentence in joke:
            output += " ".join(sentence) + " "
        return output

    def _get_xml_repr(self) -> etree.Element:
        """Get the xml representation of the Joke with all its attributes as nodes"""
        joke = etree.Element("joke")
        text = etree.SubElement(joke, "text")
        text.text = self.joke
        author = etree.SubElement(joke, "author")
        author.text = self.author
        link = etree.SubElement(joke, "link")
        link.text = self.link
        rating = etree.SubElement(joke, "rating")
        rating.text = str(self.rating)
        time = etree.SubElement(joke, "time")
        time.text = self.time
        profanity_score = etree.SubElement(joke, "profanity_score")
        profanity_score.text = str(self.num_profanities)

        return joke

    def _get_json_repr(self) -> Dict:
        dic = {}
        dic["author"] = self.author
        dic["link"] = self.link
        dic["text"] = self.joke
        dic["rating"] = int(self.rating)
        dic["time"] = self.time
        dic["profanity_score"] = self.num_profanities
        return dic

    def __repr__(self):
        """Allows for printing"""
        return self.pretty_print(self.filtered_joke)

    def __eq__(self, other):
        """Equal rating"""
        return self.rating == other.rating

    def __lt__(self, other):
        """less than rating"""
        return self.rating > other.rating

    def __gt__(self, other):
        """greater than rating"""
        return self.rating < other.rating

    def __le__(self, other):
        """less than or equal rating"""
        return self.rating >= other.rating

    def __ge__(self, other):
        """greater than or equal rating"""
        return self.rating <= other.rating

class JokeGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.jokes = self.make_jokes_objects()

    # TODO: Extend the function to accept json files
    def make_jokes_objects(self):
        with open(self.filename, "r") as lines:

            if self.filename.endswith(".csv"):
                lines = csv.reader(lines, delimiter=',')
                jokes_final = [Joke(row) for row in lines]

            elif self.filename.endswith(".json"):
                lines = json.load(lines)
                jokes_mini = []
                jokes = []

                for k, sub_dics in lines.items():   #k is the number of which dictionary aka which joke it is
                                                    #v are the single dictionaries: {'author': 'enoctis', 'link': 'enoctis', 'text': "Why do flamingos lift one leg? If they lifted both, they'd fall.", 'rating': 10, 'time': '04.01.22 03:56', 'profanity_score': 0}
                    for v in sub_dics.values():
                        jokes_mini.append(v)
                    jokes.append(jokes_mini)
                    jokes_mini = []
                jokes_final = [Joke(row) for row in jokes]

        return jokes_final

    def generate_jokes(self):
        for joke in self.jokes:
            if len(joke.filtered_joke) > 1:
                joke.tell_joke()
            time.sleep(2)

    def random_joke(self):
        joke = random.sample(self.jokes, 1)[0]
        joke.tell_joke()

    def save_jokes_xml(self, outfile: str) -> None:
        """Save all the jokes of the Generator in their xml representation to the outfile"""

        root =  etree.Element("jokes")
        for ele in self.jokes:
            root.append(ele.joke_xml)

        output = etree.tostring(root, encoding='UTF-8', pretty_print=True, xml_declaration=True)
        output_final = output.decode("utf-8")

        with open(outfile, "w", encoding="utf-8") as f1:
            f1.write(output_final)

    def save_jokes_json(self, outfile: str) -> None:
        """Save all the jokes of the Generator in their json representation to the outfile"""
        ober_dic = {}

        for i in range(1,len(self.jokes)):
            ober_dic[str(i)] = self.jokes[i].joke_json

        with open(outfile, "w", encoding="utf-8") as f1:
            json.dump(ober_dic, f1, indent=4)

if __name__ == "__main__":
    pass
    # You can use the following commands for testing your implementation

    #Task 1.1 
    # gen = JokeGenerator("reddit_dadjokes.csv")
    # gen.save_jokes_xml('reddit_dadjokes.xml')
    #Task 1.2
    # gen.save_jokes_json('reddit_dadjokes.json')

    #Task 1.3
    # gen_json = JokeGenerator("reddit_dadjokes.json")
    # gen_json.random_joke()
