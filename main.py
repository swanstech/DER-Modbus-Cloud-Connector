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

""" Decode the string types """
def decode_string(registers):
    result = ""
    for reg in registers:
        char1 = chr(reg >> 8)
        char2 = chr(reg & 0xFF)
        result += char1 + char2
    return result.rstrip('\x00')

""" Decode the uint16 data types """
def decode_uint16(registers):
    return registers[0] if registers else None

""" Decode the int16 data types """
def decode_int16(register):
    return register - 65536 if register > 32767 else register

""" Read the register values """
def read_registers_based_on_df(der_instance, client, df):
    for _, row in df.iterrows():
        start_address = row['Register Start Address']
        count = row['Register Size'] if df.notnull(row['Register Size']) else row['Register End Address'] - start_address + 1
        data_type = row['Type']
        rds_field = row['RDS Fields']

        raw_data = der_instance.read_registers(client, start_address, count)
        if raw_data is not None:
            if data_type == 'string':
                decoded_data = decode_string(raw_data)
            elif data_type == 'uint16':
                decoded_data = decode_uint16(raw_data)
            elif data_type in ['int16', 'enum16']:
                decoded_data = [decode_int16(reg) for reg in raw_data]
            else:
                decoded_data = raw_data

            print(f"Decoded Data from {rds_field} ({data_type}): {decoded_data}")
        else:
            print(f"Failed to read data for {rds_field}")


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