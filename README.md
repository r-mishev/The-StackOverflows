# SkyGuardian - When Signals Fail, We Prevail

SkyGuardian is a proof-of-concept (PoC) project designed to save lives when traditional communication networks fail. When a person is lost in remote areas such as dense forests without cellular coverage, SkyGuardian deploys drones equipped with temporary, low-power cellular base stations. This system provides a short window (e.g., 3-5 minutes) of connectivity, allowing stranded individuals to send an emergency SMS or call for help.

## Project Overview

SkyGuardian leverages a combination of hardware and software to create a life-saving network:
- **Drone Platform:** Drones equipped with GPS, autonomous flight capabilities, and payload capacity carry the communication module.
- **Embedded Communication Module:** A module acts as a temporary cellular base station. The module automatically detects connection attempts and sends an SMS notification to the connected phone.
- **Backend Services:** A lightweight backend system (located in the `app` directory) handles emergency data processing and logging.
- **Frontend Dashboard:** A web interface (located in the `web` directory) monitors drone status, connectivity, and emergency notifications.

## How It Works

1. **Deployment:**  
   A drone is deployed over a forest area. Its onboard communication module creates a localized cellular network.
   
2. **Connection & Notification:**  
   When a stranded phone connects to this network, the module automatically sends an SMS:
   > "You have been granted 5 minutes of free signal. If you are lost, use this to call Emergency Services."
   
3. **Emergency Integration:**  
   The system can further send location data and connection details to a backend endpoint for coordinated rescue efforts.

## Project Structure

The repository is organized as a monorepo with the following directories:
- **app/** – Contains the backend code.
- **web/** – Contains the frontend application.
- **embedded/** – Contains embedded code, including:
  - Drone control scripts.
  - Module integration code.
  - Unit tests and simulation scripts.

## Embedded PoC

The embedded folder includes:
- **controller.py:**  
  Code that interfaces with the module. It handles initialization, listens for connection events, sends SMS messages, and triggers an HTTP endpoint.
- **Unit Tests:**  
  A suite of tests using `unittest` and `unittest.mock` to simulate serial communication and ensure system reliability.
- **Simulation Tools:**  
  Virtual serial port emulators and mock scripts allow testing without actual hardware.

## Deployment

The project is deployed on the **Render** platform.
- **Frontend Deployment:**  
  Located in the repository root, it checks out the code, sets up Node.js, installs dependencies, builds the project, and deploys.
- **Backend Deployment:**  
  Located in the repository root, it checks out the code, sets up Uvicorn, installs the requirements, and deploys.

## Getting Started

### Prerequisites

- **Node.js** (v23 recommended for frontend development)
- **Python 3.10+** (for embedded scripts and tests)
- **Module** (or virtual serial port setup for testing)
- **Drone Hardware** (for real-world deployment)

### Running the Backend/Embedded Code

1. Navigate to the `embedded` directory.
2. Run the controller script:
```bash
   python3 controller.py <serial_port>
```
Replace `<serial_port>` with your actual device or virtual port path.

### Running Unit Tests
From the `embedded` directory, run:
```bash
    python3 -m unittest discover -s tests
```

## License
This project is licensed under the MIT license.