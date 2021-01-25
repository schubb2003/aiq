# aiq
scripts for accessing SolidFire AIQ via selenium

SolidFire AIQ access scripts
Date:	12-Jan-2021
Author:	Scott Chubb
Notes:	I am not a developer, the layout and script code can likely be improved and may well not meet best practices.
		--search-cluster, --search-customer, and --search-string as loose matches be sure to match required specificity and are case insensitive
		These scripts were written for python 3.7.2 and use printf, if you are not using a compatible version you can switch back to format or % based printing

These scripts rely on:
	Selenium for browser automation as AIQ does not offer CLI based login.
		python pip install -m install -U selenium
	PrettyTable is also in use for some scripts.
		python pip install -m install -U prettytable
	Requests for REST access (I will try to look into using urllib to avoid this dependency, but have no ETA on removing requests.)
		python pip install -m install requests

Create a directory wherever you unzip/copy the scripts to and call it output_files
	This is used to capture the output of the files to .txt files

Three of these acts a modules and have no output of their own.  They should be in the modules directory which should be in the dir with the functional scripts.
	connect_auth_aiq.py
	get_aiq_customer.py
	get_aiq_inputs.py
	aiq_build_api_payload.py
	build_api_response.py
	parser.py

Script:
	aiq_cluster_faults.py
	Used to pull faults from clusters, you can select what details you want to search on with --search-string
usage: aiq_cluster_faults.py [-h] -u user [-p user_pass]
                             [--search-customer customer name]
                             [--search-string text to search for]
                             [--sort-order sort_order]
                             [--search-cluster search_cluster]

arguments:
	-h, --help            	show this help message and exit
	-u user               	AIQ username (required)
	-p user_pass          	AIQ password  (leave blank to get prompt with blanked entry)
	--sort-order 			sort_order to display results under (optional, defaults to Type)
								Cluster, Date, Details, and Severity are the available choices as of today
	--node-id node_id     	(not used by this script)
	--search-customer 		This needs to be in quotes if there are spaces in the customer name(optional, but recommended)
								Searches should be case insensitive, no need to match case
	--search-string 		This needs to be in quotes if there are spaces in the text you want to search on (optional)
								Searches should be case insensitive, no need to match case
								Used to search the "Details" column
	--search-cluster		This is the name of a specific cluster to search on (optional)

