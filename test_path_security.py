from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()


def test_site_names_are_encoded_as_single_path_segments():
    assert 'urlparse.quote(str(value), safe="")' in CONNECTOR_SOURCE
    assert 'site_name = _quote_path_segment(param["site_name"])' in CONNECTOR_SOURCE


def test_site_type_is_enforced_in_connector_code():
    assert 'valid_site_types = {"master", "custom", "external", "operator"}' in CONNECTOR_SOURCE
    assert "site_type not in valid_site_types" in CONNECTOR_SOURCE
