import json
import logging

def print_certificate_file(cert_path):
    try:
        with open(cert_path, "r") as f:
            content = f.read()
            print("Certificate file contents:\n", content)
    except Exception as e:
        print(f"Error reading certificate file: {e}")

def pretty_print_json(data):
    print(json.dumps(data, indent=2))


def setup_logging(log_file="adp_project.log", log_level="INFO"):
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        filename=log_file,
        level=numeric_level,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console