example:
	To match a specific customer and error message:
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>" --search-string "async delay"
	Enter password for user test_user_1:
	Output file name is: cluster_faults_2021-01-13_10-26.txt
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+
	|      Cluster       | Node ID | Drive ID | Service ID |             Date            |  Type  |  Severity |                           Details                            |
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+
	| fake-prd-cluster-1 |    0    |    0     |     0      | 2020-06-12T21:02:44.326898Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |      360 minutes. Delayed volume pairs:[132:61, 137:62]      |
	| fake-prd-cluster-2 |    0    |    0     |     0      | 2020-04-28T15:50:35.696887Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[30:25, 31:26, 32:27]    |
	| fake-prd-cluster-3 |    0    |    0     |     0      | 2020-08-21T16:09:49.335146Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[1030:4732, 1032:4734,   |
	|                    |         |          |            |                             |        |           |                          1035:4737]                          |
	| fake-prd-cluster-4 |    0    |    0     |     0      | 2020-04-28T15:50:40.735523Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[25:30, 26:31, 27:32]    |
	| fake-prd-cluster-5 |    0    |    0     |     0      | 2020-06-12T21:03:00.327711Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |      360 minutes. Delayed volume pairs:[61:132, 62:137]      |
	| fake-prd-cluster-6 |    0    |    0     |     0      | 2020-09-26T23:36:44.107438Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |         360 minutes. Delayed volume pairs:[637:480]          |
	| fake-prd-cluster-7 |    0    |    0     |     0      | 2020-09-26T23:36:13.036622Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |         360 minutes. Delayed volume pairs:[480:637]          |
	| fake-prd-cluster-8 |    0    |    0     |     0      | 2020-08-21T16:09:50.590871Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[4732:1030, 4734:1032,   |
	|                    |         |          |            |                             |        |           |                          4737:1035]                          |
	| fake-prd-cluster-9 |    0    |    0     |     0      | 2018-11-21T21:50:29.299977Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |    360 minutes. Delayed volume pairs:[438:2270, 439:2271,    |
	|                    |         |          |            |                             |        |           | 440:2272, 441:2273, 442:2274, 443:2286, 444:2287, 445:2288,  |
	|                    |         |          |            |                             |        |           | 446:2289, 447:2290, 448:2291, 449:2292, 450:2293, 451:2294,  |
	|                    |         |          |            |                             |        |           | 452:2295, 453:2296, 454:2297, 455:2298, 456:2299, 457:2300,  |
	|                    |         |          |            |                             |        |           |                          458:2335]                           |
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+
example:
	To match all alerts from a specific customer:
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>"
	Enter password for user test_user_1:
	Output file name is: cluster_faults_2021-01-13_11-44.txt
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+
	|          Cluster          | Node ID | Drive ID | Service ID |             Date            |   Type  |   Severity   |                           Details                            |
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+
	|     fake-prd-cluster-1    |    0    |    0     |     0      | 2019-03-25T00:00:03.421629Z | cluster |    error     |           The cluster SSL certificate has expired            |
	|     fake-prd-cluster-1    |    0    |    0     |     0      | 2020-01-22T18:56:30.612393Z | cluster |   warning    |    Add additional capacity or free up capacity as soon as    |
	|                           |         |          |            |                             |         |              |                          possible.                           |
	|     fake-prd-cluster-1    |    0    |    0     |     0      | 2020-01-22T19:16:09.104665Z | cluster |    error     |    Local replication and synchronization of the following    |
	|                           |         |          |            |                             |         |              | volumes is in progress. Progress of the synchronization can  |
	|                           |         |          |            |                             |         |              | be seen in the Running Tasks window. [2, 3, 4, 5, 8, 9, 10,  |
	|                           |         |          |            |                             |         |              |                 12, 13, 14, 15, 16, 18, 19]                  |
	|     fake-prd-cluster-1    |    0    |    0     |     0      | 2020-01-22T19:20:01.246902Z | cluster |    error     |  The following volumes are offline. [2, 3, 4, 5, 7, 9, 10,   |
	|                           |         |          |            |                             |         |              |                 11, 12, 13, 14, 15, 18, 19]                  |
	|     fake-prd-cluster-1    |    0    |    0     |     0      | 2020-01-24T18:30:47.380510Z | cluster |    error     |   Ensemble degraded: 2/5 database servers not connectable:   |
	|                           |         |          |            |                             |         |              |                {3:192.168.0.100,5:192.168.0.101}             |
	|     fake-prd-cluster-2    |    0    |    0     |     0      | 2018-05-24T18:00:50.640743Z | cluster |   warning    |       Schedule action failed for schedule IDs: [3,4].        |
	|     fake-prd-cluster-3    |    0    |    0     |     0      | 2019-03-25T00:01:06.723096Z | cluster |    error     |           The cluster SSL certificate has expired            |
	|     fake-prd-cluster-3    |    0    |    0     |     0      | 2020-01-24T18:38:15.080553Z | cluster |   warning    | Remote nodes are not connected via the cluster network. Ping |
	|                           |         |          |            |                             |         |              |  the remote nodes using jumbo frames to test connectivity.   |
	|                           |         |          |            |                             |         |              |     Disconnected nodes: [DR-CLUSTER1:192.168.0.100,          |
	|                           |         |          |            |                             |         |              |                  1192.168.0.101, 192.168.0.102]              |
	|     fake-prd-cluster-4    |    0    |    0     |     0      | 2020-01-27T17:46:32.437589Z | cluster |   warning    | One of the clusters in a pair may have become misconfigured  |
	|                           |         |          |            |                             |         |              | or disconnected.  Remove the local pairing and retry pairing |
	|                           |         |          |            |                             |         |              | the clusters. Disconnected Cluster Pairs: [1]. Misconfigured |
	|                           |         |          |            |                             |         |              |                      Cluster Pairs: []                       |
	|     fake-prd-cluster-5    |    0    |    0     |     0      | 2019-02-28T18:10:42.990016Z | cluster | bestPractice |  SSH is enabled on nodes (1, 2, 3, 4, 5, 10) and any nodes   |
	|                           |         |          |            |                             |         |              |        added to the cluster will have SSH turned on.         |
	|     fake-prd-cluster-6    |    0    |    0     |     0      | 2019-04-04T22:10:12.638054Z | cluster | bestPractice | SSH is enabled on nodes (27, 28, 31, 32, 33, 35, 36, 38, 39, |
	|                           |         |          |            |                             |         |              |  40, 41, 42, 43, 44, 45, 46, 48, 49) and any nodes added to  |
	|                           |         |          |            |                             |         |              |             the cluster will have SSH turned on.             |
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+	

	To search all alerts from a specific customer and sort:
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>" --sort-order Details
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>" --sort-order Cluster
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>" --sort-order Date
	python aiq_cluster_faults.py -u test_user_1 --search-customer "<customer_name>" --sort-order Severity

########################################
#	Not recommended, but possible:     #
########################################
	To search all customers for a specific error message
	python aiq_cluster_faults.py -u test_user_1 --search-string "async delay"
	
	To bring your machine to a halt for 30 plus minutes search everything:
	python aiq_cluster_faults.py -u test_user_1




Script:
	Note that this requires an 11.8 or higher mnode.  The output will indicate a constant not found in this situation.
	aiq_constants_info.py
	Pulls constants and their settings from AIQ for review
usage: aiq_constants_info.py [-h] -u user [-p user_pass]
                             [--search-customer customer name]
                             [--search-string text to search for]
                             [--sort-order sort_order]
                             [--search-cluster search_cluster]
arguments:
	-h, --help            	show this help message and exit
	-u user               	AIQ username (required)
	-p user_pass          	AIQ password (leave blank to get prompt with blanked entry)
	--search-customer 		customer name (optional, but recommended)
	--search-string 		text to search for in the log file if you want to search for specifics (optional)
	--sort-order 			(not used by this script)
	--node-id node_id     	(not used by this script)
	--search-customer 		This needs to be in quotes if there are spaces in the customer name
								Searches should be case insensitive, no need to match case
	--search-string 		This can be a comma separated value with no spaces if you want to search multiple constants at once
	--search-cluster		This is the name of a specific cluster to search on (optional)

