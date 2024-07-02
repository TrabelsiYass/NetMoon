import mysql.connector
import nmap
import json
import datetime
from scapy.all import ARP, Ether, srp
from pyvis.network import Network
from PySide6.QtWidgets import QTableWidgetItem,QPushButton,QVBoxLayout,QDialog
from PySide6.QtWebEngineWidgets import QWebEngineView



class NetworkDetailsDialog2(QDialog):
    def __init__(self, html_content, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)
        self.webview.setHtml(html_content)
        self.setWindowTitle("Network Details")
        self.resize(400,600)


def scan_network(ip_range):
    try:
        arp_request = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        return devices
    except Exception as e:
        print("Error Occurred during network scanning:", e)
        return []

def nmap_scan(ip_address):
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=ip_address, arguments='-p 1-1024 -sS -O')
        return nm[ip_address]
    except Exception as e:
        print(f"Error occurred during Nmap scan for {ip_address}:", e)
        return {}
    

def create_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='nmap'
    )
    return mydb



def get_Services(device):
    nmap_result = nmap_scan(device)
    if 'osmatch' in nmap_result and nmap_result['osmatch']:
        detected_os = nmap_result['osmatch'][0]['osclass'][0].get('osfamily', 'Unknown')
    else:
        detected_os = 'Unknown'

    device_title = f"OS: {detected_os}\nServices:\n"
    
    if 'tcp' in nmap_result:
        for port, service_info in nmap_result['tcp'].items():
            service_name = service_info.get('name', 'Unknown')
            device_title += f"- Port {port}: {service_name}\n"
    else:
        device_title += f"No Tcp ports scanned on {device}\n"

    return device_title

def scan_press_admin(router_ip):
    try:
        if router_ip == "":
            router_ip = "192.168.1.1"

        ip_range = router_ip + "/24"

        devices = scan_network(ip_range)
        print("devices = ", devices)

        html_content = generate_network_html(devices, router_ip)
            
        return html_content

    except Exception as e:
        print("Error occurred while scanning the network: ", e)


def generate_network_html(devices, router_ip):
    try:
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")

        for device in devices:
            print("Device: ", device)
            device_ip = str(device['ip'])
            mac_address = str(device['mac'])
            services = json.dumps(nmap_scan(device_ip))  # Store services as JSON string
            net.add_node(device_ip, label=device_ip, title=mac_address, color='#FF5733', group="Devices")
            net.add_edge(router_ip, device_ip)

        return net.generate_html()

    except Exception as e:
        print("Error occurred while generating network HTML: ", e)

def scan_press(id_user, router_ip):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT MAX(id_area), MAX(date) FROM area")
        id_area, last_date = cursor.fetchone()

        cursor.execute("SELECT MAX(Id_Scan) FROM scan")
        id_scan = cursor.fetchone()[0]
        if id_scan is None:
            id_scan = 1
        else:
            id_scan += 1

        cursor.execute("SELECT MAX(id_router) FROM routers")
        id_router = cursor.fetchone()[0]
        if id_router is None:
            id_router = 1
        else:
            id_router = int(id_router) + 1

        if router_ip == "":
            router_ip = "192.168.1.1"

        ip_range = router_ip + "/24"

        if datetime.date.today() == last_date :

            cursor.execute("INSERT INTO scan (id_area, Id_Scan, date_scan) VALUES (%s, %s, %s)", (id_area, id_scan, datetime.datetime.now()))
            mydb.commit()

            devices = scan_network(ip_range)
            print("devices = ", devices)

            html_content = insert_data(id_router, id_scan, devices, router_ip, cursor)
            
            return html_content

        else:
            id_area += id_area

            cursor.execute("INSERT INTO area (id_area, id_user, date) VALUES (%s, %s, %s)", (id_area, id_user, datetime.date.today()))
            mydb.commit()

            cursor.execute("INSERT INTO scan (id_area, Id_Scan, date_scan) VALUES (%s, %s, %s)", (id_area, id_scan, datetime.datetime.now()))
            mydb.commit()

            devices = scan_network(ip_range)
            print("devices = ", devices)

            html_content = insert_data(id_router, id_scan, devices, router_ip, cursor)

        return html_content

    except Exception as e:
        print("Error occurred while inserting data into the database: ", e)
        mydb.rollback()
    finally:
        cursor.close()
        mydb.close()

        

