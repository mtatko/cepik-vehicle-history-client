import requests
import time

s = requests.session()

def get_current_time() -> int:
    """
    Get the current time in milliseconds since the epoch.
    :return: current unix time in milliseconds
    """
    return int(round(time.time() * 1000))

def create_session() -> dict[str, str]:
    """
    This function creates a session with the moj.gov.pl service for vehicle history.
    It retrieves the necessary cookies to start a session.
    :return: A dictionary containing the necessary cookies for the session 'NFJSESSIONID', 'BIGipServer~ePUAP-PRD-SDC~POOL_ORBEON-8080', 'BIGipServerePUAP_PRD_ORBEON-8080' and 'session-MGPRD'.
    :raises Exception: If the session creation fails, an exception is raised with the status code.
    """
    r = s.get("https://moj.gov.pl/uslugi/engine/ng/index?xFormsAppName=HistoriaPojazdu")

    if r.status_code == 200:
        response_cookies = r.cookies.get_dict()
        return response_cookies
    else:
        raise Exception(f"Failed to create session, status code: {r.status_code}")

def authenticate_session(session) -> tuple[dict[str, str], str]:
    """
    This function authenticates the session with the moj.gov.pl service for vehicle history.
    It generates a unique NF_WID (session identifier) based on the current time and sends it to the service.
    :param session: A dictionary containing the session cookies, created by the create_session function.
    :type session: dict[str, str]
    :return: The function returns the updated session cookies and the NF_WID.
    :raises Exception: If the authentication fails, an exception is raised with the status code.
    """
    current_time = get_current_time()
    nfwid = f"HistoriaPojazdu:{current_time}"

    cookies = session

    url = "https://moj.gov.pl/uslugi/engine/ng/index?xFormsAppName=HistoriaPojazdu"

    headers = {
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = f"NF_WID={nfwid}"

    r = s.post(url, headers=headers, cookies=cookies, data=data)

    if r.status_code == 200:
        response_cookies = r.cookies.get_dict()
        for cookie in response_cookies:
            cookies[cookie] = response_cookies[cookie]

        for cookie_key in session.keys():
            if cookie_key not in response_cookies:
                cookies[cookie_key] = session[cookie_key]

        return cookies, nfwid

    else:
        raise Exception(f"Failed to authenticate session, status code: {r.status_code}")

def close_session(session, nf_wid) -> None:
    """
    This function closes the session with the moj.gov.pl service for vehicle history.
    It sends a request to close the session using the NF_WID.
    :param session: A dictionary containing the authenticated session cookies, created by the authenticate_session function.
    :type session: dict
    :param nf_wid: The NF_WID (session identifier) generated during authentication.
    :type nf_wid: str
    :raises Exception: If the session closure fails, an exception is raised with the status code.
    """
    cookies = session

    headers = {
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/json, text/plain, */*",
        "Nf_wid": nf_wid
    }

    url = "https://moj.gov.pl/nforms/api/HistoriaPojazdu/1.0.17/close"

    r = s.get(url, headers=headers, cookies=cookies)

    if r.status_code == 200:
        print("Session closed successfully.")
    else:
        raise Exception(f"Failed to close session, status code: {r.status_code}")

def get_vehicle_data(session, nf_wid, registration_number, vin_number, first_registration_date):
    cookies = session

    headers = {
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/json",
        "X-Xsrf-Token": session["XSRF-TOKEN"],
        "Nf_wid": nf_wid
    }

    url = "https://moj.gov.pl/nforms/api/HistoriaPojazdu/1.0.17/data/vehicle-data"

    data = {
        "registrationNumber": registration_number,
        "VINNumber": vin_number,
        "firstRegistrationDate": first_registration_date
    }

    r = s.post(url, headers=headers, cookies=cookies, json=data)

    if r.status_code == 200:
        response_data = r.json()
        if "technicalData" in response_data:
            return response_data
        else:
            raise Exception("Technical data not found in the response.")
    else:
        raise Exception(f"Failed to get vehicle data, status code: {r.status_code}")

def get_timeline_data(session, nf_wid, registration_number, vin_number, first_registration_date):
    cookies = session

    headers = {
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/json",
        "X-Xsrf-Token": session["XSRF-TOKEN"],
        "Nf_wid": nf_wid
    }

    url = "https://moj.gov.pl/nforms/api/HistoriaPojazdu/1.0.17/data/timeline-data"

    data = {
        "registrationNumber": registration_number,
        "VINNumber": vin_number,
        "firstRegistrationDate": first_registration_date
    }

    r = s.post(url, headers=headers, cookies=cookies, json=data)

    if r.status_code == 200:
        response_data = r.json()
        if "timelineData" in response_data:
            return response_data
        else:
            raise Exception("Timeline data not found in the response.")
    else:
        raise Exception(f"Failed to get timeline data, status code: {r.status_code}")