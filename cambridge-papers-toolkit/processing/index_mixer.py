"""
Index and Content PDF Mixer
Combines index PDFs with release PDFs
Attempts Adobe Acrobat first, falls back to PyPDF2
"""

import os
import subprocess
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader


def merge_pdfs_adobe(index_pdf_path, release_pdf_path, output_path):
    """
    Merge PDFs using Adobe Acrobat Command Line.
    
    Args:
        index_pdf_path (str): Path to index PDF
        release_pdf_path (str): Path to release PDF
        output_path (str): Output path
        
    Returns:
        bool: Success status
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        adobe_paths = [
            r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
            r"C:\Program Files (x86)\Adobe\Acrobat Reader\Reader\AcroRd32.exe",
            r"C:\Program Files\Adobe\Acrobat\Acrobat.exe",
        ]
        
        adobe_exe = None
        for path in adobe_paths:
            if os.path.exists(path):
                adobe_exe = path
                break
        
        if not adobe_exe:
            print("  ✗ Adobe Acrobat not found. Using alternative method with pypdf...")
            return merge_pdfs_pypdf(index_pdf_path, release_pdf_path, output_path)
        
        js_file = output_path.replace('.pdf', '_merge.js')
        
        with open(js_file, 'w') as f:
            f.write(f'''
var doc = app.openDoc("{index_pdf_path}");
doc.insertPages({{
    nIndex: 0,
    cPath: "{release_pdf_path}",
    nStart: 0,
    nEnd: -1
}});
doc.saveAs("{output_path}");
doc.close();
app.exit();
''')
        
        subprocess.run([adobe_exe, '/s', '/o', '/n', js_file], check=True)
        
        if os.path.exists(js_file):
            os.remove(js_file)
        
        print(f"✓ Created: {output_path}\n")
        return True
        
    except Exception as e:
        print(f"  Error with Adobe method: {e}")
        print("  Falling back to pypdf method...\n")
        return merge_pdfs_pypdf(index_pdf_path, release_pdf_path, output_path)


def merge_pdfs_pypdf(index_pdf_path, release_pdf_path, output_path):
    """
    Fallback method using PyPDF2.
    
    Args:
        index_pdf_path (str): Path to index PDF
        release_pdf_path (str): Path to release PDF
        output_path (str): Output path
        
    Returns:
        bool: Success status
    """
    try:
        merger = PdfMerger()
        
        merger.append(index_pdf_path)
        merger.append(release_pdf_path)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as out_file:
            merger.write(out_file)
        
        merger.close()
        print(f"✓ Created: {output_path}\n")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}\n")
        return False


def main():
    """Main execution function."""
    base_dir = Path('.') / 'OL-Past_Paper_Release'
    index_dir = base_dir / 'Index'
    release_dir = base_dir / 'Release_PDF'
    output_dir = base_dir / 'Merged_PDF'
    
    print(f"Current working directory: {os.getcwd()}\n")
    print("Using Adobe PDF for merging (with PyPDF2 fallback)\n")
    
    papers = [
        ('Paper 2', 'Paper_2'),
        ('Paper 4', 'Paper_4'),
        ('Paper 6', 'Paper_6')
    ]
    types = ['MS', 'QP']
    
    print("Starting PDF merge process...\n")
    
    for paper_folder, paper_name in papers:
        for doc_type in types:
            print(f"Processing {paper_name} - {doc_type}:")
            
            index_path = str(index_dir / paper_folder / doc_type / f'{paper_name}_{doc_type}_Index.pdf')
            release_path = str(release_dir / paper_name / doc_type / f'{paper_name}_{doc_type}.pdf')
            output_path = str(output_dir / paper_name / f'{paper_name}_{doc_type}_Merged.pdf')
            
            if not os.path.exists(index_path):
                print(f"  ✗ Index not found: {index_path}")
                continue
            if not os.path.exists(release_path):
                print(f"  ✗ Release PDF not found: {release_path}")
                continue
            
            merge_pdfs_adobe(index_path, release_path, output_path)
    
    print("Process complete!")


if __name__ == '__main__':
    main()