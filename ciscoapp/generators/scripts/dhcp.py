from ipaddress import ip_network
from jinja2 import Environment, FileSystemLoader
import yaml

class GenerateDhcp:
    def __init__(self, network, poolname, interface, private_addr):
        super().__init__()

        self.network = network
        self.poolname = poolname
        self.interface = interface
        self.private_addr = private_addr

    def count_pool(self):
        network_host = ip_network(self.network)
        network_list = network_host.num_addresses

        return "{}".format(network_list - 2)

    def display_pool(self):
        
        return "Network Address: {} | Poolname: {} | Interface: {} | Private Address: {} ".format(self.network, str(self.poolname).upper(), self.interface, self.private_addr)


    def create_pool(self):
        ipnetaddr = ip_network(self.network)
        net_add = ipnetaddr.network_address
        net_mask = ipnetaddr.netmask
        poolname = str(self.poolname).upper()


        priv = str(self.private_addr)
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
                interface = self.interface,)
        
        return from_template
    
    

# user_dhcp = GenerateDhcp("113.61.52.0/24", "3D", "g0/0", "172.16.1.0/24")
# result = user_dhcp.create_pool()

# print(result)