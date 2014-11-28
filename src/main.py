#!/usr/bin/env python3
from persona import datasets, object_detector


def main():
    sents = datasets.fetch_dataset('1')
    entities = object_detector.analyze(sents)
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
