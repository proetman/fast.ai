
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     libraries                                             # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

import sys
import boto3
from botocore.exceptions import ClientError


#  ------------------------------------------------------------------------ #
#                                                                           # 
#                     constants                                             # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

g_profile = 'us-east'            # profiles: au | us-east | eu
g_instance_type = 'm4.large'
ami = 'ami-31ecfb26'             # only in us-east-1, virginia


# Fixed constansts
g_name = 'fast-ai'
g_cidr = '0.0.0/0'
g_cidr_block = '10.0.0.0/28'

# --- Create

#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Create VPC                                            # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


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
    # ec2_client.modify_vpc_attribute(VpcId=l_vpc_id.id, EnableDnsSupport={'Value': True})
    # ec2_client.modify_vpc_attribute(VpcId=l_vpc_id.id, EnableDnsHostnames={'Value': True})
    
    print('Creating...please wait')
    l_vpc_id.wait_until_available()
    print('Complete')
    print(l_vpc_id)
    
    return l_vpc_id
        
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Create Internet Gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

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
    
    
# -- remove
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove VPC                                            # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_all_vpc(p_ec2_resource):
    """
    Remove all VPC
    except for default
    
    This will start failing where there are dependencies....will have to fix that later!
    """

    for r in p_ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:

        l_vpc_default = r['IsDefault']
        l_vpc_id = r['VpcId']
        
        if l_vpc_default:
            print('Default vpd id {}, not removing'.format(l_vpc_id))
        else:
            print('\nprep for delete of {}'.format(l_vpc_id))
            l_vpc = p_ec2_resource.Vpc(id = l_vpc_id)

            if l_vpc.tags is not None:
                for tag in l_vpc.tags:
                    print('Display TAG: {} {}'.format(tag['Key'], tag['Value']))
                    
            if remove_vpc_internet_gateway(p_ec2_resource, l_vpc):
                l_vpc.delete()
            else:
                print('Failed to remove VPC Internet Gateways, not removing VPC')
            
   
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     detach internet gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
    
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

#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     delete internet gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
    
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
            command_status = False
            # This error is NOT ok.
            # print("Client Error({0}): {1}".format(e.errno,strerror))
        else:
            command_status = False            
            print('Unknown Error when deleting Internet Gateway {}'.format(
                    e.response['Error']['Code'])    )
            print('error text: {}'.format(e))
            
    return command_status    
            
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove Internet Gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_internet_gateway(p_ec2_resource, p_vpc_id):     
    """
    Remove all Internet Gateways...
    dunno about the default, is there one?
    Bugger it, just remove em all....
    """
 
    for ig in p_ec2_resource.meta.client.describe_internet_gateways()['InternetGateways']:
        l_ig_id = ig['InternetGatewayId']
        l_ig = p_ec2_resource.InternetGateway(l_ig_id)

        print('Internet gateway = {}'.format(l_ig_id))

        if not detach_internet_gateway(l_ig, l_ig_id):
            return False
          
        if not delete_internet_gateway(l_ig, l_ig_id):
            return False
        

      
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     main                                                  # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

def main():
    
    l_session = boto3.Session(profile_name = g_profile)
    l_region = l_session.region_name
    
    print('Current region: {}'.format(l_region))
    
    ec2_resource = l_session.resource('ec2')   
    ec2_client   = l_session.client('ec2')     # lowest level
    
    remove_all_vpc(ec2_resource)
    
    # my_vpc_id = create_vpc(ec2_resource, ec2_client)
    # print('My VPC ID: {}, type = {}'.format(my_vpc_id.id, type(my_vpc_id.id)))
    
    
    # my_gateway_id = create_gateway(ec2_resource, my_vpc_id.id)
    # print('My Internet Gateway ID: {}'.format(my_gateway_id))
    
    print('start')
    for r in ec2_resource.meta.client.describe_internet_gateways()['InternetGateways']:
        print('\nInternet Gateway: {}'.format(r))
        l_attachment = r['Attachments']
        l_tags = r['Tags']
        l_internet_gateway_id = r['InternetGatewayId']
        print('{}'.format(l_internet_gateway_id))
    print('end')
    
 #    for r in ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:
 #        l_vpc_id = r['VpcId']
 #        for s in r.meta.client.describe_internet_gateways()['InternetGateways']:
 #            print(s)    


#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     begin                                                 # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
            
if __name__ == "__main__":
    main()            
            