def alert():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    def send_email_alert(subject, message, to_email, from_email, from_password):
        """
        Send an email alert via SMTP.
        Args:
            subject (str): Email subject
            message (str): Email body
            to_email (str): Recipient email
            from_email (str): Your email
            from_password (str): Your email app password (not your normal Gmail password)
        """
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            server.quit()
            print(f"Alert email sent to {to_email}")
        except Exception as e:
            print("Failed to send email:", e)

    # ------------------------------
    # Example usage
    # ------------------------------
    if __name__ == "__main__":
        subject = "Patient Alert: Unusual Activity Detected"
        message = "The system detected unusual activity for patient. Please check immediately."
        
        to_email = "ganasreeajay@gmail.com"
        from_email = "prashanthvprashanthv46@gmail.com"
        from_password = "spqbsdbnwvrgubdo"  # Use App Password in Gmail
        
        send_email_alert(subject, message, to_email, from_email, from_password)
