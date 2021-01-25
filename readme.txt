##################################################################################
#DO NOT SHARE OUTSIDE OF NETAPP WITHOUT REMOVING CUSTOMER DATA FROM THIS DOCUMENT#
##################################################################################
SolidFire AIQ access scripts
Date:	12-Jan-2021
Author:	Scott Chubb
Notes:	I am not a developer, the layout and script code can likely be improved and may well not meet best practices.
		--search-customer and --search-string as loose matches be sure to match required specificity
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

Three of these acts a modules and have no output of their own.  They should be in the same directory as the functional scripts.
	connect_auth_aiq.py
	get_aiq_customer.py
	get_aiq_inputs.py

Script:
	aiq_cluster_faults.py
	Used to pull faults from clusters, you can select what details you want to search on with --search-string
usage: aiq_cluster_faults.py [-h] -u user [-p user_pass]
                                [--search-customer customer name]
                                [--search-string text to search for]
                                [--sort-order sort_order] [--node-id node_id]

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
example:
	To match a specific customer and error message:
	python aiq_cluster_faults.py -u cscott --search-customer "jp morgan" --search-string "async delay"
	Enter password for user cscott:
	Output file name is: cluster_faults_2021-01-13_10-26.txt
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+
	|      Cluster       | Node ID | Drive ID | Service ID |             Date            |  Type  |  Severity |                           Details                            |
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+
	| SOLIDFIRE-CDC1-030 |    0    |    0     |     0      | 2020-06-12T21:02:44.326898Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |      360 minutes. Delayed volume pairs:[132:61, 137:62]      |
	| SOLIDFIRE-CDC2-011 |    0    |    0     |     0      | 2020-04-28T15:50:35.696887Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[30:25, 31:26, 32:27]    |
	| SOLIDFIRE-CDC2-012 |    0    |    0     |     0      | 2020-08-21T16:09:49.335146Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[1030:4732, 1032:4734,   |
	|                    |         |          |            |                             |        |           |                          1035:4737]                          |
	| SOLIDFIRE-CDC2-035 |    0    |    0     |     0      | 2020-04-28T15:50:40.735523Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[25:30, 26:31, 27:32]    |
	| SOLIDFIRE-CDC2-039 |    0    |    0     |     0      | 2020-06-12T21:03:00.327711Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |      360 minutes. Delayed volume pairs:[61:132, 62:137]      |
	| SOLIDFIRE-IDN1-002 |    0    |    0     |     0      | 2020-09-26T23:36:44.107438Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |         360 minutes. Delayed volume pairs:[637:480]          |
	| SOLIDFIRE-IDN2-002 |    0    |    0     |     0      | 2020-09-26T23:36:13.036622Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |         360 minutes. Delayed volume pairs:[480:637]          |
	| solidfire-belv-009 |    0    |    0     |     0      | 2020-08-21T16:09:50.590871Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |   360 minutes. Delayed volume pairs:[4732:1030, 4734:1032,   |
	|                    |         |          |            |                             |        |           |                          4737:1035]                          |
	| solidfire-brkl-002 |    0    |    0     |     0      | 2018-11-21T21:50:29.299977Z | volume |  warning  |  Replicating volume pairs have an Async Delay greater than   |
	|                    |         |          |            |                             |        |           |    360 minutes. Delayed volume pairs:[438:2270, 439:2271,    |
	|                    |         |          |            |                             |        |           | 440:2272, 441:2273, 442:2274, 443:2286, 444:2287, 445:2288,  |
	|                    |         |          |            |                             |        |           | 446:2289, 447:2290, 448:2291, 449:2292, 450:2293, 451:2294,  |
	|                    |         |          |            |                             |        |           | 452:2295, 453:2296, 454:2297, 455:2298, 456:2299, 457:2300,  |
	|                    |         |          |            |                             |        |           |                          458:2335]                           |
	+--------------------+---------+----------+------------+-----------------------------+--------+-----------+--------------------------------------------------------------+

	To match all alerts from a specific customer:
	python aiq_cluster_faults.py -u cscott --search-customer "cisco"
	Enter password for user cscott:
	Output file name is: cluster_faults_2021-01-13_11-44.txt
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+
	|          Cluster          | Node ID | Drive ID | Service ID |             Date            |   Type  |   Severity   |                           Details                            |
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+
	|     SVS-DR-SOLIDFIRE1     |    0    |    0     |     0      | 2019-03-25T00:00:03.421629Z | cluster |    error     |           The cluster SSL certificate has expired            |
	|     SVS-DR-SOLIDFIRE1     |    0    |    0     |     0      | 2020-01-22T18:56:30.612393Z | cluster |   warning    |    Add additional capacity or free up capacity as soon as    |
	|                           |         |          |            |                             |         |              |                          possible.                           |
	|     SVS-DR-SOLIDFIRE1     |    0    |    0     |     0      | 2020-01-22T19:16:09.104665Z | cluster |    error     |    Local replication and synchronization of the following    |
	|                           |         |          |            |                             |         |              | volumes is in progress. Progress of the synchronization can  |
	|                           |         |          |            |                             |         |              | be seen in the Running Tasks window. [2, 3, 4, 5, 8, 9, 10,  |
	|                           |         |          |            |                             |         |              |                 12, 13, 14, 15, 16, 18, 19]                  |
	|     SVS-DR-SOLIDFIRE1     |    0    |    0     |     0      | 2020-01-22T19:20:01.246902Z | cluster |    error     |  The following volumes are offline. [2, 3, 4, 5, 7, 9, 10,   |
	|                           |         |          |            |                             |         |              |                 11, 12, 13, 14, 15, 18, 19]                  |
	|     SVS-DR-SOLIDFIRE1     |    0    |    0     |     0      | 2020-01-24T18:30:47.380510Z | cluster |    error     |   Ensemble degraded: 2/5 database servers not connectable:   |
	|                           |         |          |            |                             |         |              |                {3:10.0.30.131,5:10.0.30.133}                 |
	|     SVS-RTP-SOLIDFIRE1    |    0    |    0     |     0      | 2018-05-24T18:00:50.640743Z | cluster |   warning    |       Schedule action failed for schedule IDs: [3,4].        |
	|     SVS-RTP-SOLIDFIRE1    |    0    |    0     |     0      | 2019-03-25T00:01:06.723096Z | cluster |    error     |           The cluster SSL certificate has expired            |
	|     SVS-RTP-SOLIDFIRE1    |    0    |    0     |     0      | 2020-01-24T18:38:15.080553Z | cluster |   warning    | Remote nodes are not connected via the cluster network. Ping |
	|                           |         |          |            |                             |         |              |  the remote nodes using jumbo frames to test connectivity.   |
	|                           |         |          |            |                             |         |              |     Disconnected nodes: [SVS-DR-SOLIDFIRE1:10.0.30.131,      |
	|                           |         |          |            |                             |         |              |                  10.0.30.133, 10.0.30.134]                   |
	|     SVS-RTP-SOLIDFIRE1    |    0    |    0     |     0      | 2020-01-27T17:46:32.437589Z | cluster |   warning    | One of the clusters in a pair may have become misconfigured  |
	|                           |         |          |            |                             |         |              | or disconnected.  Remove the local pairing and retry pairing |
	|                           |         |          |            |                             |         |              | the clusters. Disconnected Cluster Pairs: [1]. Misconfigured |
	|                           |         |          |            |                             |         |              |                      Cluster Pairs: []                       |
	|       aer01-fab3-pib      |    0    |    0     |     0      | 2019-02-28T18:10:42.990016Z | cluster | bestPractice |  SSH is enabled on nodes (1, 2, 3, 4, 5, 10) and any nodes   |
	|                           |         |          |            |                             |         |              |        added to the cluster will have SSH turned on.         |
	|      alln01-fab3-pib      |    0    |    0     |     0      | 2019-04-04T22:10:12.638054Z | cluster | bestPractice | SSH is enabled on nodes (27, 28, 31, 32, 33, 35, 36, 38, 39, |
	|                           |         |          |            |                             |         |              |  40, 41, 42, 43, 44, 45, 46, 48, 49) and any nodes added to  |
	|                           |         |          |            |                             |         |              |             the cluster will have SSH turned on.             |
	+---------------------------+---------+----------+------------+-----------------------------+---------+--------------+--------------------------------------------------------------+	

	To search all alerts from a specific customer and sort:
	python aiq_cluster_faults.py -u cscott --search-customer "jp morgan" --sort-order Details
	python aiq_cluster_faults.py -u cscott --search-customer "jp morgan" --sort-order Cluster
	python aiq_cluster_faults.py -u cscott --search-customer "jp morgan" --sort-order Date
	python aiq_cluster_faults.py -u cscott --search-customer "jp morgan" --sort-order Severity

