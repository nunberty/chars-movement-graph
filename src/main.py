#!/usr/bin/env python3
from persona import datasets, object_detector

def main():
    title, sents = datasets.fetch_dataset('5')
    names = datasets.fetch_character_list(title)
    persons, locations = object_detector.analyze(names, sents)

    # print("\tLOCATIONS:\n")
    # for l in locations:
    #     print(l)
    #
    # print("\tPERSONS:\n")
    # for p in persons:
    #     print(p)

if __name__ == "__main__":
    main()
