import sys
import pandas as pd
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from data_mapper import combined_df  # Ensure combined_df is correctly imported

if len(sys.argv) < 3:
    print("Usage: script.py ip_address port_number")
    sys.exit(1)

ip_address = sys.argv[1]
port_number = int(sys.argv[2])

connection_settings = {
    "connection_type": "tcp",
    "ipaddress": ip_address,
    "port_number": port_number,
}

def decode_data(raw_data, data_type):
    """Decode raw data from Modbus registers based on the specified data type."""
    decoder = BinaryPayloadDecoder.fromRegisters(raw_data, byteorder=Endian.Big, wordorder=Endian.Big)

    if data_type.startswith('string'):
        # Assuming string size is twice the number of registers (2 chars per register)
        string_length = len(raw_data) * 2
        return decoder.decode_string(string_length).decode('utf-8').rstrip('\x00')
    elif data_type == 'uint16':
        return decoder.decode_16bit_uint()
    elif data_type == 'int16':
        return decoder.decode_16bit_int()
    elif data_type == 'uint32':
        return decoder.decode_32bit_uint()
    elif data_type == 'int32':
        return decoder.decode_32bit_int()
    elif data_type == 'float32':
        return decoder.decode_32bit_float()
    else:
        # Handle other data types or log an unsupported type error
        return None

def read_and_decode_registers(client, df):
    """Read and decode register values based on DataFrame configuration."""
    for _, row in df.iterrows():
        start_address = row['Register Start Address']
        data_type = row['Type']
        count = row.get('Register Size', row['Register End Address'] - start_address + 1)

        # Remove the below function and use der_modbus.py read registers function
        result = client.read_holding_registers(start_address-1, count, unit=1)
        if not result.isError():
            # Add the decode logic from the provided GitHub Link
            decoded_data = decode_data(result.registers, data_type)
            print(f"Decoded Data from {row['RDS Fields']} ({data_type}): {decoded_data}")
        else:
            print(f"Failed to read data for {row['RDS Fields']}")

def main():
    client = ModbusClient(ip_address, port=port_number)
    if client.connect():
        print(f"Succesfully Connected to the DER: {ip_address} on the Port: {port_number}")
        read_and_decode_registers(client, combined_df)
        client.close()
    else:
        print(f"Failed to Connect to the DER: {ip_address} on the Port: {port_number}")

if __name__ == "__main__":
    main()
