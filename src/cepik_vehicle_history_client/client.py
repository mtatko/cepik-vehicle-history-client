import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

import requests
import platform

class VehicleHistoryClientError(Exception):
    """Base exception class for all client-related errors."""
    pass

@dataclass
class VehicleInfo:
    """A dataclass containing vehicle identification information."""
    registration_number: str
    vin: str
    first_registration_date: str

class VehicleHistoryClient:
    """ A client for accessing the CEPiK vehicle history service."""
    def __init__(self):
        self.session = requests.Session()

        self.BASE_URL = "https://moj.gov.pl"
        self.APP_NAME = "HistoriaPojazdu"
        self.API_VERSION = "1.0.17"

        self.nf_wid: Optional[str] = None
        self.cookies: Optional[dict[str, str]] = None

        self.__setup_session_headers()

    def __setup_session_headers(self):
        self.session.headers.update({
            "Accept-Language": "pl-PL,pl;q=0.9",
            "User-Agent": f"cepik-vehicle-history-client/0.1.1; Python/{platform.python_version()}",
            })

    @staticmethod
    def _get_current_time_ms():
        """Get the current time since the epoch in milliseconds."""
        return int(round(time.time() * 1000))

    def __make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise VehicleHistoryClientError(f"Request failed: {e}")

    def create_session(self):
        """Creates a new session with the moj.gov.pl service and retrieves necessary cookies."""
        url = f"{self.BASE_URL}/uslugi/engine/ng/index?xFormsAppName={self.APP_NAME}"

        res = self.__make_request("GET", url)
        if res.status_code != 200:
            raise VehicleHistoryClientError("Failed to create session")

        self.cookies = res.cookies.get_dict()

        if not self.cookies:
            raise VehicleHistoryClientError("No cookies have been received from the server while creating a session.")

        return self.cookies

    def authenticate_session(self):
        """Authenticates the session and returns updated cookies along with the session ID (NF_WID)."""
        if not self.cookies:
            raise VehicleHistoryClientError("A session must be created before authentication.")

        current_time = self._get_current_time_ms()
        self.nf_wid = f"{self.APP_NAME}:{current_time}"

        url = f"{self.BASE_URL}/uslugi/engine/ng/index?xFormsAppName={self.APP_NAME}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = f"NF_WID={self.nf_wid}"

        res = self.__make_request("POST", url, headers=headers, cookies=self.cookies, data=data)

        if res.status_code != 200:
            raise VehicleHistoryClientError("Failed to authenticate session")

        new_cookies = res.cookies.get_dict()
        self.cookies.update(new_cookies)

        return self.cookies, self.nf_wid

    def close_session(self) -> None:
        """Properly closes the session to free up resources on the server."""
        if not self.cookies or not self.nf_wid:
            raise VehicleHistoryClientError("Session was not properly initialized.")

        url = f"{self.BASE_URL}/nforms/api/{self.APP_NAME}/{self.API_VERSION}/close"

        headers = {
            "Content-Type": "application/json, text/plain, */*",
            "Nf_wid": self.nf_wid,
            }

        self.__make_request("GET", url, headers=headers, cookies=self.cookies)
        self.cookies = None
        self.nf_wid = None
        self.session.close()

    def __make_api_request(self, endpoint: str, vehicle_info: VehicleInfo):
        if not self.cookies or not self.nf_wid:
            raise VehicleHistoryClientError("Session was not properly authenticated.")

        if "XSRF-TOKEN" not in self.cookies:
            raise VehicleHistoryClientError("Missing XSRF-TOKEN. Ensure session is authenticated.")

        url = f"{self.BASE_URL}/nforms/api/{self.APP_NAME}/{self.API_VERSION}/data/{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "X-Xsrf-Token": self.cookies["XSRF-TOKEN"],
            "Nf_wid": self.nf_wid,
        }

        data = {
            "registrationNumber": vehicle_info.registration_number,
            "VINNumber": vehicle_info.vin,
            "firstRegistrationDate": vehicle_info.first_registration_date,
        }

        res = self.__make_request("POST", url, headers=headers, cookies=self.cookies, json=data)

        return res.json()

    def get_vehicle_data(self, vehicle_info: VehicleInfo):
        """Retrieves technical vehicle data including specifications, current status, and registration details."""
        response = self.__make_api_request("vehicle-data", vehicle_info)

        if "technicalData" not in response:
            raise VehicleHistoryClientError("Invalid response format: 'technicalData' not found.")

        return response

    def get_timeline_data(self, vehicle_info: VehicleInfo):
        """Retrieves historical timeline data showing the vehicle's registration history, ownership changes, and other events."""
        response = self.__make_api_request("timeline-data", vehicle_info)

        if "timelineData" not in response:
            raise VehicleHistoryClientError("Invalid response format: 'timelineData' not found.")

        return response

    @contextmanager
    def authenticated_session(self):
        """Context manager that automatically handles session creation, authentication, and cleanup."""
        try:
            self.create_session()
            self.authenticate_session()
            yield self
        finally:
            if self.cookies and self.nf_wid:
                try:
                    self.close_session()
                except Exception as e:
                    print(f"Warning: Failed to close session: {e}")