import requests
import ipaddress

def get_geo_info(ip):
    try:
        # Skip local/private/reserved IPs
        if ipaddress.ip_address(ip).is_private:
            return "Local Network", "Private IP"

        response = requests.get(f"https://ipwho.is/{ip}", timeout=3)
        data = response.json()

        if data.get("success"):
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")
            org = data.get("connection", {}).get("org", "Unknown Org")
            location = f"{city}, {country}"
            return location, org
        else:
            print(f"[IPWHOIS ERROR] {ip} → {data.get('message')}")
            return "Unknown, Unknown", "Unknown Org"
    except Exception as e:
        print(f"[GEO EXCEPTION] Failed for {ip}: {e}")
        return "Unknown, Unknown", "Unknown Org"


# import requests

# def get_geo_info(ip):
#     try:
#         response = requests.get(f"https://ipwho.is/{ip}", timeout=3)
#         data = response.json()

#         if data.get("success"):
#             city = data.get("city", "Unknown")
#             country = data.get("country", "Unknown")
#             org = data.get("connection", {}).get("org", "Unknown Org")
#             location = f"{city}, {country}"
#             return location, org
#         else:
#             print(f"[IPWHOIS ERROR] {ip} → {data.get('message')}")
#             return "Unknown, Unknown", "Unknown Org"
#     except Exception as e:
#         print(f"[GEO EXCEPTION] Failed for {ip}: {e}")
#         return "Unknown, Unknown", "Unknown Org"
