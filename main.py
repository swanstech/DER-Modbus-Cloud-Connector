from der_modbus import DERModbus

# List of Dictionaries which consists of the DER Data
# Data Mapper can be used here
der_data_list = [
{
    "connection_type": "tcp",  # or "rtu"
    "port_number": 502,
    "ipaddress": "x.y.z.a",
    "der_name": (40021, 40036, 16),
    "der_type": (40134, 40134, 1),
    "manufacturer_serial_number": (40053, 40068, 16),
    "manufacturer_info": (40005, 40020, 16),
    "latest_sw_version": (40045, 40052, 8),
    "max_ac_current": (40144, 40144, 1),
    "max_apparent_power": (40137, 40137, 1),
    "max_active_power_tx": (40135, 40135, 1),
    "set_max_apparent_power": (40167, 40167, 1),
    "set_max_active_power_tx": (40162, 40162, 1)
}, 
{
    "connection_type": "tcp",  # or "rtu"
    "port_number": 502,
    "ipaddress": "x.y.z.a",
    "der_name": (40021, 40036, 16),
    "der_type": (40134, 40134, 1),
    "manufacturer_serial_number": (40053, 40068, 16),
    "manufacturer_info": (40005, 40020, 16),
    "latest_sw_version": (40045, 40052, 8),
    "max_ac_current": (40144, 40144, 1),
    "max_apparent_power": (40137, 40137, 1),
    "max_active_power_tx": (40135, 40135, 1),
    "set_max_apparent_power": (40167, 40167, 1),
    "set_max_active_power_tx": (40162, 40162, 1)              
},
            ]

def main():
    der_instance = DERModbus()

    # Iterate through the der_data_list
    for der_data in der_data_list:
        # Extract information from der_data
        connection_type = der_data["connection_type"]
        ip_address = der_data.get["ipaddress"]
        port_number = der_data.get["port_number"]

        # Determine the Connection Type Required
        try:
            if connection_type == "tcp":
                der_client, der_connection = der_instance.modbus_tcp(ip_address, port_number)
            elif connection_type == "rtu":
                der_client, der_connection = der_instance.modbus_rtu(
                    # These parameters are not fixed to the accurate values
                    port_number,
                    baudrate=der_data.get("baudrate", 9600),
                    parity=der_data.get("parity", 'N'),
                    bytesize=der_data.get("bytesize", 8),
                    stopbits=der_data.get("stopbits", 1),
                    meter_addr=der_data.get("meter_addr", 1)
                )
            else:
                print(f"Unsupported Communication Type: {connection_type}")
                continue
            
            # Check if the connection is established
            if der_connection:
                print(f"Succesfully Connected to the DER: {ip_address} on the Port: {port_number}")

                # Get the field and the register information to read the data
                for field, register_info in der_data.items():
                    if field not in ["connection_type", "ipaddress", "port_number"]:
                        start_addr, end_addr, count = register_info
                        data = der_instance.read_registers(der_client, start_addr, end_addr, count)
                        print(f"{field}: {data}")

        finally:
            # Close the connection after reading the data
            if der_connection:
                der_client.close()
                print(f"Connection to the DER is Closed")

if __name__ == "__main__":
    main()