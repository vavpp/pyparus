from pyparus import UmlParser


def test_parser_exists():
    parser = UmlParser()
    assert parser is not None