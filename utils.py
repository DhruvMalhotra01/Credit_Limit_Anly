from fpdf import FPDF
import base64

class CreditReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'DYNAMIC CREDIT LIMIT ANALYZER - REPORT', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(user_email, current_limit, score_data, decision_data):
    """
    Generates a PDF report for the credit decision.
    decision_data: (score, recommended_limit, explanation_text)
    """
    score, recommended_limit, explanation_text = decision_data
    
    pdf = CreditReportPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # User Info
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Customer Email: {user_email}", 0, 1)
    pdf.cell(0, 10, f"Current Credit Limit: Rs. {current_limit:,.2f}", 0, 1)
    pdf.ln(5)
    
    # Scores
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "1. Behavioral Scores", 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"Final Credit Score: {score}/100", 0, 1)
    pdf.cell(0, 8, f"Repayment Score: {score_data['repayment_score']}/100", 0, 1)
    pdf.cell(0, 8, f"Utilization Ratio: {score_data['utilization_ratio']}%", 0, 1)
    pdf.cell(0, 8, f"Stability Score: {score_data['stability_score']}/100", 0, 1)
    pdf.cell(0, 8, f"Lifestyle Score: {score_data['lifestyle_score']}/100", 0, 1)
    pdf.ln(5)
    
    # Decision
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "2. Decision Recommendation", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"New Recommended Limit: Rs. {recommended_limit:,.2f}", 0, 1)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, f"Behavior Summary & Reasoning: {explanation_text}")
    
    return pdf.output(dest='S').encode('latin-1')

def get_table_download_link(df, filename="data.csv"):
    """Generates a link to download the dataframe as a CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
