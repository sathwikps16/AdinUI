# This code is responsible for checking wether any kind of data is inserted into the databbase and if inserted then update the env file 

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent
import logging
from dotenv import set_key, load_dotenv
import os

# Configure logging
logging.basicConfig(
    filename='ticketing_system_binlog.log',
    level=logging.INFO,
    format='%(asctime)s - Inserted Data: %(message)s'
)

# Load existing .env file
env_path = '.env'
load_dotenv(env_path)

def update_env_file(service_name, instance_url):
    """
    Update the .env file with SERVICE_NAME and INSTANCE_URL.
    """
    set_key(env_path, 'SERVICE_NAME', service_name)
    set_key(env_path, 'INSTANCE_URL', instance_url)
    print(f".env file updated: SERVICE_NAME={service_name}, INSTANCE_URL={instance_url}")

def monitor_binlog(db_config):
    """
    Monitor MySQL binlog for real-time inserts in the Ticketing_System table.
    Only refreshes and processes when new events are detected.
    """
    stream = BinLogStreamReader(
        connection_settings=db_config,
        server_id=100,  # Unique server ID
        only_events=[WriteRowsEvent],  # Monitor only INSERT events
        only_tables=['Ticketing_System'],  # Focus on this table
        blocking=True,  # Wait for new events
    )

    print("Waiting for new entries in Ticketing_System...")

    try:
        for binlogevent in stream:
            for row in binlogevent.rows:
                data = row['values']
                print(f"New row detected and logged: {data}")

                # Extract relevant values
                service_name = data.get('UNKNOWN_COL1')
                instance_url = data.get('UNKNOWN_COL2')

                # If both values exist, update the .env file
                if service_name and instance_url:
                    update_env_file(service_name, instance_url)

    except KeyboardInterrupt:
        print("Stopping binlog monitoring...")
    
    finally:
        stream.close()

if __name__ == '__main__':
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': '1234',
        'database': 'ticketing_system_db'
    }

    monitor_binlog(db_config)



