import boto3
import re

redshiftclient = boto3.client('redshift')
ec2client = boto3.client('ec2')

cluster_name = 'cl123'

ec2 = boto3.resource('ec2')

vpcresponse = ec2client.create_vpc(
    CidrBlock='162.206.0.0/28',
    AmazonProvidedIpv6CidrBlock=True,
    DryRun=False,
)
print(vpcresponse)
print(vpcresponse['Vpc']['VpcId'])
vpc = ec2.Vpc(vpcresponse['Vpc']['VpcId'])

sec_grp_response = vpc.create_security_group(
    Description='RedShift VPC',
    GroupName='vpc_sec_grp' + cluster_name,
    VpcId=vpcresponse['Vpc']['VpcId'],
    DryRun=False
)

print(sec_grp_response)

grp_id_list = re.findall(r"'(.*?)'", str(sec_grp_response), re.DOTALL)
grp_id = grp_id_list[0]
print(grp_id)
#
# sec_grp_ingress_response = ec2client.authorize_security_group_ingress(GroupName=grp_id[0],
#                                             IpProtocol='tcp',
#                                             FromPort=5439,
#                                             ToPort=5439,
#                                             CidrIp='0.0.0.0/24')
#
# print(sec_grp_ingress_response)



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
            'UserIdGroupPairs': [{'GroupId': grp_id, 'VpcId': vpcresponse['Vpc']['VpcId']}]
        }
        ],
    )
print(sec_grp_ingress_response)

# subnet_response = ec2client.create_subnet(
#     CidrBlock='10.0.0.0/16',
#     VpcId=vpcresponse['Vpc']['VpcId'],
#     DryRun=False
# )
#
# print(subnet_response)
# print(subnet_response['Subnet']['SubnetId'])


subnet_response = vpc.create_subnet(
    CidrBlock='10.0.0.0/16'
)

print(subnet_response)
subnet_id_list = re.findall(r"'(.*?)'", str(subnet_response), re.DOTALL)
subnet_id = subnet_id_list[0]
print(subnet_id)

# print(subnet_response['Subnet']['SubnetId'])


cluster_subnet_response = redshiftclient.create_cluster_subnet_group(
    ClusterSubnetGroupName='redshift-subnet' + cluster_name,
    Description='Redshift subnet group',
    SubnetIds=[subnet_id]
    )

print(cluster_subnet_response)


gateway_id_resp = ec2client.create_internet_gateway()

print(gateway_id_resp)
gateway_id=gateway_id_resp['InternetGateway']['InternetGatewayId']

# gateway_id_list = re.findall(r"'(.*?)'", str(gateway_id_resp), re.DOTALL)
# gateway_id = gateway_id_list[0]
print(gateway_id)

vpc_attach_response = vpc.attach_internet_gateway(InternetGatewayId=gateway_id)

response = redshiftclient.create_cluster(
    DBName='db1',
    ClusterIdentifier=cluster_name,
    ClusterType='single-node',
    NodeType='dc2.large',
    MasterUsername='awsuser',
    MasterUserPassword='AWSPass321',
    # VpcSecurityGroupIds=[
    #     grp_id,
    # ],
    ClusterSubnetGroupName='redshift-subnet' + cluster_name,
    Port=5439,
#    NumberOfNodes=1,
    PubliclyAccessible=True,
    Encrypted=False,
    Tags=[
        {
            'Key': 'created_by',
            'Value': 'cloudmesh'
        },
    ]
)

print(response)
waiter = redshiftclient.get_waiter('cluster_available')

waiter.wait(
    ClusterIdentifier='cl123',
    TagKeys=[
        'created_by',
    ],
    TagValues=[
        'cloudmesh',
    ],
    WaiterConfig={
        'Delay': 60,
        'MaxAttempts': 30
    }
)
print("after waiting")
