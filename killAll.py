import os
import sys
import boto3
import urllib3

def main():
    access_key = ""
    secret_key = ""
    account_num = ""
    region = ""
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
    killThese = killAll(client)
    ec2 = session.resource(
        "ec2",
        verify=False
    )
    kill(ec2, killThese)

def killAll(client):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    nukeThese = []
    all = client.describe_instances()
    for res in all.get("Reservations"):
        for inst in res.get("Instances"):
            nukeThese.append(inst.get("InstanceId"))
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
