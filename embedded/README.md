# SkyGuardian Embedded

The **SkyGuardian Embedded** project is the heart of our emergency connectivity solution—designed to operate on drones and other remote platforms. This folder contains all the embedded code that runs on devices (such as Raspberry Pi) to create temporary, low-power cellular base stations in areas where traditional signals fail.

## Overview

When conventional communication networks break down in remote areas, the SkyGuardian Embedded system kicks in. Its primary functions include:

- **Drone-Based Connectivity:**  
  Operating on a drone, the system creates a localized cellular network using modules. This network provides stranded users with a limited period of connectivity.

- **Automatic SMS Notification:**  
  Upon detecting a connection (e.g., via an incoming call or connection event), the system automatically sends an SMS to the connecting device with critical instructions.

- **Emergency Data Handling:**  
  The module triggers an HTTP endpoint to register connection events and location data, aiding in rescue coordination.

## Key Components

- **controller.py:**  
  Main code that initializes the module, monitors serial communication for connection events, and sends SMS notifications. It also calls a backend endpoint to log emergency events.

- **Unit Tests:**  
  Located in the `tests/` directory, these tests simulate serial communication and verify that the system correctly processes incoming events, sends SMS messages, and triggers external endpoints.

- **Simulation Tools:**  
  Virtual serial port setups and mocks allow testing of the embedded functionality without requiring actual hardware.

## Prerequisites

- **Python 3.10+**  
- **PySerial:** Used for serial communication with the module.
- **Requests:** For sending HTTP requests to backend endpoints.
- **Drone/Hardware Platform:** (For full deployment) A Raspberry Pi or similar device to run the embedded software, along with the corresponding hardware module.

## Installation

1. **Clone the Repository**
```bash
   git clone https://github.com/yourusername/skyguardian.git
```
2. **Navigate to the Embedded Directory**
```bash
    cd the-stackoverflows/embedded/
```
3. **Install the dependency**
```bash
    ./.venv/bin/pip install pyserial
```

## Running the Embedded Code
To start the embedded code on your device (e.g. Raspberry Pi), run:
```bash
    python3 controller.py <serial_port>
```
Replace `<serial_port>` with the correct serial port path (e.g. `/dev/ttyS0` or a virtual serial port for testing).

## Testing
Unit tests for the embedded system can be executed from the embedded directory:
```bash
python3 -m unittest discover -s tests
```
These tests simulate module responses, serial communication events, and validate the proper functioning of the SMS notification and HTTP endpoint triggering.

## Architecture
![Architecture](https://www.plantuml.com/plantuml/dpng/ZP7DRjGm58NtVeehRvWHKub2oq-ae8wgg8nWO4HQiQaK6VjEQ-6VoBvf4IkUXWVZIN2SA4EAAh7poVtkEOxFMIGHgBE62Ka-0B-A69v4sDrwXnp4U69jehJKhN04VEjLPuRfS9oFA_iLbK85vzvHyCPWoEn1plbwMqEDuKxBmJFfEV3kyd87bLEjruvwP1ACbILid2OjZFuXI7i7PSaEIN3qThmZ5A0JsDYi5aisVZvAn85F5F_qdaF0s7eNCUQ4D7SeitjrXuxwZFmkC_ir4TgM8f07EMnC8GyohbpqHajDg81_tdoyu60nHd63ZztzYz39UUy3d7_Ox2RwV_pxXGAk-TFZvozEJb--UltcsJLV7P-Shk3tpr-F9C_zgkyKX2Heyq-xBZKSO1-ypRTviDdtMK14fvfeu-BlNBxgfyssgklrHRLaIUG2XiSiyghpfFTQ3cKc5vhRJzqdN0fZ6XprOWdtccx1-75N2H9iel_fUIs_ENzlKDqWODygEqjMdJL_0000)

## Additional Resources
- **[Module Specifications](https://www.espruino.com/datasheets/SIM900_AT.pdf)**
- **[Microcontroller Documentation](https://www.raspberrypi.com/documentation/)**

## License
This project is licensed under the MIT License.