example:
	python aiq_constants_info.py -u test_user_1 --search-customer "<customer_name>" --search-string cMemCtlrCorrectableErrLeakRate,cMemCtlrCorrectableErrWarnDuration,cMemCtlrCorrectableErrWarnThreshold
	Enter password for user test_user_1:
	Output file name is: cluster_constants_2021-01-13_11-37.txt
	+--------------+-------------------------------------+------------------+
	|   Cluster    |            Constant Name            | Constant Setting |
	+--------------+-------------------------------------+------------------+
	| prd-cluster1 |    cMemCtlrCorrectableErrLeakRate   |        3         |
	| prd-cluster1 |  cMemCtlrCorrectableErrWarnDuration |      86400       |
	| prd-cluster1 | cMemCtlrCorrectableErrWarnThreshold |      100000      |
	+--------------+-------------------------------------+------------------+

Script:
	aiq_get_nodes.py
	This script pulls inventory information such as cluster, node, version, serial/service tag, and MVIP/SVIPs
	It outputs to files in the local directory
	with no switches other than customer output is full_{DATE}.txt
	with model switch first output is model_{MODEL}_{DATE}.txt
	with version switch first output is version_{VERSION}_{DATE}.txt
	with --no-serial output is missing_serials_{DATE}.txt
	########################################
	#	Needs expanded to all models       #
	########################################
	
usage: aiq_get_nodes.py [-h] -u user [-p user_pass] [--version search_vers]
                        [--model search_model]
                        [--search-customer search_customer] [--no-serial]

optional arguments:
	-h, --help            	show this help message and exit
	-u user               	AIQ username  (required)
	-p user_pass          	AIQ password  (leave blank to get prompt with blanked entry)
	--version				Version of Element to search on (optional)
	--model search_model  	Type of node to search on (currently SF19210 and H610S, needs updating)
	--search-customer 		Customer to search on (optional, but recommended)
	--no-serial				add this to the command string to find nodes with missing serial numbers in AIQ

