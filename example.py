from datetime import datetime

instances = []
for res in all.get("Reservations"):
    for inst in res.get("Instances"):
        instance = [inst.get("InstanceId"), inst.get("LaunchTime")]
        instances.append(instance)
if(len(instances) > 1):
    min = datetime.timedelta(datetime.now() - instances[0][1])
    myInstance = instances[0]
    for instance in instances:
        if(min > datetime.timedelta(datetime.now() - instance[1])):
            myInstance = instance
            min = datetime.timedelta(datetime.now() - instance[1])
