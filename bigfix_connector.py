# --
# File: bigfix_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import bigfix_consts as consts
import xmltodict
import requests
import json
from bs4 import BeautifulSoup
from lxml import etree


class RetVal(tuple):
    def __new__(cls, val1, val2):
        return tuple.__new__(RetVal, (val1, val2))


class BigfixConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(BigfixConnector, self).__init__()

        self._auth = None
        self._state = None
        self._verify = None
        self._base_url = None

    def initialize(self):

        config = self.get_config()

        self._base_url = config['url'] + ('api/' if config['url'].endswith('/') else '/api/')
        self._auth = (config['username'], config['password'])
        self._verify = config['verify_server_cert']
        self._state = self.load_state()

        return phantom.APP_SUCCESS

    def finalize(self):

        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _process_empty_reponse(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code,
                error_text)

        message = message.replace('{', '{{').replace('}', '}}')

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_text_response(self, r, action_result):

        if r.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {'response': r.text})

        message = "Error from server: {0}".format(
                r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_xml_response(self, r, action_result):

        # Try to parse a dict
        try:
            resp_json = xmltodict.parse(r.text)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse XML response. Error: {0}".format(str(e))), None)

        if r.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        message = "Error from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process an xml response
        if 'xml' in r.headers.get('Content-Type', ''):
            return self._process_xml_response(r, action_result)

        # Process a plain-text response
        if 'plain' in r.headers.get('Content-Type', ''):
            return self._process_text_response(r, action_result)

        # Process an HTML resonse
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, body=None, method="get"):

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                            url,
                            data=body,
                            auth=self._auth,
                            verify=self._verify,
                            headers={'Content-Type': 'text/xml'})
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), None)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to BigFix")

        ret_val, response = self._make_rest_call('login', action_result)

        if (phantom.is_fail(ret_val)):
            self.save_progress("Test Connectivity Failed. Error: {0}".format(action_result.get_message()))
            return action_result.get_status()

        if not response.get('response', '').startswith('ok'):
            self.save_progress("Test Connectivity Failed. Could not get response from server.")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _parse_sites(self, action_result, sites, site_type):

        parsed_sites = []
        for site in sites:

            site_name = site['Name']
            if site_name == 'ActionSite':
                endpoint = 'site/master'
            else:
                endpoint = 'site/{0}/{1}'.format(consts.BIGFIX_SITE_TYPE_DICT[site_type], site_name)
            ret_val, response = self._make_rest_call(endpoint, action_result)

            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            site_data = response['BES'][site_type]
            site_data['Type'] = site_type
            parsed_sites.append(site_data)

        return parsed_sites

    def _handle_list_sites(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        ret_val, response = self._make_rest_call('sites', action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        parsed_sites = []
        for site_type in consts.BIGFIX_SITE_TYPE_DICT:

            sites = response.get('BESAPI', {}).get(site_type, [])
            if isinstance(sites, dict):
                sites = [sites]

            parsed_sites += self._parse_sites(action_result, sites, site_type)

        action_result.add_data({'Sites': parsed_sites})

        summary = action_result.update_summary({})
        summary['num_sites'] = len(parsed_sites)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_fixlets(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        site_name = param['site_name']
        site_type = param['site_type']

        ret_val, response = self._make_rest_call('fixlets/{0}/{1}'.format(site_type, site_name), action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        fixlet_json = response.get('BESAPI', {}).get('Fixlet', [])
        if isinstance(fixlet_json, dict):
            fixlet_json = [fixlet_json]

        fixlets = []
        for fixlet in fixlet_json:
            fixlet['LastModified'] = fixlet.pop('@LastModified')
            fixlet['Resource'] = fixlet.pop('@Resource')
            fixlets.append(fixlet)

        action_result.add_data({'Fixlets': fixlets})

        summary = action_result.update_summary({})
        summary['num_fixlets'] = len(fixlets)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_endpoints(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        ret_val, response = self._make_rest_call('computers', action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        computers = response.get('BESAPI', {}).get('Computer', [])
        if isinstance(computers, dict):
            computers = [computers]

        count = 0
        for computer in computers:

            comp_id = computer['ID']
            ret_val, response = self._make_rest_call('computer/{0}'.format(comp_id), action_result)

            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            computer_data = response.get('BESAPI', {}).get('Computer')
            if not computer_data:
                continue

            for prop_dict in computer_data.pop('Property'):
                computer_data[prop_dict['@Name']] = prop_dict['#text']

            action_result.add_data(computer_data)
            count += 1

        summary = action_result.update_summary({})
        summary['num_endpoints'] = count

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_run_action(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        site = param['site_name']
        fixlet = param['fixlet_id']
        action = param['action_id']
        computers = param.get('computer_ids')

        namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        root = etree.Element('BES', nsmap=namespaces, attrib={'{%s}noNamespaceSchemaLocation' % 'http://www.w3.org/2001/XMLSchema-instance': 'BES.xsd'})
        action_node = etree.SubElement(root, 'SourcedFixletAction')
        fixlet_node = etree.SubElement(action_node, 'SourceFixlet')

        etree.SubElement(fixlet_node, 'Sitename').text = site
        etree.SubElement(fixlet_node, 'FixletID').text = str(fixlet)
        etree.SubElement(fixlet_node, 'Action').text = action

        if computers:

            target_node = etree.SubElement(action_node, 'Target')

            if computers.strip() == 'all':
                etree.SubElement(target_node, 'AllComputers').text = 'true'
            else:
                computer_list = computers.split(',')
                for computer in computer_list:
                    etree.SubElement(target_node, 'ComputerID').text = computer.strip()

        print etree.tostring(root, pretty_print=True)

        ret_val, response = self._make_rest_call('actions', action_result, body=etree.tostring(root), method='post')

        if phantom.is_fail(ret_val):
            return ret_val

        spawned_action = response.get('BESAPI', {}).get('Action')
        if not spawned_action:
            return action_result.set_status(phantom.APP_ERROR, "Could not start action on BigFix. Return data:\n\n{0}".format(response.replace('{', '{{').replace('}', '}}')))

        spawned_action['Resource'] = spawned_action.pop('@Resource')
        spawned_action['LastModified'] = spawned_action.pop('@LastModified')

        action_result.add_data({'Action': spawned_action})

        summary = action_result.update_summary({})
        summary['spawned_action_id'] = spawned_action['ID']

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'list_sites':
            ret_val = self._handle_list_sites(param)
        elif action_id == 'list_fixlets':
            ret_val = self._handle_list_fixlets(param)
        elif action_id == 'list_endpoints':
            ret_val = self._handle_list_endpoints(param)
        elif action_id == 'run_action':
            ret_val = self._handle_run_action(param)

        return ret_val


if __name__ == '__main__':

    import sys
    # import pudb
    # pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = BigfixConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
