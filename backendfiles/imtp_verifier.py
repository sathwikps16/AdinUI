import imaplib

def validate_imap_credentials(email, app_password,server):
    try:
        port = 993  # Default port for IMAP over SSL

        # Create IMAP connection
        mail = imaplib.IMAP4_SSL(server, port)
        
        # Attempt to log in using the email address and app password
        mail.login(email, app_password)

        print("Authentication successful!")
        return True  # Successful authentication

    except imaplib.IMAP4.error:
        print("Authentication failed. Please check your credentials.")
        return False  # Authentication failed

    finally:
        mail.logout()

# Example usage
email = 'ragtest209@gmail.com'
app_password = 'espq juva cclw ecxn'
server = 'imap.gmail.com'
validate_imap_credentials(email, app_password,server)
