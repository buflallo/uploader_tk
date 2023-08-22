import requests

with open('ProxiesToCheck.txt', 'r') as f:
    proxies = f.readlines()

new_proxies = []

for proxy in proxies:
    proxy = proxy.strip()
    try:
        response = requests.get('https://www.tiktok.com/', proxies={'socks5://': proxy}, timeout=0.7)
        if response.status_code == 200:
            print(f'{proxy} is working')
            new_proxies.append(proxy)
        else:
            print(f'{proxy} is not working')
    except:
        print(f'{proxy} is not working')

with open('ProxiesToCheck.txt', 'w') as f:
    f.write('\n'.join(new_proxies))

print('Done')

