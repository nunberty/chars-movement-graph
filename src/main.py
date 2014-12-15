#!/usr/bin/env python3
from persona import datasets, object_detector


def main():
    title, sents = datasets.fetch_dataset('5')
    names = datasets.fetch_character_list(title)
    entities = object_detector.analyze(names, sents)

    print("\tLOCATIONS:\n")
    for e in entities:
        if e.is_location:
            print(e)

    print("\tPERSONS:\n")
    for e in entities:
        if e.is_person:
            print(e)

    print("\tUNKNOWN:\n")
    for e in entities:
        if not (e.is_person or e.is_location):
            print(e)

if __name__ == "__main__":
    main()