example:
	python aiq_get_nodes.py -u test_user_1 --search-customer "<customer_name>"
	Enter password for user test_user_1:
	Output file name is: full_report_2021-01-12.txt
	+---------------------------+-------------------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
	|          Cluster          |        Node Name                    | Node ID | Element Vers | Node Type |   Serial No    | Service Tag  |    Mgmt IP     |   Storage IP   |
	+---------------------------+-------------------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr1   |    3    |  10.1.0.83   |  Unknown  | abcd1234567890 | 123456abcd1  | 192.168.1.100  | 192.168.2.100  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr3   |    5    |  10.1.0.83   |  Unknown  | abcd1234567891 | 123456abcd2  | 192.168.1.101  | 192.168.2.101  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr13  |    19   |  10.1.0.83   |  Unknown  | abcd1234567892 | 123456abcd3  | 192.168.1.102  | 192.168.2.102  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr9   |    15   |  10.1.0.83   |  Unknown  | abcd1234567893 | 123456abcd4  | 192.168.1.103  | 192.168.2.103  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr14  |    20   |  10.1.0.83   |  Unknown  | abcd1234567894 | 123456abcd5  | 192.168.1.104  | 192.168.2.104  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr5   |    21   |  10.1.0.83   |  Unknown  | abcd1234567895 | 123456abcd6  | 192.168.1.105  | 192.168.2.105  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr8   |    14   |  10.1.0.83   |  Unknown  | abcd1234567896 | 123456abcd7  | 192.168.1.106  | 192.168.2.106  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr2   |    4    |  10.1.0.83   |  Unknown  | abcd1234567897 | 123456abcd8  | 192.168.1.107  | 192.168.2.107  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr10  |    16   |  10.1.0.83   |  Unknown  | abcd1234567898 | 123456abcd9  | 192.168.1.108  | 192.168.2.108  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr12  |    18   |  10.1.0.83   |  Unknown  | abcd1234567899 | 123456abcds  | 192.168.1.109  | 192.168.2.109  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr4   |    6    |  10.1.0.83   |  Unknown  | abcd1234567800 | 123456abcda  | 192.168.1.110  | 192.168.2.110  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr6   |    12   |  10.1.0.83   |  Unknown  | abcd1234567810 | 123456abcds  | 192.168.1.111  | 192.168.2.111  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr7   |    13   |  10.1.0.83   |  Unknown  | abcd1234567811 | 123456abcdd  | 192.168.1.112  | 192.168.2.112  |
	| testlab-solidfire-cluster1 |   testlab-solidfire-cluster1-fc1   |    2    |  10.1.0.83   |  Unknown  | abcd1234567812 |   1233bac    | 192.168.1.113  | 192.168.2.113  |
	| testlab-solidfire-cluster1 |   testlab-solidfire-cluster1-fc2   |    1    |  10.1.0.83   |  Unknown  | abcd1234567813 |   1234abc    | 192.168.1.114  | 192.168.2.114  |
	| testlab-solidfire-cluster1 |  testlab-solidfire-cluster1-svr15  |    17   |  10.1.0.83   |  Unknown  | abcd1234567814 | 123456abcdf  | 192.168.1.115  | 192.168.2.115  |
	|           testlab          |            testlab-n01             |    2    |  12.2.0.777  |  SF19210  |      None      |   3ad2sdf    | 192.168.1.100  | 192.168.2.100  |
	|           testlab          |            testlab-n02             |    3    |  12.2.0.777  |  SF19210  |      None      |   1ad4sdf    | 192.168.1.100  | 192.168.2.100  |
	|           testlab          |              node01a               |    8    |  12.2.0.777  |  SF19210  |  409620481034  |   3ad6sdf    | 192.168.1.101  | 192.168.2.101  |
	|           testlab          |              node01b               |    1    |  12.2.0.777  |  SF19210  |      None      |   1ad8sdf    | 192.168.1.102  | 192.168.2.102  |
	|           testlab          |              node01c               |    4    |  12.2.0.777  |  SF19210  |      None      |   3ad0sdf    | 192.168.1.103  | 192.168.2.103  |
	|         test-clst          |            fc-testlab1             |    7    |  11.5.1.14   |  SF19210  | a1b2c3d4e5f6g7 |   1ad2sdf    | 192.168.1.100  | 192.168.2.100  |
	|         test-clst          |            fc-testlab2             |    5    |  11.5.1.14   |  Unknown  |  ab12cd34ef5   | ab12cd34ef5  | 192.168.1.101  | 192.168.2.101  |
	|         test-clst          |            fc-testlab3             |    3    |  11.5.1.14   |  Unknown  |  ab12cd34ef5   | dr12bc34ef5  | 192.168.1.102  | 192.168.2.102  |
	|         test-clst          |            fc-node-n07             |    8    |  11.5.1.14   |  SF19210  | a1b2c3d4e0f9g8 |   a1b2c3d    | 192.168.1.103  | 192.168.2.103  |
	|         test-clst          |            fc-testlab4             |    6    |  11.5.1.14   |  Unknown  |  a1234567890   | a1234567890  | 192.168.1.104  | 192.168.2.104  |
	|         test-clst          |            fc-testlab5             |    2    |  11.5.1.14   |  Unknown  |  a1234567891   | a1234567891  | 192.168.1.105  | 192.168.2.105  |
	|         test-clst          |            fc-testlab6             |    1    |  11.5.1.14   |  Unknown  |  a1234567892   | a1234567892  | 192.168.1.106  | 192.168.2.106  |
	|         test-clst          |            fc-testlab7             |    4    |  11.5.1.14   |  Unknown  |  a1234567893   | a1234567893  | 192.168.1.107  | 192.168.2.107  |
	|         cluster1           |             ztx1sld004             |    7    |  10.4.0.35   |  Unknown  |  a1234567894   | a1234567894  | 192.168.1.100  | 192.168.2.100  |
	|         cluster1           |             ztx1sld001             |    8    |  10.4.0.35   |  Unknown  |  a1234567895   | a1234567895  | 192.168.1.101  | 192.168.2.101  |
	|         cluster1           |             ztx1sld002             |    6    |  10.4.0.35   |  Unknown  |  a1234567896   | a1234567896  | 192.168.1.102  | 192.168.2.102  |
	|         cluster1           |             ztx1sld003             |    5    |  10.4.0.35   |  Unknown  |  a1234567897   | a1234567897  | 192.168.1.103  | 192.168.2.103  |
	|        cluster2-lab        |            cls2-lab-n01            |    1    |  11.8.0.23   |  Unknown  |  a1234567898   | a1234567898  | 192.168.1.100  | 192.168.2.100  |
	|        cluster2-lab        |            cls2-lab-n02            |    2    |  11.8.0.23   |  Unknown  |  a1234567899   | a1234567899  | 192.168.1.101  | 192.168.2.101  |
	|        cluster2-lab        |            cls2-lab-n03            |    4    |  11.8.0.23   |  Unknown  |  a1234567880   | a1234567880  | 192.168.1.102  | 192.168.2.102  |
	|        cluster2-lab        |            cls2-lab-n04            |    3    |  11.8.0.23   |  Unknown  |  a1234567881   | a1234567881  | 192.168.1.103  | 192.168.2.103  |
	|      cluster-test-lab      |       cluster-test-lab-n100        |    41   |  11.8.0.23   |   H610S   |   1234567890   |  1234567890  | 192.168.1.120  | 192.168.2.120  |
	|      cluster-test-lab      |       cluster-test-lab-n101        |    40   |  11.8.0.23   |   H610S   |   1234567891   |  1234567891  | 192.168.1.121  | 192.168.2.121  |
	|      cluster-test-lab      |       cluster-test-lab-n102        |    33   |  11.8.0.23   |   H610S   |   1234567892   |  1234567892  | 192.168.1.122  | 192.168.2.122  |
	|      cluster-test-lab      |       cluster-test-lab-n103        |    35   |  11.8.0.23   |   H610S   |   1234567893   |  1234567893  | 192.168.1.123  | 192.168.2.123  |
	|      cluster-test-lab      |       cluster-test-lab-n104        |    44   |  11.8.0.23   |   H610S   |   1234567894   |  1234567894  | 192.168.1.124  | 192.168.2.124  |
	|      cluster-test-lab      |       cluster-test-lab-n105        |    49   |  11.8.0.23   |   H610S   |   1234567895   |  1234567895  | 192.168.1.125  | 192.168.2.125  |
	|      cluster-test-lab      |       cluster-test-lab-n106        |    27   |  11.8.0.23   |   H610S   |   1234567896   |  1234567896  | 192.168.1.126  | 192.168.2.126  |
	|      cluster-test-lab      |       cluster-test-lab-n107        |    43   |  11.8.0.23   |   H610S   |   1234567897   |  1234567897  | 192.168.1.127  | 192.168.2.127  |
	+----------------------------+------------------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
