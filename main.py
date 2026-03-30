import os
import sys
import argparse
from adp_project.adp_OAA_veza import oaa_hris_definition
from adp_project.adp_api import ADPAPIClient
from adp_project.utils import print_certificate_file, setup_logging
from adp_project.config import CLIENT_CERT_FILE

def main():
    
    # Set log level as environment variable for setup_logging
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider_name", required=True)
    parser.add_argument("--domain_file", required=True)
    parser.add_argument("--log_file", default="adp_project.log")
    parser.add_argument("--log_level", default="INFO")
    args = parser.parse_args()

    setup_logging(log_file=args.log_file, log_level=args.log_level)
    oaa_hris_definition(args.provider_name, args.domain_file)

    print(f"[DEBUG] Running: {__file__}")
    print(f"[DEBUG] CWD: {os.getcwd()}")
    print(f"[DEBUG] sys.path: {sys.path}")
    #print_certificate_file(CLIENT_CERT_FILE)
    client = ADPAPIClient()
    """#token = client.get_access_token()
    token = "1"
    if token:
        print("Access token obtained successfully.")
        print(f"Access token: {token}")
        #get list of employees
        #client.get_employees(limit=1)
        #print("\nAll employee records (paginated):")
        #client.get_all_employees()
    else:
        print("Authentication failed.")

    # Push ADP HRIS definition to Veza
    print("\nPushing ADP HRIS definition to Veza...")
    parser = argparse.ArgumentParser(description="Push ADP HRIS definition to Veza with domain filtering.")
    parser.add_argument("--provider_name", required=True, help="Name of the provider (e.g., 'ADP Jencap')")
    parser.add_argument("--domain_file", required=True, help="Path to the domain file (e.g., 'jencap.txt')")
    args, _ = parser.parse_known_args()
    oaa_hris_definition(args.provider_name, args.domain_file)
    """

if __name__ == "__main__":
    main()
