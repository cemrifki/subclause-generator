"""
subclauses.py
This module (version 0.2.0) provides functionality for generating subclauses from sentences in English and 
Turkish, using spaCy for dependency parsing. It includes preprocessing utilities for tokenization and 
normalization, and a SubclauseGenerator class that segments sentences into subclauses based on dependency 
relationships. The module is designed for aspect-based sentiment analysis and can be extended for other NLP 
tasks.
Classes:
    SubclauseGenerator: Generates subclauses from input sentences using dependency parsing.
Functions:
    normalize_tokenize(string): Preprocesses and tokenizes input text.
    main(args=None): Example usage of SubclauseGenerator.
Usage:
    Run the module directly to see example subclause extraction for Turkish sentences.
    The SubclauseGenerator can be instantiated for English ("en") or Turkish ("tr") and used to
    convert sentences into lists of subclauses. Several examples are also provided in the main method.

    
Author: Cem Rifki Aydin
Date: 06.09.2025

"""

import re
from collections import defaultdict

import spacy 


# Punctuation marks across the module can be handled more efficiently and consistently in future.
p = re.compile(r"([.?!])[\"\']*$")
tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')


# Preprocessing is performed through the below function.
def normalize_tokenize(string):
    """
    This is a basic, generic tokenizer.

    :param string: Text to be tokenized.
    :type string: str
    :return: String in a tokenized form that is to be split later by other helper methods.
    :rtype: str
    """
    string = string.lower()
    # HTML tags are removed by the below line of code.
    string = tag_re.sub(' ', string)
    # This is added to reduce the same characters appearing consecutively more than twice
    # to the same two chars only.
    string = re.sub(r"(.)(\1)\1{2,}", r"\1\1\1", string)
    # Added, since mentions (e.g. @trump) do not contribute to sentiment.
    string = re.sub(r"@[a-zA-ZçÇğĞıİöÖşŞüÜ0-9()#,!?:=;\-\\'`./]+", r"", string)
    # Some extra chars are added to be taken into account.
    string = re.sub(r"[^A-Za-zçÇğĞıİöÖşŞüÜ0-9()#,!?:=;\-\\'`./]", " ", string)

    # Numeric forms and emoticons, such as 22:30, are not disrupted.
    string = re.sub(r"([^\d)(])([,.:;]+)([^\d()]|$)", r"\1 \2 \3", string)
    # The punctuation marks "?" and "!" can be indicative of expressing sentiment. These
    # are therefore not removed.
    string = re.sub(r"([!?]+)", r" \1 ", string)

    # The below four regex commands are implemented to put blank spaces before or after
    # parens without disrupting emoticons.

    string = re.sub(r"\(([A-Za-zçÇğĞıİöÖşŞüÜ0-9,!?\-\\'`])", r"( \1", string)
    string = re.sub(r"([A-Za-zçÇğĞıİöÖşŞüÜ0-9,!?\-\\'`])\(", r"\1 (", string)

    string = re.sub(r"([A-Za-zçÇğĞıİöÖşŞüÜ0-9,!?\-\\'`])\)", r"\1 )", string)
    string = re.sub(r"\)([A-Za-zçÇğĞıİöÖşŞüÜ0-9,!?\-\\'`])", r") \1", string)

    # "(?!)" and similar forms that likely indicate sarcasm are kept.
    string = re.sub(r"(\() +([?!]+) +(\))", r"\1\2\3", string)
    # Useless parens are removed.
    string = re.sub(r"(^|[ ])+([()]+)([ ]+|$)", r" ", string)
    # Other useless punctuations are also eliminated.
    string = re.sub(r"(^|[ ])+([.;,]+)([ ]+|$)", r" ", string)

    # Emoticons ":s" and ":D".
    string = re.sub(r"((\s|^)[:]+)[ ]+([dDsSpP]+(\s|$))", r"\1\3", string)
    # Emoticon handling.
    string = re.sub(r"([:;.]+)([()dDsSpP]+)", r" \1\2 ", string)

    string = re.sub(r"\s{2,}", " ", string)
    return string


