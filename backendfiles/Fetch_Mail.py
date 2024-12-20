# username='ragtest209@gmail.com',
        # password='espq juva cclw ecxn',
        # imap_server='imap.gmail.com',
        # check_interval=9  # Check every 60 seconds

#pip install html2text
#Call Back



import imaplib
import email
from email.header import decode_header
import time
import re
import html2text

def strip_html_tags(text):
    """
    Remove HTML tags from text and convert to plain text.
    
    :param text: Input text with potential HTML
    :return: Plain text without HTML tags
    """
    # Use html2text to convert HTML to markdown, then strip to plain text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    
    # First, try html2text conversion
    try:
        plain_text = h.handle(text).strip()
        # Remove excessive newlines
        plain_text = re.sub(r'\n+', '\n', plain_text)
        return plain_text
    except Exception:
        # Fallback method if html2text fails
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        # Decode HTML entities
        clean_text = clean_text.replace('&nbsp;', ' ')
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&lt;', '<')
        clean_text = clean_text.replace('&gt;', '>')
        
        return clean_text.strip()

def extract_email_content(email_message):
    """
    Extract plain text content from email
    
    :param email_message: Parsed email message
    :return: Dictionary with email content details
    """
    # Decode email headers
    def decode_header_value(header_value):
        if header_value:
            decoded_parts = []
            for part, encoding in decode_header(header_value):
                if isinstance(part, bytes):
                    decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
                else:
                    decoded_parts.append(part)
            return ' '.join(decoded_parts)
        return ''

    # Extract basic headers
    email_content = {
        'subject': decode_header_value(email_message['Subject']),
        'from': decode_header_value(email_message['From']),
        'to': decode_header_value(email_message.get('To', '')),
        'date': decode_header_value(email_message['Date']),
        'body': ''
    }

    # Process multipart email
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            
            # Prefer plain text, fallback to HTML
            if content_type == 'text/plain':
                try:
                    body = part.get_payload(decode=True).decode(
                        part.get_content_charset() or 'utf-8', 
                        errors='replace'
                    )
                    email_content['body'] += body + '\n'
                except:
                    pass
            
            # If no plain text, convert HTML
            elif content_type == 'text/html' and not email_content['body']:
                try:
                    html_body = part.get_payload(decode=True).decode(
                        part.get_content_charset() or 'utf-8', 
                        errors='replace'
                    )
                    email_content['body'] = strip_html_tags(html_body)
                except:
                    pass
    else:
        # Non-multipart email
        try:
            body = email_message.get_payload(decode=True).decode(
                email_message.get_content_charset() or 'utf-8', 
                errors='replace'
            )
            email_content['body'] = strip_html_tags(body) if 'html' in email_message.get_content_type() else body
        except:
            pass

    return email_content

def fetch_new_emails(username, password, imap_server, mailbox='INBOX', check_interval=60):
    """
    Continuously check for new emails at specified intervals.
    """
    last_email_id = None
    
    while True:
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(username, password)
            mail.select(mailbox)
            
            # Search for all emails
            _, search_data = mail.search(None, 'ALL')
            email_ids = search_data[0].split()
            
            # Check if there are new emails
            if email_ids and (last_email_id is None or email_ids[-1] != last_email_id):
                # Process new emails
                new_emails = email_ids if last_email_id is None else email_ids[email_ids.index(last_email_id)+1:]
                
                for email_id in new_emails:
                    # Fetch the email
                    _, email_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = email_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract email content
                    full_content = extract_email_content(email_message)
                    
                    # Print full email details in plain text
                    print("\n--- NEW EMAIL ---")
                    print(f"Subject: {full_content['subject']}")
                    print(f"From: {full_content['from']}")
                    print(f"To: {full_content['to']}")
                    print(f"Date: {full_content['date']}")
                    print("\n--- EMAIL BODY ---")
                    print(full_content['body'])
                    print("\n" + "-"*50)
                
                # Update last processed email
                last_email_id = email_ids[-1]
            else:
                print("No new emails.")
            
            # Close the connection
            mail.close()
            mail.logout()
            
            # Wait before next check
            print(f"Waiting {check_interval} seconds before next check...")
            time.sleep(check_interval)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Retrying in {check_interval} seconds...")
            time.sleep(check_interval)


if __name__ == "__main__":
    
    fetch_new_emails(
        username='ragtest209@gmail.com',
        password='espq juva cclw ecxn',
        imap_server='imap.gmail.com',
        check_interval=9  
    )