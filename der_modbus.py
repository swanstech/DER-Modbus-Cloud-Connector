from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient

class der_modbus:
    def __init__(self):
        pass
    
    # Modbus TCP Connection
    def modbus_tcp(self, ip_addr, port_num):
        client = ModbusTcpClient(ip_addr, port_num)
        try:
            connection = client.connect()
            return client, connection
        except Exception as e:
            print(f"Error Connecting to Modbus TCP: {e}")
            return None, False
            
    # Modbus RTU Connection
    def modbus_rtu(self, port, baudrate, parity, bytesize=8, stopbits=1, meter_addr=1):
        client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, 
                                    bytesize=bytesize, stopbits=stopbits, parity=parity, timeout=3)
        try:
            connection = client.connect()
            return client, connection
        except Exception as e:
            print(f"Error Connecting to Modbus RTU: {e}")
            return None, False
    
    # Reading the Registers
    def read_registers(self, client, start_addr, end_addr=None, count=None):
        if count is None and end_addr is not None:
            count = (end_addr + 1) - start_addr
        elif count is None:
            # If count and end_addr are both None, you need a default or an error.
            count = 1  # Defaulting to reading 1 register, adjust as needed.
        try:
            result = client.read_holding_registers(start_addr, count)
            print(f"Result Value is: {result}")
            if not result.isError():
                return result.registers
            else:
                print(f"Error Reading Register {start_addr}: {result}")
                return None
        except Exception as e:
            print(f"Error Reading Register {start_addr}: {e}")
            return None
