import base64
import json
from urllib.parse import urlparse
from ping3 import ping
from tqdm import tqdm
from datetime import datetime
import os
from pathlib import Path  # Import Path
from database.db_config import DatabaseManager

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
                return True, ping_result
            else:
                print(f"Ping failed for {server['type']} server {server['host']}:{server['port']}")
                return False, None
        except Exception as e:
            print(f"Error checking connectivity: {str(e)}")
            return False, None

class ConfigFilter:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.input_file = self.get_latest_file('data/current')  # Find the latest file
        self.output_file = f'data/current/worked_sub7_{self.timestamp}.txt'
        self.archive_dir = 'data/archive'
        self.db_manager = DatabaseManager()

    def get_latest_file(self, directory):
        # List all files in specified directory
        files = list(Path(directory).glob('*'))
        # Return the most recently modified file
        return max(files, key=os.path.getctime).as_posix()

    def archive_old_files(self):
        if os.path.exists(self.input_file):
            archive_name = f'sub7_{self.timestamp}_archive.txt'
            archive_path = os.path.join(self.archive_dir, archive_name)
            
            with open(self.input_file, 'r') as f:
                content = f.read()
                self.db_manager.save_server_data(archive_name, content)

    def filter_configs(self):
        working_servers = []
        
        with open(self.input_file, 'r') as infile:
            configs = infile.readlines()
            
        for config in tqdm(configs):
            config = config.strip()
            is_working, latency = ConfigChecker.check_connectivity(config)
            if is_working:
                working_servers.append({
                    'config': config,
                    'latency': latency
                })

        working_servers.sort(key=lambda x: x['latency'])

        with open(self.output_file, 'w') as outfile:
            for server in working_servers:
                outfile.write(f"{server['config']}\n")

        self.db_manager.save_server_data(
            f'worked_sub7_{self.timestamp}',
            '\n'.join([s['config'] for s in working_servers])
        )

def main():
    os.makedirs('data/current', exist_ok=True)
    os.makedirs('data/archive', exist_ok=True)
    
    config_filter = ConfigFilter()
    config_filter.archive_old_files()
    config_filter.filter_configs()

if __name__ == "__main__":
    main()
