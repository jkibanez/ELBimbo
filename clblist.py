import boto3
import pprint
import sys
import json
from datetime import datetime, timezone
import csv

def getinstancename(instanceid):
    instances=ec2.describe_instances(Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceid
            ]
        },
    ],)
    resultset = {}    
    for instance in instances["Reservations"]:
        for inst in instance["Instances"]:
            resultset["State"]=inst["State"]["Name"]    
            for tag in inst["Tags"]:
                if tag['Key'] == 'Name':
                    resultset["Name"]=tag['Value']
    # print (resultset)  
    return resultset
             
def getinstancehealth(lbname,instanceid):
    instancestate=elb.describe_instance_health(
            LoadBalancerName=lbname,
            Instances = [{
                'InstanceId' : instanceid
            }]
            )
    
    return instancestate['InstanceStates'][0]['State']
    
def describelbs():
    
    lbs = elb.describe_load_balancers(PageSize=400)

    lb_tg_data = []

    for lb in lbs["LoadBalancerDescriptions"]:
        lbjson={}
        lbjson['Name']=lb["LoadBalancerName"]
        lbjson['HealthCheck']=lb["HealthCheck"]
        lbjson['Instances']=[]

        if len(lb["Instances"]) > 0:
            InstanceList=[]
            for instance in lb["Instances"]:
                instance.update(getinstancename(instance["InstanceId"]))
                instance['Health']=getinstancehealth(lb["LoadBalancerName"], instance["InstanceId"])
                InstanceList.append(instance)
            
            lbjson['Instances']=InstanceList
        # print("\n",json.dumps(lbjson, indent=4, sort_keys=True))

        lb_tg_data.append(lbjson)
    return(lb_tg_data)    
    
if __name__ == "__main__":
    #if len(sys.argv) < 3:
        #print(" – Region Name and the Profile name is mandatory – ")
        #print(" Syntax: python3 clb-list-json.py us-east-1 default")
        #exit()
    #region_name = sys.argv[1]
    aws_environment = sys.argv[1]
    #print("profilename selected:",profile)
    #print("regionname selected: ",region_name)
    region_names = [
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "ap-south-1",
        "ap-northeast-3",
        "ap-northeast-2",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ca-central-1",
        "eu-central-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "eu-north-1",
        "sa-east-1"
    ]
    #print(region)
    #region_name = sys.argv[2]



    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Using str.replace() to remove spaces
    aws_environment = aws_environment.replace(" ", "")
    
    # Define the CSV file name
    csv_file_name = f"{aws_environment}-CLB_{formatted_date}.csv"
    
    # Define the header names based on the data we are collecting
    # headers = ['ELBName', 'Email', 'ConsoleAccess', 'IsServiceAccount', 'MFA', 'AccessKeys', 'LastLogin', 'LoggedInAfterDisablementDate', 'ForImmediateDeletion']
    headers = ['AWS Environment', 'Region', 'CLB Name', 'Target Server', 'Instance ID']
    
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header
        writer.writeheader()
        for region in region_names:
            #print(region)
            # session = boto3.session.Session(profile_name='default', region_name=region)
            session = boto3.session.Session(region_name=region)
            elb = session.client('elb')
            ec2 = session.client('ec2')
            elbdata = describelbs()

            print(elbdata)

            for elb in elbdata:
                region_data = region
                # print(region_data)
                elb_name = elb['Name']
                print(elb_name)
                print(elb['Name'])
                for tg in elb['Instances']:
                    print(tg['Name'])
                    ec2_data = tg['Name']
                    instanceid_data = tg['InstanceId']
                    print(tg['InstanceId'])
                    #tg_data = tg['Name']
                    #print(tg['Name'])
                    #print(tg['Instances'])
                    #for ec2 in tg['Instances']:
                        #ec2_data = ec2['Name']
                        #instanceid_data = ec2['Target']['Id']
                        #print(ec2['Name'])
                        #print(ec2['Target']['Id'])
                #Write the user's details to the CSV
                writer.writerow({
                    'AWS Environment': aws_environment,
                    'Region': region_data,
                    'CLB Name': elb_name,
                    # 'Target Group': tg_data,
                    'Target Server': ec2_data,
                    'Instance ID': instanceid_data
                })