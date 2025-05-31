# CEPIK Vehicle History Client

A Python client for retrieving vehicle history data from the Polish government's historiapojazdu.gov.pl service (CEPIK - Centralna Ewidencja Pojazdów i Kierowców).

## Description

This repository contains a Python library that provides programmatic access to vehicle history information from the CEPiK database. The client handles session management, authentication, and data retrieval for both technical vehicle data and timeline/history information.

## Features

- **Session Management**: Automatic creation and management of authenticated sessions with moj.gov.pl
- **Vehicle Technical Data**: Retrieve detailed technical specifications and current vehicle information
- **Timeline Data**: Access complete vehicle history including ownership changes, registrations, and other events
- **Session Cleanup**: Proper session closure to prevent conflicts between executions

## Requirements

- Python 3.7+
- `requests` library
- `json` (built-in)
- `time` (built-in)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mtatko/cepik-vehicle-history-client.git
cd cepik-vehicle-history-client
```

2. Install required dependencies:
```bash
pip install requests
```

## Usage

To use the client, you need three pieces of information about the vehicle:
- Registration number (license plate)
- VIN number
- First registration date

### Basic Example

```python
from cepik_client import create_session, authenticate_session, get_vehicle_data, get_timeline_data, close_session

# Create and authenticate session
session = create_session()
session, nf_wid = authenticate_session(session)

# Vehicle information
registration_number = "ABC12345"
vin_number = "1234567890ABCDEFG"
first_registration_date = "2020-01-15"

try:
    # Get vehicle technical data
    vehicle_data = get_vehicle_data(session, nf_wid, registration_number, vin_number, first_registration_date)
    print("Vehicle Data:", vehicle_data)
    
    # Get vehicle timeline/history
    timeline_data = get_timeline_data(session, nf_wid, registration_number, vin_number, first_registration_date)
    print("Timeline Data:", timeline_data)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Always close the session
    close_session(session, nf_wid)
```

## API Functions

### `create_session() -> dict`
Creates a new session with the moj.gov.pl service and retrieves necessary cookies.

### `authenticate_session(session) -> tuple[dict, str]`
Authenticates the session and returns updated cookies along with the session ID (NF_WID).

### `get_vehicle_data(session, nfwid, registration_number, vin_number, first_registration_date) -> dict`
Retrieves technical vehicle data including specifications, current status, and registration details.

### `get_timeline_data(session, nfwid, registration_number, vin_number, first_registration_date) -> dict`
Retrieves historical timeline data showing the vehicle's registration history, ownership changes, and other events.

### `close_session(session, nfwid) -> None`
Properly closes the session to free up resources on the server.

## Data Format

The service returns data in Polish. Common fields include:
- **Vehicle Data**: Technical specifications, current registration status, vehicle category
- **Timeline Data**: Chronological history of registrations, ownership transfers, inspections

## Important Notes

- This client accesses a Polish government service - use it responsibly and in accordance with their terms of service and local law
- The service may have rate limiting - avoid making excessive requests
- **Always** ensure sessions are properly closed using `close_session()`
- Vehicle data requires accurate input - incorrect VIN, registration number, or date will result in no data

## Legal and Ethical Use

This tool is intended for legitimate purposes, e.g.:
- Vehicle purchase verification
- Fleet management

Please ensure you have proper authorization to access vehicle information and comply with Polish data protection laws.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and legitimate business purposes. Users are responsible for ensuring compliance with applicable laws and terms of service.

## Disclaimer

This is an unofficial client for the Polish government's vehicle history service. The authors are not affiliated with the Polish Government or the CEPiK system. Use at your own risk and ensure compliance with all applicable laws and regulations.