from jinja2 import Environment, FileSystemLoader
import yaml

class GenerateQos:
    
    def __init__(self):
        super().__init__()

    def create_qos(self, policy_name, bandwidth, interface, device):
        template_dir = "ciscoapp/generators/template"
        ENV = Environment(loader=FileSystemLoader(template_dir))
        qos_baseline = ENV.get_template('qos.j2')

        from_template= qos_baseline.render(
                policy_name=policy_name,
                bandwidth=bandwidth,
                device = device,
                interface=interface)
        
        return from_template

# user_qos = GenerateQos("3D", 50, 'G0/0', 'Router')
# result = user_qos.create_qos()
# print(result)
        
        