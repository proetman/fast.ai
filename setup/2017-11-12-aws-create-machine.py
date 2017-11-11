
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

# In[4]:


g_profile = 'us-east'
g_instance_type = 'm4.large'
ami = 'ami-31ecfb26'             # only in us-east-1, virginia


# In[14]:


# Fixed constansts
g_name = 'fast-ai'
g_cidr = '0.0.0/0'


# In[15]:


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
'Vpc.VpcId'

    
    


# ## Main

# In[ ]:


session = boto3.Session(profile_name = g_profile)

ec2_client = session.client('ec2')
response = ec2.describe_instances()
print(response)

l_vpc_id = create_vpc(ec2_client )
    

