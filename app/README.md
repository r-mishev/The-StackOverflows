# SkyGuardian App

The **SkyGuardian App** is the backend component of the SkyGuardian project. It processes emergency data received from drones deployed with temporary cellular base stations, logs connection events, and provides RESTful API endpoints for the SkyGuardian Web dashboard. This backend helps coordinate rescue operations and serves as the central hub for managing and monitoring emergency connectivity events.

## Overview

When a drone is deployed over remote areas, its embedded system (via the module) sends data such as connection events and location information to the SkyGuardian App. The app processes these events, logs them, and exposes API endpoints for real-time monitoring. In addition, it can trigger integrations with external emergency services.

## Features

- **RESTful API Endpoints:**  
  Provides endpoints for retrieving, connection logs, and emergency notifications.
- **Data Logging:**  
  Logs events from the embedded system to enable historical analysis and real-time monitoring.
- **Rescue Coordination:**  
  Integrates with external services to help coordinate emergency response when a connection event is detected.
- **Scalable Architecture:**  
  Designed to handle multiple simultaneous events and scale with demand.

## Project Structure

The `app/` directory includes the following:

- **routers**: Routes for the application.
  - **detection.py**: Routes for person detection.
  - **ws.py**: Websocket client.
- **firebase.py**: Firebase controller file.
- **models.py**: Database models.
- ...s

## Prerequisites

- **Python** (v3.12 or later recommended)
- **pip** for dependency management
- **Firebase Account**
- **Environment Variables**

## Installation

1. **Clone the Repository**
```bash
   git clone https://github.com/yourusername/skyguardian.git
```
2. **Navigate to the App Directory**
```bash
    cd the-stackoverflows/app
```
3. **Activate the venv**
```bash
python3 -m venv .venv

./.venv/bin/activate
```
4. **Install dependencies**
```bash
./.venv/bin/pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the `app/` directory with the necessary environment variables.

## Running the Server
To start the server in development mode:
```bash
uvicorn app.main:app 00host 127.0.0.1 --port 8000 --reload
```

## License
This project is licensed under the MIT license.