example:
	python aiq_get_nodes.py -u test_user_1 --search-customer "<customer_name>" --model SF19210 --version 12.2.0.777
	Enter password for user test_user_1:
	Output file name is: model_SF19210_2021-01-12.txt
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
	|         Cluster         |       Node Name       | Node ID | Element Vers | Node Type |   Serial No    | Service Tag |    Mgmt IP     |   Storage IP   |
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
	|          ntap01         |   ntap01-n01.lab.com  |    2    |  12.2.0.777  |  SF19210  |      None      |   abcd111   | 192.168.100.12 | 192.168.100.3  |
	|          ntap01         |   ntap01-n02.lab.com  |    3    |  12.2.0.777  |  SF19210  |      None      |   abcd112   | 192.168.100.13 | 192.168.100.37 |
	|          ntap01         |   ntap01-n03.lab.com  |    8    |  12.2.0.777  |  SF19210  |  402988000078  |   abcd113   | 192.168.100.35 | 192.168.100.36 |
	|          ntap01         |   ntap01-n04.lab.com  |    1    |  12.2.0.777  |  SF19210  |      None      |   abcd114   | 192.168.100.11 | 192.168.100.35 |
	|          ntap01         |   ntap01-n05.lab.com  |    4    |  12.2.0.777  |  SF19210  |      None      |   abcd115   | 192.168.100.14 | 192.168.100.34 |
	|          ntap03         |   ntap03-n01.lab.com  |    7    |  11.5.1.14   |  SF19210  | STVJM000090000 |   abcd116   | 100.86.143.66  | 192.168.200.33 |
	|          ntap03         |   ntap03-n02.lab.com  |    8    |  11.5.1.14   |  SF19210  | STVJM009000000 |   abcd117   | 100.86.143.67  | 192.168.200.32 |
	|          ntap02         |   ntap02-n01.lab.com  |    10   |  12.2.0.777  |  SF19210  |  409620481024  |   abcd118   | 110.83.145.17  | 192.168.110.35 |
	|          ntap02         |   ntap02-n02.lab.com  |    11   |  12.2.0.777  |  SF19210  |  409620481025  |   abcd119   | 110.83.145.13  | 192.168.110.34 |
	|          ntap02         |   ntap02-n03.lab.com  |    13   |  12.2.0.777  |  SF19210  |  409620481026  |   abcd120   | 110.83.145.16  | 192.168.110.33 |
	|          ntap02         |   ntap02-n04.lab.com  |    12   |  12.2.0.777  |  SF19210  |  409620481027  |   abcd121   | 110.83.145.15  | 192.168.110.32 |
	|          ntap02         |   ntap02-n05.lab.com  |    7    |  12.2.0.777  |  SF19210  |  409620481028  |   abcd122   | 110.83.145.14  | 192.168.110.31 |
	| test-solidfire-cluster2 |  test-solidfire2-fca  |    1    |  11.5.0.63   |  SF19210  |  409620481029  |   abcd123   |  20.16.14.195  | 192.168.120.31 |
	| test-solidfire-cluster2 |  test-solidfire2-fcb  |    2    |  11.5.0.63   |  SF19210  |  409620481030  |   abcd124   |  20.16.14.196  | 192.168.120.32 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-N4   |    8    |  10.1.0.83   |  SF19210  | STVJM000000001 |   abcd125   |  10.200.29.34  | 192.168.100.31 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-FC4  |    4    |  10.1.0.83   |  SF19210  | STVJM000000010 |   abcd126   |  10.200.29.24  | 192.168.100.32 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-FC2  |    9    |  10.1.0.83   |  SF19210  | STVJM000000100 |   abcd127   |  10.200.29.22  | 192.168.100.33 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-N1   |    5    |  10.1.0.83   |  SF19210  | STVJM000001000 |   abcd128   |  10.200.29.31  | 192.168.100.34 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-FC3  |    3    |  10.1.0.83   |  SF19210  | STVJM000010000 |   abcd129   |  10.200.29.23  | 192.168.100.35 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-N2   |    6    |  10.1.0.83   |  SF19210  | STVJM000100000 |   abcd132   |  10.200.29.32  | 192.168.100.36 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-N3   |    7    |  10.1.0.83   |  SF19210  | STVJM001000000 |   abcd133   |  10.200.29.33  | 192.168.100.37 |
	|     RTP-SOLIDFIRE1      |    RTP-SOLIDFIRE-FC1  |    1    |  10.1.0.83   |  SF19210  | STVJM010000000 |   abcd134   |  10.200.29.21  | 192.168.100.38 |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-FC2 |    2    |  10.1.0.83   |  SF19210  | STVJM100000000 |   abcd135   |  10.100.29.34  | 10.100.30.137  |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-N1  |    3    |  10.1.0.83   |  SF19210  | STVJM200000000 |   abcd136   |  10.100.29.24  | 10.100.30.131  |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-N3  |    5    |  10.1.0.83   |  SF19210  | STVJM020000000 |   abcd137   |  10.100.29.22  | 10.100.30.133  |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-FC1 |    1    |  10.1.0.83   |  SF19210  | STVJM002000000 |   abcd138   |  10.100.29.31  | 10.100.30.121  |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-N2  |    4    |  10.1.0.83   |  SF19210  | STVJM000200000 |   abcd139   |  10.100.29.23  | 10.100.30.132  |
	|    SVL-DR-SOLIDFIRE1    |  SVL-DR-SOLIDFIRE-N4  |    6    |  10.1.0.83   |  SF19210  | STVJM000020000 |   abcd140   |  10.100.29.32  | 10.100.30.134  |
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
example:
	python aiq_get_nodes.py -u test_user_1 --search-customer "<customer_name>" --version 10.1.0.83
	Enter password for user test_user_1:
	Output file name is: version_10.1.0.83_2021-01-12.txt
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
	|          Cluster          |       Node Name          | Node ID | Element Vers | Node Type |   Serial No    | Service Tag |   Mgmt IP    |  Storage IP  |
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
	| testlab-solidfire-cluster1 | testlab-solidfire-svr1  |    3    |  10.1.0.83   |  Unknown  |  abcd2234abc   | abcd2234abc | 10.86.143.81 | 192.168.1.11 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr2  |    5    |  10.1.0.83   |  Unknown  |  abcd3234abc   | abcd3234abc | 10.86.143.83 | 192.168.1.13 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr3  |    19   |  10.1.0.83   |  Unknown  |      None      | abcd4234abc | 10.86.143.60 | 192.168.1.23 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr4  |    15   |  10.1.0.83   |  Unknown  |  abcd5234abc   | abcd5234abc | 10.86.143.54 | 192.168.1.19 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr6  |    20   |  10.1.0.83   |  Unknown  |      None      | abcd6234abc | 10.86.143.61 | 192.168.1.24 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr5  |    21   |  10.1.0.83   |  Unknown  |  abcd7234abc   | abcd7234abc | 10.86.143.85 | 192.168.1.15 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr8  |    14   |  10.1.0.83   |  Unknown  |  abcd8234abc   | abcd8234abc | 10.86.143.53 | 192.168.1.18 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr2  |    4    |  10.1.0.83   |  Unknown  |  abcd9234abc   | abcd9234abc | 10.86.143.82 | 192.168.1.12 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr10 |    16   |  10.1.0.83   |  Unknown  |  abcd1334abc   | abcd1334abc | 10.86.143.55 | 192.168.1.20 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr12 |    18   |  10.1.0.83   |  Unknown  |  abcd1434abc   | abcd1434abc | 10.86.143.59 | 192.168.1.22 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr14 |    6    |  10.1.0.83   |  Unknown  |  abcd1534abc   | abcd1534abc | 10.86.143.84 | 192.168.1.14 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr25 |    12   |  10.1.0.83   |  Unknown  |  abcd1634abc   | abcd1634abc | 10.86.143.86 | 192.168.1.16 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr28 |    13   |  10.1.0.83   |  Unknown  |  abcd1734abc   | abcd1734abc | 10.86.143.52 | 192.168.1.17 |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr2  |    2    |  10.1.0.83   |  Unknown  | NNG01111111111 |   22y12bb   | 10.86.143.80 | 192.168.1.4  |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr20 |    1    |  10.1.0.83   |  Unknown  | NNG01222222222 |   22x63bc   | 10.86.143.79 | 192.168.1.3  |
	| testlab-solidfire-cluster1 | testlab-solidfire-svr12 |    17   |  10.1.0.83   |  Unknown  |  abcd1234abc   | abcd1234abc | 10.86.143.57 | 192.168.1.21 |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    1    |  10.1.0.83   |  SF19210  | STVJM123456710 |   abcd120   |  10.0.29.34  |  10.0.30.34  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    3    |  10.1.0.83   |  SF19210  | STVJM123456712 |   abcd121   |  10.0.29.24  |  10.0.30.24  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    4    |  10.1.0.83   |  SF19210  | STVJM123456713 |   abcd122   |  10.0.29.22  |  10.0.30.22  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    5    |  10.1.0.83   |  SF19210  | STVJM123456714 |   abcd123   |  10.0.29.31  |  10.0.30.31  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    8    |  10.1.0.83   |  SF19210  | STVJM123456715 |   abcd124   |  10.0.29.23  |  10.0.30.23  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    16   |  10.1.0.83   |  SF19210  | STVJM123456716 |   abcd125   |  10.0.29.32  |  10.0.30.32  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    17   |  10.1.0.83   |  SF19210  | STVJM123456717 |   abcd126   |  10.0.29.33  |  10.0.30.33  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    21   |  10.1.0.83   |  SF19210  | STVJM123456721 |   abcd127   |  10.0.29.21  |  10.0.30.21  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    22   |  10.1.0.83   |  SF19210  | STVJM123456724 |   abcd128   | 10.0.29.122  | 10.0.30.122  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    13   |  10.1.0.83   |  SF19210  | STVJM123456725 |   abcd129   | 10.0.29.131  | 10.0.30.131  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    15   |  10.1.0.83   |  SF19210  | STVJM123456746 |   abcd130   | 10.0.29.133  | 10.0.30.133  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    12   |  10.1.0.83   |  SF19210  | STVJM123456747 |   abcd131   | 10.0.29.121  | 10.0.30.121  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    24   |  10.1.0.83   |  SF19210  | STVJM123456784 |   abcd132   | 10.0.29.132  | 10.0.30.132  |
	| testlab-solidfire-cluster2 |  testlab2-replication   |    26   |  10.1.0.83   |  SF19210  | STVJM123456735 |   abcd133   | 10.0.29.134  | 10.0.30.134  |
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
example:
	python aiq_get_nodes.py -u test_user_1 --search-customer "<customer_name>" --no-serial
	Enter password for user test_user_1:
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	|          Cluster          |        Node Name         | Node ID | Element Vers | Node Type | Serial No | Service Tag  |    Mgmt IP     |   Storage IP   |
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	| testlab-solidfire-clster2 |  test-lab-cls3-node-001  |    19   |  10.1.0.83   |  Unknown  |    None   | ab123456741  |  10.86.143.60  |  192.168.1.23  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-002  |    20   |  10.1.0.83   |  Unknown  |    None   | ab123456742  |  10.86.143.61  |  192.168.1.24  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-003  |    2    |  12.2.0.777  |  SF19210  |    None   |   abc1234    | 192.168.100.12 | 192.168.101.12 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-004  |    3    |  12.2.0.777  |  SF19210  |    None   |   abc1235    | 192.168.100.13 | 192.168.101.13 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-005  |    1    |  12.2.0.777  |  SF19210  |    None   |   abc1236    | 192.168.100.11 | 192.168.101.11 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-006  |    4    |  12.2.0.777  |  SF19210  |    None   |   abc1237    | 192.168.100.14 | 192.168.101.14 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-007  |    13   |  10.4.0.35   |  Unknown  |    None   | ab123456733  | 10.240.161.96  | 10.240.192.141 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-008  |    2    |  10.4.0.35   |  Unknown  |    None   | ab123456734  | 10.240.161.95  | 10.240.192.140 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-009  |    42   |  10.4.0.35   |  Unknown  |    None   | ab123456735  | 10.240.161.97  | 10.240.192.142 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-010  |    4    |  10.4.0.35   |  Unknown  |    None   | ab123456736  | 10.240.161.94  | 10.240.192.139 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-011  |    11   |  10.4.0.35   |   H610S   |    None   | 3a1001001007 |  10.140.5.103  |  10.240.59.35  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-012  |    7    |  10.4.0.35   |  Unknown  |    None   | ab123456720  |  10.140.5.175  |  10.240.59.15  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-013  |    21   |  10.4.0.35   |  Unknown  |    None   | ab123456721  |  10.140.5.169  |  10.240.59.9   |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-014  |    5    |  10.4.0.35   |  Unknown  |    None   | ab123456722  |  10.140.5.173  |  10.240.59.13  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-015  |    33   |  10.4.0.35   |  Unknown  |    None   | ab123456723  |  10.140.5.171  |  10.240.59.11  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-016  |    23   |  10.4.0.35   |  Unknown  |    None   | ab123456724  |  10.140.5.170  |  10.240.59.10  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-017  |    8    |  10.4.0.35   |  Unknown  |    None   | ab123456725  |  10.140.5.166  |  10.240.59.16  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-018  |    6    |  10.4.0.35   |  Unknown  |    None   | ab123456726  |  10.140.5.174  |  10.240.59.14  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-019  |    62   |  11.8.0.23   |  Unknown  |    None   | ab123456727  | 10.100.22.245  | 10.100.20.134  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-020  |    17   |  11.8.0.23   |  Unknown  |    None   | ab123456728  | 10.100.22.241  | 10.100.20.133  |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-021  |    54   |  11.8.0.23   |  Unknown  |    None   | ab123456729  | 10.120.152.168 | 10.120.252.200 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-022  |    53   |  11.8.0.23   |  Unknown  |    None   | ab123456730  | 10.120.152.167 | 10.120.252.199 |
	| testlab-solidfire-clster2 |  test-lab-cls3-node-023  |    52   |  11.8.0.23   |  Unknown  |    None   | ab123456731  | 10.120.152.166 | 10.120.252.198 |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-001  |    8    |   10.4.2.9   |   H610S   |    None   | 3a1001001001 | 10.120.110.235 | 10.120.104.201 |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-002  |    6    |  11.5.0.63   |  Unknown  |    None   | 3a1001001002 | 10.86.143.100  |  192.168.1.14  |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-003  |    3    |  11.5.0.63   |  Unknown  |    None   | 3a1001001003 |  10.86.143.97  |  192.168.1.11  |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-004  |    4    |  11.5.0.63   |  Unknown  |    None   | 3a1001001004 |  10.86.143.98  |  192.168.1.12  |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-005  |    5    |  11.5.0.63   |  Unknown  |    None   | 3a1001001005 |  10.86.143.99  |  192.168.1.13  |
	| testlab-solidfire-clster3 |  test-lab-cls3-node-006  |    1    |  11.8.0.23   |   H610S   |    None   | 3a1001001006 | 10.246.39.152  |  10.246.39.23  |
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	
	
