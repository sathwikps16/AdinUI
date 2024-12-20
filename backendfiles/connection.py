#PG NETWORK
# from pymilvus import connections

# try:
#     connections.connect(
#         host='192.168.0.130', 
#         port='19530'
#     )
#     print("Connection successful!")
# except Exception as e:
#     print(f"Connection failed: {e}")

#OFFICE NETWORK
from pymilvus import connections

try:
    connections.connect(
        host='10.1.7.137', 
        port='19530'
    )
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
