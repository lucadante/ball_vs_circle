
import socket
import ipaddress
import time
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(200, 200, 500, 500)
    window.setWindowTitle("IP Port Scanner")

    layout = QVBoxLayout()

    label = QLabel("Enter target information below") 
    input_ip = QTextEdit()
    input_start_port = QTextEdit()
    input_end_port = QTextEdit()
    checkbox = QCheckBox()
    button = QPushButton("Scan Ports")
    

    layout.addWidget(label)
    layout.addWidget(checkbox)
    checkbox.setText("Banner grab?")
    layout.addWidget(input_ip)
    input_ip.setPlaceholderText("Enter IP Address Here")
    layout.addWidget(input_start_port)
    input_start_port.setPlaceholderText("Enter Port Lower Limit Here")
    layout.addWidget(input_end_port)
    input_end_port.setPlaceholderText("Enter Port Upper Limit Here")

    layout.addWidget(button)

    window.setLayout(layout)

    button.clicked.connect(lambda : initiate_scan(input_start_port.toPlainText(), input_end_port.toPlainText(), input_ip.toPlainText()))
    checkbox.clicked.connect(lambda : activate_grab_banner())


    window.show()
    app.exec_()



def display_results(msg):
    message = QMessageBox()
    if len(msg) == 0:
        message.setText("No open ports found")
    else:
        message.setText(f"The ports open for the IP you entered are: {msg}")
    message.exec_()



def get_service_name(port):
    try:
        service = socket.getservbyport(port)
        return service
    except:
        return "Unknown service"
user_wants_banner = None
def activate_grab_banner():
    print("Grab banner activated")
    global user_wants_banner
    user_wants_banner = True

def grab_banner(target, port):
    if user_wants_banner == True:
        try:
            sock = socket.socket()
            sock.connect((target, port))
            sock.settimeout(1)
            banner = sock.recv(1024).decode().strip()
            return banner
        except:
            return "No banner"
    else:
        return "N/A"
    

def scan_port(target, port):
    try:
        # Create a new socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout so it doesn't hang
        socket.setdefaulttimeout(1)
        # Try to connect to the port
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open, service: {get_service_name(port)}, banner: {grab_banner(target,port)}")
            sock.close()
            return port
        sock.close()
        return None
    except socket.error as e:
        print(f"Error scanning port {port}: {e}")

def scan_range(start_port, end_port, target):
    for i in range(start_port, end_port + 1):
        result = scan_port(target, i)
        if result is not None:
            collect_port(result)

ports_list = []
def collect_port(port):
    ports_list.append(port)

def thread_assignment(start_port, end_port, thread_count):
    chunk = end_port - start_port
    chunk_size = chunk // thread_count
    port_ranges = []
    for i in range(thread_count):
        if i == thread_count - 1:
            start = start_port + chunk_size * i
            end = end_port
            port_ranges.append((start, end))
        else:
            start = start_port + chunk_size * i
            end = start + chunk_size - 1
            port_ranges.append((start,end))
    return port_ranges
        

def initiate_scan(start_port, end_port, target):
    # Dealing with no input
    if target == '':
        target = "127.0.0.1"
        print(f"No IP entered, defaulted to {target}")
    try:
        # Validate the IP address
        ip = ipaddress.ip_address(target)
    except ValueError as e:
        print(f"Invalid IP input: {e}")
        return
    
    # No value entered, default to:
    if start_port == '':
        start_port = 0
    if end_port == '':
        end_port = 1023 
    try:
        # Convert ports to integers
        start_port = int(start_port)
        end_port = int(end_port)
        # Validate port range
        if start_port < 0 or start_port > 49152 or end_port < 0 or end_port > 49152:
            raise ValueError("Port range must be between 0 and 49152")
        if end_port < start_port:
            raise ValueError("End port must be greater than start port")
    except ValueError as e:
        print(f"Invalid port input: {e}")
        return  # Exit function on invalid input
    
    print(f"Scanning {target}...")   

    # Iterate through ports 
    start_time = time.time()
    threads = []
    thread_count = 1000
    port_ranges = thread_assignment(start_port, end_port, thread_count)
    ## incomplete
    for start, end in port_ranges:
        t = threading.Thread(target = scan_range, args=(start, end, target))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


    print(f"the port list has this: {ports_list}")
    display_results(ports_list)
    end_time = time.time()

    print(f"Time to scan {end_port - start_port} ports was {end_time-start_time}")

if __name__ == "__main__":
    main()
    