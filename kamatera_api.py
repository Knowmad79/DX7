"""
Kamatera API Client - Check and manage server status
Using the cloudcli API endpoint
"""
import requests
import json

CLIENT_ID = "7709dd8b46b3f0eec99366a07b7e1edb"
API_SECRET = "ae7fdb5dec5ca50daac06363ccf1f206"

# Try different API endpoints
API_ENDPOINTS = [
    "https://cloudcli.cloudwm.com",
    "https://console.kamatera.com/service",
    "https://api.kamatera.com",
    "https://cloudcli.kamatera.com"
]

def try_auth(base_url):
    """Try to authenticate with a given base URL"""
    print(f"\n  Trying: {base_url}")
    try:
        # Method 1: JSON body
        response = requests.post(
            f"{base_url}/service/authenticate",
            json={"clientId": CLIENT_ID, "secret": API_SECRET},
            timeout=10
        )
        if response.status_code == 200:
            return base_url, response.json()
        
        # Method 2: Headers
        response = requests.get(
            f"{base_url}/service/server",
            headers={
                "AuthClientId": CLIENT_ID,
                "AuthSecret": API_SECRET
            },
            timeout=10
        )
        if response.status_code == 200:
            return base_url, {"servers": response.json()}
            
    except Exception as e:
        print(f"    Error: {e}")
    return None, None

def list_servers_direct(base_url):
    """List servers using direct header auth"""
    print(f"\n[2] Listing servers from {base_url}...")
    try:
        response = requests.get(
            f"{base_url}/service/server",
            headers={
                "AuthClientId": CLIENT_ID,
                "AuthSecret": API_SECRET
            },
            timeout=15
        )
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)[:500]}")
            return data
        else:
            print(f"    Body: {response.text[:200]}")
    except Exception as e:
        print(f"    Error: {e}")
    return None

def main():
    print("=" * 60)
    print("KAMATERA API - SERVER STATUS CHECK")
    print("=" * 60)
    
    print("\n[1] Testing API endpoints...")
    working_url = None
    
    for url in API_ENDPOINTS:
        base, result = try_auth(url)
        if result:
            working_url = base
            print(f"    SUCCESS with {base}!")
            print(f"    Result: {json.dumps(result, indent=2)[:300]}")
            break
    
    if not working_url:
        print("\n  Trying direct server list...")
        for url in API_ENDPOINTS:
            data = list_servers_direct(url)
            if data:
                working_url = url
                break
    
    if not working_url:
        print("\n" + "=" * 60)
        print("Could not connect to Kamatera API.")
        print("Please verify your API credentials are correct.")
        print("You can also check the server status in the Kamatera console:")
        print("  https://console.kamatera.com/")
        print("=" * 60)
    else:
        print(f"\n  Working API: {working_url}")

if __name__ == "__main__":
    main()
