
#!env python3
import sys
import os
import logging
from oaaclient.client import OAAClient, OAAClientError
from oaaclient.templates import OAAPropertyType, HRISProvider, IdPProviderType
from adp_project.config import VEZA_URL, VEZA_API_KEY
from adp_project.adp_api import ADPAPIClient

HRIS_ICON_B64 = """
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
"""

def connect_to_veza():
    veza_url = VEZA_URL
    veza_api_key = VEZA_API_KEY
    if None in (veza_url, veza_api_key):
        print("Unable to find all environment variables")
        logging.error("VEZA_URL or VEZA_API_KEY environment variable not set")
        sys.exit(1)

    return OAAClient(url=veza_url, api_key=veza_api_key)

def load_users(adp_app, domain_file_path) -> None:
    """Populate the idp with users from ADP API"""
    adp_app.property_definitions.define_employee_property("custom_property", OAAPropertyType.STRING)

    # Use ADPAPIClient to fetch users
    logging.debug("Loading ADP API Class...")
    adp_client = ADPAPIClient()
    logging.debug("Generating Access Token for ADP...")
    token = adp_client.get_access_token()
    if not token:
        print("Failed to get ADP access token.")
        logging.error("Failed to get ADP access token.")
        return
    # Fetch all users with pagination
    logging.debug("Fetching employees from ADP API...")
    adp_users = adp_client.get_filtered_employees(domains=domain_file_path)
    if not adp_users:
        print("No users returned from ADP API.")
        logging.warning("No users returned from ADP API.")
        return

    # Map fields from ADP sample data structure
    logging.debug(f"Processing {len(adp_users)} users from ADP API...")
    for user in adp_users:
        employee_number = user.get("workerID", {}).get("idValue", "")
        associate_oid = user.get("associateOID", "")
        person = user.get("person", {})
        legal_name = person.get("legalName", {})
        preferred_name = person.get("preferredName", {})
        display_name = legal_name.get("formattedName") or preferred_name.get("givenName") or ""
        first_name = legal_name.get("givenName") or preferred_name.get("givenName") or ""
        last_name = legal_name.get("familyName1") or preferred_name.get("familyName1") or ""
        is_active = user.get("workerStatus", {}).get("statusCode", {}).get("codeValue", "Active") == "Active"
        employment_status = user.get("workerStatus", {}).get("statusCode", {}).get("codeValue", "Active")
        email = ""
        # Try to get business email, fallback to personal
        business_comm = user.get("businessCommunication", {})
        emails = business_comm.get("emails", [])
        if emails and isinstance(emails, list):
            email = emails[0].get("emailUri", "")
        else:
            comm = person.get("communication", {})
            personal_emails = comm.get("emails", [])
            if personal_emails and isinstance(personal_emails, list):
                email = personal_emails[0].get("emailUri", "")

        # Manager attribute from reportsTo
        manager = ""
        work_assignments = user.get("workAssignments", [])
        job_title = ""
        department = ""
        if work_assignments and isinstance(work_assignments, list):
            wa = work_assignments[0]
            # Job title
            job_title = wa.get("jobTitle", "")
            # Department: try assignedOrganizationalUnits or homeOrganizationalUnits
            org_units = wa.get("assignedOrganizationalUnits", [])
            if not org_units:
                org_units = wa.get("homeOrganizationalUnits", [])
            for unit in org_units:
                if unit.get("typeCode", {}).get("codeValue", "") == "Department":
                    department = unit.get("nameCode", {}).get("longName", "") or unit.get("nameCode", {}).get("codeValue", "")
                    break
            # Manager
            reports_to = wa.get("reportsTo", [])
            if reports_to and isinstance(reports_to, list):
                manager = reports_to[0].get("positionID", None)

        # Fallback: try customFieldGroup for department
        custom_fields = user.get("customFieldGroup", {})
        code_fields = custom_fields.get("codeFields", [])
        for field in code_fields:
            if field.get("nameCode", {}).get("codeValue", "") in ["Department (Seg 3)", "Department"]:
                department = field.get("longName", "") or field.get("codeValue", "")
                break

        employee = adp_app.add_employee(
            unique_id=employee_number,
            name=display_name,
            employee_number=employee_number,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            employment_status=employment_status
        )
        employee.email = email
        employee.company = ""
        employee.canonical_name = display_name
        employee.idpid = associate_oid
        employee.managers = manager
        employee.job_title = job_title
        logging.debug(f"Processed employee: {employee}")
        # Add department as group if not present, then assign
        if department:
            if department not in adp_app.groups:
                adp_app.add_group(unique_id=department, name=department, group_type="Department")
                logging.debug(f"Added new department group: {department}")
            employee.department = department

    total_users = len(adp_app.employees)
    print(f"Loaded {total_users} users from ADP API.")
    logging.info(f"Loaded {total_users} users from ADP API.")
    return


def oaa_hris_definition(provider_name, domain_file):
    # Create an instance of the OAA Custom HRIS custom provider class, modeling the application name and type
    domain_file_path = os.path.join(os.path.dirname(__file__), domain_file)
    adp_app = HRISProvider(name=provider_name, hris_type="ADP", url="www.adp.com")
    logging.debug(f"Defining HRIS Provider instance for {provider_name}")

    # HRIS employees can be automatically linked to IdP users, setting the IdP provider type to use for matching
    adp_app.system.add_idp_type(IdPProviderType.ACTIVE_DIRECTORY)
    adp_app.system.add_idp_type(IdPProviderType.AZURE_AD)
    logging.debug("Configured IdP provider types for user matching...")

    # Load users from source (ADP)
    load_users(adp_app, domain_file_path)

    # Push data to Veza
    veza_con = connect_to_veza()
    datasource_name = f"{provider_name} Datasource"
    provider = veza_con.get_provider(provider_name)
    if provider:
        print("-- Found existing provider")
        logging.debug(f"Found existing provider {provider_name} ({provider['id']})")
    else:
        print(f"++ Creating Provider {provider_name}")
        logging.info(f"Creating provider {provider_name}")
        provider = veza_con.create_provider(provider_name, adp_app.TEMPLATE)
    print(f"-- Provider: {provider['name']} ({provider['id']})")
    logging.debug(f"Using provider {provider['name']} ({provider['id']})")
    veza_con.update_provisioning_status(provider['id'], True)

    # Push the metadata payload:
    if HRIS_ICON_B64:
        try:
            veza_con.update_provider_icon(provider["id"], HRIS_ICON_B64)
            logging.debug("Updated provider icon")
        except OAAClientError as e:
            if e.details:
                print(f"++ Warning: Unable to update provider icon: {e.details[0]}", file=sys.stderr)
                logging.warning(f"Unable to update provider icon: {e.details[0]}")
    try:
        response = veza_con.push_application(provider_name,
                                             datasource_name,
                                             adp_app,
                                             save_json=False)
        if response.get("warnings", None):
            print("-- Push succeeded with warnings:")
            logging.warning("Push succeeded with warnings:")
            for e in response["warnings"]:
                print(f"  - {e}")
    except OAAClientError as e:
        print(f"-- Error: {e.error}: {e.message} ({e.status_code})", file=sys.stderr)
        logging.error(f"Error pushing application: {e.error}: {e.message} ({e.status_code})")
        if hasattr(e, "details"):
            for d in e.details:
                print(f"  -- {d}", file=sys.stderr)
    return