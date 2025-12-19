"""
PDF Cleaner and Repair Tool
Repairs corrupted PDFs using multiple strategies
Creates backups before modifications and generates detailed logs
"""

import os
import shutil
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from pikepdf import Pdf
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_cleaning.log'),
        logging.StreamHandler()
    ]
)


class PDFCleaner:
    """PDF cleaning and repair utility."""
    
    def __init__(self, root_directory):
        """
        Initialize PDF Cleaner.
        
        Args:
            root_directory (str): Root directory to scan for PDFs
        """
        self.root_dir = Path(root_directory)
        self.backup_dir = self.root_dir / "PDF_Backups"
        self.error_dir = self.root_dir / "PDF_Errors"
        self.stats = {
            'total': 0,
            'cleaned': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def setup_directories(self):
        """Create backup and error directories."""
        self.backup_dir.mkdir(exist_ok=True)
        self.error_dir.mkdir(exist_ok=True)
        logging.info(f"Backup directory: {self.backup_dir}")
        logging.info(f"Error directory: {self.error_dir}")
    
    def find_all_pdfs(self):
        """
        Recursively find all PDF files.
        
        Returns:
            list: List of PDF file paths
        """
        pdf_files = list(self.root_dir.rglob("*.pdf"))
        pdf_files.extend(self.root_dir.rglob("*.PDF"))
        logging.info(f"Found {len(pdf_files)} PDF files")
        return pdf_files
    
    def backup_pdf(self, pdf_path):
        """
        Create backup of original PDF.
        
        Args:
            pdf_path (Path): Path to PDF file
        """
        relative_path = pdf_path.relative_to(self.root_dir)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf_path, backup_path)
        logging.info(f"Backed up: {pdf_path.name}")
    
    def clean_with_pikepdf(self, pdf_path):
        """
        Clean PDF using pikepdf (more robust for corrupted files).
        
        Args:
            pdf_path (Path): Path to PDF file
            
        Returns:
            bool: Success status
        """
        try:
            with Pdf.open(pdf_path, allow_overwriting_input=True) as pdf:
                if pdf.is_encrypted:
                    logging.info(f"Removing encryption from: {pdf_path.name}")
                
                for page in pdf.pages:
                    page.remove_unreferenced_resources()
                
                pdf.save(pdf_path, 
                        linearize=True,
                        compress_streams=True,
                        preserve_pdfa=False,
                        min_version="1.4")
                
                return True
        except Exception as e:
            logging.error(f"pikepdf failed for {pdf_path.name}: {str(e)}")
            return False
    
    def clean_with_pypdf2(self, pdf_path):
        """
        Clean PDF using PyPDF2 (fallback method).
        
        Args:
            pdf_path (Path): Path to PDF file
            
        Returns:
            bool: Success status
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            if reader.is_encrypted:
                logging.info(f"Removing encryption (PyPDF2): {pdf_path.name}")
            
            with open(pdf_path, 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            logging.error(f"PyPDF2 failed for {pdf_path.name}: {str(e)}")
            return False
    
    def verify_pdf(self, pdf_path):
        """
        Verify PDF can be opened and read.
        
        Args:
            pdf_path (Path): Path to PDF file
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            with Pdf.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                if num_pages == 0:
                    return False, "No pages found"
                return True, f"Valid PDF with {num_pages} pages"
        except Exception as e:
            return False, str(e)
    
    def move_to_errors(self, pdf_path):
        """
        Move problematic PDFs to error directory.
        
        Args:
            pdf_path (Path): Path to PDF file
        """
        relative_path = pdf_path.relative_to(self.root_dir)
        error_path = self.error_dir / relative_path
        error_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf_path), str(error_path))
        logging.warning(f"Moved to errors: {pdf_path.name}")
    
    def clean_pdf(self, pdf_path):
        """
        Main cleaning process for a single PDF.
        
        Args:
            pdf_path (Path): Path to PDF file
            
        Returns:
            bool: Success status
        """
        self.stats['total'] += 1
        logging.info(f"\n{'='*60}")
        logging.info(f"Processing [{self.stats['total']}]: {pdf_path.name}")
        logging.info(f"Path: {pdf_path.relative_to(self.root_dir)}")
        
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            logging.error(f"File missing or empty: {pdf_path.name}")
            self.stats['failed'] += 1
            return False
        
        is_valid, msg = self.verify_pdf(pdf_path)
        if is_valid:
            logging.info(f"Pre-check: {msg}")
        else:
            logging.warning(f"Pre-check failed: {msg}")
        
        try:
            self.backup_pdf(pdf_path)
        except Exception as e:
            logging.error(f"Backup failed: {str(e)}")
            self.stats['failed'] += 1
            return False
        
        success = self.clean_with_pikepdf(pdf_path)
        
        if not success:
            logging.info("Trying PyPDF2 as fallback...")
            success = self.clean_with_pypdf2(pdf_path)
        
        if success:
            is_valid, msg = self.verify_pdf(pdf_path)
            if is_valid:
                logging.info(f"✓ Successfully cleaned: {msg}")
                self.stats['cleaned'] += 1
                return True
            else:
                logging.error(f"Verification failed after cleaning: {msg}")
                self.move_to_errors(pdf_path)
                self.stats['failed'] += 1
                return False
        else:
            logging.error(f"✗ Failed to clean")
            self.move_to_errors(pdf_path)
            self.stats['failed'] += 1
            return False
    
    def clean_all(self):
        """Clean all PDFs in the directory tree."""
        print("\n" + "="*60)
        print("PDF CLEANER - Starting Process")
        print("="*60 + "\n")
        
        self.setup_directories()
        pdf_files = self.find_all_pdfs()
        
        if not pdf_files:
            logging.warning("No PDF files found!")
            return
        
        print(f"\nFound {len(pdf_files)} PDF files to process")
        response = input("Do you want to continue? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("Operation cancelled.")
            return
        
        for pdf_path in pdf_files:
            self.clean_pdf(pdf_path)
        
        print("\n" + "="*60)
        print("CLEANING COMPLETE - SUMMARY")
        print("="*60)
        print(f"Total PDFs found:      {self.stats['total']}")
        print(f"Successfully cleaned:  {self.stats['cleaned']}")
        print(f"Failed/Moved to errors: {self.stats['failed']}")
        print(f"Success rate:          {(self.stats['cleaned']/self.stats['total']*100):.1f}%")
        print(f"\nBackups saved in:      {self.backup_dir}")
        print(f"Problem files in:      {self.error_dir}")
        print(f"Detailed log:          pdf_cleaning.log")
        print("="*60 + "\n")


def main():
    """Main execution function."""
    ROOT_DIRECTORY = "."
    
    cleaner = PDFCleaner(ROOT_DIRECTORY)
    cleaner.clean_all()


if __name__ == "__main__":
    main()