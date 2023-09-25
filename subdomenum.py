# import pandas as pd
# import socket

# # Function to resolve a domain name to IP addresses
# def resolve_domain_to_ip(domain):
#     try:
#         ips = socket.gethostbyname_ex(domain)
#         return ips[2]
#     except socket.gaierror:
#         return None

# # Function to determine if a domain is associated with Cloudflare
# def is_cloudflare(ip_addresses):
#     return len(ip_addresses) > 1 if ip_addresses else False

# # Load the Excel file into a DataFrame
# excel_file = "threatmap_data.xlsx"  # Replace with the path to your Excel file
# df = pd.read_excel(excel_file)

# # Create a new column 'ip_addresses' and populate it with resolved IP addresses (excluding None)
# df['ip_addresses'] = df['Domain'].apply(resolve_domain_to_ip)

# # Create a new column 'is_cloudflare' and set it based on the IP addresses (excluding None)
# df['is_cloudflare'] = df['ip_addresses'].apply(is_cloudflare)

# # Drop rows where 'ip_addresses' is None (domains not found)
# df = df.dropna(subset=['ip_addresses'])

# # Create a new CSV file with the original data, IP addresses, and Cloudflare flag
# new_csv_file = "new_csv_file.csv"  # Replace with the desired name for the new CSV file
# df.to_csv(new_csv_file, index=False)

import pandas as pd
import socket

# Function to resolve a domain name to IP addresses
def resolve_domain_to_ip(domain):
    try:
        ips = socket.gethostbyname_ex(domain)
        return ips[2]
    except socket.gaierror:
        return None

# Function to determine if a domain is associated with Cloudflare
def is_cloudflare(ip_addresses):
    return len(ip_addresses) > 1 if ip_addresses else False

# Load the Excel file into a DataFrame
excel_file = "threatmap_data.xlsx"  # Replace with the path to your Excel file
df = pd.read_excel(excel_file)

# Create a new column 'ip_addresses' and populate it with resolved IP addresses (excluding None)
df['ip_addresses'] = df['Domain'].apply(resolve_domain_to_ip)

# Create a new column 'is_cloudflare' and set it based on the IP addresses (excluding None)
df['is_cloudflare'] = df['ip_addresses'].apply(is_cloudflare)

# Create a new CSV file with the original data, Cloudflare flag, and without the second IP address column
new_csv_file = "resolved_file.csv"
df.to_csv(new_csv_file, index=False)