def insert_data(id_router,id_scan, devices, router_ip, cursor):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()
        # Insert router IP into routers table
        cursor.execute("INSERT INTO routers (id_router,Id_scan, ip_adress) VALUES (%s,%s, %s)", (str(id_router),id_scan, router_ip))
        mydb.commit()

        print("Data Router inserted successfully.")

        # Increment id_device
        cursor.execute("SELECT MAX(id_device) FROM devices")
        id_device = cursor.fetchone()[0]

        if id_device is None:
            id_device = 1
        else:
            id_device = int(id_device) + 1

        # Insert devices and their services into devices table
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")

        for device in devices:
            print("1 = " , device)
            device_ip = str(device['ip'])
            mac_address = str(device['mac'])
            services = json.dumps(nmap_scan(device_ip))  # Store services as JSON string
            cursor.execute("INSERT INTO devices (id_routeer, id_device, ip_adress_router, ip_adress, mac_adress, services) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(id_router), str(id_device), router_ip, device_ip, mac_address, services))
            mydb.commit()
            id_device += 1
            print('device add')
            net.add_node(device_ip, label=device_ip, title=mac_address, color='#FF5733', group="Devices")
            net.add_edge(router_ip, device_ip)


        return  net.generate_html()


            
        


    except Exception as e:
        print("Error occurred while inserting data into the database: 2 ", e)


    finally:
        cursor.close()
        mydb.close()


def retrieve_data():
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT routers.ip_adress, devices.ip_adress, devices.services FROM routers JOIN scan ON scan.Id_Scan = routers.Id_scan JOIN users ON users.Id_user = scan.id_user JOIN devices ON routers.id_router = devices.id_routeer")
        rows = cursor.fetchall()

        # Group data by router IP address
        router_devices = {}
        for row in rows:
            router_ip = row[0]
            device_ip = row[1]
            services = json.loads(row[2])
            if router_ip not in router_devices:
                router_devices[router_ip] = []
            router_devices[router_ip].append((device_ip, services))

        # Generate graph for each router
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content after processing all routers
        html_content = net.generate_html()
        with open(f"scan_reseau.html", "w") as file:
            file.write(html_content)

    except Exception as e :
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()

def retriving_port(data_dict):
    for port, details in data_dict.get('tcp', {}).items():
        if details.get('state') == 'open':
            first_open_tcp_port = port
            return first_open_tcp_port
        else :
            return -1




def populate_fourth_table(area_ids,table):
        table.clear()

        # Set the column count and headers
        table.setColumnCount(2)  # Adjust the number of columns as needed
        headers = ["Merged Area ID's", "Display"]  # Adjust column headers
        table.setHorizontalHeaderLabels(headers)

        # Set the row count to 1
        table.setRowCount(1)

        # Populate the table with data
        merged_area_id = " ".join(str(id) for id in area_ids)

        # Merged Area ID
        table.setItem(0, 0, QTableWidgetItem(merged_area_id))

        # Button to display merged network
        btn_display_merged_network = QPushButton("Click Here")
        btn_display_merged_network.clicked.connect(lambda: display_merged_network(area_ids))
        table.setCellWidget(0, 1, btn_display_merged_network)

        table.resizeColumnsToContents()

def display_merged_network(area_ids):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        merged_router_devices = {}  # Dictionary to hold merged router devices from all selected scans

        for area_id in area_ids:
            cursor.execute("SELECT routers.ip_adress , devices.ip_adress , devices.services ""FROM scan "
            "JOIN routers ON scan.Id_Scan = routers.Id_scan "
            "JOIN devices ON routers.id_router = devices.id_routeer "
            "WHERE scan.id_area = %s", (area_id,))
            rows = cursor.fetchall()

            # Group data by router IP address for the current scan
            router_devices = {}
            for row in rows:
                router_ip = row[0]
                device_ip = row[1]
                services = json.loads(row[2])
                if router_ip not in router_devices:
                    router_devices[router_ip] = []
                router_devices[router_ip].append((device_ip, services))

            # Merge router devices from the current scan into the merged dictionary
            for router_ip, devices in router_devices.items():
                if router_ip not in merged_router_devices:
                    merged_router_devices[router_ip] = []
                merged_router_devices[router_ip].extend(devices)

        # Generate graph for merged router devices
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in merged_router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content for the merged network
        html_content = net.generate_html()
        with open(f"nmap_network.html", "w") as file:
            file.write(html_content)

        dialog = NetworkDetailsDialog2(html_content)
        dialog.exec()

    except Exception as e:
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()




def populate_third_table(id_scan,table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(4)  # Adjust the number of columns as needed
            headers = ["IP ADRESS ROUTER", "DEVICE IP ADRESS","DEVICE MAC ADRESS","DEVICE SERVICES"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT devices.ip_adress_router,devices.ip_adress,devices.mac_adress,devices.services  FROM scan JOIN routers ON routers.id_scan = scan.id_scan JOIN devices ON devices.id_routeer = routers.id_router  WHERE scan.Id_Scan = %s ", (id_scan,))
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            

        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()



def populate_second_table_admin(user,table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(3)  # Adjust the number of columns as needed
            headers = ["Scan id", "Scan Date","Device Found"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT scan.Id_Scan, scan.date_scan, COUNT(devices.id_device) FROM scan JOIN area ON scan.Id_area = area.Id_area JOIN routers ON scan.Id_scan = routers.Id_scan JOIN devices ON devices.id_routeer = routers.id_router JOIN users ON users.Id_user = area.id_user WHERE users.Username = %s GROUP BY scan.Id_Scan, scan.date_scan", (user,))
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            

        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()





def populate_second_table(id_area,table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(2)  # Adjust the number of columns as needed
            headers = ["Scan id", "Scan Date"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT Id_Scan , date_scan  FROM scan WHERE id_area = %s ", (id_area,))
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            

        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()


def populate_table_users(table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(3)  # Adjust the number of columns as needed
            headers = ["User Pseudo", "User Email", "User Password"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT Username,email,Password FROM users ")
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            


        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()


def populate_table_admin(table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(3)  # Adjust the number of columns as needed
            headers = ["Admin's Pseudo", "Email", "Password"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT * from admin")
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            


        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()



def populate_table_feedback(table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(3)  # Adjust the number of columns as needed
            headers = ["user Pseudo", "feedback", "Date"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT users.Username , feedback.msg , feedback.feed_date from feedback,users WHERE feedback.id_user = users.Id_user")
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            


        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()





def populate_table(id_user,table):
        try :
            mydb = create_connection()
            cursor = mydb.cursor()

            # Clear existing data in the table
            table.clear()

            # Set the column count and headers
            table.setColumnCount(3)  # Adjust the number of columns as needed
            headers = ["Name User", "Area ID", "Scan Date"]  # Adjust column headers
            table.setHorizontalHeaderLabels(headers)

            # Example data to populate the table


            cursor.execute("SELECT users.Username , area.id_area , area.date FROM users JOIN area ON users.Id_user = area.id_user WHERE users.Id_user = %s GROUP BY date", (id_user,))
            data = cursor.fetchall()
            # Set the row count
            table.setRowCount(len(data))

            # Populate the table with data
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))

            table.resizeColumnToContents(1)
            


        except Exception as e :
            print("Error occurred while retrieving data from the database:", e)
        finally:
            cursor.close()
            mydb.close()



def getting_network_one_id(scan_id):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT routers.ip_adress, devices.ip_adress, devices.services FROM routers JOIN scan ON scan.Id_Scan = routers.Id_scan JOIN devices ON routers.id_router = devices.id_routeer WHERE  scan.Id_Scan = %s",(scan_id,))
        rows = cursor.fetchall()

        # Group data by router IP address
        router_devices = {}
        for row in rows:
            router_ip = row[0]
            device_ip = row[1]
            services = json.loads(row[2])
            if router_ip not in router_devices:
                router_devices[router_ip] = []
            router_devices[router_ip].append((device_ip, services))

        # Generate graph for each router
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content after processing all routers
        html_content = net.generate_html()
        with open(f"nmap_network.html", "w") as file:
            file.write(html_content)
        return html_content

    except Exception as e :
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()



def getting_network_multiple_area(area_ids):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        merged_router_devices = {}  # Dictionary to hold merged router devices from all selected scans

        for area_id in area_ids:
            cursor.execute("SELECT routers.ip_adress , devices.ip_adress , devices.services "
               "FROM scan "
               "JOIN routers ON scan.Id_Scan = routers.Id_scan "
               "JOIN devices ON routers.id_router = devices.id_routeer "
               "WHERE scan.id_area = %s", (area_id,))
            rows = cursor.fetchall()

            # Group data by router IP address for the current scan
            router_devices = {}
            for row in rows:
                router_ip = row[0]
                device_ip = row[1]
                services = json.loads(row[2])
                if router_ip not in router_devices:
                    router_devices[router_ip] = []
                router_devices[router_ip].append((device_ip, services))

            # Merge router devices from the current scan into the merged dictionary
            for router_ip, devices in router_devices.items():
                if router_ip not in merged_router_devices:
                    merged_router_devices[router_ip] = []
                merged_router_devices[router_ip].extend(devices)

        # Generate graph for merged router devices
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in merged_router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content for the merged network
        html_content = net.generate_html()
        with open(f"nmap_network.html", "w") as file:
            file.write(html_content)
        return html_content

    except Exception as e:
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()



def getting_network_one_id_area(area_id):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT routers.ip_adress , devices.ip_adress , devices.services "
               "FROM scan "
               "JOIN routers ON scan.Id_Scan = routers.Id_scan "
               "JOIN devices ON routers.id_router = devices.id_routeer "
               "WHERE scan.id_area = %s", (area_id,))
        rows = cursor.fetchall()

        # Group data by router IP address
        router_devices = {}
        for row in rows:
            router_ip = row[0]
            device_ip = row[1]
            services = json.loads(row[2])
            if router_ip not in router_devices:
                router_devices[router_ip] = []
            router_devices[router_ip].append((device_ip, services))

        # Generate graph for each router
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content after processing all routers
        html_content = net.generate_html()
        with open(f"nmap_network.html", "w") as file:
            file.write(html_content)
        return html_content

    except Exception as e :
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()



def getting_network_multiple(scan_ids):
    try:
        mydb = create_connection()
        cursor = mydb.cursor()

        merged_router_devices = {}  # Dictionary to hold merged router devices from all selected scans

        for scan_id in scan_ids:
            cursor.execute("SELECT routers.ip_adress, devices.ip_adress, devices.services FROM routers JOIN scan ON scan.Id_Scan = routers.Id_scan JOIN devices ON routers.id_router = devices.id_routeer WHERE  scan.Id_Scan = %s",(scan_id,))
            rows = cursor.fetchall()

            # Group data by router IP address for the current scan
            router_devices = {}
            for row in rows:
                router_ip = row[0]
                device_ip = row[1]
                services = json.loads(row[2])
                if router_ip not in router_devices:
                    router_devices[router_ip] = []
                router_devices[router_ip].append((device_ip, services))

            # Merge router devices from the current scan into the merged dictionary
            for router_ip, devices in router_devices.items():
                if router_ip not in merged_router_devices:
                    merged_router_devices[router_ip] = []
                merged_router_devices[router_ip].extend(devices)

        # Generate graph for merged router devices
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        for router_ip, devices in merged_router_devices.items():
            net.add_node(router_ip, label=router_ip, color="#33FF57", group="Routers")
            for device_ip, services in devices:
                services_str = json.dumps(services , indent=2)
                net.add_node(device_ip, label=device_ip, title=services_str, color='#FF5733', group="Devices")
                net.add_edge(router_ip, device_ip)

        # Generate HTML content for the merged network
        html_content = net.generate_html()
        with open(f"nmap_network.html", "w") as file:
            file.write(html_content)
        return html_content

    except Exception as e:
        print("Error occurred while retrieving data from the database:", e)
    finally:
        cursor.close()
        mydb.close()

