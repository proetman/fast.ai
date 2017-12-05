
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
    

# --- deletes   
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     detach internet gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
    
def detach_internet_gateway(p_ig, p_ig_id):
    """
    Detach the Internet Gateway from the VPC
    If it fails with Client Error of not attached, it should be OK
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
            print("Unable to delete internet gateway due to a dependency violation")
            print('error text: {}'.format(e))
        else:
            command_status = False            
            print('Unknown Error when deleting Internet Gateway {}'.format(e.response['Error']['Code']) )
            print('error text: {}'.format(e))
            
    return command_status    


#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     delete security group                                 # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
    
def delete_security_group(p_sg, p_sg_id):
    """
    delete the security group from the VPC

    """
    command_status = False
    
    try:
        l_response = p_sg.delete()
        delete_result = l_response['ResponseMetadata']['HTTPStatusCode']
        if delete_result == 200:
            command_status = True
        else:
            print('ERROR: Failed to delete security for unknown reasons, error not raised')
            print(l_response)
            print('-----------------------------------------------------')
            command_status = False
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'DependencyViolation':
            command_status = False
            # This error is NOT ok.
            print("Unable to delete security group due to a dependency violation")
            print('error text: {}'.format(e))
        else:
            command_status = False            
            print('Unknown Error when deleting Security Group {}'.format(e.response['Error']['Code']) )
            print('error text: {}'.format(e))
            
    return command_status    

#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     delete subnet                                         # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
    
def delete_subnet(p_subnet, p_subnet_id):
    """
    delete the subnet from the VPC

    """
    command_status = False
    
    try:
        l_response = p_subnet.delete()
        delete_result = l_response['ResponseMetadata']['HTTPStatusCode']
        if delete_result == 200:
            command_status = True
        else:
            print('ERROR: Failed to delete subnet for unknown reasons, error not raised')
            print(l_response)
            print('-----------------------------------------------------')
            command_status = False
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'DependencyViolation':
            command_status = False
            # This error is NOT ok.
            print("Unable to delete subnet due to a dependency violation")
            print('error text: {}'.format(e))
        else:
            command_status = False            
            print('Unknown Error when deleting subnet {}'.format(e.response['Error']['Code']) )
            print('error text: {}'.format(e))
            
    return command_status    
     

# --- remove components
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc network acls                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_network_acls(p_ec2_resource, p_vpc_id, p_level):   
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for subnet in p_ec2_resource.meta.client.describe_network_acls()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        

#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc vpn attachments                            # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_vpn_attachments(p_ec2_resource, p_vpc_id, p_level):  
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for subnet in p_ec2_resource.meta.client.describe_vpn_gateways()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
        
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc route tables                                # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 
                


def remove_vpc_route_tables(p_ec2_resource, p_vpc_id, p_level):   
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for subnet in p_ec2_resource.meta.client.describe_route_tables()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
                    
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc network interfaces                         # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_network_interfaces(p_ec2_resource, p_vpc_id, p_level): 
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for subnet in p_ec2_resource.meta.client.describe_network_interfaces()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
    
                
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc peering connections                        # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_peering_connections(p_ec2_resource, p_vpc_id, p_level):  
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for subnet in p_ec2_resource.meta.client.describe_vpc_peering_connections()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
        
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc vpn connections                            # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

                
def remove_vpc_vpn_connection(p_ec2_resource, p_vpc_id, p_level): 
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for vpn in p_ec2_resource.meta.client.describe_vpn_connections()['SecurityGroups']:
        
        l_subnet_id = subnet['GroupId']
        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
        
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc subnet                                     # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_subnets(p_ec2_resource, p_vpc_id, p_level):     
    """
    Remove all subnets for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False

    
    for subnet in p_ec2_resource.meta.client.describe_subnets()['Subnets']:

        l_vpc_owner_id = subnet['VpcId'] 
        l_subnet_id = subnet['SubnetId']
        l_subnet = p_ec2_resource.SecurityGroup(l_subnet_id)

        if l_vpc_owner_id != p_vpc_id.id:
            print('{} subnet VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_subnet_id, l_vpc_owner_id))
            continue

        
        
        print('{} subnet {}, owner VPC {}'.format(' '*p_level, l_subnet_id, l_vpc_owner_id))
        if not delete_subnet(l_subnet, l_subnet_id):
            overall_success = False
        else:
            print('{}     subnet deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        
    
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove vpc security group                             # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_security_group(p_ec2_resource, p_vpc_id, p_level):     
    """
    Remove all security groups for this vpc
    """
    p_level += 4
 
    overall_success = True
    overall_success = False
    
    
    for sg in p_ec2_resource.meta.client.describe_security_groups()['SecurityGroups']:
        
        l_sg_id = sg['GroupId']
        l_vpc_owner_id = sg['VpcId'] 
        l_sg = p_ec2_resource.SecurityGroup(l_sg_id)
        
        if l_vpc_owner_id != p_vpc_id.id:
            print('{} Security Group VPC {}, owner VPC {} - skip, wrong VPC'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
            continue
        
        print('{} Security Group {}, owner VPC {}'.format(' '*p_level, l_sg_id, l_vpc_owner_id))
        if not delete_security_group(l_sg, l_sg_id):
            overall_success = False
        else:
            print('{}     security group deleted'.format(' '*p_level))    
            
    p_level -= 4
    return overall_success        



#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     Remove Internet Gateway                               # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 


def remove_vpc_internet_gateway(p_ec2_resource, p_vpc_id, p_level):     
    """
    Remove all Internet Gateways...
    dunno about the default, is there one?
    Bugger it, just remove em all....
    """
    
    p_level += 4
 
    overall_success = True
    
    for ig in p_ec2_resource.meta.client.describe_internet_gateways()['InternetGateways']:
        
        l_ig_id = ig['InternetGatewayId']
        
        # This gateway can be attached to multiple VPC
        # Loop through each attachment, and see if attached to this VPC at all.
        is_attached_to_vpc = False  
        is_attached_count = 0
        
        for att in ig['Attachments']:
            is_attached_count += 1
            l_vpc_owner_id = att['VpcId']
            if l_vpc_owner_id != p_vpc_id.id:
                is_attached_to_vpc = True
         

        if not is_attached_to_vpc:
            print('{} internet gateway not attached to this VPC - skip'.format(' '*p_level))
            continue
 
        l_ig = p_ec2_resource.InternetGateway(l_ig_id)

        print('{} Process removal internet gateway : {}'.format(' ' * p_level, l_ig_id))

        p_level += 4
        if not detach_internet_gateway(l_ig, l_ig_id):
            print('{} internet gateway failed to detach '.format(' '*p_level))    
            overall_success = False
        else:
            print('{} internet gateway detached'.format(' '*p_level))    
            is_attached_count -= 1
          
        # Test to see if attached to any other VPC, if not, then delete.
        if is_attached_count == 0:             
            if not delete_internet_gateway(l_ig, l_ig_id):
                print('{} internet gateway failed to delete '.format(' '*p_level))    
                overall_success = False
            else:
                print('{} internet gateway deleted'.format(' '*p_level))    
        
        p_level -= 4
        
    p_level -= 4
    return overall_success        
    
# --- remove VPC
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
    level = 0
    print('Start process - Remove all VPC except default')
    for r in p_ec2_resource.meta.client.describe_vpcs()[ 'Vpcs']:

        level += 4
        
        l_vpc_default = r['IsDefault']
        l_vpc_id = r['VpcId']
        
        vpc_ready_for_delete = True
        
        if l_vpc_default:
            print('    vpc id {}: is default, not removing'.format(l_vpc_id))
        else:
            print('    vpc id {}: prepare for delete'.format(l_vpc_id))
            
            l_vpc = p_ec2_resource.Vpc(id = l_vpc_id)

            if l_vpc.tags is not None:
                for tag in l_vpc.tags:
                    print('{} vpc tags: : {} {}'.format(' '*level * 2, tag['Key'], tag['Value']))
            
            if not remove_vpc_security_group(p_ec2_resource, l_vpc, level):
                vpc_ready_for_delete = False
            
            if not remove_vpc_subnets(p_ec2_resource, l_vpc, level):
                vpc_ready_for_delete = False
            
            if not remove_vpc_network_acls(p_ec2_resource, l_vpc, level):
                vpc_ready_for_delete = False
                
# =============================================================================
#             if not remove_vpc_vpn_attachments(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
#                 
#             if not remove_vpc_route_tables(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
#                 
#             if not remove_vpc_network_interfaces(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
#                 
#             if not remove_vpc_vpc_peering_connections(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
#                 
#             if not remove_vpc_vpn_connection(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
#             
#             if not remove_vpc_internet_gateway(p_ec2_resource, l_vpc, level):
#                 vpc_ready_for_delete = False
# =============================================================================

            if vpc_ready_for_delete:
                l_vpc.delete()
            else:
                print('{} VPC not ready for delete...bugger'.format(' '*level))
            
# =============================================================================
#                
# Possible dependencies
# ---------------------
# DONE Security Group
# DONE Internet Gateways
#
# Subnets
# Network ACLs
# VPN Attachments
# Route Tables
# Network Interfaces
# VPC Peering Connections
# vpn-connection. 
#             
# =============================================================================

# =============================================================================
#                dir(p_ec2_resource.meta.client)
#                
#  u'describe_subnets',
#                
#  u'describe_network_acls',
#
#  u'describe_vpn_gateways',            
#
#  u'describe_route_tables',
#
#  u'describe_network_interfaces',
#
#  u'describe_vpc_peering_connections',
#
#  u'describe_vpn_connections',
# ---------------------------------                
#  u'describe_account_attributes',
#  u'describe_addresses',
#  u'describe_availability_zones',
#  u'describe_bundle_tasks',
#  u'describe_classic_link_instances',
#  u'describe_conversion_tasks',
#  u'describe_customer_gateways',
#  u'describe_dhcp_options',
#  u'describe_egress_only_internet_gateways',
#  u'describe_export_tasks',
#  u'describe_flow_logs',
#  u'describe_fpga_images',
#  u'describe_host_reservation_offerings',
#  u'describe_host_reservations',
#  u'describe_hosts',
#  u'describe_iam_instance_profile_associations',
#  u'describe_id_format',
#  u'describe_identity_id_format',
#  u'describe_image_attribute',
#  u'describe_images',
#  u'describe_import_image_tasks',
#  u'describe_import_snapshot_tasks',
#  u'describe_instance_attribute',
#  u'describe_instance_status',
#  u'describe_instances',
#  u'describe_internet_gateways',
#  u'describe_key_pairs',
#  u'describe_moving_addresses',
#  u'describe_nat_gateways',
#  u'describe_network_interface_attribute',
#  u'describe_network_interface_permissions',
#  u'describe_placement_groups',
#  u'describe_prefix_lists',
#  u'describe_regions',
#  u'describe_reserved_instances',
#  u'describe_reserved_instances_listings',
#  u'describe_reserved_instances_modifications',
#  u'describe_reserved_instances_offerings',
#  u'describe_scheduled_instance_availability',
#  u'describe_scheduled_instances',
#  u'describe_security_group_references',
#  u'describe_security_groups',
#  u'describe_snapshot_attribute',
#  u'describe_snapshots',
#  u'describe_spot_datafeed_subscription',
#  u'describe_spot_fleet_instances',
#  u'describe_spot_fleet_request_history',
#  u'describe_spot_fleet_requests',
#  u'describe_spot_instance_requests',
#  u'describe_spot_price_history',
#  u'describe_stale_security_groups',
#  u'describe_tags',
#  u'describe_volume_attribute',
#  u'describe_volume_status',
#  u'describe_volumes',
#  u'describe_volumes_modifications',
#  u'describe_vpc_attribute',
#  u'describe_vpc_classic_link',
#  u'describe_vpc_classic_link_dns_support',
#  u'describe_vpc_endpoint_services',
#  u'describe_vpc_endpoints',
#  u'describe_vpcs',
#             
# =============================================================================
# --- main      
#  ------------------------------------------------------------------------ # 
#                                                                           # 
#                     main                                                  # 
#                                                                           # 
#  ------------------------------------------------------------------------ # 

def main():
    
    l_session = boto3.Session(profile_name = g_profile)
    l_region = l_session.region_name
    
    print('Configuration')
    print('-------------')
    print('    Current region: {}'.format(l_region))
    print('\n')
    
    ec2_resource = l_session.resource('ec2')   
    ec2_client   = l_session.client('ec2')     # lowest level
    
    remove_all_vpc(ec2_resource)
    
    # my_vpc_id = create_vpc(ec2_resource, ec2_client)
    # print('My VPC ID: {}, type = {}'.format(my_vpc_id.id, type(my_vpc_id.id)))
    
    
    # my_gateway_id = create_gateway(ec2_resource, my_vpc_id.id)
    # print('My Internet Gateway ID: {}'.format(my_gateway_id))
    
     
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
            