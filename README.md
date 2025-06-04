# CEPiK Vehicle History Client

A Python client for retrieving vehicle history data from the Polish government's historiapojazdu.gov.pl service (CEPiK - Centralna Ewidencja Pojazdów i Kierowców).

## Description

This repository contains a Python library that provides programmatic access to vehicle history information from the CEPiK database. The client handles session management, authentication, and data retrieval for both technical vehicle data and timeline/history information.

## Features

- **Session Management**: Automatic creation and management of authenticated sessions with moj.gov.pl
- **Vehicle Technical Data**: Retrieve detailed technical specifications and current vehicle information
- **Timeline Data**: Access complete vehicle history including ownership changes, registrations, and other events
- **Context Manager**: Convenient `authenticated_session()` context manager for automatic session cleanup
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Session Cleanup**: Proper session closure to prevent conflicts between executions

## Requirements

- Python 3.13+
- PyPI

## Installation

You can install the client using pip:

```bash
pip install cepik-vehicle-history-client
```

## Usage

To use the client, you need three pieces of information about the vehicle:
- Registration number (license plate)
- VIN
- First registration date

### Basic Example with Context Manager (Recommended)

```python
from cepik_vehicle_history_client import VehicleHistoryClient, VehicleInfo

# Create vehicle info object
vehicle_info = VehicleInfo(
    registration_number="ABC12345",
    vin="1234567890ABCDEFG",
    first_registration_date="2020-01-15"
)

# Use context manager for automatic session management
client = VehicleHistoryClient()

try:
    with client.authenticated_session() as session:
        # Get vehicle technical data
        vehicle_data = session.get_vehicle_data(vehicle_info)
        print("Vehicle Data:", vehicle_data)
        
        # Get vehicle timeline/history
        timeline_data = session.get_timeline_data(vehicle_info)
        print("Timeline Data:", timeline_data)
        
except Exception as e:
    print(f"Error: {e}")
```

### Manual Session Management

```python
from cepik_vehicle_history_client import VehicleHistoryClient, VehicleInfo

# Create client and vehicle info
client = VehicleHistoryClient()
vehicle_info = VehicleInfo(
    registration_number="ABC12345",
    vin="1234567890ABCDEFG",
    first_registration_date="2020-01-15"
)

try:
    # Manual session creation and authentication
    client.create_session()
    client.authenticate_session()
    
    # Get vehicle data
    vehicle_data = client.get_vehicle_data(vehicle_info)
    print("Vehicle Data:", vehicle_data)
    
    # Get timeline data
    timeline_data = client.get_timeline_data(vehicle_info)
    print("Timeline Data:", timeline_data)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Always close the session
    client.close_session()
```

## API Reference

### Classes

#### `VehicleInfo`
A dataclass containing vehicle identification information.

**Attributes:**
- `registration_number` (str): Vehicle registration number (license plate)
- `vin` (str): Vehicle Identification Number
- `first_registration_date` (str): First registration date in YYYY-MM-DD format

#### `VehicleHistoryClient`
Main client class for accessing the CEPiK vehicle history service.

### Methods

#### `create_session() -> dict[str, str]`
Creates a new session with the moj.gov.pl service and retrieves necessary cookies.

#### `authenticate_session() -> tuple[dict[str, str], str]`
Authenticates the session and returns updated cookies along with the session ID (NF_WID).

#### `get_vehicle_data(vehicle_info: VehicleInfo) -> dict`
Retrieves technical vehicle data including specifications, current status, and registration details.

#### `get_timeline_data(vehicle_info: VehicleInfo) -> dict`
Retrieves historical timeline data showing the vehicle's registration history, ownership changes, and other events.

#### `close_session() -> None`
Properly closes the session to free up resources on the server.

#### `authenticated_session()` (Context Manager)
Context manager that automatically handles session creation, authentication, and cleanup.

### Exceptions

#### `VehicleHistoryClientError`
Base exception class for all client-related errors.

## Data Format

The service returns data in Polish. Common fields include:
- **Vehicle Data**: Technical specifications, current registration status, vehicle category
- **Timeline Data**: Chronological history of registrations, ownership transfers, inspections

## Important Notes

- This client accesses a Polish government service - use it responsibly and in accordance with their terms of service and local law
- The service may have rate limiting - avoid making excessive requests
- **Always** ensure sessions are properly closed (use the context manager when possible)
- Vehicle data requires accurate input - incorrect VIN, registration number, or date will result in no data

## Legal and Ethical Use

This tool is intended for legitimate purposes, e.g.:
- Vehicle purchase verification
- Fleet management
- Insurance verification

Please ensure you have proper authorisation to access vehicle information and comply with Polish data protection laws.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and legitimate business purposes. Users are responsible for ensuring compliance with applicable laws and the terms of service.

## Disclaimer

This is an unofficial client for the Polish government's vehicle history service. The authors are not affiliated with the Polish Government or the CEPiK system. Use at your own risk and ensure compliance with all applicable laws and regulations.
