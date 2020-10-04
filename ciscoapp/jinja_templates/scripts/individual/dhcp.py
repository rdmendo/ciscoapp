from ipaddress import ip_network
from jinja2 import Environment, FileSystemLoader
import yaml

class GenerateDhcp:

    def count_pool(self, network):
        network_host = ip_network(network)
        network_list = network_host.num_addresses

        return "{}".format(network_list - 2)


    def create_pool(self, network, poolname, interface, private_addr):
        ipnetaddr = ip_network(network)
        net_add = ipnetaddr.network_address
        net_mask = ipnetaddr.netmask
        poolname = str(poolname).upper()

        priv = str(private_addr)
        priv_split = priv.split('.')
        priv_addr = f"{priv_split[0]}.{priv_split[1]}"

        template_dir = "ciscoapp/generators/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        dhcp_baseline = ENV.get_template('dhcp.j2')

        from_template= dhcp_baseline.render(
                network=net_add,
                ipaddr=ipnetaddr.hosts(),
                mask=net_mask,
                poolname = poolname,
                priv_address = priv_addr,
                interface = interface,)
        
        return from_template
    
    

# user_dhcp = GenerateDhcp("113.61.52.0/24", "3D", "g0/0", "172.16.1.0/24")
# result = user_dhcp.create_pool()

# print(result)