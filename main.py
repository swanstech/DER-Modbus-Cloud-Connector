import sys
from der_modbus import der_modbus  
from data_mapper import combined_df

if len(sys.argv) < 3:
    print("Usage: script.py ip_address port_number")
    sys.exit(1)

ip_address = sys.argv[1]
port_number = int(sys.argv[2])

# Example connection settings (now using command-line arguments)
connection_settings = {
    "connection_type": "tcp",
    "ipaddress": ip_address,
    "port_number": port_number,
}

def read_registers_based_on_df(der_instance, client):
    for _, row in combined_df.iterrows():
        start_address = row['Register Start Address']
        count = row["Register Size"]
        if not count:
            # 'Size' needs to be calculated as 'End Address' - 'Start Address' + 1
            count = row['Register End Address'] - start_address + 1

        # Reading data using the der_modbus instance
        data = der_instance.read_registers(client, start_address, count=count)
        if data is not None:
            # The data has to be converted/decoded based on their datatype
            print(f"Data from {row['RDS Fields']}: {data}")
        else:
            print(f"Failed to read data for {row['RDS Fields']}")

def main():
    der_instance = der_modbus()
    connection_type = connection_settings["connection_type"]
    ip_address = connection_settings["ipaddress"]
    port_number = connection_settings["port_number"]

    # Determine the Connection Type Required
    try:
        if connection_type == "tcp":
            der_client, der_connection = der_instance.modbus_tcp(ip_address, port_number)
        elif connection_type == "rtu":
            der_client, der_connection = der_instance.modbus_rtu(
                    ''' 
                        These parameters required but are not fixed to the accurate values
                        port_number,
                        baudrate=der_data.get("baudrate", 9600),
                        parity=der_data.get("parity", 'N'),
                        bytesize=der_data.get("bytesize", 8),
                        stopbits=der_data.get("stopbits", 1),
                        meter_addr=der_data.get("meter_addr", 1)
                    '''
            )
        else:
            print(f"Unsupported Communication Type: {connection_type}")
            return
            
        # Check if the connection is established
        if der_connection:
            print(f"Succesfully Connected to the DER: {ip_address} on the Port: {port_number}")
            read_registers_based_on_df(der_instance, der_client)
            der_client.close()
        else:
            print(f"Failed to Connected to the DER: {ip_address} on the Port: {port_number}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'der_connection' in locals() and der_connection:
            try:
                der_client.close()
                print("Connection closed.")
            except Exception as e:
                print(f"Error closing the connection: {e}")

if __name__ == "__main__":
    main()