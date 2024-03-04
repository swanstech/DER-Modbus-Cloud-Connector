import pymodbus

# Establish Communication using Modbus or Modbus RTU
class der_modbus:
    def __init__(self):
        pass
    
    # Modbus TCP Connection
    def modbus_tcp(self, ip_addr, port_num):
        client = pymodbus.client.ModbusTcpClient(ip_addr, port_num)
        try:
            connection = client.connect()
            return client,connection
        except Exception as e:
            print(f"Error Connecting to Modbus TCP: {e}")
            return None,False
            
            
        
    # Modbus RTU Connection
    def modbus_rtu(self, port, baudrate, parity, bytesize=None, stopbits=None, meter_addr=None):
        client = pymodbus.client.AsyncModbusSerialClient(port, baudrate, bytesize, stopbits, parity, meter_addr)
        try:
            connection = client.connect()
            return client,connection
        except Exception as e:
            print(f"Error Connecting to Modbus RTU: {e}")
            return None,False
    
    # Reading the Registers
    def read_registers(self, client, start_addr, end_addr=None, count=None):
        if count == None:
            count = (end_addr+1) - start_addr
        try:
            data = client.read_holding_registers(start_addr, count)
            return data
        except Exception as e:
            print(f"Error Reading Register {start_addr}: {e}")
            return None