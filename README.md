# ADP Project Deployment & Automation Guide

This guide explains how to deploy the `adp_project` Python application on a Linux server, install dependencies, configure logging, and schedule it to run daily using cron.

## 1. Prerequisites
- Linux server (Ubuntu, CentOS, etc.)
- Python 3.8+ installed (recommended: Python 3.10 or newer)

## 2. Unzip the Project
Transfer the zip file to your Linux server and unzip it:
```bash
unzip adp_project.zip -d /path/to/target_folder
cd /path/to/target_folder/ADP/adp_project
```

## 3. Set Up Python Environment
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies
Install all required packages using the provided `requirements.txt` file:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Environment Variables
Edit the `.env` file in the project folder and set all required secrets and configuration values. Example:

```
VEZA_URL=https://your-veza-instance.com
VEZA_API_KEY=your_veza_api_key
ADP_CLIENT_ID=your_adp_client_id
ADP_CLIENT_SECRET=your_adp_client_secret
ADP_CERT_PATH=certs/adp_cert.crt
ADP_KEY_PATH=certs/adp_key.key
```

**Where to save certificate and key files:**

1. Create a folder named `certs` inside your project directory:
   ```bash
   mkdir -p certs
   ```
2. Save your ADP certificate file as `adp_cert.crt` and your key file as `adp_key.key` inside the `certs` folder:
   ```bash
   cp /path/to/your/adp_cert.crt certs/adp_cert.crt
   cp /path/to/your/adp_key.key certs/adp_key.key
   ```
3. Make sure the paths in your `.env` file match the location and filenames above.

**Note:** Never commit your `.env`, certificate, or key files to version control.

## 6. Test the Application
Run the main script to verify setup. You can specify the provider name, domain file, log file, and log level using command-line arguments:

```bash
python -m adp_project_filter.main --provider_name "ADP Jencap" --domain_file "jencap.txt" --log_file "jencap.log" --log_level "INFO"
```

To use a different provider and domain file, simply change the arguments:

```bash
python -m adp_project_filter.main --provider_name "ADP Epic" --domain_file "epic.txt" --log_file "epic.log" --log_level "DEBUG"
```

**Logging Options:**
- `--log_file`: Specify the filename to store logs locally (default: `adp_project.log`).
- `--log_level`: Set the logging level (`INFO`, `DEBUG`, `WARNING`, `ERROR`, `CRITICAL`). Use `DEBUG` for verbose output and troubleshooting.

The domain file should be a text file (e.g., `jencap.txt`, `epic.txt`) located in the same folder or provide the full path.

## 7. Automate with Cron
You can schedule the script to run with different provider/domain combinations and logging options in separate cron jobs. For example:

1. Find the full path to your Python executable:
   ```bash
   which python3
   # Or, if using a virtualenv:
   /path/to/venv/bin/python
   ```
2. Edit the crontab:
   ```bash
   crontab -e
   ```
3. Add lines for each provider/domain combination (replace paths as needed):
   ```
   # Run ADP Jencap at 2:00 AM
   0 2 * * * cd /path/to/ADP/adp_project_filter && /path/to/venv/bin/python -m adp_project_filter.main --provider_name "ADP Jencap" --domain_file "jencap.txt" --log_file "cron_jencap.log" --log_level "INFO" >> /path/to/ADP/adp_project_filter/cron_jencap.log 2>&1

   # Run ADP Epic at 3:00 AM
   0 3 * * * cd /path/to/ADP/adp_project_filter && /path/to/venv/bin/python -m adp_project_filter.main --provider_name "ADP Epic" --domain_file "epic.txt" --log_file "cron_epic.log" --log_level "DEBUG" >> /path/to/ADP/adp_project_filter/cron_epic.log 2>&1
   ```
   - Each line runs the script with a different provider, domain file, and logging configuration, logging output to a separate file.

## 8. Troubleshooting
- Check your specified log file (e.g., `cron_jencap.log`) for errors and script output.
- Ensure `.env` is readable by the cron user.
- If using a virtualenv, always use the full path to the Python executable in cron.

## 9. Updating the Project
To update code and dependencies:
- Replace the project folder with a new zip file and repeat steps 2–4.
- If dependencies change, update `requirements.txt` and re-run:
   ```bash
   pip install -r requirements.txt
   ```

---

For questions or support, contact the project maintainer.
