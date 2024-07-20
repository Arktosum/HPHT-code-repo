def list_active_com_ports():
    ports = serial.tools.list_ports.comports()
    active_ports = []
    for port, desc, hwid in sorted(ports):
        active_ports.append(port)
    return active_ports