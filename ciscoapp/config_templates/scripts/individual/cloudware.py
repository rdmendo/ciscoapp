from ipaddress import ip_network
from jinja2 import Environment, FileSystemLoader
import yaml

class Cloudware():
    
    def create_office(self, name, level, inet, network_address, interface, bandwidth, implementation_type):
        network = ip_network(network_address)
        template_dir = "/root/ciscoapp/ciscoapp/generators/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        new_office_baseline = ENV.get_template('cloudware.j2')

        from_template= new_office_baseline.render(
                implementation_type = implementation_type,
                level = level,
                name=name,
                inet=inet,
                network=network,
                interface = interface,
                bandwidth=bandwidth)
        
        return from_template
        


# user_cloudware = Cloudware()
# result = user_cloudware.create_office("3D", 5, 1812, '113.61.52.0/24', "g0/0", 50)
        
    