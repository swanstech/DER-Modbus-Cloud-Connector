import os
import boto3
from botocore.exceptions import ClientError
import psycopg2
import json
import datetime

class database_tx:
    def __init__(self):
        pass
    
    def get_rds_creds(self):
        secret_name = "aws_postgres_swans_database"
        region_name = "ap-southeast-2"
        aws_id = os.environ.get('AWS_AccessKeyID')
        aws_key = os.environ.get('AWS_SecretAccessKey')

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=aws_id,
            aws_secret_access_key=aws_key
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
                return e
        else:
            
            if 'SecretString' in get_secret_value_response:
                text_secret_data = get_secret_value_response['SecretString']
                return json.loads(text_secret_data)
            else:
                binary_secret_data = get_secret_value_response['SecretBinary']
                return json.loads(binary_secret_data)
    
    # Create Operation - table_name:string -> ex - der_control, fields:dict -> {max_active_power:20, max_reactive_power:30}
    # Update Operation can also be created
    def store_data(self, table_name, table_data, creds, operation):
    
        try:
            # Initial Approach
            # table_fields = []
            # table_values = []
            # for x, y in table_data.items():
            #     table_fields.append(x)
            #     table_fields.append(y)
                
            # table_fields = tuple(table_fields)
            # table_values = tuple(table_values)
                
            # db_query = f'insert into {table_name} {table_fields} values {table_values}'
            
            # Current Approach
            table_fields = ', '.join(table_data.keys())
            # print(table_fields)
            placeholders = ', '.join(['%s' for x in table_data.values()])
            # print(placeholders)
            db_query = f'''insert into {table_name} ({table_fields}) values ({placeholders});'''
            # print(db_query)
            # print(tuple([x for x in table_data]))
        
            # Get the creds from AWS Secrets Manager
            db_host = creds['host']
            db_port = creds['port']
            db_name = creds['dbname']
            db_user = creds['user']
            db_pwd = creds['password']

            with psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pwd) as connect:
                with connect.cursor() as cursor:
                    cursor.execute(db_query, tuple([x for x in table_data.values()]))
                    connect.commit()
            return 'Data inserted succesfully'
            
        except Exception as e:
            # return 'Failed to Insert Data'
            return e

db_instance = database_tx()

# def format_time(date):
#     # Convert to string in the expected format
#     return date.strftime('%Y-%m-%d %H:%M:%S')

# # 'manufacture_date': format_time(datetime.datetime(2024, 3, 14)),

der_info = {
    'der_id': None,
    'der_name': 'Sp_Pro',
    'der_type': 'Inverter',
    'manufacturer_id': 'SP_123',
    'manufacturer_serial_number': 'Selectronics_123',
    'manufacture_date': '2023-10-19',
    'manufacturer_info': 'Selectronics',
    'manufacture_model_number': '000',
    'manufacture_hw_version': 'TBD',
    'latest_sw_version': 'TBD',
    'latest_sw_release_date': '2023-10-19',
    'latest_firmware_version': 'TBD',
    'latest_firmware_release_date': '2023-10-19',
    'location': 'Smart Energy Lab'
}

print(db_instance.store_data('der_information', der_info, db_instance.get_rds_creds()))