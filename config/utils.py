from payos import PayOS
import os

payOS = PayOS(client_id= os.environ.get('PAYOS_CLIENT_ID'), api_key=os.environ.get('PAYOS_API_KEY'), checksum_key=os.environ.get('PAYOS_CHECKSUM_KEY'))
