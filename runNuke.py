import os
import sys
import boto3
import urllib3

def main():
    access_key = ""
    secret_key = ""
    account_num = ""
    region = ""
    # Instances tagged with the tags listed here that are set to a "1" will be destroyed
    target_tags = ["dispensible"]
    try:
        # creates boto3 session
        session = boto3.session.Session(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            region_name = region,
        )
    except Exception as e:
        print("Error creating AWS session: "+str(e))
        sys.exit(3)
    client = session.client(
        "ec2",
        verify=False
    )
    killThese = filterByTag(client, target_tags)
    ec2 = session.resource(
        "ec2",
        verify=False
    )
    kill(ec2, killThese)

def filterByTag(client, target_tags):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    nukeThese = []
    # this is so gross... sorry
    all = client.describe_instances()
    for res in all["Reservations"]:
        for inst in res["Instances"]:
            for tag in inst["Tags"]:
                for each in target_tags:
                    if(tag["Key"] == each and tag["Value"] == '1'):
                        nukeThese.append(inst["InstanceId"])
    return nukeThese

def kill(ec2, instances):
    print("Attempting killing all of these:")
    print(instances)
    try:
        ec2.instances.filter(InstanceIds = instances).terminate()
    except Exception as e:
        print("Yikes, terminate function failed: "+e)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted \_[*.*]_/\n')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
