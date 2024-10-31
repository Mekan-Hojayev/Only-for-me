import base64
import json
from urllib.parse import urlparse
from ping3 import ping
from tqdm import tqdm

class ConfigChecker:
    @staticmethod
    def decode_base64(data):
        return base64.b64decode(data + '=' * (-len(data) % 4)).decode()

    @staticmethod
    def parse_trojan(url):
        parsed = urlparse(url)
        return {
            'type': 'trojan',
            'host': parsed.hostname,
            'port': parsed.port
        }

    @staticmethod
    def parse_ss(url):
        parsed = urlparse(url)
        decoded = ConfigChecker.decode_base64(parsed.username)
        host, port = parsed.hostname, parsed.port
        return {
            'type': 'ss',
            'host': host,
            'port': port
        }

    @staticmethod
    def parse_vmess(url):
        decoded = json.loads(ConfigChecker.decode_base64(url.split('://')[1]))
        return {
            'type': 'vmess',
            'host': decoded['add'],
            'port': decoded['port']
        }

    @staticmethod
    def parse_ultra(url):
        if url.startswith("trojan") or url.startswith("vless"):
            return ConfigChecker.parse_trojan(url)
        elif url.startswith("ss"):
            return ConfigChecker.parse_ss(url)
        else:
            return ConfigChecker.parse_vmess(url)

    @staticmethod
    def check_connectivity(config):
        try:
            server = ConfigChecker.parse_ultra(config)
            ping_result = ping(server['host'], timeout=1)
            if ping_result is not None:
                print(f"Ping successful for {server['type']} server {server['host']}:{server['port']}. Latency: {ping_result:.2f} ms")
                return True
            else:
                print(f"Ping failed for {server['type']} server {server['host']}:{server['port']}")
                return False
        except Exception as e:
            print(f"Error checking connectivity: {str(e)}")
            return False

class ConfigFilter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def filter_configs(self):
        with open(self.input_file, 'r') as infile, open(self.output_file, 'w') as outfile:
            for line in tqdm(infile):
                config = line.strip()
                if ConfigChecker.check_connectivity(config):
                    outfile.write(config + '\n')

if __name__ == "__main__":
    config_filter = ConfigFilter('sub7.txt', 'worked_sub7.txt')
    config_filter.filter_configs()