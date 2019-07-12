import os
import sys
import boto3
import urllib3

# Instances tagged with BOTH of these tags and values will be destroyed
target_tags = {
    "dispensible": "1",
    "Test": "Teeest"
}

groupTags = False

def main():
    global groupTags
    access_key = "AKIAIBHX65FJEYDUYH5A"
    secret_key = "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"
    account_num = "070317122463"
    region = "us-west-2"
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
    filter = buildFilter()
    if(groupTags):
        killThese = filterByTag(client,filter)
    else:
        killThese = segmentedFilterByTag(client, filter)
    ec2 = session.resource(
        "ec2",
        verify=False
    )
    kill(ec2, killThese)

def buildFilter():
    global target_tags
    filter = []
    for key, value in target_tags.items():
        filter.append({'Name': 'tag:'+key, 'Values': [value]})
    print(filter)
    return filter

def filterByTag(client,filter):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    nukeThese = []
    all = client.describe_instances(Filters=filter)
    for res in all.get("Reservations"):
        for inst in res.get("Instances"):
            nukeThese.append(inst.get("InstanceId"))
    return nukeThese

def segmentedFilterByTag(client,filter):
    killThese = []
    for each in filter:
        killThese.extend(filterByTag(client,[each]))
    killThese = list(dict.fromkeys(killThese))
    print(killThese)
    return killThese


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