Script:
	aiq_cluster_faults.py
usage: aiq_cluster_faults.py [-h] -u user [-p user_pass]
                             [--search-customer customer name]
                             [--search-string text to search for]
                             [--sort-order sort_order]
                             [--search-cluster search_cluster]

arguments:
	-h, --help            	show this help message and exit
	-u user               	AIQ username (required)
	-p user_pass          	AIQ password  (leave blank to get prompt with blanked entry)
	--sort-order 			(Not used by this script)
	--node-id node_id     	(not used by this script)
	--search-customer 		This needs to be in quotes if there are spaces in the customer name (required)
								Searches should be case insensitive, no need to match case
	--search-string 		This is the string you want to find in "Details", if blank it will query all (optional)
								Searches should be case insensitive, no need to match case
	--search-cluster		This is a specific cluster you want, if blank it will query all (optional)
example:	
	python aiq_node_network_info.py -u test_user_1 --search-customer "<customer_name>" --search-clsuter test-cluster-0002 --node-id 7
	Enter password for user test_user_1:
	Output file name is: node_ip_cfg_info_2021-01-14_15-54.txt
	+---------+----------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+
	|   Bond  |    Address     |      Mode     |          DNS Search         |         DNS servers          | MTU  |     Netmask     |   Gateway    | VLAN |
	+---------+----------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+
	|  Bond1G |                | ActivePassive |     test.demo.netapp.com    | 192.168.100.3, 192.168.100.4 | 1500 |                 |              |  0   |
	| Bond10G | 100.215.19.194 |      LACP     |     test.demo.netapp.com    | 192.168.100.3, 192.168.100.4 | 9000 | 255.255.255.192 | 100.215.19.1 |  0   |
	+---------+----------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+

