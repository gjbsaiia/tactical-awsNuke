import os
import sys

def main():
    config = "config/nuke-config.yml"
    template = "config_template.txt"
    # random 'instance ids' for testing
    nukeThese = ["7829317893", "378947289", "3290483290", "38920489328940", "38924043", "83942083290"]
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
        file.write("accounts:\n  YOUR_ACCOUNT_NUMBER: {}")
        file.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted \_[*.*]_/\n')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
