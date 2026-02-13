from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from auth import get_credentials

def send_decision_email(to_email, score, current_limit, recommended_limit, explanation):
    """
    Sends a credit decision email using the Gmail API.
    """
    creds = get_credentials()
    if not creds:
        return False, "Authentication credentials not found."

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        subject = "Your Dynamic Credit Limit Analysis Report"
        body = f"""
        Dear Customer ({to_email}),

        Thank you for using the Dynamic Credit Limit Analyzer. Our system has completed the analysis of your transaction behavior.

        CREDIT DECISION SUMMARY:
        -------------------------
        Current Credit Limit: ₹{current_limit:,.2f}
        Final Credit Score: {score}/100
        Recommended Credit Limit: ₹{recommended_limit:,.2f}
        
        Decision Reason:
        {explanation}

        This decision was reached based on your repayment history, spending stability, and credit utilization ratio.

        Best regards,
        Credit Decision Engine
        Dynamic Bank Ltd.
        """

        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        send_message = service.users().messages().send(
            userId="me", 
            body={'raw': raw_message}
        ).execute()
        
        return True, f"Email sent successfully! Message ID: {send_message['id']}"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
