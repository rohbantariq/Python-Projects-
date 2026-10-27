import os
import re
import smtplib
import tkinter as tk
from tkinter import ttk, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_PATH = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(ENV_PATH)


COMPANY_EMAIL = os.getenv(
    "EMAIL_ADDRESS"
)

COMPANY_APP_PASSWORD = os.getenv(
    "EMAIL_APP_PASSWORD"
)

COMPANY_RECEIVING_EMAIL = os.getenv(
    "COMPANY_RECEIVING_EMAIL"
)

COMPANY_NAME = os.getenv(
    "COMPANY_NAME"
)


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# =========================================================
# CHECK ENVIRONMENT CONFIGURATION
# =========================================================

def check_configuration():

    missing = []

    if not COMPANY_EMAIL:
        missing.append("EMAIL_ADDRESS")

    if not COMPANY_APP_PASSWORD:
        missing.append("EMAIL_APP_PASSWORD")

    if not COMPANY_RECEIVING_EMAIL:
        missing.append("COMPANY_RECEIVING_EMAIL")

    if not COMPANY_NAME:
        missing.append("COMPANY_NAME")

    if missing:

        return False, (
            "Missing environment variables: "
            + ", ".join(missing)
        )

    return True, "Configuration loaded successfully."


# =========================================================
# EMAIL VALIDATION
# =========================================================

def is_valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    ) is not None


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    to_email,
    subject,
    body,
    reply_to=None
):

    config_ok, config_message = check_configuration()

    if not config_ok:

        print(
            "CONFIGURATION ERROR:",
            config_message
        )

        return False, config_message


    message = MIMEMultipart()

    message["From"] = COMPANY_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    if reply_to:

        message["Reply-To"] = reply_to

    message.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )


    server = None


    try:

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        )

        server.starttls()

        server.login(
            COMPANY_EMAIL,
            COMPANY_APP_PASSWORD
        )

        server.send_message(
            message
        )

        return True, "Email sent successfully!"


    except smtplib.SMTPAuthenticationError as e:

        print(
            "SMTP AUTHENTICATION ERROR:",
            repr(e)
        )

        return False, "SMTP authentication failed."


    except smtplib.SMTPException as e:

        print(
            "SMTP ERROR TYPE:",
            type(e)
        )

        print(
            "SMTP ERROR:",
            repr(e)
        )

        return False, "SMTP error occurred."


    except OSError as e:

        print(
            "CONNECTION ERROR:",
            repr(e)
        )

        return False, "Connection error occurred."


    except Exception as e:

        print(
            "GENERAL ERROR TYPE:",
            type(e)
        )

        print(
            "GENERAL ERROR:",
            repr(e)
        )

        return False, "Unexpected error occurred."


    finally:

        if server:

            try:

                server.quit()

            except Exception:

                pass


# =========================================================
# MAIN APPLICATION
# =========================================================

class EmailAutomationApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Customer Inquiry System"
        )

        self.root.geometry(
            "750x700"
        )

        self.root.minsize(
            700,
            600
        )

        self.show_customer_form()


    # =====================================================
    # CLEAR SCREEN
    # =====================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():

            widget.destroy()


    # =====================================================
    # CUSTOMER FORM
    # =====================================================

    def show_customer_form(self):

        self.clear_screen()


        main_frame = ttk.Frame(
            self.root
        )

        main_frame.pack(
            fill="both",
            expand=True
        )


        canvas = tk.Canvas(
            main_frame,
            highlightthickness=0
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        frame = ttk.Frame(
            canvas,
            padding=30
        )


        canvas_window = canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )


        frame.bind(
            "<Configure>",
            lambda event:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        canvas.bind(
            "<Configure>",
            lambda event:
            canvas.itemconfig(
                canvas_window,
                width=event.width
            )
        )


        # =================================================
        # TITLE
        # =================================================

        ttk.Label(
            frame,
            text="CUSTOMER INQUIRY FORM",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(0, 8)
        )


        ttk.Label(
            frame,
            text=(
                "Tell us about the service you need "
                "and your requirements."
            )
        ).pack(
            pady=(0, 20)
        )


        # =================================================
        # CUSTOMER NAME
        # =================================================

        ttk.Label(
            frame,
            text="Customer Name *"
        ).pack(
            anchor="w"
        )


        self.name_entry = ttk.Entry(
            frame
        )

        self.name_entry.pack(
            fill="x",
            pady=(4, 12)
        )


        # =================================================
        # CUSTOMER EMAIL
        # =================================================

        ttk.Label(
            frame,
            text="Customer Email *"
        ).pack(
            anchor="w"
        )


        self.email_entry = ttk.Entry(
            frame
        )

        self.email_entry.pack(
            fill="x",
            pady=(4, 12)
        )


        # =================================================
        # PHONE NUMBER
        # =================================================

        ttk.Label(
            frame,
            text="Phone Number"
        ).pack(
            anchor="w"
        )


        self.phone_entry = ttk.Entry(
            frame
        )

        self.phone_entry.pack(
            fill="x",
            pady=(4, 12)
        )


        # =================================================
        # COMPANY NAME
        # =================================================

        ttk.Label(
            frame,
            text="Company Name"
        ).pack(
            anchor="w"
        )


        self.company_entry = ttk.Entry(
            frame
        )

        self.company_entry.pack(
            fill="x",
            pady=(4, 12)
        )


        # =================================================
        # SERVICE
        # =================================================

        ttk.Label(
            frame,
            text="Service Required *"
        ).pack(
            anchor="w"
        )


        self.service_combo = ttk.Combobox(
            frame,
            state="readonly"
        )


        self.service_combo["values"] = (

            "Website Development",
            "App Development",
            "Logo Design",
            "Social Media Marketing",
            "PPC / Advertising",
            "Video Animation",
            "Other"
        )


        self.service_combo.pack(
            fill="x",
            pady=(4, 12)
        )

        self.service_combo.current(0)


        # =================================================
        # PRIORITY
        # =================================================

        ttk.Label(
            frame,
            text="Priority"
        ).pack(
            anchor="w"
        )


        self.priority_combo = ttk.Combobox(
            frame,
            state="readonly"
        )


        self.priority_combo["values"] = (
            "Low",
            "Medium",
            "High"
        )


        self.priority_combo.pack(
            fill="x",
            pady=(4, 12)
        )

        self.priority_combo.current(1)


        # =================================================
        # REQUIREMENTS
        # =================================================

        ttk.Label(
            frame,
            text="Requirements *"
        ).pack(
            anchor="w"
        )


        self.requirements_text = tk.Text(
            frame,
            height=7,
            wrap="word"
        )


        self.requirements_text.pack(
            fill="x",
            pady=(4, 12)
        )


        # =================================================
        # ADDITIONAL NOTES
        # =================================================

        ttk.Label(
            frame,
            text="Additional Notes"
        ).pack(
            anchor="w"
        )


        self.notes_text = tk.Text(
            frame,
            height=5,
            wrap="word"
        )


        self.notes_text.pack(
            fill="x",
            pady=(4, 20)
        )


        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ttk.Frame(
            frame
        )


        button_frame.pack(
            pady=10
        )


        ttk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear_form
        ).pack(
            side="left",
            padx=10
        )


        ttk.Button(
            button_frame,
            text="SUBMIT INQUIRY",
            command=self.submit_inquiry
        ).pack(
            side="left",
            padx=10
        )


    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.name_entry.delete(
            0,
            tk.END
        )

        self.email_entry.delete(
            0,
            tk.END
        )

        self.phone_entry.delete(
            0,
            tk.END
        )

        self.company_entry.delete(
            0,
            tk.END
        )

        self.service_combo.current(0)

        self.priority_combo.current(1)

        self.requirements_text.delete(
            "1.0",
            tk.END
        )

        self.notes_text.delete(
            "1.0",
            tk.END
        )


    # =====================================================
    # SUBMIT INQUIRY
    # =====================================================

    def submit_inquiry(self):

        # -------------------------------------------------
        # GET FORM DATA
        # -------------------------------------------------

        name = (
            self.name_entry
            .get()
            .strip()
        )


        customer_email = (
            self.email_entry
            .get()
            .strip()
        )


        phone = (
            self.phone_entry
            .get()
            .strip()
        )


        customer_company = (
            self.company_entry
            .get()
            .strip()
        )


        service = (
            self.service_combo
            .get()
            .strip()
        )


        priority = (
            self.priority_combo
            .get()
            .strip()
        )


        requirements = (
            self.requirements_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        notes = (
            self.notes_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        # =================================================
        # VALIDATION
        # =================================================

        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter your name."
            )

            return


        if not customer_email:

            messagebox.showwarning(
                "Missing Email",
                "Please enter your email address."
            )

            return


        if not is_valid_email(
            customer_email
        ):

            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )

            return


        if not service:

            messagebox.showwarning(
                "Missing Service",
                "Please select a service."
            )

            return


        if not requirements:

            messagebox.showwarning(
                "Missing Requirements",
                "Please describe your requirements."
            )

            return


        # =================================================
        # AUTOMATIC SUBJECTS
        # =================================================

        company_subject = (
            f"New Customer Inquiry - {service}"
        )


        customer_subject = (
            f"Your {service} Inquiry Has Been Received"
        )


        # =================================================
        # COMPANY EMAIL
        # =================================================

        company_body = f"""Hello Team,

A new customer inquiry has been submitted through the
Customer Inquiry System.

CUSTOMER INFORMATION
====================

Name:
{name}

Email:
{customer_email}

Phone:
{phone if phone else "Not provided"}

Company:
{customer_company if customer_company else "Not provided"}


SERVICE INFORMATION
===================

Service Required:
{service}

Priority:
{priority}


CUSTOMER REQUIREMENTS
=====================

{requirements}


ADDITIONAL NOTES
================

{notes if notes else "No additional notes."}


Please review the customer's requirements and contact
the customer using the email address provided above.

Regards,
{COMPANY_NAME}
"""


        # =================================================
        # CUSTOMER CONFIRMATION EMAIL
        # =================================================

        customer_body = f"""Dear {name},

Thank you for contacting {COMPANY_NAME}.

We have successfully received your inquiry.

SERVICE REQUESTED
=================

{service}


Your requirements have been forwarded to our team
for review.

Our team will review your request and contact you soon.

You do not need to submit the same inquiry again.

Thank you for choosing {COMPANY_NAME}.

Regards,
{COMPANY_NAME}
"""


        # =================================================
        # SEND EMAIL TO COMPANY
        # =================================================

        company_success, company_message = send_email(

            COMPANY_RECEIVING_EMAIL,

            company_subject,

            company_body,

            reply_to=customer_email
        )


        if not company_success:

            # Detailed error is ONLY shown in terminal
            print(
                "BACKEND COMPANY EMAIL ERROR:",
                company_message
            )

            # Customer sees only a simple message
            messagebox.showerror(
                "Submission Failed",
                "We couldn't submit your inquiry right now.\n\n"
                "Please try again later."
            )

            return


        # =================================================
        # SEND CONFIRMATION TO CUSTOMER
        # =================================================

        customer_success, customer_message = send_email(

            customer_email,

            customer_subject,

            customer_body
        )


        if not customer_success:

            # Detailed error is ONLY shown in terminal
            print(
                "BACKEND CUSTOMER EMAIL ERROR:",
                customer_message
            )

            # Do not expose SMTP/backend details
            messagebox.showinfo(
                "Inquiry Received",
                "Your inquiry has been received successfully.\n\n"
                "Our team will contact you soon."
            )

            return


        # =================================================
        # SUCCESS
        # =================================================

        messagebox.showinfo(
            "Inquiry Submitted",
            "Your inquiry has been received successfully!\n\n"
            "A confirmation email has been sent "
            "to your email address."
        )


        # Clear form

        self.clear_form()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = EmailAutomationApp(
        root
    )

    root.mainloop()