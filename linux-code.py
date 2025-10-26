#!/usr/bin/env python3
"""
Simple Linux Security Audit Tool
This script performs a basic security audit of a Linux system based on
common hardening guidelines and CIS benchmarks.

Must be run as root (sudo).
"""

import subprocess
import os
import sys

# --- Global Variables ---
# We'll store our findings in this list
report = []
# We'll calculate a compliance score
score = 0
max_score = 0

# --- Helper Function ---
def run_command(command):
    """
    Runs a shell command and returns its stdout.
    Returns None if the command fails.
    """
    try:
        # Runs a command in the shell
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=False,  # Don't raise error on failure
            timeout=30    # Add a timeout for safety
        )
        if result.returncode != 0:
            # If command fails, log to stderr (visible in terminal)
            print(f"Warning: Command '{command}' failed: {result.stderr.strip()}", file=sys.stderr)
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running command '{command}': {e}", file=sys.stderr)
        return None

# --- Audit Check Functions ---

def check_firewall():
    """Checks if ufw (Uncomplicated Firewall) is active."""
    global score, max_score
    max_score += 1
    print("[*] Checking Firewall (ufw)...")

    status = run_command("systemctl is-active ufw")

    if status == "active":
        report.append({
            "check": "Firewall",
            "status": "PASS",
            "message": "Firewall (ufw) is active.",
            "recommendation": "None."
        })
        score += 1
    elif status == "inactive":
        report.append({
            "check": "Firewall",
            "status": "FAIL",
            "message": "Firewall (ufw) is INACTIVE.",
            "recommendation": "Enable the firewall using 'sudo ufw enable'."
        })
    else:
        # Handles 'None' from run_command or other statuses
        report.append({
            "check": "Firewall",
            "status": "ERROR",
            "message": "Could not determine ufw status. Is 'ufw' installed?",
            "recommendation": "If this is not an Ubuntu/Debian system, you may need to check for 'firewalld'."
        })

def check_ssh_config():
    """Checks for insecure SSH 'PermitRootLogin' setting."""
    global score, max_score
    max_score += 1
    print("[*] Checking SSH configuration...")

    config_file = "/etc/ssh/sshd_config"
    
    if not os.path.exists(config_file):
        report.append({
            "check": "SSH Root Login",
            "status": "ERROR",
            "message": f"SSH config file not found at {config_file}.",
            "recommendation": "Ensure SSH server is installed correctly."
        })
        return

    # 'grep ... || true' ensures the command doesn't fail if the string isn't found
    config = run_command(f"grep '^PermitRootLogin' {config_file} || true")

    if config == "PermitRootLogin no":
        report.append({
            "check": "SSH Root Login",
            "status": "PASS",
            "message": "PermitRootLogin is set to 'no'.",
            "recommendation": "None."
        })
        score += 1
    else:
        # This catches 'PermitRootLogin yes', 'PermitRootLogin prohibit-password', or if it's commented out
        report.append({
            "check": "SSH Root Login",
            "status": "FAIL",
            "message": f"PermitRootLogin is NOT securely set to 'no'. Found: '{config}'",
            "recommendation": "Edit /etc/ssh/sshd_config and set 'PermitRootLogin no' and restart the SSH service."
        })

def check_file_permissions():
    """Checks permissions on /etc/passwd and /etc/shadow."""
    global score, max_score
    print("[*] Checking critical file permissions...")

    files_to_check = {
        "/etc/passwd": "644",
        "/etc/shadow": ["640", "600", "400"] # Allow 640 (group read) or 600/400 (root only)
    }

    for file_path, expected_perms_list in files_to_check.items():
        max_score += 1
        if not isinstance(expected_perms_list, list):
            expected_perms_list = [expected_perms_list] # Make it a list

        if not os.path.exists(file_path):
            report.append({
                "check": f"Permissions: {file_path}",
                "status": "ERROR",
                "message": f"File not found: {file_path}.",
                "recommendation": "This is a critical system file. Investigate immediately."
            })
            continue

        # Get permissions in octal format (e.g., '644')
        try:
            perms = oct(os.stat(file_path).st_mode)[-3:]
            
            if perms in expected_perms_list:
                report.append({
                    "check": f"Permissions: {file_path}",
                    "status": "PASS",
                    "message": f"Permissions are {perms}.",
                    "recommendation": "None."
                })
                score += 1
            else:
                report.append({
                    "check": f"Permissions: {file_path}",
                    "status": "FAIL",
                    "message": f"Permissions are {perms} (Expected: {expected_perms_list}).",
                    "recommendation": f"Run 'sudo chmod {expected_perms_list[0]} {file_path}'."
                })
        except Exception as e:
            report.append({
                "check": f"Permissions: {file_path}",
                "status": "ERROR",
                "message": f"Could not check permissions: {e}",
                "recommendation": "Investigate file system issue."
            })

