import serial.tools.list_ports

def find_xbee_port():
    # List available serial ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Check for XBee keyword in the port description (adjust condition if needed)
        if 'XBee' in port.description or 'XB' in port.description:
            return port.device
    return None

if __name__ == "__main__":
    port = find_xbee_port()
    if port:
        print(f"Found XBee on port: {port}")
    else:
        print("No XBee device found.")
