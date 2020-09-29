from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config, napalm_configure
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from ipaddress import ip_network
import os

class Divert:
    
    os.environ["NET_TEXTFSM"] = "ntc-templates"
    nr = InitNornir(config_file="ciscoapp/generators/scripts/config.yml")

    def __init__(self, mitigate_address, action_to_be_done):
        super().__init__()

        self.mitigate_address = mitigate_address
        self.action_to_be_done = action_to_be_done

    def advertise_to_incapsula(self, task):
        acl_template = task.run(task=template_file,
        name="Buildling ACL Configuration",
        net= ip_network(self.mitigate_address),
        mitigate=self.action_to_be_done,
        template="divert.j2", 
        path=f"ciscoapp/generators/template/{task.host}")

        task.host["acl"] = acl_template.result
        acl_output = task.host["acl"]
        # acl_send = acl_output.splitlines()

        task.run(task=netmiko_send_config,
        name="Pushing ACL Commands",
        config_commands=acl_output)
        
    def clear_bgp(self, task):
        task.run(netmiko_send_command, command_string="clear ip bgp * soft out")

        
        