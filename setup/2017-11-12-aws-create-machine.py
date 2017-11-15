
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

# In[16]:


g_profile = 'us-east'
g_instance_type = 'm4.large'
ami = 'ami-31ecfb26'             # only in us-east-1, virginia


# In[17]:


# Fixed constansts
g_name = 'fast-ai'
g_cidr = '0.0.0/0'


# In[18]:


# Import libraries
import boto3


# ## Functions

# In[13]:


def create_vpc(p_ec2_client):
    """
    export vpcId=$(aws ec2 create-vpc --cidr-block 10.0.0.0/28 --query 'Vpc.VpcId' --output text)
    aws ec2 create-tags --resources $vpcId --tags --tags Key=Name,Value=$name
    aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-support "{\"Value\":true}"
    aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-hostnames "{\"Value\":true}"

    """
    # Find out if a VPC already exists for this range


    
    


# ## Main

# In[34]:


session = boto3.Session(profile_name = g_profile)

ec2 = boto3.resource('ec2')
my_region = session.region_name

print('Current region: {}'.format(my_region))

filters = [{'Name':'tag:Name', 'Values':[g_name]}]

print('List of available VPC')
list(ec2.vpcs.filter(Filters=filters))
print('END List of available VPC')


ec2_client = session.client('ec2')

# List all instances for this client
response = ec2_client.describe_instances()
print(response)


    


# In[38]:


get_ipython().run_line_magic('pinfo', 'ec2_client.modify_vpc_attribute')


# In[45]:


my_vpc = ec2_client.create_vpc(CidrBlock = '10.0.0.0/28')

setval = [{'Value':True}]
my_vpc['Vpc']['VpcId']

# list(ec2_boto3.vpcs)


# In[46]:


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

