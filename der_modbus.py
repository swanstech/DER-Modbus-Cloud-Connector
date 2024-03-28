#from pymodbus import ModbusTcpClient, ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient

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
            
    """
    Modbus RTU Connection
    def modbus_rtu(self, port, baudrate, parity, bytesize=8, stopbits=1, meter_addr=1):
        client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, 
                                    bytesize=bytesize, stopbits=stopbits, parity=parity, timeout=3)
        try:
            connection = client.connect()
            return client, connection
        except Exception as e:
            print(f"Error Connecting to Modbus RTU: {e}")
            return None, False
    """
    
    # Reading the Registers
    def read_registers(self, client, start_addr, end_addr=None, count=None):
        print("Read_Registers", start_addr, end_addr, count)
        if count is None and end_addr is not None:
            count = (end_addr + 1) - start_addr
        
        try:
        # start_address is to be subtracted by 1 as per documentation
            result = client.read_holding_registers(start_addr-1, count, unit=1)
            print(f"Result Value is: {result.registers}")
            if not result.isError():
                return result.registers
            else:
                print(f"Error Reading Register {start_addr}: {result}")
                return None
        except Exception as e:
            print(f"Error Reading Register {start_addr}: {e}")
            return None