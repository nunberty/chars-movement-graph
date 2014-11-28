import xml.etree.ElementTree as ET

import nltk

from . import config


def fetch_dataset(name):
    """ Returns sentencses of the named dataset"""
    dataset_dir = config.DATASETS_DIR / name
    if not dataset_dir.exists():
        raise Exception("Can't find dataset {}".format(name))
    dataset_file = dataset_dir / "{}.fb2".format(name)
    tokenizer = _load_tokenizer('english')
    return _fb2_to_sents(dataset_file, tokenizer)


def _fb2_to_sents(file_path, tokenizer):
    tree = ET.parse(str(file_path))
    sents = []
    for body in tree.find('body'):
        for p in body.findall('p'):
            if p.text:
                sents.extend(tokenizer.tokenize(p.text.strip()))
    return sents

def _load_tokenizer(language):
    return nltk.data.load('tokenizers/punkt/{}.pickle'.format(language))