Script:
	aiq_cluster_events.py
	Pulls a list of events (currently all faults)
	
usage: aiq_cluster_events.py [-h] -u user [-p user_pass]
                             [--search-customer customer name]
                             [--search-string text to search for]
                             [--sort-order sort_order]
                             [--search-cluster search_cluster]

arguments:
	-h, --help            	show this help message and exit
	-u user               	AIQ username (required)
	-p user_pass          	AIQ password  (leave blank to get prompt with blanked entry)
	--sort-order 			Not used by this script due to issues with sorting columns with lists/dicts in them
	--node-id node_id     	Not used by this script
	--search-customer 		This needs to be in quotes if there are spaces in the customer name (required)
								Searches should be case insensitive, no need to match case
	--search-string 		This string searches the event "Message", it cannot do details due to the nature of the information returned (optional)
								Searches should be case insensitive, no need to match case
	--search-cluster		This is a specific cluster you want, if blank it will query all (optional)
	
example:
	python aiq_cluster_events.py -u test_user_1 --search-customer "<customer_name>"
	Enter password for user test_user_1:
	Output file name is: cluster_events_2021-01-14_15-54.txt
'+---------------+----------+---------+----------+------------+----------------+------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------------------+
'|    Cluster    | Event ID | Node ID | Drive ID | Service ID |      Type      |          Message             | Severity |                                                                                                                         Details                                                                                                                                  |    Report to AIQ Time    |        Event Time        |
'+---------------+----------+---------+----------+------------+----------------+------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -----+--------------------------+--------------------------+
'| cluster-0002  | 2375410  |    6    |   None   |    171     | schedulerEvent | Schedule action successful   |    0     |                                                                                          {'scheduleID': 26, 'scheduleType': 'Snapshot', 'scheduleName': 'flextest152-01'}                                                                                        | 2021-01-15T15:55:00.336Z | 2021-01-15T15:55:00.336Z |
'| cluster-0002  | 2375409  |    6    |   None   |    None    |    apiEvent    | API Call (CreateSnapshot)    |    0     |   {'success': True, 'params': {'scheduleID': 26, 'enableRemoteReplication': True, 'name': 'flextest152-01', 'volumeID': '7130', 'retention': '0:10:00'}, 'method': 'CreateSnapshot', 'context': {'ip': '0.0.0.0', 'authMethod': 'Cluster', 'user': 'internal'}}  | 2021-01-15T15:55:00.333Z | 2021-01-15T15:55:00.333Z |
'| cluster-0002  | 2375408  |    6    |   None   |    171     |   sliceEvent   |     Snapshot succeeded       |    0     |                                                                                                     {'snapshotID': 138591, 'volumeID': 7130, 'durationMS': 17}                                                                                                   | 2021-01-15T15:55:00.328Z | 2021-01-15T15:55:00.328Z |
'| cluster-0002  | 2375407  |    6    |   None   |    171     | schedulerEvent | Schedule action successful   |    0     |                                                                                          {'scheduleID': 25, 'scheduleType': 'Snapshot', 'scheduleName': 'flextest151-01'}                                                                                        | 2021-01-15T15:55:00.276Z | 2021-01-15T15:55:00.276Z |
'| cluster-0002  | 2375406  |    6    |   None   |    None    |    apiEvent    | API Call (CreateSnapshot)    |    0     |   {'success': True, 'params': {'scheduleID': 25, 'enableRemoteReplication': True, 'name': 'flextest151-01', 'volumeID': '7129', 'retention': '0:10:00'}, 'method': 'CreateSnapshot', 'context': {'ip': '0.0.0.0', 'authMethod': 'Cluster', 'user': 'internal'}}  | 2021-01-15T15:55:00.273Z | 2021-01-15T15:55:00.273Z |
'| cluster-0002  | 2375405  |    6    |   None   |    171     |   sliceEvent   |     Snapshot succeeded       |    0     |                                                                                                     {'snapshotID': 138590, 'volumeID': 7129, 'durationMS': 21}                                                                                                   | 2021-01-15T15:55:00.269Z | 2021-01-15T15:55:00.269Z |
'+---------------+----------+---------+----------+------------+----------------+------------------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------------------+
