from nornir import InitNornir
from nornir.core.filter import F
import os
import logging
import pathlib
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from datetime import date

nr = InitNornir(config_file="config.yaml")


def backups_dir():
    config_dir = "config-archive"
    date_dir = config_dir + "/" + str(date.today())
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    return date_dir

def create_backups_dir():
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

def save_config_to_file(hostname, building, config):
    filename =  f"{hostname}.cfg"
    BACKUP_DIR = backups_dir()+ "/" + building
    pathlib.Path(BACKUP_DIR).mkdir(exist_ok=True)
    with open(os.path.join(BACKUP_DIR, filename), "w") as f:
        f.write(config)

def backups():
    file = open("bk_building.txt", "r")
    for building in file:
        devices = nr.filter(F(groups__contains=building.strip()))
        backup_results = devices.run(task=netmiko_send_command, command_string="show run")
        for hostname in backup_results:
            save_config_to_file(hostname, building.strip(), backup_results[hostname][0].result )


def main ():
    #create_backups_dir()
    backups()

if __name__ == "__main__":
    main()
