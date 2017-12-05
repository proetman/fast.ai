
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

# In[93]:


g_profile = 'us-east'            # profiles: au | us-east | eu
g_instance_type = 'm4.large'
ami = 'ami-31ecfb26'             # only in us-east-1, virginia


# In[94]:


# Fixed constansts
g_name = 'fast-ai'
g_cidr = '0.0.0/0'
g_cidr_block = '10.0.0.0/28'


# In[188]:


# Import libraries
import sys
import boto3
from botocore.exceptions import ClientError


# ## Main

# ###  Create Functions

# In[114]:


# Functions

# Doc: https://gist.github.com/iMilnb/0ff71b44026cfd7894f8

# ---------------------------------------------------------------------------------
# 
#                      Create VPC
# 
# ---------------------------------------------------------------------------------

def create_vpc(p_ec2_resource, p_ec2_client):
    """
    Create a Virtual Private Channel (VPC)
    Add a tag, even though I cannot see the tag later.... <sigh>
    Enable DNS
    Enable Hostname support
    Return the ID.
    """
    
    l_vpc_id = p_ec2_resource.create_vpc(CidrBlock=g_cidr_block)
    l_vpc_id.create_tags(Tags=[{"Key": "VPCName", "Value": g_name}])
    print('----------')
    print(l_vpc_id.id)
    # int(l_vpc_id['id'])
    print('----------')
    ec2_client.modify_vpc_attribute(VpcId=l_vpc_id.id, EnableDnsSupport={'Value': True})
    ec2_client.modify_vpc_attribute(VpcId=l_vpc_id.id, EnableDnsHostnames={'Value': True})
    
    print('Creating...please wait')
    l_vpc_id.wait_until_available()
    print('Complete')
    print(l_vpc_id)
    
    return l_vpc_id
        

# ---------------------------------------------------------------------------------
# 
#                      Create Internet Gateway
# 
# ---------------------------------------------------------------------------------

def create_gateway(p_ec2_resource, p_vpc_id):
    """
    Create an Internet Gateway
    Add a tag, still do not understand tags <bigger sigh>
    return ID
    """
    
    l_ig = p_ec2_resource.create_internet_gateway()
    print('my ig = {}'.format(l_ig))
    l_ig.attach_to_vpc(VpcId=p_vpc_id)
    return l_ig
    
# ec2_client.modify_vpc_attribute(VpcId=my_vpc['Vpc']['VpcId'], EnableDnsSupport={'Value':True})
# ec2_client.modify_vpc_attribute(VpcId=my_vpc['Vpc']['VpcId'], EnableDnsHostnames={'Value':True})    

# Create an Internet Gateway
# export internetGatewayId=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' 
#                              --output text)
# aws ec2 create-tags --resources $internetGatewayId --tags --tags Key=Name,Value=$name-gateway
# aws ec2 attach-internet-gateway --internet-gateway-id $internetGatewayId --vpc-id $vpcId
    
    


# In[132]:


l_session = boto3.Session(profile_name = g_profile)
l_region = l_session.region_name

print('Current region: {}'.format(l_region))

ec2_resource = l_session.resource('ec2')   
ec2_client   = l_session.client('ec2')     # lowest level


# my_vpc_id = create_vpc(ec2_resource, ec2_client)
# print('My VPC ID: {}, type = {}'.format(my_vpc_id.id, type(my_vpc_id.id)))


# my_gateway_id = create_gateway(ec2_resource, my_vpc_id.id)
# print('My Internet Gateway ID: {}'.format(my_gateway_id))

print('start')
for r in ec2_resource.meta.client.describe_internet_gateways()['InternetGateways']:
    print(r)
    l_attachment = r['Attachments']
    l_tags = r['Tags']
    l_internet_gateway_id = r['InternetGatewayId']
    print('{}'.format(l_internet_gateway_id))
print('end')

for r in ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:
    l_vpc_id = r['VpcId']
    for s in r.meta.client.describe_internet_gateways()['InternetGateways']:
        print(s)

        # l_vpc_id


# myfilters = [{'Name': 'tag:Name', 'Values':['fast-ai']}]
# myfilters = [{'Name': 'VpcId', 'Values':['*']}]
# print(myfilters)
# l_vpc = list(ec2_resource.vpcs.filter(Filters=myfilters))
# print('len l_vpc = {}'.format(len(l_vpc)))
# for vpc in l_vpc:
#     response = client.describe_vpcs(VpcIds=[vpc.id,])
#     print(json.dumps(response, sort_keys=True, indent=4))
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


    


# ## Cleanup

# ### functions

# In[215]:


# Functions

# Doc: https://gist.github.com/iMilnb/0ff71b44026cfd7894f8

# ---------------------------------------------------------------------------------
# 
#                      Remove VPC
# 
# ---------------------------------------------------------------------------------


