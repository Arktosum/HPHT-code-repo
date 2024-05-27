import serial
import serial.tools.list_ports
import csv
import time
def list_active_com_ports():
    ports = serial.tools.list_ports.comports()
    active_ports = []
    for port, desc, hwid in sorted(ports):
        active_ports.append(port)
    return active_ports

SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200  

def read_from_serial(serial_port, baud_rate):
    ser = serial.Serial(serial_port, baud_rate)
    ser.flushInput()
    return ser

def write_to_csv(file_name, data):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    serial_port = SERIAL_PORT
    active_ports =  list_active_com_ports()
    
    if serial_port not in active_ports:
        print(serial_port,'not in active ports!')
        return
    
    print("Found serial port " + serial_port)
    print('-------------- STARTING EXPORT -----------------')
    baud_rate = BAUD_RATE
    file_name = 'serial_data.csv'
    ser = read_from_serial(serial_port, baud_rate)
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                data = line.split(',')  # Assuming the serial data is comma-separated
                write_to_csv(file_name, data)
                print(f"Written to CSV: {data}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
