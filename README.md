[comment]: # "Auto-generated SOAR connector documentation"
# BigFix

Publisher: Splunk  
Connector Version: 2\.0\.7  
Product Vendor: IBM  
Product Name: BigFix  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app supports several investigative actions on IBM Big Fix

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a BigFix asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**url** |  required  | string | URL including port
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
**username** |  required  | string | Username
**password** |  required  | password | Password

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list device groups](#action-list-device-groups) - List all sites on the system  
[list patches](#action-list-patches) - List patches from a site  
[list endpoints](#action-list-endpoints) - List all endpoints connected to the system  
[deploy patch](#action-deploy-patch) - Deploy a patch  
[get host](#action-get-host) - Get Bigfix ID  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list device groups'
List all sites on the system

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.Sites\.\*\.Description | string | 
action\_result\.data\.\*\.Sites\.\*\.Domain | string |  `domain` 
action\_result\.data\.\*\.Sites\.\*\.GatherURL | string |  `url` 
action\_result\.data\.\*\.Sites\.\*\.GlobalReadPermission | string | 
action\_result\.data\.\*\.Sites\.\*\.Name | string |  `bigfix site` 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.CustomGroup\.\@JoinByIntersection | string | 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.CustomGroup\.SearchComponentPropertyReference\.\@Comparison | string | 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.CustomGroup\.SearchComponentPropertyReference\.\@PropertyName | string | 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.CustomGroup\.SearchComponentPropertyReference\.Relevance | string | 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.CustomGroup\.SearchComponentPropertyReference\.SearchText | string | 
action\_result\.data\.\*\.Sites\.\*\.Subscription\.Mode | string | 
action\_result\.data\.\*\.Sites\.\*\.Type | string | 
action\_result\.summary\.num\_sites | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list patches'
List patches from a site

Type: **investigate**  
Read only: **True**

This action lists all fixlets on a given site\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**site\_name** |  required  | Site Name | string |  `bigfix site` 
**site\_type** |  required  | Site Type | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.site\_name | string |  `bigfix site` 
action\_result\.parameter\.site\_type | string | 
action\_result\.data\.\*\.Fixlets\.\*\.ID | string | 
action\_result\.data\.\*\.Fixlets\.\*\.LastModified | string | 
action\_result\.data\.\*\.Fixlets\.\*\.Name | string | 
action\_result\.data\.\*\.Fixlets\.\*\.Resource | string |  `url` 
action\_result\.summary\.num\_fixlets | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list endpoints'
List all endpoints connected to the system

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.\@Resource | string |  `url` 
action\_result\.data\.\*\.Active Directory Path | string | 
action\_result\.data\.\*\.Agent Type | string | 
action\_result\.data\.\*\.Agent Version | string |  `ip` 
action\_result\.data\.\*\.BES Relay Selection Method | string | 
action\_result\.data\.\*\.BES Relay Service Installed | string | 
action\_result\.data\.\*\.BES Root Server | string | 
action\_result\.data\.\*\.BIOS | string | 
action\_result\.data\.\*\.CPU | string | 
action\_result\.data\.\*\.Client Settings | string | 
action\_result\.data\.\*\.Computer Name | string |  `host name` 
action\_result\.data\.\*\.Computer Type | string | 
action\_result\.data\.\*\.DNS Name | string |  `host name` 
action\_result\.data\.\*\.Device Type | string | 
action\_result\.data\.\*\.Distance to BES Relay | string | 
action\_result\.data\.\*\.Free Space on System Drive | string | 
action\_result\.data\.\*\.ID | string | 
action\_result\.data\.\*\.IP Address | string |  `ip` 
action\_result\.data\.\*\.Last Report Time | string | 
action\_result\.data\.\*\.License Type | string | 
action\_result\.data\.\*\.Locked | string | 
action\_result\.data\.\*\.OS | string | 
action\_result\.data\.\*\.RAM | string | 
action\_result\.data\.\*\.Relay | string | 
action\_result\.data\.\*\.Relay Name of Client | string | 
action\_result\.data\.\*\.Setting\.\@Resource | string | 
action\_result\.data\.\*\.Subnet Address | string |  `ip` 
action\_result\.data\.\*\.Subscribed Sites | string |  `url` 
action\_result\.data\.\*\.Total Size of System Drive | string | 
action\_result\.data\.\*\.User Name | string | 
action\_result\.summary\.num\_endpoints | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'deploy patch'
Deploy a patch

Type: **generic**  
Read only: **False**

Create an action on BigFix that will run the given action from the given fixlet\.<br><br>The <b>computer\_ids</b> parameter takes a comma\-separated list of BigFix computer IDs\. If no computers are given, the action will be run on the default computers configured on BigFix\. If the action should run on all computers set the <b>computer\_ids</b> parameter to <b>all</b>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fixlet\_id** |  required  | Fixlet ID | numeric |  `bigfix fixlet id` 
**action\_id** |  required  | Action ID | string | 
**site\_name** |  required  | Site Name | string |  `bigfix site` 
**computer\_ids** |  optional  | Target Computer IDs | string |  `bigfix computer id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.action\_id | string | 
action\_result\.parameter\.computer\_ids | string |  `bigfix computer id` 
action\_result\.parameter\.fixlet\_id | numeric |  `bigfix fixlet id` 
action\_result\.parameter\.site\_name | string |  `bigfix site` 
action\_result\.data\.\*\.Action\.ID | string | 
action\_result\.data\.\*\.Action\.LastModified | string | 
action\_result\.data\.\*\.Action\.Name | string | 
action\_result\.data\.\*\.Action\.Resource | string |  `url` 
action\_result\.summary\.spawned\_action\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get host'
Get Bigfix ID

Type: **investigate**  
Read only: **True**

Get BigFix ID from Hostname\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hostname** |  required  | Hostname | string |  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.hostname | string |  `host name` 
action\_result\.data\.\*\.Answer | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 