def remove_all_vpc(p_ec2_resource):
    """
    Remove all VPC
    except for default
    
    This will start failing where there are dependencies....will have to fix that later!
    """

    for r in p_ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:
        l_vpc_default = r['IsDefault']
        l_vpc_id = r['VpcId']
        if curr_default:
            print('Default vpd id {}, not removing'.format(l_vpc_id))
        else:
            print('\nprep for delete of {}'.format(curr_id))
            l_vpc = ec2_resource.Vpc(id = l_vpc_id)

            if l_vpc.tags is not None:
                for tag in l_vpc.tags:
                    print('Display TAG: {} {}'.format(tag['Key'], tag['Value']))
                    
            if remove_vpc_internet_gateway(p_ec2_resource, l_vpc):
                l_vpc.delete()
            else:
                print('Failed to remove VPC Internet Gateways, not removing VPC')
            
# ---------------------------------------------------------------------------------
# 
#                      Remove Internet Gateway
# 
# ---------------------------------------------------------------------------------


def remove_vpc_internet_gateway(p_ec2_resource, p_vpc_id):     
    """
    Remove all Internet Gateways...
    dunno about the default, is there one?
    Bugger it, just remove em all....
    """
    
    def detach_internet_gateway(p_ig, p_ig_id):
        """
        Detach the Internet Gateway from the VPC
        If it fails with Client Error, it should be OK
            verify error is 
               'ClientError: An error occurred (Gateway.NotAttached) when calling the 
               DetachInternetGateway operation: resource igw-8f4bc9f6 is not 
               attached to network igw-8f4bc9f6'
        """
        command_status = False
        
        try:
            l_response = p_ig.detach_from_vpc(VpcId = p_ig_id)
            
            print(l_response)
            command_status = True
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'Gateway.NotAttached':
                # This error is ok.
                command_status = True

        
        return command_status
    
    def delete_internet_gateway(p_ig, p_ig_id):
        """
        delete the Internet Gateway from the VPC
        If it fails with Client Error, NOT OK
            verify error is 
               'ClientError: An error occurred (DependencyViolation) when calling 
               the DeleteInternetGateway operation: The internetGateway 'igw-8f4bc9f6' 
               has dependencies and cannot be deleted.

        """
        command_status = False
        
        try:
            l_response = p_ig.delete()
            print(l_response)
            command_status = True
        except ClientError as e:
            if e.response['Error']['Code'] == 'DependencyViolation':
                # This error is NOT ok.
                print('------------------------------')
                print(e)
                print(e.response['Error']['Code'])
                print('------------------------------')
                # print("Client Error({0}): {1}".format(e.errno,strerror))
            else:
                print('------------------------------')
                print('------------------------------')
                print('------------------------------')
                print(e)
                print('------------------------------')
                print('------------------------------')
                print('------------------------------')
        
        return command_status    
    
    for ig in p_ec2_resource.meta.client.describe_internet_gateways()['InternetGateways']:
        l_ig_id = ig['InternetGatewayId']
        l_ig = p_ec2_resource.InternetGateway(l_ig_id)

        print('Internet gateway = {}'.format(l_ig_id))

        if not detach_internet_gateway(l_ig, l_ig_id):
            return False
          
        if not delete_internet_gateway(l_ig, l_ig_id):
            return False
        
        # l_response = l_ig.delete()
        # print(l_response)
        # print(l_response['ResponseMetadata'])
        
        
    

# for r in ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:
#     l_vpc_id = r['VpcId']
#     for s in r.meta.client.describe_internet_gateways()['InternetGateways']:
#         print(s)    


# In[216]:


# Execute cleanup Routines

# last cleanup, VPC
remove_all_vpc(ec2_resource)

# finished cleanup! Yay.


# ### Verify VPC parameters are correct

# ### How to delete a VPC (incomplete)

