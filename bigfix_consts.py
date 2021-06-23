# --
# File: bigfix_consts.py
#
# Copyright (c) 2017-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --

BIGFIX_SITE_TYPE_DICT = {
        "ExternalSite": "external",
        "CustomSite": "custom",
        "OperatorSite": "operator",
        "ActionSite": "action"}
BIGFIX_CONNECTING_PROGRESS = "Connecting to BigFix"
EMPTY_RESPONSE = "Empty response and no information in the header"
CANNOT_PARSE_ERROR = "Cannot parse error details"
SUCCESSFULLY_RETRIEVED = "Successfully retrieved BigFix ID from Host Name"
COULD_NOT_PARSE = "Could not parse reply"
TEST_CONNECTIVITY_PASSED = "Test Connectivity Passed"
ERROR_CODE_EXCEPTION = "Error code unavailable"
ERROR_MSG_EXCEPTIOIN = "Unknown error occurred. Please check the asset configuration and|or action parameters."
