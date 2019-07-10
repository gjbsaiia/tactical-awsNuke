import os
import sys
import boto3
import urllib3

def main():
    access_key = ""
    secret_key = ""
    # Instances tagged with the tags listed here that are set to a "1" will be destroyed
    target_tags = ["dispensible"]
    try:
        # creates boto3 session
        client = boto3.client(
            "ec2",
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            region_name = "us-east-1",
            verify=False
        )
    except Exception as e:
        print("Error creating AWS session: "+str(e))
        sys.exit(3)
    # updates nuke-config.yml
    filterByTag(client, target_tags)
    try:
        nuke_it(access_key, secret_key) #call method to nuke account
        #print("this is where we would nuke")
    except Exception as e:
        print("Error calling the nuke_it functions: {}".format(e))
        sys.exit(3)

def filterByTag(client, target_tags):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    config = "config/nuke-config.yml"
    template = "config_template.txt"

    nukeThese = []
    # this is so gross... sorry
    all = client.describe_instances()
    for res in all["Reservations"]:
        for inst in res["Instances"]:
            for tag in inst["Tags"]:
                for each in target_tags:
                    if(tag["Key"] == each and tag["Value"] == '1'):
                        nukeThese.append(inst["InstanceId"])
    base = ""
    with open(template, "r") as temp:
        base = temp.read()
        temp.close()
    with open(config, "w") as file:
        file.write(base+"\n")
        file.close()
    with open(config, "a") as file:
        for each in nukeThese:
            file.write("  - "+each+"\n")
        file.write("accounts:\n  070317122463: {}")
        file.close()

def nuke_it(access_key,secret_key):
    osCmd = "aws-nuke --force --no-dry-run -c config/nuke-config.yml --access-key-id " + access_key +  " --secret-access-key " + secret_key
    print (osCmd)
    response = os.system(osCmd)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted \_[*.*]_/\n')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
