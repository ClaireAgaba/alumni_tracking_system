import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.conf import settings
from datetime import date
import logging
import traceback

logger = logging.getLogger(__name__)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def generate_graduate_pdf(response, graduates):
    """Generate PDF with UBTEB header and graduate details."""
    logger.info("Starting PDF generation...")
    
    try:
        # Create the PDF object using the response object as its "file"
        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),  # Use landscape orientation
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
            title="Graduate Details"
        )

        # Container for the 'Flowable' objects
        elements = []
        
        # Create styles
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica-Bold',
        )
        
        contact_left_style = ParagraphStyle(
            'ContactLeft',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            fontName='Helvetica',
        )
        
        contact_center_style = ParagraphStyle(
            'ContactCenter',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            fontName='Helvetica',
        )
        
        contact_right_style = ParagraphStyle(
            'ContactRight',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            fontName='Helvetica',
        )
        
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold',
        )

        # Create header table
        header_text = Paragraph('<b>UGANDA BUSINESS AND TECHNICAL EXAMINATIONS BOARD</b>', header_style)
        elements.append(header_text)
        elements.append(Spacer(1, 10))
        
        # Get logo
        logo_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'images', 'ubteb_logo.jpg'))
        logger.debug(f"Looking for logo at: {logo_path}")
        
        if os.path.exists(logo_path):
            logger.debug("Logo file found!")
            try:
                img = Image(logo_path)
                img.drawHeight = 1*inch
                img.drawWidth = 1*inch
            except Exception as e:
                logger.error(f"Error processing logo: {str(e)}")
                img = None
        else:
            logger.warning(f"Logo file not found at {logo_path}")
            img = None

        # Create contact info table with 3 columns
        address_info = Paragraph('''
            <b>Address:</b><br/>
            P.O.Box 1499<br/>
            Kampala, Uganda
        ''', contact_left_style)
        
        logo_cell = img if img else Paragraph('', contact_center_style)
        
        contact_info = Paragraph('''
            <b>Contact:</b><br/>
            Tel: +256 414 289786<br/>
            Email: info@ubteb.go.ug
        ''', contact_right_style)
        
        # Create table for header layout
        header_table_data = [[address_info, logo_cell, contact_info]]
        header_table = Table(header_table_data, colWidths=[doc.width/3.0]*3)
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 20))
        
        # Add title
        elements.append(Paragraph('List of Graduates', title_style))
        
        # Create the graduates table
        logger.debug("Creating table...")
        try:
            # Define column headers
            data = [['Name', 'Age', 'Course', 'Institution', 'District', 'Contact', 'Employment Status']]
            
            for graduate in graduates:
                # Calculate age
                age = calculate_age(graduate.date_of_birth) if graduate.date_of_birth else ''
                
                # Format contact information
                contact = f"Tel: {graduate.phone_number}"
                if graduate.email:
                    contact += f"\nEmail: {graduate.email}"
                
                # Add row data
                data.append([
                    Paragraph(f"{graduate.first_name} {graduate.last_name}", styles['Normal']),
                    Paragraph(str(age), styles['Normal']),
                    Paragraph(graduate.course.name if graduate.course else '', styles['Normal']),
                    Paragraph(graduate.exam_center.name if graduate.exam_center else '', styles['Normal']),
                    Paragraph(graduate.exam_center.district.name if graduate.exam_center and graduate.exam_center.district else '', styles['Normal']),
                    Paragraph(contact, styles['Normal']),
                    Paragraph('Employed' if graduate.is_employed else 'Not Employed', styles['Normal'])
                ])

            # Create table with specific widths for landscape orientation
            table = Table(data, colWidths=[
                doc.width*0.18,  # Name
                doc.width*0.07, # Age
                doc.width*0.18,  # Course
                doc.width*0.18,  # Institution
                doc.width*0.12, # District
                doc.width*0.12,  # Contact
                doc.width*0.15   # Employment Status
            ], repeatRows=1)
            
            # Style the table
            table.setStyle(TableStyle([
                # Header style
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),  # Slightly reduced font size
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                
                # Data rows style
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                # Allow word wrapping
                ('WORDWRAP', (0, 0), (-1, -1), True),
                # Minimum row height
                ('MINROWHEIGHT', (0, 0), (-1, -1), 40),
            ]))
            
            elements.append(table)
        except Exception as e:
            logger.error(f"Error creating table: {str(e)}")
            raise

        logger.debug("Building PDF...")
        try:
            doc.build(elements)
            logger.info("PDF generation completed successfully!")
        except Exception as e:
            logger.error(f"Error building PDF: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
            
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
