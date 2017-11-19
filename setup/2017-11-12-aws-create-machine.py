
# coding: utf-8

# # Create AWS machine

# ## Setup

# ### Other options

# Other instance types available
# ```
# while testing the setup, use a free teir!
# export instanceType="t2.micro"  # cannot do spot rates with this
# 
# g_instanceType="m4.large"    # 4 c per hour
# g_instanceType="m4.xlarge"   # 7 c per hour
# g_instanceType="p2.xlarge"   # 23 c per hour
# ```
# 
# Other Regions available
# ```
# g_profile = 'eu'
# g_profile = 'us-east'
# g_profile = 'au'
# 
# 
# default region (leave null)
# ap-southeast-2   # Sydney
# ```
# 
# AMI
# ```
# ami = 'ami-bc508adc'   # Oregon   "us-west-2" 
# ami = 'ami-b43d1ec7'   # Ireland  "eu-west-1"
# ami = 'ami-31ecfb26'   # Virginia "us-east-1" 
# ```
# 

# ### Constants and Env variables

# In[3]:


g_profile = 'us-east'            # profiles: au | us-east | eu
g_instance_type = 'm4.large'
ami = 'ami-31ecfb26'             # only in us-east-1, virginia


# In[4]:


# Fixed constansts
g_name = 'fast-ai'
g_cidr = '0.0.0/0'


# In[5]:


# Import libraries
import boto3


# ## Functions

# In[42]:


def create_vpc(p_ec2_resource):
    """
    export vpcId=$(aws ec2 create-vpc --cidr-block 10.0.0.0/28 --query 'Vpc.VpcId' --output text)
    aws ec2 create-tags --resources $vpcId --tags --tags Key=Name,Value=$name
    aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-support "{\"Value\":true}"
    aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-hostnames "{\"Value\":true}"

    """
    # Find out if a VPC already exists for this range

    
    filters = [{"Name": "tag:Name", "Values": [g_name]}]
    filters = [{"Name": "tag:Name", "Values": '*'}]
    l_vpc = list(p_ec2_resource.vpcs.filter(Filters=filters))
    
    if len(l_vpc) == 0:
        print('There are no VPC for tag: {}, so will create one!'.format(g_name))
        l_vpc_id = p_ec2_resource.create_vpc(CidrBlock='10.0.0.0/28')
        l_vpc_id.create_tags(Tags=[{"Key": "Name", "Value": g_name}])
        print('Creating...please wait')
        l_vpc_id.wait_until_available()
        print('Complete')
        print(l_vpc_id)
    else:
        print('There is a VPC for tag: {} already. Doing nothing.')
        


    
    


# ## Main

# In[69]:


l_session = boto3.Session(profile_name = g_profile)
l_region = l_session.region_name

print('Current region: {}'.format(l_region))

ec2_resource = l_session.resource('ec2')   
ec2_client   = l_session.client('ec2')     # lowest level

vpc_to_delete = 'vpc-7577f10d'

# l_vpc = ec2_resource.Vpc(id = vpc_to_delete)
# print(l_vpc)
# l_vpc.delete()

filters = [{'Name': "tag:Name", 'Values':['fast*']}]
l_vpc = list(ec2_resource.vpcs.filter(Filters=filters))
print('len l_vpc = {}'.format(len(l_vpc)))
for vpc in l_vpc:
    response = client.describe_vpcs(VpcIds=[vpc.id,])
    print(json.dumps(response, sort_keys=True, indent=4))
# print(l_vpc)

# vpc_id = ec2_resource.Vpc(vpc)
# vpc_id.id
# print('vpc id = {}'.format(vpc_id))
# print(dir(ec2_resource))
# ec2_resource.Vpc.



# ec2_resource.create_vpc
# ec2_client.create_vpc

# reate_vpc(ec2_resource)

# List all instances for this client
# response = ec2_client.describe_instances()
# print(response)


    


# In[13]:


get_ipython().run_line_magic('pinfo', 'ec2_client.modify_vpc_attribute')


# In[14]:


my_vpc = ec2_client.create_vpc(CidrBlock = '10.0.0.0/28')

setval = [{'Value':True}]
my_vpc['Vpc']['VpcId']

# list(ec2_boto3.vpcs)


# In[16]:


ec2_client.modify_vpc_attribute(VpcId=my_vpc['Vpc']['VpcId'], EnableDnsSupport={'Value':True})


# In[51]:


ec2_client.modify_vpc_attribute(VpcId=my_vpc['Vpc']['VpcId'], EnableDnsHostnames={'Value':True})


# ### Verify VPC parameters are correct

# ### How to delete a VPC (incomplete)

# In[66]:


vpc_iterator = ec2.vpcs.all()
for x in vpc_iterator:
    print(x)
    try:
        x.delete()
    except:
        print('    Probably has dependencies, skipping needs more coding here!')

# https://gist.github.com/neilswinton/d37787a8d84387c591ff365594bd26ed

# Call EC2.Client.describe_vpc_endpoints. Filter on your VPC id.Call EC2.client.delete_vpc_endpoints on each

# Call VPC.security_groups. Delete the group unless its group_name attribute is "main". The main security group will be deleted via VPC.delete().

# Call EC2.Client.describe_vpc_peering_connections. Filter on your VPC id as the requester-vpc-info.vpc-id. (My VPC is a requester. There is also accepter-vpc-info.vpc-id among other filters.) Iterate through the entries keyed by VpcPeeringConnections. Get an instance of the peering connection by instantiating a EC2.ServiceResource.VpcPeeringConnection with the VpcPeeringConnectionId. Call VpcPeeringConnection.delete() to remove the peering connection.

# Call vpc.route_tables.all() and iterate through the route tables. For each route table, iterate through its routes using the RouteTable.routes attribute. Delete the routes where route['Origin'] is 'CreateRoute'. I deleted using EC2.Client.delete_route using EC2.RouteTable.id and route['DestinationCidrBlock']. After removing the routes, call EC2.RouteTable.delete() to remove the route table itself. I set up exception handlers for each delete. Not every route table can be deleted, but I haven't cracked the code code. Maybe next week.

# Iterate through vpc.network_acls.all(), test the NetworkAcl.is_default attribute and call NetworkAcl.delete for non-default acls.

# Iterate through vpc.subnets.all().network_interfaces.all(). Call EC2.NetworkInterface.delete() on each.

# Iterate through vpc.internet_gateways.all(). Call EC2.InternetGateway.delete() on each.

# Call vpc.delete()
        


# In[62]:


get_ipython().run_line_magic('pinfo', 'ec2.vpcs.all')

