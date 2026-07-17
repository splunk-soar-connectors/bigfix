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
CONSTS_SOURCE = Path("bigfix_consts.py").read_text()


def test_xml_document_type_declarations_are_rejected():
    assert '"<!DOCTYPE" in r.text.upper()' in CONNECTOR_SOURCE
    assert "XML document type declarations are not allowed" in CONNECTOR_SOURCE


def test_response_bodies_are_streamed_with_a_hard_size_limit():
    assert "MAX_RESPONSE_BYTES = 5 * 1024 * 1024" in CONSTS_SOURCE
    assert "stream=True" in CONNECTOR_SOURCE
    assert "response.iter_content(chunk_size=64 * 1024)" in CONNECTOR_SOURCE
    assert "len(content) > consts.MAX_RESPONSE_BYTES" in CONNECTOR_SOURCE