def check_unused_services():
    """Lists enabled services for manual review."""
    # This check is informational, so we don't score it.
    print("[*] Checking enabled services...")
    
    services = run_command("systemctl list-unit-files --type=service --state=enabled | grep '.service'")
    
    if services is not None:
        report.append({
            "check": "Enabled Services",
            "status": "INFO",
            "message": "Review this list for any services you don't need.",
            "recommendation": f"Disable unneeded services with 'sudo systemctl disable <service_name>'.\nServices found:\n{services}"
        })
    else:
        report.append({
            "check": "Enabled Services",
            "status": "ERROR",
            "message": "Could not list enabled services.",
            "recommendation": "Check systemctl logs."
        })

def check_cis_umask():
    """CIS Benchmark 5.4.4 - Ensure default umask is 027 or more restrictive."""
    global score, max_score
    max_score += 1
    print("[*] Checking CIS (Default umask)...")
    
    # Check in /etc/profile which is a common place
    umask_setting = run_command("grep '^umask' /etc/profile || true")
    
    if "umask 027" in umask_setting or "umask 077" in umask_setting:
        report.append({
            "check": "CIS: Default Umask",
            "status": "PASS",
            "message": f"Umask setting found: {umask_setting}",
            "recommendation": "None."
        })
        score += 1
    else:
        report.append({
            "check": "CIS: Default Umask",
            "status": "FAIL",
            "message": f"Default umask is not set to 027 or 077. Found: {umask_setting}",
            "recommendation": "Add or edit the 'umask 027' line in /etc/profile or /etc/bash.bashrc."
        })

def check_rootkits():
    """Checks for rootkits using 'rkhunter'."""
    print("[*] Checking for rootkits (using rkhunter)...")
    
    # First, check if rkhunter is installed
    if run_command("command -v rkhunter") is None:
        report.append({
            "check": "Rootkit Scan",
            "status": "ERROR",
            "message": "rkhunter is not installed.",
            "recommendation": "Install rkhunter ('sudo apt install rkhunter') and run 'sudo rkhunter --update' then 'sudo rkhunter --check'."
        })
        return

    # If it's installed, run the check.
    # '--check' runs the scan. '--rwo' (report warnings only) simplifies output.
    print("    (This may take a minute or two...)")
    scan_output = run_command("sudo rkhunter --check --rwo")
    
    if scan_output is None:
        report.append({
            "check": "Rootkit Scan",
            "status": "ERROR",
            "message": "rkhunter scan failed to run.",
            "recommendation": "Run 'sudo rkhunter --check' manually to debug."
        })
    elif "Warning:" in scan_output:
        report.append({
            "check": "Rootkit Scan",
            "status": "WARNING",
            "message": "rkhunter found warnings. This is common on new installs (e.g., file prop changes).",
            "recommendation": f"Run 'sudo rkhunter --check' manually to review. Warnings found:\n{scan_output}"
        })
    else:
        report.append({
            "check": "Rootkit Scan",
            "status": "PASS",
            "message": "rkhunter scan completed with no warnings.",
            "recommendation": "None."
        })

# --- Main Execution ---
def main():
    """Main function to run all audit checks and print the report."""
    
    # Check if running as root
    if os.geteuid() != 0:
        print("This script must be run as root to access all system files.")
        print("Please run with: sudo python3 audit.py")
        sys.exit(1)

    print("============================================")
    print("  Starting Simple Linux Security Audit Tool ")
    print("============================================")
    
    # Run all our check functions
    check_firewall()
    check_ssh_config()
    check_file_permissions()
    check_cis_umask()
    check_unused_services() # Informational, not scored
    check_rootkits()        # Informational, not scored
    
    print("\n\n============================================")
    print("           Audit Report Summary           ")
    print("============================================")
    
    # Print the formatted report
    for item in report:
        print(f"\n--- Check: {item['check']} ---")
        print(f"  [!] Status: {item['status']}")
        print(f"  [+] Message: {item['message']}")
        print(f"  [>] Action: {item['recommendation']}")

    # Print the final score
    print("\n\n============================================")
    print("                 Final Score                ")
    print("============================================")
    
    if max_score > 0:
        final_score = (score / max_score) * 100
        print(f"Your system compliance score is: {score}/{max_score} ({final_score:.2f}%)")
        print("NOTE: 'INFO' and 'WARNING' checks do not count towards the score.")
    else:
        print("No scorable checks were completed.")

if __name__ == "__main__":
    main()