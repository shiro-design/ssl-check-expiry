import ssl
import sys
import datetime
import socket

def ssl_expiry_date(domain):
    try:
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain,
        )
        conn.settimeout(3.0)
        conn.connect((domain, 443))
        ssl_info = conn.getpeercert()
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    except ssl.SSLError as e: 
        print(f"Error: {e} for {domain}")
        sys.exit(0)
    except socket.gaierror as e:
        print(f"Error: {e} for {domain}")
        sys.exit(0)


if __name__ == '__main__':
    endpoints = sys.argv[1:]
    
    
    if len(endpoints):
        num_of_end = len(endpoints)
        print(f"Checking {num_of_end} endpoints")
        for endpoint in endpoints:
            ssl_expiry_date(endpoint)
            expiry_date = ssl_expiry_date(endpoint)
            current_date = datetime.datetime.now()

            left_day = str(expiry_date - current_date).split(',', 1)[0]
            if expiry_date < current_date:
                print(f"The SSL certificate for {endpoint} has expired on {expiry_date}")
            else:
                print(f"The SSL certificate for {endpoint} will expire on {left_day}")