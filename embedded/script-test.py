import serial
import time
import threading

VIRTUAL_PORT = '/dev/pts/4'  # Change to the appropriate port from socat

def sim900_simulator():
    try:
        ser = serial.Serial(VIRTUAL_PORT, 9600, timeout=1)
        print("SIM900 Simulator running on", VIRTUAL_PORT)
        while True:
            # Simulate a response for an AT command, if any command is received.
            if ser.inWaiting():
                data = ser.read(ser.inWaiting())
                print("Simulator received:", data.decode('utf-8', errors='ignore'))
                # If it is an AT command, send a generic OK response.
                ser.write(b'OK\r\n')
            
            # Periodically simulate an incoming call:
            time.sleep(10)  # wait 10 seconds between simulations
            print("Simulator: Sending unsolicited RING message")
            ser.write(b'RING\r\n')
            time.sleep(1)
            print("Simulator: Sending unsolicited CLIP message")
            ser.write(b'CLIP: "+1234567890",145,"",,"",0\r\n')
    except Exception as e:
        print("Simulator error:", e)

if __name__ == '__main__':
    sim_thread = threading.Thread(target=sim900_simulator)
    sim_thread.daemon = True
    sim_thread.start()

    # Keep the simulator running.
    while True:
        time.sleep(1)
