from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config, napalm_configure
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from ipaddress import ip_network
import os

class ISPReroute:
    
    os.environ["NET_TEXTFSM"] = "ntc-templates"
    nr = InitNornir(config_file="ciscoapp/api/config.yml")
    
    def __init__(self, ipaddress, to_isp):
        super().__init__()

        self.ipaddress = ipaddress
        self.to_isp = to_isp
        
    def reroute(self, task):
        acl_template = task.run(task=template_file,
        name="Buildling Static Configuration",
        ipaddress = self.ipaddress,
        reroute_to=self.to_isp,
        template="reroute.j2", 
        path=f"ciscoapp/jinja_templates/template/reroute/{task.host}")

        task.host["acl"] = acl_template.result
        acl_output = task.host["acl"]
        acl_send = acl_output.splitlines()

        task.run(task=netmiko_send_config,
        name="Pushing Static Commands",
        config_commands=acl_send, delay_factor=.2)
        
    
