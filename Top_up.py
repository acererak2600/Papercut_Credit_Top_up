import os
import sys
import xmlrpc.client

if len(sys.argv) < 2:
    print("Usage: python topup.py <username>")
    exit()

username = sys.argv[1]
amount = float(25) #change to credit required

# Server configuration
server_url = "https://YOUR_SERVER_URL/rpc/api/xmlrpc"
secret_token = os.environ.get("API_TOKEN")  # Replace with your actual token env variable
if not secret_token:
    raise ValueError("Please set the API_TOKEN environment variable")


# Create server connection
server = xmlrpc.client.ServerProxy(server_url)

try:
    if not server.api.isUserExists(secret_token, username):
        print(f"User '{username}' does not exist")
        exit()
    balance = server.api.getUserAccountBalance(secret_token, username)
    print (username,"Acc Balance: ",balance)

    if balance >= amount:
        print("Balance already at or above top-up threshold, skipping.")
        exit()
    result = server.api.setUserAccountBalance(secret_token, username, amount, "Balance top-up via automation script")
    print(f"Set balance result: {result}")
    print (f"New balance for '{username}':", server.api.getUserAccountBalance(secret_token, username)) 
    
except xmlrpc.client.Fault as fault:
    print(f"XML-RPC Fault: {fault.faultCode} - {fault.faultString}")
except Exception as e:
    print(f"Error: {e}")
