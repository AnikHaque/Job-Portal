from datetime import timedelta
from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

FEATURED_PACKAGES = {
    '7': {'days': 7, 'price': 499},
    '14': {'days': 14, 'price': 899},
    '30': {'days': 30, 'price': 1499},
}

def apply_featured(job, days):
    job.is_featured = True
    job.featured_until = timezone.now() + timedelta(days=days)
    job.save()

def generate_invoice_pdf(payment):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>JobPortal Invoice</b>", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Invoice ID:</b> {payment.id}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {payment.created_at.strftime('%d %b %Y')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Status:</b> {payment.status}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [
        ['Company', payment.job.company.name],
        ['Job Title', payment.job.title],
        ['Featured Duration', f'{payment.days} days'],
        ['Amount Paid', f'৳ {payment.amount}'],
    ]

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])
    elements.append(table)

    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Thank you for your business.", styles['Italic']))

    doc.build(elements)
    return response

def send_application_email(application, status):
    try:
        subject = ''
        template = ''

        if status == 'shortlisted':
            subject = 'You have been shortlisted!'
            template = 'emails/shortlisted.html'
        elif status == 'rejected':
            subject = 'Application Update'
            template = 'emails/rejected.html'
        else:
            return

        message = render_to_string(template, {
            'name': application.applicant.username,
            'job': application.job.title,
            'company': application.job.company.name,
        })

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [application.applicant.email],
            html_message=message,
            fail_silently=False,   # debug mode
        )

    except Exception as e:
        print("EMAIL ERROR:", e)