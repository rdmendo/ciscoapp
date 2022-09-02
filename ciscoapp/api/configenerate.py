from ipaddress import ip_network
from jinja2 import Environment, FileSystemLoader
import yaml

class ConfigTemplate:
    def __init__(self):
        super().__init__()
        
class GenerateDhcp:

    def count_pool(self, network):
        network_host = ip_network(network)
        network_list = network_host.num_addresses

        return "{}".format(network_list - 2)

    def create_pool(self, network, poolname, private_addr):
        ipnetaddr = ip_network(network)
        net_add = ipnetaddr.network_address
        net_mask = ipnetaddr.netmask
        poolname = str(poolname).upper()

        priv = str(private_addr)
        priv_split = priv.split('.')
        priv_addr = f"{priv_split[0]}.{priv_split[1]}"

        template_dir = "ciscoapp/config_templates/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        dhcp_baseline = ENV.get_template('dhcp.j2')

        from_template= dhcp_baseline.render(
                network=net_add,
                ipaddr=ipnetaddr.hosts(),
                mask=net_mask,
                poolname = poolname,
                priv_address = priv_addr)
        
        return from_template
    
class GenerateQos:
    def create_qos(self, policy_name, bandwidth, interface, device):
        template_dir = "ciscoapp/config_templates/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        qos_baseline = ENV.get_template('qos.j2')

        from_template= qos_baseline.render(
                policy_name=policy_name,
                bandwidth=bandwidth,
                device = device,
                interface=interface)
        
        return from_template
    
    
class GenerateCloudware:
    
    def create_office(self, name, level, inet, network_address, interface, bandwidth, implementation_type):
        network = ip_network(network_address)
        template_dir = "ciscoapp/config_templates/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        new_office_baseline = ENV.get_template('new.j2')

        from_template= new_office_baseline.render(
                level = level,
                name=name,
                inet=inet,
                network=network,
                interface = interface,
                bandwidth=bandwidth,
                implementation_type = implementation_type,)
        
        return from_template
    
class GenerateAdditional:
    
    def create_additional(self,new_link, existing_link ):
        network = ip_network(new_link)
        template_dir = "ciscoapp/config_templates/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        new_office_baseline = ENV.get_template('additional.j2')

        from_template= new_office_baseline.render(
                existing_link = existing_link,
                new_network=network)
        
        return from_template

# dhcp = GenerateDhcp()
# result = dhcp.create_pool('TESTPOOL', '10.10.10.0/24')
# print(result)

