"""
PDF Health Checker
Scans directory trees for PDF files and performs comprehensive integrity checks
Automatically quarantines damaged files and generates detailed reports
"""

import os
import shutil
from pathlib import Path
import PyPDF2
from PyPDF2.errors import PdfReadError

# Configuration
PARENT_FOLDER = "Cambridge_Past_Papers_0971"
DAMAGE_FOLDER = os.path.join(PARENT_FOLDER, "DAMAGED_FILES")

# Statistics
stats = {
    'total_files': 0,
    'healthy_files': 0,
    'damaged_files': 0,
    'moved_files': 0
}


def is_pdf_valid(file_path):
    """
    Check if a PDF file is valid and not corrupted.
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            
            if num_pages == 0:
                return False, "No pages found"
            
            # Try to read the first page
            try:
                first_page = pdf_reader.pages[0]
            except:
                return False, "Cannot read pages"
            
            return True, f"Valid ({num_pages} pages)"
    except PdfReadError as e:
        return False, f"PDF Read Error: {str(e)[:50]}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def move_to_damage(file_path, reason):
    """
    Move damaged file to damage folder with folder structure preservation.
    
    Args:
        file_path (str): Path to damaged file
        reason (str): Reason for damage classification
        
    Returns:
        tuple: (success: bool, destination_path: str)
    """
    try:
        rel_path = os.path.relpath(file_path, PARENT_FOLDER)
        damage_subfolder = os.path.join(DAMAGE_FOLDER, os.path.dirname(rel_path))
        Path(damage_subfolder).mkdir(parents=True, exist_ok=True)
        
        dest_path = os.path.join(damage_subfolder, os.path.basename(file_path))
        shutil.move(file_path, dest_path)
        
        return True, dest_path
    except Exception as e:
        return False, str(e)


def check_file_size(file_path):
    """
    Check if file size is suspiciously small.
    
    Args:
        file_path (str): Path to file
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    file_size = os.path.getsize(file_path)
    if file_size < 1024:
        return False, f"Suspiciously small ({file_size} bytes)"
    return True, f"Size OK ({file_size / 1024:.1f} KB)"


def scan_directory():
    """
    Scan parent folder for PDF files and perform health checks.
    """
    Path(DAMAGE_FOLDER).mkdir(exist_ok=True)
    
    print(f"Starting health check on: {PARENT_FOLDER}\n")
    print("=" * 80)
    
    for root, dirs, files in os.walk(PARENT_FOLDER):
        if "DAMAGED_FILES" in root:
            continue
        
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                stats['total_files'] += 1
                
                # Check file size first
                size_valid, size_msg = check_file_size(file_path)
                
                if not size_valid:
                    is_valid = False
                    reason = size_msg
                else:
                    is_valid, reason = is_pdf_valid(file_path)
                
                rel_path = os.path.relpath(file_path, PARENT_FOLDER)
                
                if is_valid:
                    stats['healthy_files'] += 1
                    print(f"✓ HEALTHY: {rel_path}")
                    print(f"  └─ {reason}")
                else:
                    stats['damaged_files'] += 1
                    print(f"✗ DAMAGED: {rel_path}")
                    print(f"  └─ {reason}")
                    
                    success, result = move_to_damage(file_path, reason)
                    if success:
                        stats['moved_files'] += 1
                        print(f"  └─ Moved to: {os.path.relpath(result, PARENT_FOLDER)}")
                    else:
                        print(f"  └─ Error moving file: {result}")


def print_summary():
    """Print health check summary."""
    print("\n" + "=" * 80)
    print("HEALTH CHECK SUMMARY")
    print("=" * 80)
    print(f"Total PDF Files:     {stats['total_files']}")
    print(f"Healthy Files:       {stats['healthy_files']} ✓")
    print(f"Damaged Files:       {stats['damaged_files']} ✗")
    print(f"Files Moved:         {stats['moved_files']}")
    print(f"\nDamaged files moved to: {DAMAGE_FOLDER}")
    print("\nHealth Check Complete!")


def save_report():
    """Save health check report to file."""
    report_path = os.path.join(PARENT_FOLDER, "HEALTH_CHECK_REPORT.txt")
    with open(report_path, 'w') as f:
        f.write("PDF HEALTH CHECK REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total PDF Files:     {stats['total_files']}\n")
        f.write(f"Healthy Files:       {stats['healthy_files']}\n")
        f.write(f"Damaged Files:       {stats['damaged_files']}\n")
        f.write(f"Files Moved:         {stats['moved_files']}\n\n")
        f.write(f"Damaged files location: {DAMAGE_FOLDER}\n")
    
    print(f"\nReport saved to: {report_path}")


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("PDF HEALTH CHECKER")
    print("=" * 80 + "\n")
    
    scan_directory()
    print_summary()
    save_report()


if __name__ == '__main__':
    main()