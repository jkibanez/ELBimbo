import boto3
import pprint
import sys
import json
from datetime import datetime, timezone
import csv

def gettargetgroups(arn):
    tgs=elb.describe_target_groups(LoadBalancerArn=arn)
    tgstring=[]
    for tg in tgs["TargetGroups"]:
        tgstring.append(tg["TargetGroupName"])
    return tgstring
 
def gettargetgrouparns(arn):
    tgs=elb.describe_target_groups(LoadBalancerArn=arn)
    tgarns=[]
    for tg in tgs["TargetGroups"]:
        tgarns.append(tg["TargetGroupArn"])
    return tgarns
 
def getinstancename(instanceid):
    instances=ec2.describe_instances(Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceid
            ]
        },
    ],)
    for instance in instances["Reservations"]:
        for inst in instance["Instances"]:
            for tag in inst["Tags"]:
                if tag['Key'] == 'Name':
                    return (tag['Value'])
 
   
def gettargethealth(arn):
    # print("arn",arn)
    inss=elb.describe_target_health(TargetGroupArn=arn)
    instanceids=[]
    result=[]
    for ins in inss["TargetHealthDescriptions"]:
        ins["Name"]=getinstancename(ins['Target']['Id'])
       
        instanceids.append(ins['Target']['Id'])
        result.append(ins)
    return result
 
def describelbs():
    lbs = elb.describe_load_balancers(PageSize=400)
   
    lb_tg_data = []
   
    #for _ in range(3):
    for lb in lbs["LoadBalancers"][:3]:
        lbjson={}
       
        # print (f"{lb["LoadBalancerName"]}")
       
        lbjson['Name']=lb["LoadBalancerName"]
        lbjson['Type']=lb["Type"]
        lbjson['TG']=gettargetgrouparns(lb["LoadBalancerArn"])
        lbjson['TGData']=[]
 
        TGLIST=[]
        if len(lbjson["TG"]) > 0:
            for tgs in lbjson['TG']:
                TGD={}
                TGD['Name']=tgs.split("/")[1]
                tgh=gettargethealth(tgs)
                if len(tgh) > 0:
                    TGD['Instances']=tgh
                else:
                    TGD['Instances']=""
                TGLIST.append(TGD)
               
            lbjson['TGData'] = TGLIST
           
        lb_tg_data.append(lbjson)
       
    return lb_tg_data
        # print("\n",json.dumps(lbjson, indent=4, sort_keys=True))        
 
       
 
if __name__ == "__main__":
    #if len(sys.argv) < 3:
     #   print(" – Region Name and the Profile name is mandatory – ")
     #   print(" Syntax: python3 clb-list-json.py us-east-1 default")
     #   exit()

    aws_environment = sys.argv[1]
    # region_names = [
    #     "us-east-1",
    #     "us-east-2",
    #     "us-west-1",
    #     "us-west-2",
    #     "ap-south-1",
    #     "ap-northeast-3",
    #     "ap-northeast-2",
    #     "ap-southeast-1",
    #     "ap-southeast-2",
    #     "ap-northeast-1",
    #     "ca-central-1",
    #     "eu-central-1",
    #     "eu-west-1",
    #     "eu-west-2",
    #     "eu-west-3",
    #     "eu-north-1",
    #     "sa-east-1"
    # ]
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
    csv_file_name = f"{aws_environment}-ALB_{formatted_date}_.csv"
    
    # Define the header names based on the data we are collecting
    # headers = ['ELBName', 'Email', 'ConsoleAccess', 'IsServiceAccount', 'MFA', 'AccessKeys', 'LastLogin', 'LoggedInAfterDisablementDate', 'ForImmediateDeletion']
    headers = ['AWS Environment', 'Region', 'ALB Name', 'Target Group', 'Target Server', 'Instance ID']
    
    iam = boto3.client("iam")
    iam.attach_user_policy(UserName='sre-cli-user',PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")
    time.sleep(10)

    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()

        for region in region_names:
            print(region)

            # session = boto3.session.Session(profile_name='default', region_name=region)
            session = boto3.session.Session(region_name=region)
            elb = session.client('elbv2')
            ec2 = session.client('ec2')

            elbdata = describelbs()

            for elb in elbdata:
                region_data = region
                # print(region_data)
                elb_name = elb['Name']
                print(elb_name)
                #print(elb['Name'])
                for tg in elb['TGData']:
                    
                    print(tg)
                    tg_data = tg['Name']
                    #print(tg['Name'])
                    #print(tg['Instances'])
                    for ec2 in tg['Instances']:
                        ec2_data = ec2['Name']
                        instanceid_data = ec2['Target']['Id']
                        #print(ec2['Name'])
                        #print(ec2['Target']['Id'])
            
                # Write the user's details to the CSV
                        writer.writerow({
                            'AWS Environment': aws_environment,
                            'Region': region_data,
                            'ALB Name': elb_name,
                            'Target Group': tg_data,
                            'Target Server': ec2_data,
                            'Instance ID': instanceid_data
                    
                            # 'Email': email,
                            # 'ConsoleAccess': console_access,
                            # 'LastLogin': last_login,
                            # 'LoggedInAfterDisablementDate': logged_in_after_disablement_date,
                            # 'IsServiceAccount': service_account,
                            # 'MFA': mfa,
                            # 'AccessKeys': access_keys,
                            # 'ForImmediateDeletion': for_immediate_deletion
                        })

                # input("")
    
    iam.detach_user_policy(UserName='sre-cli-user',PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")