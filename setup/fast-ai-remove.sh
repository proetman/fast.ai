#!/bin/bash
aws ec2 disassociate-address --association-id eipassoc-6be4d751
aws ec2 release-address --allocation-id eipalloc-6d374557
aws ec2 terminate-instances --instance-ids i-013e3f156e65fdea6
aws ec2 wait instance-terminated --instance-ids i-013e3f156e65fdea6
aws ec2 delete-security-group --group-id sg-94f98ff2
aws ec2 disassociate-route-table --association-id rtbassoc-31983957
aws ec2 delete-route-table --route-table-id rtb-a606b8c1
aws ec2 detach-internet-gateway --internet-gateway-id igw-d745edb3 --vpc-id vpc-dc283eb8
aws ec2 delete-internet-gateway --internet-gateway-id igw-d745edb3
aws ec2 delete-subnet --subnet-id subnet-6ba79432
aws ec2 delete-vpc --vpc-id vpc-dc283eb8
echo If you want to delete the key-pair, please do it manually.
