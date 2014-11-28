import collections
# Entity = collections.namedtuple("Entity", ["name", "position"])
# Some experiments with named tuple for hashing my own objects =)

import nltk
nltk.download()
# Symbol Meaning               Example
#
# S      sentence              the man walked
# NP     noun phrase           dog
# VP     verb phrase           saw a park
# PP     prepositional phrase  with a telescope
# Det    determiner            the
# N      noun                  dog
# V      verb                  walked
# P      preposition           in

# Experiments with sentences syntax
groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

grammar = nltk.data.load('grammars/large_grammars/atis_sentences.txt')
print(grammar)

#sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
#parser = nltk.ChartParser(groucho_grammar)
#for tree in parser.parse(sent):
#    print(tree)

#nltk.data.show_cfg('grammars/book_grammars/sql0.fcfg')
