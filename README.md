# ElevateLabs-Project

# Linux Hardening Audit Tool 🐧

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)
![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)

A command-line tool that acts as a basic security scanner for your Linux system. It automatically checks for common security misconfigurations and vulnerabilities, runs all checks in a few seconds, and provides a final compliance score.

## Example Output

Here is an example of what the report looks like when you run the script:

```bash
$ sudo python3 audit.py

Starting security audit...
==================================================
           LINUX AUDIT REPORT SUMMARY
==================================================

[ PASS ] Check: Firewall (ufw)
         Details: Firewall is active.

[ FAIL ] Check: SSH Root Login
         Details: PermitRootLogin is set to 'yes' or not found. (FAIL)

[ PASS ] Check: /etc/passwd Permissions
         Details: Permissions are 644. (PASS)

[ PASS ] Check: /etc/shadow Permissions
         Details: Permissions are 640. (PASS)

[ FAIL ] Check: Default umask
         Details: umask in /etc/profile is '022'. (FAIL)

[ INFO ] Check: Enabled Services
         Details: Found 15 services enabled on boot. (Manual review required)
         ... (list of services) ...

[ WARN ] Check: Rootkit Scan (rkhunter)
         Details: Found 5 warnings. (Manual review of /var/log/rkhunter/rkhunter.log recommended)

==================================================
           FINAL COMPLIANCE SCORE: 60.0%
==================================================







# Steganography GUI Tool 🖼️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=yellow)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A simple desktop application built with Python and Tkinter that allows you to hide secret text messages inside images and extract them.


## Features

* **Embed:** Hide a secret text message inside an image file.
* **Extract:** Reveal a secret message from an image file.
* **GUI:** A simple, user-friendly graphical interface built with Tkinter.

## How It Works

This tool uses the **Least Significant Bit (LSB)** steganography technique.

1.  Every pixel in an image has Red, Green, and Blue (RGB) color values.
2.  Each of these values (0-255) can be represented in binary (e.g., `11111111`).
3.  The "Least Significant Bit" is the very last bit on the right.
4.  This tool works by altering this last bit to embed the bits of the secret message. This change is so tiny that it is completely invisible to the human eye, allowing the message to be hidden in plain sight.

## Technology Stack

* **Python:** Core programming language.
* **Tkinter:** Python's built-in library for the GUI.
* **Pillow (PIL):** Used for opening, processing, and saving image files.
* **Stepic:** A powerful library that handles all the complex LSB steganography logic for encoding and decoding.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Install dependencies:**
    This project requires `Pillow` and `Stepic`. You can install them using pip:
    ```bash
    pip install Pillow stepic
    ```
    *(Alternatively, you can create a `requirements.txt` file with this content and run `pip install -r requirements.txt`)*

## How to Use

1.  **Run the application:**
    ```bash
    python your_script_name.py 
    ```
    *(Replace `your_script_name.py` with the actual name of your Python file.)*

2.  **To Embed (Hide) a Message:**
    * Click the **"Select..."** button and choose your "cover" image.
    * Type the secret message you wish to hide into the text box.
    * Click the **"Embed Message"** button.
    * A "Save As" dialog will appear. Choose a name for your new image.
    * **Important:** You must save the file as a **`.png`** to ensure the hidden data is preserved!

3.  **To Extract (Reveal) a Message:**
    * Click the **"Select..."** button and choose the image that contains a hidden message.
    * Click the **"Extract Message"** button.
    * If a message is found, the text box will be cleared and the secret message will be displayed.

## Future Improvements

This project is a great foundation. Here are some potential features to add:

* [ ] **Hide Files:** Expand the logic to embed entire files (like `.txt` or `.zip`) instead of just text.
* [ ] **Encryption:** Add a password field to encrypt the message *before* it is embedded, providing a second layer of security.
* [D] **Drag-and-Drop:** Improve the GUI to allow users to drag an image file directly onto the window.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
