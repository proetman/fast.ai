#!/bin/bash
#
# Configure a p2.xlarge instance

# get the correct ami
export region=$(aws configure get region --profile us-east)
if [ $region = "us-east-1" ]; then
  export ami="ami-31ecfb26" # Virginia
else
  echo "Only us-west-2 (Oregon), eu-west-1 (Ireland), and us-east-1 (Virginia) are currently supported"
  exit 1
fi

# while testing the setup, use a free teir!
# export instanceType="t2.micro"  # cannot do spot rates with this
export instanceType="m4.large"    # 4 c per hour
export instanceType="m4.xlarge"   # 7 c per hour
export instanceType="p2.xlarge"   # 23 c per hour

export instanceType="m4.large"    # 4 c per hour

. $(dirname "$0")/setup_instance_spot.sh
