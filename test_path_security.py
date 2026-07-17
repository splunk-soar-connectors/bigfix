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
from pathlib import Path


CONNECTOR_SOURCE = Path("bigfix_connector.py").read_text()


def test_site_names_are_encoded_as_single_path_segments():
    assert 'urlparse.quote(str(value), safe="")' in CONNECTOR_SOURCE
    assert 'site_name = _quote_path_segment(param["site_name"])' in CONNECTOR_SOURCE


def test_site_type_is_enforced_in_connector_code():
    assert 'valid_site_types = {"master", "custom", "external", "operator"}' in CONNECTOR_SOURCE
    assert "site_type not in valid_site_types" in CONNECTOR_SOURCE