# vpc_iterator = ec2.vpcs.all()
# for x in vpc_iterator:
#     print(x)
#     try:
#         x.delete()
#     except:
#         print('    Probably has dependencies, skipping needs more coding here!')
# 
# ```
# # https://gist.github.com/neilswinton/d37787a8d84387c591ff365594bd26ed
# 
# # Call EC2.Client.describe_vpc_endpoints. Filter on your VPC id.Call EC2.client.delete_vpc_endpoints on each
# 
# # Call VPC.security_groups. Delete the group unless its group_name attribute is "main". The main security group will be deleted via VPC.delete().
# 
# # Call EC2.Client.describe_vpc_peering_connections. Filter on your VPC id as the requester-vpc-info.vpc-id. (My VPC is a requester. There is also accepter-vpc-info.vpc-id among other filters.) Iterate through the entries keyed by VpcPeeringConnections. Get an instance of the peering connection by instantiating a EC2.ServiceResource.VpcPeeringConnection with the VpcPeeringConnectionId. Call VpcPeeringConnection.delete() to remove the peering connection.
# 
# # Call vpc.route_tables.all() and iterate through the route tables. For each route table, iterate through its routes using the RouteTable.routes attribute. Delete the routes where route['Origin'] is 'CreateRoute'. I deleted using EC2.Client.delete_route using EC2.RouteTable.id and route['DestinationCidrBlock']. After removing the routes, call EC2.RouteTable.delete() to remove the route table itself. I set up exception handlers for each delete. Not every route table can be deleted, but I haven't cracked the code code. Maybe next week.
# 
# # Iterate through vpc.network_acls.all(), test the NetworkAcl.is_default attribute and call NetworkAcl.delete for non-default acls.
# 
# # Iterate through vpc.subnets.all().network_interfaces.all(). Call EC2.NetworkInterface.delete() on each.
# 
# # Iterate through vpc.internet_gateways.all(). Call EC2.InternetGateway.delete() on each.
# 
# # Call vpc.delete()
# ```        

