import boto3
import re

redshiftclient = boto3.client('redshift')
ec2client = boto3.client('ec2')

cluster_name = 'cl123'

ec2 = boto3.resource('ec2')

# cr_response = redshiftclient.create_cluster(
#     DBName='db1',
#     ClusterIdentifier=cluster_name,
#     ClusterType='single-node',
#     NodeType='dc2.large',
#     MasterUsername='awsuser',
#     MasterUserPassword='AWSPass321',
#     # VpcSecurityGroupIds=[
#     #     grp_id,
#     # ],
#     #ClusterSubnetGroupName='redshift-subnet' + cluster_name,
#     Port=5439,
# #    NumberOfNodes=1,
#     PubliclyAccessible=True,
#     Encrypted=False,
#     Tags=[
#         {
#             'Key': 'created_by',
#             'Value': 'cloudmesh'
#         },
#     ]
# )
#
# print(cr_response)
# print("waiting for cluster to be available")
# waiter = redshiftclient.get_waiter('cluster_available')
#
# waiter.wait(
#     ClusterIdentifier='cl123',
#     TagKeys=[
#         'created_by',
#     ],
#     TagValues=[
#         'cloudmesh',
#     ],
#     WaiterConfig={
#         'Delay': 60,
#         'MaxAttempts': 30
#     }
# )
# print("after waiting")
#
#
desc_response = redshiftclient.describe_clusters(
    ClusterIdentifier=cluster_name,
)

print(desc_response)
print(desc_response['Clusters'][0]['VpcId'])
vpc_id = desc_response['Clusters'][0]['VpcId']

# print(desc_response['Clusters']['ClusterSecurityGroups']['ClusterSecurityGroupName'])

# grp_id = desc_response['Clusters']['ClusterSecurityGroups']['ClusterSecurityGroupName']

import boto3

vpc = ec2.Vpc(vpc_id)
# vpc_resp = vpc.get_available_subresources()
# print(vpc_resp)

# response = boto.create_security_group(GroupName='my_group_name', Description='my_description', VpcId=vpc_id)
# security_group_id = response['GroupId']


# sec_grp_response = vpc.create_security_group(
#     Description='RedShift VPC',
#     GroupName='vpc_sec_grp' + cluster_name,
#     VpcId=vpc_id,
#     DryRun=False
# )
#
# print(sec_grp_response)
#
# grp_id_list = re.findall(r"'(.*?)'", str(sec_grp_response), re.DOTALL)
# grp_id = grp_id_list[0]
# print(grp_id)



security_group_iterator = vpc.security_groups.all()
print(security_group_iterator)
for s in security_group_iterator:
    print(s)


security_group_iterator2 = vpc.security_groups.filter(
    GroupNames=[
        'default',
    ]
)
print(security_group_iterator2)
for s2 in security_group_iterator2:
    print(s2)

grp_id_list = re.findall(r"'(.*?)'", str(s2), re.DOTALL)
grp_id = grp_id_list[0]
print(grp_id)

security_group = ec2.SecurityGroup(grp_id)

sec_grp_ingress_response = security_group.authorize_ingress(
    GroupId = grp_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 5439,
            'ToPort': 5439,
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'all ext'
                },
            ],
            'UserIdGroupPairs': [{'GroupId': grp_id, 'VpcId': vpc_id}]
        }
        ],
    )
print(sec_grp_ingress_response)
