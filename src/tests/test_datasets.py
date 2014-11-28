import pytest

from persona import datasets

def test_can_fetch_existing_fb2_dataset():
    sents = datasets.fetch_dataset('1')
    assert (len(sents) > 42)

def test_raises_exception_for_non_existing_dataset():
    with pytest.raises(Exception):
        datasets.fetch_dataset("Plan 9 From Outer Space")
