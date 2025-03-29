import serial
import time
import re
import threading

# Serial port configuration for the SIM900 module.
SERIAL_PORT = '/dev/ttyS0'
BAUD_RATE = 9600

# SMS message to be sent.
SMS_MESSAGE = ("You have been granted 5 minutes of free signal. "
               "If you are lost, use this to call Emergency Services.")

# Keep track of phone numbers that have already been served.
served_numbers = set()

def init_sim900(ser):
    """
    Initializes the SIM900 module:
      - Tests communication with an AT command.
      - Sets SMS mode to text.
      - Enables Caller ID notification (CLIP) to receive incoming caller numbers.
    """
    # Flush any existing data.
    ser.flushInput()
    
    # Test communication.
    ser.write(b'AT\r')
    time.sleep(1)
    response = ser.read(ser.inWaiting())
    print("AT response:", response.decode('utf-8', errors='ignore'))
    
    # Set SMS text mode.
    ser.write(b'AT+CMGF=1\r')
    time.sleep(1)
    response = ser.read(ser.inWaiting())
    print("CMGF response:", response.decode('utf-8', errors='ignore'))
    
    # Enable caller ID (CLIP) notifications.
    ser.write(b'AT+CLIP=1\r')
    time.sleep(1)
    response = ser.read(ser.inWaiting())
    print("CLIP response:", response.decode('utf-8', errors='ignore'))

def send_sms(ser, phone_number, message):
    """
    Sends an SMS to the specified phone number using the SIM900 module.
    It waits for the prompt ('>') indicating readiness for the message text
    and terminates the message with the Ctrl+Z character.
    """
    command = f'AT+CMGS="{phone_number}"\r'
    ser.write(command.encode())
    time.sleep(1)
    
    # Read until we receive the '>' prompt.
    prompt = ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
    if '>' not in prompt:
        print("Did not receive prompt for SMS text. Received:", prompt)
    else:
        print("Received prompt for SMS text.")

    # Send the SMS text and terminate with Ctrl+Z (ASCII 26).
    ser.write(message.encode() + b'\x1A')
    print(f"Sending SMS to {phone_number}...")
    
    # Wait for the module to process and return a confirmation.
    time.sleep(3)
    response = ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
    print("SMS send confirmation:", response)

def monitor_serial(ser):
    """
    Continuously monitors the SIM900 serial interface for unsolicited messages.
    It looks for connection events signaled by 'RING' and extracts caller ID
    information from 'CLIP:' messages.
    """
    buffer = ""
    while True:
        try:
            if ser.inWaiting() > 0:
                data = ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
                buffer += data
                # Process complete lines.
                lines = buffer.split("\r\n")
                buffer = lines[-1]  # Incomplete line remains.
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        print("Unsolicited:", line)
                        process_unsolicited(line, ser)
            else:
                time.sleep(0.1)
        except Exception as e:
            print("Error reading from serial port:", e)
            time.sleep(1)

def process_unsolicited(message, ser):
    """
    Processes unsolicited messages from the SIM900 module. Specifically, it
    looks for the 'RING' event and then for a 'CLIP:' message containing the
    caller's phone number.
    """
    # Detect incoming call notification.
    if "RING" in message:
        print("Incoming call detected. Awaiting caller ID info...")
    # Detect Caller ID info.
    if "CLIP:" in message:
        # Example CLIP message format: CLIP: "+1234567890",145,"",,"",0
        match = re.search(r'\"(\+\d+)\"', message)
        if match:
            phone_number = match.group(1)
            print("Detected caller number:", phone_number)
            # Ensure we only serve a phone once.
            if phone_number not in served_numbers:
                served_numbers.add(phone_number)
                send_sms(ser, phone_number, SMS_MESSAGE)
            else:
                print(f"Phone number {phone_number} has already been served.")
        else:
            print("Failed to parse phone number from CLIP message.")

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print("Failed to open serial port:", e)
        return
    
    print("Initializing SIM900 module...")
    init_sim900(ser)
    print("SIM900 initialized. Now listening for connection requests...")
    
    # Start a separate thread to continuously monitor unsolicited messages.
    thread = threading.Thread(target=monitor_serial, args=(ser,))
    thread.daemon = True
    thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        ser.close()

if __name__ == '__main__':
    main()
