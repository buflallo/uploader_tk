import requests
def check_proxies(proxies_file):
    """
    Check if proxies in a file are available by making a simple request with a timeout of 3 seconds.

    Parameters
    ----------
    proxies_file : str
        The path to the file containing proxies, one per line.

    Returns
    -------
    available_proxies : list
        A list of available proxies.
    """
    available_proxies = []
    with open(proxies_file, 'r') as f:
        for line in f:
            proxy = line.strip()
            try:
                response = requests.get('https://www.tiktok.com', proxies={'socks5': proxy}, timeout=1)
                if response.status_code == 200:
                    available_proxies.append(proxy)
                print(f"Proxy {proxy} checked with status code {response.status_code}")
            except:
                print(f"Proxy {proxy} is invalid")
                pass
    return available_proxies


print (check_proxies('socks5_proxies.txt'))
