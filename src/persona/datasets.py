import xml.etree.ElementTree as ET

import nltk
import urllib
import bs4

from . import config

def fetch_dataset(name):
    """ Returns sentencses of the named dataset. """
    dataset_dir = config.DATASETS_DIR / name
    if not dataset_dir.exists():
        raise Exception("Can't find dataset {}".format(name))
    dataset_file = dataset_dir / "{}.fb2".format(name)
    tokenizer = _load_tokenizer('english')
    return _get_book_name(dataset_file), _fb2_to_sents(dataset_file, tokenizer)

def _get_book_name(dataset_file):
    title_path = 'description/title-info/book-title'
    tree = ET.parse(str(dataset_file))
    for description in tree.getroot().findall(title_path):
        return description.text

def fetch_character_list(book_name):
    def prepare_book_name(book_name):
        return '-'.join(book_name.split())

    name = prepare_book_name(book_name)
    url = 'http://www.cliffsnotes.com/literature/'
    url += name[0] + '/' + name + '/character-list'
    page = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(page.read().decode('utf8'))
    return [next(x.children).text for x in soup.select('.litNoteText')]

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
