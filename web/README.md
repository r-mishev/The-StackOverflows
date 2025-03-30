# SkyGuardian Web

The **SkyGuardian Web** project is the frontend component of the SkyGuardian. This web application serves as the user dashboard and monitoring interface, allowing operators to view drone statuses, connectivity logs, and emergency notifications.

## Overview

When a drone equipped with a temporary cellular base station is deployed over remote areas, the web interface displays real-time information about:
- **Connectivity Logs:** When and which devices have connected to the temporary network.
- **Emergency Notifications:** Alerts from the embedded module when a user connects.

This interface is built using React, TypeScript, Next.js, and Tailwind CSS and leverages a responsive design to ensure accessibility from both desktop and mobile devices.

## Project Structure

The `web/` directory contains all source code related to the frontend:
- **src/**: Source code for the application.
  - **components/**: Reusable UI components.
  - **pages/**: Page components for different routes (e.g., dashboard, logs).
  - **services/**: API services for interacting with backend endpoints.
- **public/**: Static assets such as images and styles.
- **package.json**: Project metadata and dependency configuration.

## Getting Started

### Prerequisites

- **Node.js** (v16 or later is recommended)
- **npm**

### Installation

1. Navigate to the `web/` directory:
```bash
   cd web/
```
2. Install the dependencies:
```bash
    npm install
```

### Development

To start the development server with hot reloading:
```bash
npm run dev
```
This command launches the application on a local development server.
