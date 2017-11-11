#!/bin/bash
aws ec2 disassociate-address --association-id eipassoc-d1b595eb
aws ec2 release-address --allocation-id eipalloc-1f82e825
aws ec2 terminate-instances --instance-ids i-08b13203ed6d7a15e
aws ec2 wait instance-terminated --instance-ids i-08b13203ed6d7a15e
aws ec2 delete-security-group --group-id sg-d27c18b4
aws ec2 disassociate-route-table --association-id rtbassoc-dcd606ba
aws ec2 delete-route-table --route-table-id rtb-1653e671
aws ec2 detach-internet-gateway --internet-gateway-id igw-555cfe31 --vpc-id vpc-aa6768ce
aws ec2 delete-internet-gateway --internet-gateway-id igw-555cfe31
aws ec2 delete-subnet --subnet-id subnet-6572473c
aws ec2 delete-vpc --vpc-id vpc-aa6768ce
echo If you want to delete the key-pair, please do it manually.
