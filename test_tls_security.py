import json
from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()
APP_JSON = json.loads(Path("bigfix.json").read_text())


def test_tls_verification_defaults_on_and_is_used_for_requests():
    assert APP_JSON["configuration"]["verify_server_cert"]["default"] is True
    assert 'config.get("verify_server_cert", True)' in CONNECTOR_SOURCE
    assert "verify=self._verify" in CONNECTOR_SOURCE
