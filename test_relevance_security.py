from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()


def test_hostname_cannot_escape_relevance_string_literal():
    assert "Hostname cannot contain a double quote" in CONNECTOR_SOURCE


def test_relevance_expression_is_encoded_as_a_query_parameter():
    assert "urlparse.urlencode({'relevance': relevance})" in CONNECTOR_SOURCE
