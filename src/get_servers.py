from datetime import datetime
import os
import requests

class ServerUpdater:
    def __init__(self, subscription_url, output_file):
        self.subscription_url = subscription_url
        # self.output_file = output_file
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_file = f'data/current/sub7_{self.timestamp}.txt'
        self.worked_file = f'data/current/worked_sub7_{self.timestamp}.txt'
    # def get_subscription_servers(self):
    #     response = requests.get(self.subscription_url)
    #     servers = response.text.strip().split('\n')
    #     return servers
    def get_subscription_servers(self):
        if self.subscription_url:
            response = requests.get(self.subscription_url)
            servers = response.text.strip().split('\n')
            # Filter out servers that don't start with the specified prefixes
            filtered_servers = [server for server in servers if server.startswith(('vmess', 'vless', 'ss', 'trojan'))]
            return filtered_servers
        else:
            return []

    # def update_servers(self):
    #     subscription_servers = self.get_subscription_servers()
    #     with open(self.output_file, 'w') as file:
    #         file.write('\n'.join(subscription_servers))

    #     print(f"Servers written to {self.output_file}")

    def update_servers(self):
        subscription_servers = self.get_subscription_servers()
        os.makedirs('data/current', exist_ok=True)
        os.makedirs('data/archive', exist_ok=True)
        
        with open(self.current_file, 'w') as file:
            file.write('\n'.join(subscription_servers))

if __name__ == '__main__':
    subscription_url = 'https://raw.githubusercontent.com/barry-far/V2ray-Configs/refs/heads/main/Sub7.txt'
    output_file = 'sub7.txt'
    updater = ServerUpdater(subscription_url, output_file)
    updater.update_servers()