class SubclauseGenerator:
    """
    This class is used to generate subclauses from texts.
    """

    # The below basic set can be expanded with other relationships that you think mark the beginning of the
    # existence of subclauses with respect to the dependency tree of the input.
    subclause_marker_relationships = {"conj", "ccomp"}

    def __init__(self, lang: str):
        self.lang = lang  # "en" for English, "tr" for Turkish
        if self.lang not in ("en", "tr"):
            raise ValueError(f"Unsupported language '{self.lang}'. Only 'en' and 'tr' are supported.")
        
        # For Turkish scenario, you can also update the code to leverage tr_core_news_trf
        self.lang_model = "tr_core_news_lg" if self.lang == "tr" else "en_core_web_sm"  

        # Attempt to download the model (only if not already installed)
        try:
            self.nlp = spacy.load(self.lang_model)
        except OSError:
            print(f"Downloading {self.lang_model} model...")
            spacy.cli.download(self.lang_model)
            self.nlp = spacy.load(self.lang_model)


        self.conj_and_punc_list = ["ve", "veya", "ama", "buna rağmen", "ayrıca", "?", "!", ".", ",", ":", ";", ] if self.lang == "tr" \
            else ["and", "or", "but", "however", "also", "?", "!", ".", ",", ":", ";", ]



    def convert_to_subclauses(self, sentence):
        """
        The helper method that converts a sentence as a whole in string format to its corresponding subclauses.
        This actually is not used in this project, but can be employed by anyone who wants
            to break a sentence in string format into its subclauses as list.

        :param sentence: An input string: sentence to be broken down into its subclauses.
        :type sentence: str
        :return: The result subclauses from this sentence.
        :rtype: list of lists
        """

        # A basic tokenizer is used to perform preprocessing operations. This could be skipped as well.
        # Instead, you can use your own tokenizer provided that the output is of type str.
        sentence = normalize_tokenize(sentence)

        str_sentence_arr = [tok.text for tok in self.nlp(sentence)]

        str_sentence = " ".join(str_sentence_arr)
        final_punc_mark = self.final_punc_mark(str_sentence)

        str_sentence = re.sub(r"[ ]+", r" ", str_sentence)
        rev_subclauses = self.get_all_subclauses_of_sent(str_sentence)

        subclauses_with_puncs = []

        # The below block is mainly used to handle the final punctuation mark.
        for ind, rev_subclause in enumerate(rev_subclauses):
            adapted_subcl = self.remove_trailing_puncs(" ".join(rev_subclause))
            # The final punctuation mark of the last sentence is appended to the end of all
            # sentences. This could be updated and enhanced.
            adapted_subcl += " " + final_punc_mark

            updated_sentence = adapted_subcl.strip().split()
            subclauses_with_puncs.append(updated_sentence)
        return subclauses_with_puncs

    def final_punc_mark(self, s):
        """
        This method is used to detect the final punctuation mark at the end of the text.

        :param s: Text string.
        :type s: str
        :return: Punctuation mark at the end of the text.
        :rtype: str
        """

        res = re.search(p, s)
        final_punc = res.group(1) if res else "."
        return final_punc

    def get_children_recurs(self, tok, lev):
        """
        This method finds the children nodes of a target word recursively, all of which
            on a whole constitute a subclause.
        If the dependency relations stated in the subclause_marker_relationships set are encountered,
            it marks the existence of a new subclause and therefore the recursively scanning mechanism
            is stopped. However, this rule set could be expanded with other dependency relationships.

        :param tok: The target token whose children in the subclause are to be generated.
        :type tok: spacy.tokens.token.Token
        :param lev: The height (level) of the recursive tree.
        :type lev: int
        :return: All the kids of a token in a recursive subclause tree.
        :rtype: set
        """

        all_children = set([])
        if lev == 0:
            all_children.add(tok.text + "-" + str(tok.i))
        lev += 1
        for kid in tok.children:
            tag = kid.tag_.lower()
            dep = kid.dep_.lower()
            
            # print(tag, dep, kid.text, kid.i)
            # print(tok.lemma_.lower(), tok.pos_ , tok.is_alpha, tok.is_stop)

            # The below if statement segments the text into subclauses if the parser encounters a
            # subclause-related dependency relationship and a verb marking its existence.
            # if (dep in self.subclause_marker_relationships) and (tag == "vbd" or tag == "vbz" or tag == "vbg"):
            if (dep in self.subclause_marker_relationships) and (tag == "verb" or tag == "vbd" or tag == "vbz" or tag == "vbg"):
                # print("Subclause marker found: ", dep, " for token: ", kid.text)
                continue
            all_children.add(kid.text + "-" + str(kid.i))
            all_children |= self.get_children_recurs(kid, lev)
        return all_children

    def get_all_deps(self, sentence):
        """
        This helper method generates all the tokens which are connected to each other
        via a dependency relationship.

        :param sentence: The input text (e.g. sentence).
        :type sentence: str
        :return: All the words connected to each other via dependency relationships in the
            same subclause.
        :rtype: list
        """

        doc = self.nlp(sentence)
        res = [self.get_children_recurs(token, 0) for token in doc]
        return res

    def get_all_subclauses_of_sent(self, sentence):
        """
        This helper method generates the set of all subclauses from a given sentence.

        :param sentence: The input text (e.g. sentence).
        :type sentence: str
        :return: All the subclauses generated from "sentence".
        :rtype: list
        """

        sent = sentence.strip()
        final_punc = sent[-1]
        if not re.match(r"[?.!]+$", final_punc):
            final_punc = "."
        subclauses = defaultdict(set)
        all_deps = self.get_all_deps(sent)
        all_toks = set({})
        for dep in all_deps:
            for tok in dep:
                all_toks.add(tok)
                if len(subclauses[tok]) < len(dep):
                    subclauses[tok] = dep
        final_subclauses = set([tuple(subclauses[tok]) for tok in all_toks])

        final_subclauses_tmp = set({})
        for ind, subcl in enumerate(final_subclauses):
            subcl = list(subcl)
            # Words in a subclause become ordered thanks to the below code.
            subcl.sort(key=lambda token: int(token[token.rindex("-") + 1:]))
            final_subclauses_tmp.add(tuple(subcl))

        # Subclauses are ordered thanks to the below two lines of code.
        final_subclauses_tmp = list(final_subclauses_tmp)
        final_subclauses_tmp.sort(key=lambda token: int(token[0][token[0].rindex("-") + 1:]))

        final_subclauses_upd = []

        for subcl in final_subclauses_tmp:
            subcl = list(subcl)
            subcl = self.remove_ind(subcl)
            if subcl[-1] not in ".?!;:":
                subcl = subcl + [final_punc]
            subcl = self.remove_trailing_conjs_and_puncs(subcl, self.conj_and_punc_list)
            final_subclauses_upd.append(subcl)
        return final_subclauses_upd

    def remove_ind(self, s):
        """
        This is a helper method, which removes the hyphen and index information
        from the end of a token. This is a supplementary function.

        :param s: A list of words (i.e. sentence or a whole review).
        :type s: list
        :return: Words stripped of their hyphen and rudimentary suffixes.
        :rtype: list
        """

        return [re.sub(re.compile(r"(.*)-[0-9]+"), r"\1", tok) for tok in s]

    def remove_trailing_puncs(self, s):
        """
        A helper method that removes the trailing punctuation marks.

        :param s: A text input.
        :type s: str
        :return: The text stripped off its unnecessary punctuation marks.
        :rtype: str
        """

        return re.sub(r"[,;:.?!\"]+$", r"", s)

    def remove_trailing_conjs_and_puncs(self, s, conjunction_list):
        """
        This method removes the trailing conjunctions and punctuation marks that are specified
        in the variable conj_and_punc_list.
        This is useful, since a subclause cannot in general start with a punctuation mark or, say "and".


        :param s: A list of tokens (e.g. a sentence).
        :type s: list
        :param conjunction_list: The list of conjunctions and punctuation marks.
        :type conjunction_list: list
        :return: The sentence or subclause stripped off its unnecessary conjunctions or
            punctuation marks in the beginning or end.
        :rtype: list
        """

        if len(s) <= 1:
            return s
        while True:
            neither_conj = 0
            if s[0] in conjunction_list:
                s = s[1:]
                neither_conj += 1
            if s[-1] in conjunction_list:
                s = s[:-1]
                neither_conj += 2
            if neither_conj == 0 or len(s) <= 1:
                break
        return s


def main(args=None):
    # Examples for English
    sc_en = SubclauseGenerator("en")

    # The below is an example that converts a sentence into the subclauses thereof.
    print(sc_en.convert_to_subclauses("The service was awesome, and the food was incredible!"))

    # An example for Turkish
    sc_tr = SubclauseGenerator("tr")

    print(sc_tr.convert_to_subclauses("Yemek çok iyiydi ve servis de süperdi."))

if __name__ == "__main__":
    main()