########################################
#	Not recommended, but possible:     #
########################################
	To search all customers for a specific error message
	python aiq_cluster_faults.py -u cscott --search-string "async delay"
	
	To bring your machine to a halt for 30 plus minutes search everything:
	python aiq_cluster_faults.py -u cscott




Script:
	Note that this requires an 11.8 or higher mnode.  The output will indicate a constant not found in this situation.
	aiq_constants_info.py
	Pulls constants and their settings from AIQ for review
usage: aiq_constants_info.py [-h] -u user [-p user_pass]
                                [--search-customer customer name]
                                [--search-string text to search for]
                                [--sort-order sort_order] [--node-id node_id]
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

example:
	python aiq_constants_info.py -u cscott --search-customer "JP morg" --search-string cMemCtlrCorrectableErrLeakRate,cMemCtlrCorrectableErrWarnDuration,cMemCtlrCorrectableErrWarnThreshold
	Enter password for user cscott:
	Output file name is: cluster_constants_2021-01-13_11-37.txt
	+-------------+-------------------------------------+------------------+
	|   Cluster   |            Constant Name            | Constant Setting |
	+-------------+-------------------------------------+------------------+
	| hnyce04ac01 |    cMemCtlrCorrectableErrLeakRate   |        3         |
	| hnyce04ac01 |  cMemCtlrCorrectableErrWarnDuration |      86400       |
	| hnyce04ac01 | cMemCtlrCorrectableErrWarnThreshold |      100000      |
	+-------------+-------------------------------------+------------------+

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
	python aiq_get_nodes.py -u cscott --search-customer "cisco"
	Enter password for user cscott:
	Output file name is: full_report_2021-01-12.txt
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
	|          Cluster          |        Node Name         | Node ID | Element Vers | Node Type |   Serial No    | Service Tag  |    Mgmt IP     |   Storage IP   |
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr1   |    3    |  10.1.0.83   |  Unknown  |  FCH1942V1Q3   | FCH1942V1Q3  |  10.86.143.81  |  192.168.1.11  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr3   |    5    |  10.1.0.83   |  Unknown  |  FCH1942V1PW   | FCH1942V1PW  |  10.86.143.83  |  192.168.1.13  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr13  |    19   |  10.1.0.83   |  Unknown  |      None      | FCH2220V11B  |  10.86.143.60  |  192.168.1.23  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr9   |    15   |  10.1.0.83   |  Unknown  |  FCH2143V0Y3   | FCH2143V0Y3  |  10.86.143.54  |  192.168.1.19  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr14  |    20   |  10.1.0.83   |  Unknown  |      None      | FCH2220V11D  |  10.86.143.61  |  192.168.1.24  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr5   |    21   |  10.1.0.83   |  Unknown  |  FCH2017V1EH   | FCH2017V1EH  |  10.86.143.85  |  192.168.1.15  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr8   |    14   |  10.1.0.83   |  Unknown  |  FCH2143V0YJ   | FCH2143V0YJ  |  10.86.143.53  |  192.168.1.18  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr2   |    4    |  10.1.0.83   |  Unknown  |  FCH1942V1Q0   | FCH1942V1Q0  |  10.86.143.82  |  192.168.1.12  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr10  |    16   |  10.1.0.83   |  Unknown  |  FCH2143V103   | FCH2143V103  |  10.86.143.55  |  192.168.1.20  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr12  |    18   |  10.1.0.83   |  Unknown  |  FCH2143V1G9   | FCH2143V1G9  |  10.86.143.59  |  192.168.1.22  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr4   |    6    |  10.1.0.83   |  Unknown  |  FCH1942V1Q4   | FCH1942V1Q4  |  10.86.143.84  |  192.168.1.14  |
	| aurora-solidfire-cluster1 |   ccbu-solidfire-svr6    |    12   |  10.1.0.83   |  Unknown  |  FCH2038V0CH   | FCH2038V0CH  |  10.86.143.86  |  192.168.1.16  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr7   |    13   |  10.1.0.83   |  Unknown  |  FCH2143V0YH   | FCH2143V0YH  |  10.86.143.52  |  192.168.1.17  |
	| aurora-solidfire-cluster1 |   aurora-solidfire-fcb   |    2    |  10.1.0.83   |  Unknown  | NNG05154111108 |   14Y4P22    |  10.86.143.80  |  192.168.1.4   |
	| aurora-solidfire-cluster1 |   aurora-solidfire-fca   |    1    |  10.1.0.83   |  Unknown  | NNG05154111107 |   14Z5P22    |  10.86.143.79  |  192.168.1.3   |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr11  |    17   |  10.1.0.83   |  Unknown  |  FCH2143V17S   | FCH2143V17S  |  10.86.143.57  |  192.168.1.21  |
	|           intlab          |     iscsi2.acme.test     |    2    |  12.2.0.777  |  SF19210  |      None      |   2N7JPD2    | 192.168.100.12 | 192.168.101.12 |
	|           intlab          |     iscsi3.acme.test     |    3    |  12.2.0.777  |  SF19210  |      None      |   58DNND2    | 192.168.100.13 | 192.168.101.13 |
	|           intlab          |         SF-927A          |    8    |  12.2.0.777  |  SF19210  |  701846000014  |   GDDHCP2    | 192.168.100.35 | 192.168.101.19 |
	|           intlab          |     iscsi1.acme.test     |    1    |  12.2.0.777  |  SF19210  |      None      |   58FKND2    | 192.168.100.11 | 192.168.101.11 |
	|           intlab          |     iscsi4.acme.test     |    4    |  12.2.0.777  |  SF19210  |      None      |   53NDND2    | 192.168.100.14 | 192.168.101.14 |
	|         sf-24k-c1         |        sf-24k-fca        |    7    |  11.5.1.14   |  SF19210  | STVJM172024004 |   J3Y6HH2    |  10.86.143.66  |  192.168.1.6   |
	|         sf-24k-c1         |       sf-24k-svr5        |    5    |  11.5.1.14   |  Unknown  |  FCH2139V05X   | FCH2139V05X  |  10.86.143.76  |  192.168.1.25  |
	|         sf-24k-c1         |       sf-24k-svr3        |    3    |  11.5.1.14   |  Unknown  |  FCH2138V2H5   | FCH2138V2H5  |  10.86.143.74  |  192.168.1.23  |
	|         sf-24k-c1         |        sf-24k-fcb        |    8    |  11.5.1.14   |  SF19210  | STVJM172024002 |   J3Y8HH2    |  10.86.143.67  |  192.168.1.7   |
	|         sf-24k-c1         |       sf-24k-svr6        |    6    |  11.5.1.14   |  Unknown  |  FCH2138V1KE   | FCH2138V1KE  |  10.86.143.77  |  192.168.1.26  |
	|         sf-24k-c1         |       sf-24k-svr2        |    2    |  11.5.1.14   |  Unknown  |  FCH2138V05P   | FCH2138V05P  |  10.86.143.69  |  192.168.1.22  |
	|         sf-24k-c1         |       sf-24k-svr1        |    1    |  11.5.1.14   |  Unknown  |  FCH2137V1DM   | FCH2137V1DM  |  10.86.143.68  |  192.168.1.21  |
	|         sf-24k-c1         |       sf-24k-svr4        |    4    |  11.5.1.14   |  Unknown  |  FCH2138V2D2   | FCH2138V2D2  |  10.86.143.75  |  192.168.1.24  |
	|        dfw01sdfr01        |        ztx1sld004        |    7    |  10.4.0.35   |  Unknown  |  FCH2127V0AT   | FCH2127V0AT  | 10.255.12.229  |  10.240.59.7   |
	|        dfw01sdfr01        |        ztx1sld001        |    8    |  10.4.0.35   |  Unknown  |  FCH2127V0H8   | FCH2127V0H8  | 10.255.12.226  |  10.240.59.4   |
	|        dfw01sdfr01        |        ztx1sld002        |    6    |  10.4.0.35   |  Unknown  |  FCH2127V0HC   | FCH2127V0HC  | 10.255.12.227  |  10.240.59.5   |
	|        dfw01sdfr01        |        ztx1sld003        |    5    |  10.4.0.35   |  Unknown  |  FCH2127V012   | FCH2127V012  | 10.255.12.228  |  10.240.59.6   |
	|        yyz01sdfr01        |        zto1sld001        |    1    |  11.8.0.23   |  Unknown  |  FCH2129V27V   | FCH2129V27V  |  10.250.6.20   | 10.240.245.36  |
	|        yyz01sdfr01        |        zto1sld002        |    2    |  11.8.0.23   |  Unknown  |  FCH2129V2JD   | FCH2129V2JD  |  10.250.6.21   | 10.240.245.37  |
	|        yyz01sdfr01        |        zto1sld004        |    4    |  11.8.0.23   |  Unknown  |  FCH2119V0XE   | FCH2119V0XE  |  10.250.6.23   | 10.240.245.39  |
	|        yyz01sdfr01        |        zto1sld003        |    3    |  11.8.0.23   |  Unknown  |  FCH2129V2ZA   | FCH2129V2ZA  |  10.250.6.22   | 10.240.245.38  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az3-003  |    41   |  11.8.0.23   |   H610S   |  371907000068  | 371907000068 |  10.123.227.6  |  10.123.227.6  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az3-006  |    40   |  11.8.0.23   |   H610S   |  371833000193  | 371833000193 |  10.123.227.9  |  10.123.227.9  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az1-013  |    33   |  11.8.0.23   |   H610S   |  371850000063  | 371850000063 | 10.123.227.16  | 10.123.227.16  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az1-010  |    35   |  11.8.0.23   |   H610S   |  371850000043  | 371850000043 | 10.123.227.13  | 10.123.227.13  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az2-020  |    44   |  11.8.0.23   |   H610S   |  371907000049  | 371907000049 | 10.123.227.20  | 10.123.227.20  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az3-009  |    49   |  11.8.0.23   |   H610S   |  371907000052  | 371907000052 | 10.123.227.12  | 10.123.227.12  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az1-007  |    27   |  11.8.0.23   |   H610S   |  371850000048  | 371850000048 | 10.123.227.10  | 10.123.227.10  |
	|      alln01-fab3-pib      | alln01-fab3-pib-az2-002  |    43   |  11.8.0.23   |   H610S   |  371907000109  | 371907000109 |  10.123.227.5  |  10.123.227.5  |
	+---------------------------+--------------------------+---------+--------------+-----------+----------------+--------------+----------------+----------------+
	
	python aiq_get_nodes.py -u cscott --search-customer "cisco" --model SF19210 --version 12.2.0.777
	Enter password for user cscott:
	Output file name is: model_SF19210_2021-01-12.txt
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
	|         Cluster         |       Node Name       | Node ID | Element Vers | Node Type |   Serial No    | Service Tag |    Mgmt IP     |   Storage IP   |
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
	|          intlab         |    iscsi2.acme.test   |    2    |  12.2.0.777  |  SF19210  |      None      |   2N7JPD2   | 192.168.100.12 | 192.168.101.12 |
	|          intlab         |    iscsi3.acme.test   |    3    |  12.2.0.777  |  SF19210  |      None      |   58DNND2   | 192.168.100.13 | 192.168.101.13 |
	|          intlab         |        SF-927A        |    8    |  12.2.0.777  |  SF19210  |  701846000014  |   GDDHCP2   | 192.168.100.35 | 192.168.101.19 |
	|          intlab         |    iscsi1.acme.test   |    1    |  12.2.0.777  |  SF19210  |      None      |   58FKND2   | 192.168.100.11 | 192.168.101.11 |
	|          intlab         |    iscsi4.acme.test   |    4    |  12.2.0.777  |  SF19210  |      None      |   53NDND2   | 192.168.100.14 | 192.168.101.14 |
	|        sf-24k-c1        |       sf-24k-fca      |    7    |  11.5.1.14   |  SF19210  | STVJM172024004 |   J3Y6HH2   |  10.86.143.66  |  192.168.1.6   |
	|        sf-24k-c1        |       sf-24k-fcb      |    8    |  11.5.1.14   |  SF19210  | STVJM172024002 |   J3Y8HH2   |  10.86.143.67  |  192.168.1.7   |
	|         pod-nam         |        SF-AA39        |    10   |  12.2.0.777  |  SF19210  |  701846000015  |   2TCSCP2   | 10.83.145.217  | 10.200.203.15  |
	|         pod-nam         |        SF-B748        |    11   |  12.2.0.777  |  SF19210  |  701821000173  |   GH2KCP2   | 10.83.145.213  | 10.200.203.11  |
	|         pod-nam         |        SF-F2BB        |    13   |  12.2.0.777  |  SF19210  |  701820000024  |   GFXGCP2   | 10.83.145.216  | 10.200.203.14  |
	|         pod-nam         |        SF-C6A9        |    12   |  12.2.0.777  |  SF19210  |  701823000003  |   2N2SCP2   | 10.83.145.215  | 10.200.203.13  |
	|         pod-nam         |        SF-08EC        |    7    |  12.2.0.777  |  SF19210  |  701821000171  |   GH1HCP2   | 10.83.145.214  | 10.200.203.12  |
	| ccbu-solidfire-cluster2 |  ccbu-solidfire2-fca  |    1    |  11.5.0.63   |  SF19210  |  701840000074  |   2SQVMN2   |  10.86.143.95  |  192.168.1.3   |
	| ccbu-solidfire-cluster2 |  ccbu-solidfire2-fcb  |    2    |  11.5.0.63   |  SF19210  |  701810000001  |   8C4FHL2   |  10.86.143.96  |  192.168.1.4   |
	|    SVS-RTP-SOLIDFIRE1   |  SVS-RTP-SOLIDFIRE-N4 |    8    |  10.1.0.83   |  SF19210  | STVJM171425043 |   5NNRDH2   |   10.0.29.34   |   10.0.30.34   |
	|    SVS-RTP-SOLIDFIRE1   | SVS-RTP-SOLIDFIRE-FC4 |    4    |  10.1.0.83   |  SF19210  | STVJM171424002 |   J3R6HH2   |   10.0.29.24   |   10.0.30.24   |
	|    SVS-RTP-SOLIDFIRE1   | SVS-RTP-SOLIDFIRE-FC2 |    9    |  10.1.0.83   |  SF19210  | STVJM171124015 |   8MTJDH2   |   10.0.29.22   |   10.0.30.22   |
	|    SVS-RTP-SOLIDFIRE1   |  SVS-RTP-SOLIDFIRE-N1 |    5    |  10.1.0.83   |  SF19210  | STVJM171425041 |   5NN2HH2   |   10.0.29.31   |   10.0.30.31   |
	|    SVS-RTP-SOLIDFIRE1   | SVS-RTP-SOLIDFIRE-FC3 |    3    |  10.1.0.83   |  SF19210  | STVJM171424008 |   J3YXDH2   |   10.0.29.23   |   10.0.30.23   |
	|    SVS-RTP-SOLIDFIRE1   |  SVS-RTP-SOLIDFIRE-N2 |    6    |  10.1.0.83   |  SF19210  | STVJM171425042 |   5NN3HH2   |   10.0.29.32   |   10.0.30.32   |
	|    SVS-RTP-SOLIDFIRE1   |  SVS-RTP-SOLIDFIRE-N3 |    7    |  10.1.0.83   |  SF19210  | STVJM171425022 |   5NVXDH2   |   10.0.29.33   |   10.0.30.33   |
	|    SVS-RTP-SOLIDFIRE1   | SVS-RTP-SOLIDFIRE-FC1 |    1    |  10.1.0.83   |  SF19210  | STVJM171424022 |   J3YQDH2   |   10.0.29.21   |   10.0.30.21   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-FC2 |    2    |  10.1.0.83   |  SF19210  | STVJM171424025 |   J3KRDH2   |  10.0.29.122   |  10.0.30.122   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-N1  |    3    |  10.1.0.83   |  SF19210  | STVJM171425009 |   5NMXDH2   |  10.0.29.131   |  10.0.30.131   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-N3  |    5    |  10.1.0.83   |  SF19210  | STVJM171425003 |   5NTVDH2   |  10.0.29.133   |  10.0.30.133   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-FC1 |    1    |  10.1.0.83   |  SF19210  | STVJM171424016 |   J3YRDH2   |  10.0.29.121   |  10.0.30.121   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-N2  |    4    |  10.1.0.83   |  SF19210  | STVJM170625891 |   33NGXG2   |  10.0.29.132   |  10.0.30.132   |
	|    SVS-DR-SOLIDFIRE1    |  SVS-DR-SOLIDFIRE-N4  |    6    |  10.1.0.83   |  SF19210  | STVJM171425029 |   5NVWDH2   |  10.0.29.134   |  10.0.30.134   |
	+-------------------------+-----------------------+---------+--------------+-----------+----------------+-------------+----------------+----------------+
	
	python aiq_get_nodes.py -u cscott --search-customer "cisco" --version 10.1.0.83
	Enter password for user cscott:
	Output file name is: version_10.1.0.83_2021-01-12.txt
	+---------------------------+------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
	|          Cluster          |       Node Name        | Node ID | Element Vers | Node Type |   Serial No    | Service Tag |   Mgmt IP    |  Storage IP  |
	+---------------------------+------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
	| aurora-solidfire-cluster1 | aurora-solidfire-svr1  |    3    |  10.1.0.83   |  Unknown  |  FCH1942V1Q3   | FCH1942V1Q3 | 10.86.143.81 | 192.168.1.11 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr3  |    5    |  10.1.0.83   |  Unknown  |  FCH1942V1PW   | FCH1942V1PW | 10.86.143.83 | 192.168.1.13 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr13 |    19   |  10.1.0.83   |  Unknown  |      None      | FCH2220V11B | 10.86.143.60 | 192.168.1.23 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr9  |    15   |  10.1.0.83   |  Unknown  |  FCH2143V0Y3   | FCH2143V0Y3 | 10.86.143.54 | 192.168.1.19 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr14 |    20   |  10.1.0.83   |  Unknown  |      None      | FCH2220V11D | 10.86.143.61 | 192.168.1.24 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr5  |    21   |  10.1.0.83   |  Unknown  |  FCH2017V1EH   | FCH2017V1EH | 10.86.143.85 | 192.168.1.15 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr8  |    14   |  10.1.0.83   |  Unknown  |  FCH2143V0YJ   | FCH2143V0YJ | 10.86.143.53 | 192.168.1.18 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr2  |    4    |  10.1.0.83   |  Unknown  |  FCH1942V1Q0   | FCH1942V1Q0 | 10.86.143.82 | 192.168.1.12 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr10 |    16   |  10.1.0.83   |  Unknown  |  FCH2143V103   | FCH2143V103 | 10.86.143.55 | 192.168.1.20 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr12 |    18   |  10.1.0.83   |  Unknown  |  FCH2143V1G9   | FCH2143V1G9 | 10.86.143.59 | 192.168.1.22 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr4  |    6    |  10.1.0.83   |  Unknown  |  FCH1942V1Q4   | FCH1942V1Q4 | 10.86.143.84 | 192.168.1.14 |
	| aurora-solidfire-cluster1 |  ccbu-solidfire-svr6   |    12   |  10.1.0.83   |  Unknown  |  FCH2038V0CH   | FCH2038V0CH | 10.86.143.86 | 192.168.1.16 |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr7  |    13   |  10.1.0.83   |  Unknown  |  FCH2143V0YH   | FCH2143V0YH | 10.86.143.52 | 192.168.1.17 |
	| aurora-solidfire-cluster1 |  aurora-solidfire-fcb  |    2    |  10.1.0.83   |  Unknown  | NNG05154111108 |   14Y4P22   | 10.86.143.80 | 192.168.1.4  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-fca  |    1    |  10.1.0.83   |  Unknown  | NNG05154111107 |   14Z5P22   | 10.86.143.79 | 192.168.1.3  |
	| aurora-solidfire-cluster1 | aurora-solidfire-svr11 |    17   |  10.1.0.83   |  Unknown  |  FCH2143V17S   | FCH2143V17S | 10.86.143.57 | 192.168.1.21 |
	|     SVS-RTP-SOLIDFIRE1    |  SVS-RTP-SOLIDFIRE-N4  |    8    |  10.1.0.83   |  SF19210  | STVJM171425043 |   5NNRDH2   |  10.0.29.34  |  10.0.30.34  |
	|     SVS-RTP-SOLIDFIRE1    | SVS-RTP-SOLIDFIRE-FC4  |    4    |  10.1.0.83   |  SF19210  | STVJM171424002 |   J3R6HH2   |  10.0.29.24  |  10.0.30.24  |
	|     SVS-RTP-SOLIDFIRE1    | SVS-RTP-SOLIDFIRE-FC2  |    9    |  10.1.0.83   |  SF19210  | STVJM171124015 |   8MTJDH2   |  10.0.29.22  |  10.0.30.22  |
	|     SVS-RTP-SOLIDFIRE1    |  SVS-RTP-SOLIDFIRE-N1  |    5    |  10.1.0.83   |  SF19210  | STVJM171425041 |   5NN2HH2   |  10.0.29.31  |  10.0.30.31  |
	|     SVS-RTP-SOLIDFIRE1    | SVS-RTP-SOLIDFIRE-FC3  |    3    |  10.1.0.83   |  SF19210  | STVJM171424008 |   J3YXDH2   |  10.0.29.23  |  10.0.30.23  |
	|     SVS-RTP-SOLIDFIRE1    |  SVS-RTP-SOLIDFIRE-N2  |    6    |  10.1.0.83   |  SF19210  | STVJM171425042 |   5NN3HH2   |  10.0.29.32  |  10.0.30.32  |
	|     SVS-RTP-SOLIDFIRE1    |  SVS-RTP-SOLIDFIRE-N3  |    7    |  10.1.0.83   |  SF19210  | STVJM171425022 |   5NVXDH2   |  10.0.29.33  |  10.0.30.33  |
	|     SVS-RTP-SOLIDFIRE1    | SVS-RTP-SOLIDFIRE-FC1  |    1    |  10.1.0.83   |  SF19210  | STVJM171424022 |   J3YQDH2   |  10.0.29.21  |  10.0.30.21  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-FC2  |    2    |  10.1.0.83   |  SF19210  | STVJM171424025 |   J3KRDH2   | 10.0.29.122  | 10.0.30.122  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-N1   |    3    |  10.1.0.83   |  SF19210  | STVJM171425009 |   5NMXDH2   | 10.0.29.131  | 10.0.30.131  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-N3   |    5    |  10.1.0.83   |  SF19210  | STVJM171425003 |   5NTVDH2   | 10.0.29.133  | 10.0.30.133  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-FC1  |    1    |  10.1.0.83   |  SF19210  | STVJM171424016 |   J3YRDH2   | 10.0.29.121  | 10.0.30.121  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-N2   |    4    |  10.1.0.83   |  SF19210  | STVJM170625891 |   33NGXG2   | 10.0.29.132  | 10.0.30.132  |
	|     SVS-DR-SOLIDFIRE1     |  SVS-DR-SOLIDFIRE-N4   |    6    |  10.1.0.83   |  SF19210  | STVJM171425029 |   5NVWDH2   | 10.0.29.134  | 10.0.30.134  |
	+---------------------------+------------------------+---------+--------------+-----------+----------------+-------------+--------------+--------------+
	
	python aiq_get_nodes.py -u cscott --search-customer "cisco" --no-serial
	Enter password for user cscott:
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	|          Cluster          |        Node Name         | Node ID | Element Vers | Node Type | Serial No | Service Tag  |    Mgmt IP     |   Storage IP   |
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr13  |    19   |  10.1.0.83   |  Unknown  |    None   | FCH2220V11B  |  10.86.143.60  |  192.168.1.23  |
	| aurora-solidfire-cluster1 |  aurora-solidfire-svr14  |    20   |  10.1.0.83   |  Unknown  |    None   | FCH2220V11D  |  10.86.143.61  |  192.168.1.24  |
	|           intlab          |     iscsi2.acme.test     |    2    |  12.2.0.777  |  SF19210  |    None   |   2N7JPD2    | 192.168.100.12 | 192.168.101.12 |
	|           intlab          |     iscsi3.acme.test     |    3    |  12.2.0.777  |  SF19210  |    None   |   58DNND2    | 192.168.100.13 | 192.168.101.13 |
	|           intlab          |     iscsi1.acme.test     |    1    |  12.2.0.777  |  SF19210  |    None   |   58FKND2    | 192.168.100.11 | 192.168.101.11 |
	|           intlab          |     iscsi4.acme.test     |    4    |  12.2.0.777  |  SF19210  |    None   |   53NDND2    | 192.168.100.14 | 192.168.101.14 |
	|        dfw02sdfr02        |        zta1sld007        |    13   |  10.4.0.35   |  Unknown  |    None   | FCH2201V0BQ  | 10.240.161.96  | 10.240.192.141 |
	|        dfw02sdfr02        |        zta1sld006        |    2    |  10.4.0.35   |  Unknown  |    None   | FCH2134V06W  | 10.240.161.95  | 10.240.192.140 |
	|        dfw02sdfr02        |        zta1sld008        |    4    |  10.4.0.35   |  Unknown  |    None   | FCH2202V0PR  | 10.240.161.97  | 10.240.192.142 |
	|        dfw02sdfr02        |        zta1sld005        |    1    |  10.4.0.35   |  Unknown  |    None   | FCH2134V03X  | 10.240.161.94  | 10.240.192.139 |
	|        dfw01sdfr02        |      dfw01sdfr02-03      |    11   |  10.4.0.35   |   H610S   |    None   | 371832000074 |  10.240.5.103  |  10.240.59.35  |
	|        dfw01sdfr02        |        ztx1sld011        |    7    |  10.4.0.35   |  Unknown  |    None   | FCH2201V105  |  10.240.5.175  |  10.240.59.15  |
	|        dfw01sdfr02        |        ztx1sld005        |    21   |  10.4.0.35   |  Unknown  |    None   | FCH2134V00D  |  10.240.5.169  |  10.240.59.9   |
	|        dfw01sdfr02        |        ztx1sld009        |    5    |  10.4.0.35   |  Unknown  |    None   | FCH2201V101  |  10.240.5.173  |  10.240.59.13  |
	|        dfw01sdfr02        |        ztx1sld007        |    3    |  10.4.0.35   |  Unknown  |    None   | FCH2133V1QS  |  10.240.5.171  |  10.240.59.11  |
	|        dfw01sdfr02        |        ztx1sld006        |    2    |  10.4.0.35   |  Unknown  |    None   | FCH2133V2JD  |  10.240.5.170  |  10.240.59.10  |
	|        dfw01sdfr02        |        ztx1sld012        |    8    |  10.4.0.35   |  Unknown  |    None   | FCH2201V107  |  10.240.5.166  |  10.240.59.16  |
	|        dfw01sdfr02        |        ztx1sld010        |    6    |  10.4.0.35   |  Unknown  |    None   | FCH2201V106  |  10.240.5.174  |  10.240.59.14  |
	|        sjcl1sdfr01        |      sjcl1sdfr01-02      |    2    |  11.8.0.23   |  Unknown  |    None   | FCH2129V2TZ  | 10.100.22.245  | 10.100.20.134  |
	|        sjcl1sdfr01        |      sjcl1sdfr01-01      |    1    |  11.8.0.23   |  Unknown  |    None   | FCH2129V2S0  | 10.100.22.241  | 10.100.20.133  |
	|        sin01sdfr03        |      sin01sdfr03-04      |    4    |  11.8.0.23   |  Unknown  |    None   | FCH2133V0HR  | 10.120.152.168 | 10.120.152.200 |
	|        sin01sdfr03        |      sin01sdfr03-03      |    3    |  11.8.0.23   |  Unknown  |    None   | FCH2132V1SH  | 10.120.152.167 | 10.120.152.199 |
	|        sin01sdfr03        |      sin01sdfr03-02      |    2    |  11.8.0.23   |  Unknown  |    None   | FCH2133V0J9  | 10.120.152.166 | 10.120.152.198 |
	|        lhr03sdfr03        |      lhr03sdfr03-05      |    8    |   10.4.2.9   |   H610S   |    None   | 371844000011 | 10.120.110.235 | 10.120.104.201 |
	|  ccbu-solidfire-cluster2  |   ccbu-solidfire2-svr4   |    6    |  11.5.0.63   |  Unknown  |    None   | FCH2253V015  | 10.86.143.100  |  192.168.1.14  |
	|  ccbu-solidfire-cluster2  |   ccbu-solidfire2-svr1   |    3    |  11.5.0.63   |  Unknown  |    None   | FCH2251V0BD  |  10.86.143.97  |  192.168.1.11  |
	|  ccbu-solidfire-cluster2  |   ccbu-solidfire2-svr2   |    4    |  11.5.0.63   |  Unknown  |    None   | FCH2253V033  |  10.86.143.98  |  192.168.1.12  |
	|  ccbu-solidfire-cluster2  |   ccbu-solidfire2-svr3   |    5    |  11.5.0.63   |  Unknown  |    None   | FCH2253V035  |  10.86.143.99  |  192.168.1.13  |
	|   syd01sdfr01.webex.com   | syd01sdfr01-05.webex.com |    5    |  11.8.0.23   |   H610S   |    None   | 371930000038 | 10.246.39.152  |  10.246.39.23  |
	+---------------------------+--------------------------+---------+--------------+-----------+-----------+--------------+----------------+----------------+
	
	
