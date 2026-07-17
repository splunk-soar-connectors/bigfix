# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()
APP_JSON = json.loads(Path("bigfix.json").read_text())


def test_tls_verification_defaults_on_and_is_used_for_requests():
    assert APP_JSON["configuration"]["verify_server_cert"]["default"] is True
    assert 'config.get("verify_server_cert", True)' in CONNECTOR_SOURCE
    assert "verify=self._verify" in CONNECTOR_SOURCE
