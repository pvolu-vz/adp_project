import sys
import requests
import logging
from adp_project.config import ADP_TOKEN_URL, EMPLOYEE_API_URL, CLIENT_ID, CLIENT_SECRET, CLIENT_CERT_FILE, CLIENT_KEY_FILE, PAGE_SIZE, status_url, introspect_url
from adp_project.utils import pretty_print_json

class ADPAPIClient:
    def get_filtered_employees(self, domains, page_size=100):
        """
        Fetch all employees from ADP API using pagination, then filter in memory by email domain list.
        """
        if not self.token:
            print("No access token. Call get_access_token() first.")
            logging.error("No access token. Call get_access_token() first.")
            return []
        logging.debug(f"Token exists: {self.token}")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        skip = 0
        page = 1
        all_employees = []
        print(f"Filtering by domains: {domains}")
        logging.debug(f"Filtering by domains: {domains}")
        while True:
            params = {
                "$top": page_size,
                "$skip": skip
            }
            print(f"Fetching page {page}: $top={page_size}, $skip={skip}")
            logging.debug(f"Fetching page {page}: $top={page_size}, $skip={skip}")
            try:
                response = requests.get(
                    EMPLOYEE_API_URL,
                    headers=headers,
                    params=params,
                    cert=(CLIENT_CERT_FILE, CLIENT_KEY_FILE)  # <-- Added mTLS cert here
                )
                logging.debug(f"Response: {response}")
                response.raise_for_status()
                data = response.json()
                employees = data.get("workers", [])
                all_employees.extend(employees)
                print(f"Page {page} fetched, users so far: {len(all_employees)}")
                if not employees:
                    print("No more employees returned, stopping pagination.")
                    logging.debug("No more employees returned, stopping pagination.")
                    break
                skip += page_size
                page += 1
            except Exception as e:
                print(f"Error fetching employees: {e}")
                logging.error(f"Error fetching employees: {e}")
                break
        # If domains is a file path, read domains from file
        if isinstance(domains, str):
            with open(domains, "r") as f:
                domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        domains_set = set(d.lower() for d in domains)
        filtered_employees = []
        for user in all_employees:
            # Try to get business email, fallback to personal
            email = ""
            business_comm = user.get("businessCommunication", {})
            emails = business_comm.get("emails", [])
            if emails and isinstance(emails, list):
                email = emails[0].get("emailUri", "")
            else:
                person = user.get("person", {})
                comm = person.get("communication", {})
                personal_emails = comm.get("emails", [])
                if personal_emails and isinstance(personal_emails, list):
                    email = personal_emails[0].get("emailUri", "")
            # Compare email domain
            for domain in domains_set:
                if email.lower().endswith(f"@{domain}"):
                    filtered_employees.append(user)
                    break
        print(f"Total filtered employees: {len(filtered_employees)}")
        return filtered_employees

    def __init__(self):
        self.token = None

    def get_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "api_scope"
        }
        try:
            response = requests.post(
                ADP_TOKEN_URL,
                data=data,
                cert=(CLIENT_CERT_FILE, CLIENT_KEY_FILE)
            )
            logging.debug(f"Response: {response}")
            response.raise_for_status()
            logging.debug(f"Access token response: {response.json()}")
            self.token = response.json().get("access_token")
            return self.token
        except Exception as e:
            logging.error(f"Error during mTLS request: {e}")
            logging.info("Exiting due to error in getting access token.")
            sys.exit(1)
            return None

    def get_employees(self, limit=2):
        if not self.token:
            print("No access token. Call get_access_token() first.")
            return []
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        params = {"limit": limit}
        try:
            response = requests.get(
                EMPLOYEE_API_URL,
                headers=headers,
                params=params,
                cert=(CLIENT_CERT_FILE, CLIENT_KEY_FILE)  # <-- Added mTLS cert here
            )
            response.raise_for_status()
            data = response.json()
            pretty_print_json(data)
            return data
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []

    def get_all_employees(self):
        """
        Fetch all employees from ADP using OData-style pagination ($top, $skip, $count).
        First, fetch total count using $count=true & $top=1, then paginate using $top/$skip.
        """
        if not self.token:
            print("No access token. Call get_access_token() first.")
            return []
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        top = PAGE_SIZE
        # Step 1: Get total count
        params_count = {"$count": "true", "$top": 1}
        print("Fetching total employee count...")
        try:
            response = requests.get(
                EMPLOYEE_API_URL,
                headers=headers,
                params=params_count,
                cert=(CLIENT_CERT_FILE, CLIENT_KEY_FILE)  # <-- Added mTLS cert here
            )
            response.raise_for_status()
            data = response.json()
            # Try to get total count from @odata.count, meta, or similar field
            total_count = data.get("@odata.count")
            if not total_count:
                meta = data.get("meta", {})
                total_count = meta.get("totalCount") or meta.get("totalNumber") or data.get("totalCount")
            if not total_count:
                print("Could not determine total employee count, will paginate until empty page.")
                total_count = None
            else:
                print(f"Total count reported by ADP: {total_count}")
        except Exception as e:
            print(f"Error fetching total count: {e}")
            total_count = None

        # Step 2: Paginate
        skip = 0
        all_employees = []
        page = 1
        while True:
            params = {"$top": top, "$skip": skip}
            print(f"Fetching page {page}: $top={top}, $skip={skip}")
            try:
                response = requests.get(
                    EMPLOYEE_API_URL,
                    headers=headers,
                    params=params,
                    cert=(CLIENT_CERT_FILE, CLIENT_KEY_FILE)  # <-- Added mTLS cert here
                )
                response.raise_for_status()
                data = response.json()
                employees = data.get("workers", [])
                all_employees.extend(employees)
                print(f"Page {page} fetched, users so far: {len(all_employees)}")
                if not employees:
                    print("No more employees returned, stopping pagination.")
                    break
                skip += top
                page += 1
                # Optionally, stop if skip >= total_count
                if total_count and skip >= int(total_count):
                    print("Reached total count, stopping pagination.")
                    break
            except Exception as e:
                print(f"Error fetching employees: {e}")
                break
        print(f"Total employees fetched: {len(all_employees)}")
        return all_employees