Script:
	aiq_cluster_faults.py
usage: aiq_cluster_faults.py [-h] -u user [-p user_pass]
                                [--search-customer customer name]
                                [--search-string text to search for]
                                [--sort-order sort_order] [--node-id node_id]

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
	
	python aiq_node_network_info.py -u cscott --search-customer "bank of amer" --search-string LABSFH610SC01 --node-id 7
	Enter password for user cscott:
	Output file name is: node_ip_cfg_info_2021-01-14_15-54.txt
	+---------+--------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+
	|   Bond  |   Address    |      Mode     |          DNS Search         |         DNS servers          | MTU  |     Netmask     |   Gateway    | VLAN |
	+---------+--------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+
	|  Bond1G |              | ActivePassive | elab.corp.bankofamerica.com | 171.140.4.138, 171.172.3.251 | 1500 |                 |              |  0   |
	| Bond10G | 30.245.191.4 |      LACP     | elab.corp.bankofamerica.com | 171.140.4.138, 171.172.3.251 | 9000 | 255.255.255.192 | 30.245.191.1 |  0   |
	+---------+--------------+---------------+-----------------------------+------------------------------+------+-----------------+--------------+------+

Script:
	aiq_cluster_events.py
	Pulls a list of events (currently all faults)
	
usage: aiq_cluster_events.py [-h] -u user [-p user_pass]
                                [--search-customer customer name]
                                [--search-string text to search for]
                                [--sort-order sort_order] [--node-id node_id]

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
	python aiq_cluster_events.py -u cscott --search-customer "bank of amer"
	Enter password for user cscott:
	Output file name is: cluster_events_2021-01-14_15-54.txt
