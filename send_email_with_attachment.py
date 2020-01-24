subject = 'Testing'
body = 'Works!'
recipients = ['bob@example.com']

def send(account=account, subject=subject, body=body, recipients=recipients, attachments=[]):
    """
    Send an email.

    Parameters
    ----------
    account : Account object
    subject : str
    body : str
    recipients : list of str
        Each str is an email adress
    attachments : list of str
        Each str is a path of file

    Examples
    --------
    >>> send_email(account, 'Subject line', 'Hello!', ['info@example.com'])
    """
    to_recipients = []
    for recipient in recipients:
        to_recipients.append(Mailbox(email_address=recipient))
    # Create message
    m = Message(account=account,
                subject=subject,
                body=body,
                to_recipients=to_recipients)

    # Read attachment
    # attachments : list of tuples or None
    # (filename, binary contents)
    files = []
    for file in attachments:
        with open(file, 'rb') as f:
            content = f.read()
        files.append((file, content))

    # attach files
    for attachment_name, attachment_content in files or []:
        file = FileAttachment(name=attachment_name, content=attachment_content)
        m.attach(file)
    m.send()