import serial
import time

# Configuration for the serial port connected to the SIM900 module.
SERIAL_PORT = '/dev/ttyS0'
BAUD_RATE = 9600

# SMS message to be sent.
SMS_MESSAGE = ("You have been granted 5 minutes of free signal."
               "If you are lost, use this to call Emergency Services.")

def init_sim900(ser):
    """Initializes the SIM900 module by sending basic AT commands."""
    # Test communication with the SIM900 module.
    ser.write(b'AT\r')
    time.sleep(1)
    response = ser.read(ser.inWaiting())
    print("Response to AT:", response.decode('utf-8', errors='ignore'))
    
    # Set SMS mode to text.
    ser.write(b'AT+CMGF=1\r')
    time.sleep(1)
    response = ser.read(ser.inWaiting())
    print("Set SMS text mode response:", response.decode('utf-8', errors='ignore'))

def send_sms(ser, phone_number, message):
    """Sends an SMS to the specified phone number."""
    # Start SMS sending command.
    command = f'AT+CMGS="{phone_number}"\r'
    ser.write(command.encode())
    time.sleep(1)
    
    # Send the message text and signal end-of-message with Ctrl+Z (ASCII 26).
    ser.write(message.encode() + b'\x1A')
    print("SMS command sent, waiting for confirmation...")
    
    # Wait and then read the module's response.
    time.sleep(3)
    response = ser.read(ser.inWaiting())
    print("SMS send response:", response.decode('utf-8', errors='ignore'))

def main():
    # Open the serial connection to the SIM900 module.
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print("Error opening serial port:", e)
        return
    
    print("Initializing SIM900 module...")
    init_sim900(ser)
    
    print("SIM900 initialized and ready.")
    print("Drone broadcasting message: 'Connect to our network for 5 minutes of free signal!'")
    print("Waiting for phone connection (simulate by pressing Enter)...")
    
    # Simulate a connection event.
    input("Press Enter to simulate a phone connection event...")
    
    # For demonstration, we use a dummy phone number.
    dummy_phone_number = "+1234567890"
    print(f"Detected phone connection from {dummy_phone_number}. Sending SMS...")
    
    send_sms(ser, dummy_phone_number, SMS_MESSAGE)
    
    print("Demo complete. Closing serial connection.")
    ser.close()

if __name__ == '__main__':
    main()
