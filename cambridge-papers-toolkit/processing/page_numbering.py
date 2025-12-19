"""
PDF Page Numbering Tool
Adds centered page numbers to PDFs starting from a specific page
Configurable start page and start number
"""

import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


def add_centered_page_numbers(input_pdf, output_pdf, start_from_page=3, start_number=1):
    """
    Add centered page numbers to a PDF starting from a specific page.
    
    Args:
        input_pdf (str): Path to input PDF
        output_pdf (str): Path to output PDF
        start_from_page (int): Which page to start numbering (1-indexed, default page 3)
        start_number (int): What number to start with (default 1)
        
    Returns:
        bool: Success status
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        print(f"  Total pages: {total_pages}")
        print(f"  Adding numbers starting from page {start_from_page}")
        
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            if page_num >= start_from_page - 1:
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                
                current_page_num = start_number + (page_num - (start_from_page - 1))
                
                can.setFont("Helvetica", 10)
                text_width = can.stringWidth(str(current_page_num), "Helvetica", 10)
                center_x = (page_width - text_width) / 2
                can.drawString(center_x, 20, str(current_page_num))
                
                can.save()
                packet.seek(0)
                
                number_pdf = PdfReader(packet)
                page.merge_page(number_pdf.pages[0])
            
            writer.add_page(page)
        
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        
        print(f"✓ Numbered: {os.path.basename(output_pdf)}\n")
        return True
        
    except Exception as e:
        print(f"✗ Error numbering PDF: {e}\n")
        return False


def main():
    """Main execution function."""
    base_dir = Path('.') / 'OL-Past_Paper_Release'
    merged_dir = base_dir / 'Merged_PDF'
    numbered_dir = base_dir / 'Numbered_PDF'
    
    print(f"Current working directory: {os.getcwd()}\n")
    print("="*60)
    print("Adding Centered Page Numbers (Starting from Page 3)")
    print("="*60 + "\n")
    
    papers = [
        ('Paper_2', ['MS', 'QP']),
        ('Paper_4', ['MS', 'QP']),
        ('Paper_6', ['MS', 'QP'])
    ]
    
    for paper_name, types in papers:
        for doc_type in types:
            input_filename = f'{paper_name}_{doc_type}_Merged.pdf'
            input_path = merged_dir / paper_name / input_filename
            
            output_filename = f'{paper_name}_{doc_type}_Numbered.pdf'
            output_path = numbered_dir / paper_name / output_filename
            
            if not input_path.exists():
                print(f"Processing {paper_name} - {doc_type}:")
                print(f"  ✗ Input file not found: {input_path}\n")
                continue
            
            print(f"Processing {paper_name} - {doc_type}:")
            add_centered_page_numbers(
                str(input_path), 
                str(output_path),
                start_from_page=3,
                start_number=1
            )
    
    print("="*60)
    print("Process complete!")
    print("="*60)
    print(f"\nOutput directory: {numbered_dir}")


if __name__ == '__main__':
    main()