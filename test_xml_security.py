from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()
CONSTS_SOURCE = Path("bigfix_consts.py").read_text()


def test_xml_document_type_declarations_are_rejected():
    assert '"<!DOCTYPE" in r.text.upper()' in CONNECTOR_SOURCE
    assert "XML document type declarations are not allowed" in CONNECTOR_SOURCE


def test_response_bodies_are_streamed_with_a_hard_size_limit():
    assert "MAX_RESPONSE_BYTES = 5 * 1024 * 1024" in CONSTS_SOURCE
    assert "stream=True" in CONNECTOR_SOURCE
    assert "response.iter_content(chunk_size=64 * 1024)" in CONNECTOR_SOURCE
    assert "len(content) > consts.MAX_RESPONSE_BYTES" in CONNECTOR_SOURCE
