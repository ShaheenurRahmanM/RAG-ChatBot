#!/usr/bin/env python3
"""
SWS AI Policy Assistant - Example PDF Creator
Creates a sample PDF for testing without needing external PDFs
"""

import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
except ImportError:
    print("Error: reportlab not installed")
    print("Install it with: pip install reportlab")
    sys.exit(1)

def create_sample_pdf():
    """Create a sample leave policy PDF for testing"""
    
    pdf_path = "backend/data/pdfs/Sample_Leave_Policy.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Define styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#0066cc',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#0052a3',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    # Add content
    story.append(Paragraph("SWS AI COMPANY", title_style))
    story.append(Paragraph("Leave Policy", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("1. ANNUAL LEAVE ENTITLEMENT", heading_style))
    story.append(Paragraph(
        "All full-time employees are entitled to 20 days of paid annual leave per calendar year. "
        "Part-time employees receive annual leave on a pro-rata basis. Annual leave is calculated "
        "based on the employee's start date and is available immediately upon employment.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2. LEAVE REQUEST PROCEDURES", heading_style))
    story.append(Paragraph(
        "Employees must submit leave requests at least 2 weeks in advance through the HR management "
        "system. Emergency leave requests should be communicated to the direct manager immediately. "
        "All leave requests require manager approval. During peak periods (December and summer), "
        "approval depends on business needs and team availability.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("3. SICK LEAVE", heading_style))
    story.append(Paragraph(
        "Employees are entitled to 10 days of paid sick leave per year. Medical certificates are required "
        "for absences exceeding 3 consecutive days. Unused sick leave does not carry over to the next year. "
        "Sick leave must be reported to your manager within 2 hours of absence.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("4. PUBLIC HOLIDAYS", heading_style))
    story.append(Paragraph(
        "All employees receive paid public holidays as per national laws. These are in addition to "
        "annual leave entitlements. If an employee is required to work on a public holiday, "
        "they receive double pay plus time-off in lieu.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("5. PARENTAL LEAVE", heading_style))
    story.append(Paragraph(
        "Maternity leave: 4 months paid leave for birth mothers. Paternity leave: 2 weeks paid leave. "
        "Adoption leave: 3 months paid leave. All parental leave must be taken within 12 months of birth/adoption. "
        "Benefits continuation during parental leave is guaranteed.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("6. LEAVE RECORD KEEPING", heading_style))
    story.append(Paragraph(
        "HR maintains detailed records of all employee leave. Employees can view their leave balance "
        "through the HR portal. Annual leave balances are reset on January 1st each year. "
        "Unused leave from the previous year expires unless otherwise approved in writing.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("7. CONTACT INFORMATION", heading_style))
    story.append(Paragraph(
        "For leave-related inquiries, contact the HR Department:<br/>"
        "Email: hr@swsai.com<br/>"
        "Phone: +1 (555) 123-4567<br/>"
        "Office: Building A, 2nd Floor, HR Department",
        body_style
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Sample PDF created: {pdf_path}")
    print("  You can now test the application with this PDF")
    print("  Run: python app/ingest.py")

if __name__ == "__main__":
    try:
        create_sample_pdf()
    except Exception as e:
        print(f"Error creating PDF: {e}")
        print("\nTo create PDFs, install reportlab:")
        print("  pip install reportlab")