+---------------+----------+---------+----------+------------+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------------------+
|    Cluster    | Event ID | Node ID | Drive ID | Service ID |      Type      |                                                                                    Message                                                                                    | Severity |                                                                                                                                                                                   Details                                                                                                                                                                                   |    Report to AIQ Time    |        Event Time        |
+---------------+----------+---------+----------+------------+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------------------+
| LABSFH610SC01 | 2375410  |    6    |   None   |    171     | schedulerEvent |                                                                           Schedule action successful                                                                          |    0     |                                                                                                                                               {'scheduleID': 26, 'scheduleType': 'Snapshot', 'scheduleName': 'flextest152-01'}                                                                                                                                              | 2021-01-15T15:55:00.336Z | 2021-01-15T15:55:00.336Z |
| LABSFH610SC01 | 2375409  |    6    |   None   |    None    |    apiEvent    |                                                                           API Call (CreateSnapshot)                                                                           |    0     |                                                        {'success': True, 'params': {'scheduleID': 26, 'enableRemoteReplication': True, 'name': 'flextest152-01', 'volumeID': '7130', 'retention': '0:10:00'}, 'method': 'CreateSnapshot', 'context': {'ip': '0.0.0.0', 'authMethod': 'Cluster', 'user': 'internal'}}                                                        | 2021-01-15T15:55:00.333Z | 2021-01-15T15:55:00.333Z |
| LABSFH610SC01 | 2375408  |    6    |   None   |    171     |   sliceEvent   |                                                                               Snapshot succeeded                                                                              |    0     |                                                                                                                                                          {'snapshotID': 138591, 'volumeID': 7130, 'durationMS': 17}                                                                                                                                                         | 2021-01-15T15:55:00.328Z | 2021-01-15T15:55:00.328Z |
| LABSFH610SC01 | 2375407  |    6    |   None   |    171     | schedulerEvent |                                                                           Schedule action successful                                                                          |    0     |                                                                                                                                               {'scheduleID': 25, 'scheduleType': 'Snapshot', 'scheduleName': 'flextest151-01'}                                                                                                                                              | 2021-01-15T15:55:00.276Z | 2021-01-15T15:55:00.276Z |
| LABSFH610SC01 | 2375406  |    6    |   None   |    None    |    apiEvent    |                                                                           API Call (CreateSnapshot)                                                                           |    0     |                                                        {'success': True, 'params': {'scheduleID': 25, 'enableRemoteReplication': True, 'name': 'flextest151-01', 'volumeID': '7129', 'retention': '0:10:00'}, 'method': 'CreateSnapshot', 'context': {'ip': '0.0.0.0', 'authMethod': 'Cluster', 'user': 'internal'}}                                                        | 2021-01-15T15:55:00.273Z | 2021-01-15T15:55:00.273Z |
| LABSFH610SC01 | 2375405  |    6    |   None   |    171     |   sliceEvent   |                                                                               Snapshot succeeded                                                                              |    0     |                                                                                                                                                          {'snapshotID': 138590, 'volumeID': 7129, 'durationMS': 21}                                                                                                                                                         | 2021-01-15T15:55:00.269Z | 2021-01-15T15:55:00.269Z |
+---------------+----------+---------+----------+------------+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------+--------------------------+