# Stuff left to do:
# 
# ```
# 
# ### # Create a Virtual Private Cloud
# ### export vpcId=$(aws ec2 create-vpc --cidr-block 10.0.0.0/28 --query 'Vpc.VpcId' --output text)
# ### aws ec2 create-tags --resources $vpcId --tags --tags Key=Name,Value=$name
# ### aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-support "{\"Value\":true}"
# ### aws ec2 modify-vpc-attribute --vpc-id $vpcId --enable-dns-hostnames "{\"Value\":true}"
# 
# 
# 
# 
# ### # Create an Internet Gateway
# ### export internetGatewayId=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
# ### aws ec2 create-tags --resources $internetGatewayId --tags --tags Key=Name,Value=$name-gateway
# ### aws ec2 attach-internet-gateway --internet-gateway-id $internetGatewayId --vpc-id $vpcId
# 
# export subnetId=$(aws ec2 create-subnet --vpc-id $vpcId --cidr-block 10.0.0.0/28 --query 'Subnet.SubnetId' --output text)
# aws ec2 create-tags --resources $subnetId --tags --tags Key=Name,Value=$name-subnet
# 
# export routeTableId=$(aws ec2 create-route-table --vpc-id $vpcId --query 'RouteTable.RouteTableId' --output text)
# aws ec2 create-tags --resources $routeTableId --tags --tags Key=Name,Value=$name-route-table
# export routeTableAssoc=$(aws ec2 associate-route-table --route-table-id $routeTableId --subnet-id $subnetId --output text)
# aws ec2 create-route --route-table-id $routeTableId --destination-cidr-block 0.0.0.0/0 --gateway-id $internetGatewayId
# 
# # Setup Security Groups
# export securityGroupId=$(aws ec2 create-security-group --group-name $name-security-group --description "SG for fast.ai machine" --vpc-id $vpcId --query 'GroupId' --output text)
# # ssh
# aws ec2 authorize-security-group-ingress --group-id $securityGroupId --protocol tcp --port 22 --cidr $cidr
# # jupyter notebook
# aws ec2 authorize-security-group-ingress --group-id $securityGroupId --protocol tcp --port 8888-8898 --cidr $cidr
# 
# if [ ! -d ~/.ssh ]
# then
#         mkdir ~/.ssh
# fi
# 
# if [ ! -f ~/.ssh/aws-key-$name.pem ]
# then
#         aws ec2 create-key-pair --key-name aws-key-$name --query 'KeyMaterial' --output text > ~/.ssh/aws-key-$name.pem
#         chmod 400 ~/.ssh/aws-key-$name.pem
# fi
# # ----------------------------------------------------------------------- #
# #                                                                         #
# #                     Create Instance                                     #
# #                                                                         #
# # ----------------------------------------------------------------------- #
# 
# command="aws ec2 \
#     run-instances \
#     --image-id $ami \
#     --count 1 \
#     --instance-type $instanceType \
#     --key-name aws-key-$name \
#     --security-group-ids $securityGroupId \
#     --subnet-id $subnetId \
#     --associate-public-ip-address \
#     --block-device-mapping "[ { \"DeviceName\": \"/dev/sda1\", \"Ebs\": { \"VolumeSize\": 128, \"VolumeType\": \"gp2\" } } ]" \
#     --query 'Instances[0].InstanceId' \
#     --output text)
# "
# 
# export instanceId=$(aws ec2 run-instances --image-id $ami --count 1 --instance-type $instanceType --key-name aws-key-$name --security-group-ids $securityGroupId --subnet-id $subnetId --associate-public-ip-address --block-device-mapping "[ { \"DeviceName\": \"/dev/sda1\", \"Ebs\": { \"VolumeSize\": 128, \"VolumeType\": \"gp2\" } } ]" --query 'Instances[0].InstanceId' --output text)
# aws ec2 create-tags --resources $instanceId --tags --tags Key=Name,Value=$name-gpu-machine
# export allocAddr=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
# 
# echo Waiting for instance start...
# aws ec2 wait instance-running --instance-ids $instanceId
# sleep 10 # wait for ssh service to start running too
# export assocId=$(aws ec2 associate-address --instance-id $instanceId --allocation-id $allocAddr --query 'AssociationId' --output text)
# export instanceUrl=$(aws ec2 describe-instances --instance-ids $instanceId --query 'Reservations[0].Instances[0].PublicDnsName' --output text)
# #export ebsVolume=$(aws ec2 describe-instance-attribute --instance-id $instanceId --attribute  blockDeviceMapping  --query BlockDeviceMappings[0].Ebs.VolumeId --output text)
# 
# # reboot instance, because I was getting "Failed to initialize NVML: Driver/library version mismatch"
# # error when running the nvidia-smi command
# # see also http://forums.fast.ai/t/no-cuda-capable-device-is-detected/168/13
# aws ec2 reboot-instances --instance-ids $instanceId
# 
# 
# 
# # save commands to file
# echo \# Connect to your instance: > $name-commands.txt # overwrite existing file
# echo ssh -i ~/.ssh/aws-key-$name.pem ubuntu@$instanceUrl >> $name-commands.txt
# echo \# Stop your instance: : >> $name-commands.txt
# echo aws ec2 stop-instances --instance-ids $instanceId  >> $name-commands.txt
# echo \# Start your instance: >> $name-commands.txt
# echo aws ec2 start-instances --instance-ids $instanceId  >> $name-commands.txt
# echo \# Reboot your instance: >> $name-commands.txt
# echo aws ec2 reboot-instances --instance-ids $instanceId  >> $name-commands.txt
# echo ""
# # export vars to be sure
# echo export instanceId=$instanceId >> $name-commands.txt
# echo export subnetId=$subnetId >> $name-commands.txt
# echo export securityGroupId=$securityGroupId >> $name-commands.txt
# echo export instanceUrl=$instanceUrl >> $name-commands.txt
# echo export routeTableId=$routeTableId >> $name-commands.txt
# echo export name=$name >> $name-commands.txt
# echo export vpcId=$vpcId >> $name-commands.txt
# echo export internetGatewayId=$internetGatewayId >> $name-commands.txt
# echo export subnetId=$subnetId >> $name-commands.txt
# echo export allocAddr=$allocAddr >> $name-commands.txt
# echo export assocId=$assocId >> $name-commands.txt
# echo export routeTableAssoc=$routeTableAssoc >> $name-commands.txt
# 
# # save delete commands for cleanup
# echo "#!/bin/bash" > $name-remove.sh # overwrite existing file
# echo aws ec2 disassociate-address --association-id $assocId >> $name-remove.sh
# echo aws ec2 release-address --allocation-id $allocAddr >> $name-remove.sh
# 
# # save delete commands for cleanup
# echo "#!/bin/bash" > $name-remove.sh # overwrite existing file
# echo aws ec2 disassociate-address --association-id $assocId >> $name-remove.sh
# echo aws ec2 release-address --allocation-id $allocAddr >> $name-remove.sh
# 
# # volume gets deleted with the instance automatically
# echo aws ec2 terminate-instances --instance-ids $instanceId >> $name-remove.sh
# echo aws ec2 wait instance-terminated --instance-ids $instanceId >> $name-remove.sh
# echo aws ec2 delete-security-group --group-id $securityGroupId >> $name-remove.sh
# 
# echo aws ec2 disassociate-route-table --association-id $routeTableAssoc >> $name-remove.sh
# echo aws ec2 delete-route-table --route-table-id $routeTableId >> $name-remove.sh
# 
# echo aws ec2 detach-internet-gateway --internet-gateway-id $internetGatewayId --vpc-id $vpcId >> $name-remove.sh
# echo aws ec2 delete-internet-gateway --internet-gateway-id $internetGatewayId >> $name-remove.sh
# echo aws ec2 delete-subnet --subnet-id $subnetId >> $name-remove.sh
# 
# echo aws ec2 delete-vpc --vpc-id $vpcId >> $name-remove.sh
# echo echo If you want to delete the key-pair, please do it manually. >> $name-remove.sh
# 
# chmod +x $name-remove.sh
# 
# echo All done. Find all you need to connect in the $name-commands.txt file and to remove the stack call $name-remove.sh
# echo Connect to your instance: ssh -i ~/.ssh/aws-key-$name.pem ubuntu@$instanceUrl
# 
# 
# ```
# 
