"""
Cambridge IGCSE Chemistry (0620) Past Papers Downloader
Downloads papers from physicsandmathstutor.com
Handles multiple variants (v1, v2, v3) and specimen papers
"""

import os
import time
import re
import requests
from pathlib import Path
from urllib.parse import quote

# Configuration
BASE_URL = "https://pmt.physicsandmathstutor.com/download/Chemistry/GCSE/Past-Papers/CIE/"
OUTPUT_DIR = "Cambridge_Past_Papers_0620"
DELAY_BETWEEN_DOWNLOADS = 2  # seconds

# Paper definitions
PAPERS = {
    "Paper-2": {
        "QP": [
            'June 2010 (v1)', 'June 2010 (v2)', 'June 2010 (v3)',
            'June 2011 (v1)', 'June 2011 (v2)',
            'June 2012 (v1)', 'June 2012 (v2)', 'June 2012 (v3)',
            'June 2013 (v1)', 'June 2013 (v3)',
            'June 2014 (v1)', 'June 2014 (v2)', 'June 2014 (v3)',
            'June 2015 (v1)',
            'June 2016 (v1)', 'June 2016 (v2)', 'June 2016 (v3)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018 (v1)', 'June 2018 (v2)', 'June 2018 (v3)',
            'June 2019 (v1)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)', 'June 2020 (v3)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2015 (v2)', 'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2010 (v1)', 'November 2010 (v2)', 'November 2010 (v3)',
            'November 2011 (v1)', 'November 2011 (v2)', 'November 2011 (v3)',
            'November 2012 (v1)', 'November 2012 (v2)', 'November 2012 (v3)',
            'November 2013 (v1)', 'November 2013 (v2)', 'November 2013 (v3)',
            'November 2014 (v1)', 'November 2014 (v2)', 'November 2014 (v3)',
            'November 2015 (v1)', 'November 2015 (v2)', 'November 2015 (v3)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ],
        "MS": [
            'June 2010 (v1)', 'June 2010 (v2)',
            'June 2011 (v1)', 'June 2011 (v2)',
            'June 2012 (v1)', 'June 2012 (v2)', 'June 2012 (v3)',
            'June 2013 (v1)', 'June 2013 (v2)', 'June 2013 (v3)',
            'June 2014 (v1)', 'June 2014 (v2)', 'June 2014 (v3)',
            'June 2015 (v1)',
            'June 2016 (v1)', 'June 2016 (v2)', 'June 2016 (v3)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018 (v1)', 'June 2018 (v2)', 'June 2018 (v3)',
            'June 2019 (v1)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2015 (v2)', 'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2010 (v1)', 'November 2010 (v2)', 'November 2010 (v3)',
            'November 2011 (v1)', 'November 2011 (v2)', 'November 2011 (v3)',
            'November 2012 (v1)', 'November 2012 (v2)', 'November 2012 (v3)',
            'November 2013 (v1)', 'November 2013 (v2)', 'November 2013 (v3)',
            'November 2014 (v1)', 'November 2014 (v2)', 'November 2014 (v3)',
            'November 2015 (v1)', 'November 2015 (v2)', 'November 2015 (v3)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ]
    },
    "Paper-4": {
        "QP": [
            'June 2016 (v1)', 'June 2016 (v2)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018 (v1)', 'June 2018 (v3)',
            'June 2019 (v1)', 'June 2019 (v2)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)', 'June 2020 (v3)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ],
        "MS": [
            'June 2016 (v1)', 'June 2016 (v2)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018 (v1)', 'June 2018 (v3)',
            'June 2019 (v1)', 'June 2019 (v2)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)', 'June 2020 (v3)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ]
    },
    "Paper-6": {
        "QP": [
            'June 2010 (v1)', 'June 2010 (v2)', 'June 2010 (v3)',
            'June 2011 (v1)', 'June 2011 (v2)', 'June 2011 (v3)',
            'June 2012 (v1)', 'June 2012 (v2)', 'June 2012 (v3)',
            'June 2013 (v1)', 'June 2013 (v2)', 'June 2013 (v3)',
            'June 2014 (v1)', 'June 2014 (v2)', 'June 2014 (v3)',
            'June 2015 (v1)',
            'June 2016 (v1)', 'June 2016 (v2)', 'June 2016 (v3)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018',
            'June 2019 (v1)', 'June 2019 (v2)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)', 'June 2020 (v3)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2015 (v2)', 'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2010 (v1)', 'November 2010 (v2)', 'November 2010 (v3)',
            'November 2011 (v1)', 'November 2011 (v2)', 'November 2011 (v3)',
            'November 2012 (v1)', 'November 2012 (v2)', 'November 2012 (v3)',
            'November 2013 (v1)', 'November 2013 (v2)', 'November 2013 (v3)',
            'November 2014 (v1)', 'November 2014 (v2)', 'November 2014 (v3)',
            'November 2015 (v1)', 'November 2015 (v2)', 'November 2015 (v3)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ],
        "MS": [
            'June 2010 (v1)', 'June 2010 (v2)', 'June 2010 (v3)',
            'June 2011 (v1)', 'June 2011 (v2)', 'June 2011 (v3)',
            'June 2012 (v1)', 'June 2012 (v2)', 'June 2012 (v3)',
            'June 2013 (v1)', 'June 2013 (v2)', 'June 2013 (v3)',
            'June 2014 (v1)', 'June 2014 (v2)', 'June 2014 (v3)',
            'June 2015 (v1)',
            'June 2016 (v1)', 'June 2016 (v2)', 'June 2016 (v3)',
            'June 2017 (v1)', 'June 2017 (v2)', 'June 2017 (v3)',
            'June 2018',
            'June 2019 (v1)', 'June 2019 (v2)', 'June 2019 (v3)',
            'June 2020 (v1)', 'June 2020 (v2)', 'June 2020 (v3)',
            'June 2021 (v1)', 'June 2021 (v2)', 'June 2021 (v3)',
            'June 2022 (v1)', 'June 2022 (v2)', 'June 2022 (v3)',
            'June 2023 (v1)', 'June 2023 (v2)', 'June 2023 (v3)',
            'June 2024 (v1)', 'June 2024 (v2)', 'June 2024 (v3)',
            'March 2015 (v2)', 'March 2016 (v2)', 'March 2017 (v2)', 'March 2018 (v2)', 'March 2019 (v2)',
            'March 2020 (v2)', 'March 2021 (v2)', 'March 2022 (v2)', 'March 2023 (v2)', 'March 2024 (v2)',
            'November 2010 (v1)', 'November 2010 (v2)', 'November 2010 (v3)',
            'November 2011 (v1)', 'November 2011 (v2)', 'November 2011 (v3)',
            'November 2012 (v1)', 'November 2012 (v2)', 'November 2012 (v3)',
            'November 2013 (v1)', 'November 2013 (v2)', 'November 2013 (v3)',
            'November 2014 (v1)', 'November 2014 (v2)', 'November 2014 (v3)',
            'November 2015 (v1)', 'November 2015 (v2)', 'November 2015 (v3)',
            'November 2016 (v1)', 'November 2016 (v2)', 'November 2016 (v3)',
            'November 2017 (v1)', 'November 2017 (v2)', 'November 2017 (v3)',
            'November 2018 (v1)', 'November 2018 (v2)', 'November 2018 (v3)',
            'November 2019 (v1)', 'November 2019 (v2)', 'November 2019 (v3)',
            'November 2020 (v1)', 'November 2020 (v2)', 'November 2020 (v3)',
            'November 2021 (v1)', 'November 2021 (v2)', 'November 2021 (v3)',
            'November 2022 (v1)', 'November 2022 (v2)', 'November 2022 (v3)',
            'November 2023 (v1)', 'November 2023 (v2)', 'November 2023 (v3)',
            'November 2024 (v1)', 'November 2024 (v2)', 'November 2024 (v3)',
            'Specimen 2016', 'Specimen 2020', 'Specimen 2023'
        ]
    }
}


def parse_paper_info(paper_str):
    """Extract year, month, and variant from paper string."""
    if 'Specimen' in paper_str:
        match = re.search(r'Specimen (\d{4})', paper_str)
        if match:
            return match.group(1), 'Specimen', None
    
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})(?: \(v(\d+)\))?', paper_str)
    if match:
        month = match.group(1)
        year = match.group(2)
        variant = match.group(3) if match.group(3) else None
        return year, month, variant
    
    return None, None, None


def build_url(paper_num, doc_type, paper_str):
    """Build the download URL."""
    filename = f"{paper_str} {doc_type}.pdf"
    encoded_filename = quote(filename)
    url = f"{BASE_URL}{paper_num}/International/{doc_type}/{encoded_filename}"
    return url


def create_directory_structure(year, month):
    """Create the directory structure for organizing files."""
    path = Path(OUTPUT_DIR) / year / month
    path_ms = path / "MS"
    path_qp = path / "QP"
    
    path_ms.mkdir(parents=True, exist_ok=True)
    path_qp.mkdir(parents=True, exist_ok=True)
    
    return path


def download_file(url, dest_path):
    """Download a file with health check."""
    try:
        print(f"  Downloading: {dest_path.name}...", end=" ")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '')
        if 'application/pdf' not in content_type.lower():
            print(f"✗ FAILED (Not a PDF)")
            return False
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = dest_path.stat().st_size
        if file_size < 1024:
            print(f"✗ FAILED (File too small: {file_size} bytes)")
            dest_path.unlink()
            return False
        
        with open(dest_path, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                print(f"✗ FAILED (Invalid PDF header)")
                dest_path.unlink()
                return False
        
        print(f"✓ OK ({file_size / 1024:.1f} KB)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ FAILED ({str(e)[:50]})")
        if dest_path.exists():
            dest_path.unlink()
        return False
    except Exception as e:
        print(f"✗ ERROR ({str(e)[:50]})")
        if dest_path.exists():
            dest_path.unlink()
        return False


def main():
    """Main execution function."""
    print("=" * 80)
    print("CIE IGCSE Chemistry (0620) Past Papers Downloader")
    print("=" * 80)
    print()
    
    total_files = 0
    downloaded = 0
    failed = 0
    skipped = 0
    
    for paper_num, types in PAPERS.items():
        for doc_type, papers in types.items():
            total_files += len(papers)
    
    print(f"Total files to download: {total_files}")
    print(f"Output directory: {OUTPUT_DIR}/")
    print()
    
    for paper_num, types in PAPERS.items():
        print(f"\n{'=' * 80}")
        print(f"Processing {paper_num}")
        print('=' * 80)
        
        for doc_type, papers in types.items():
            print(f"\n{doc_type} ({len(papers)} files):")
            print("-" * 80)
            
            for paper_str in papers:
                year, month, variant = parse_paper_info(paper_str)
                
                if not year or not month:
                    print(f"  ⚠ Skipping invalid format: {paper_str}")
                    skipped += 1
                    continue
                
                base_path = create_directory_structure(year, month)
                
                if variant:
                    filename = f"{month}_{year}_v{variant}_{paper_num.replace('Paper-', 'P')}_{doc_type}.pdf"
                else:
                    filename = f"{month}_{year}_{paper_num.replace('Paper-', 'P')}_{doc_type}.pdf"
                
                dest_path = base_path / doc_type / filename
                
                if dest_path.exists():
                    file_size = dest_path.stat().st_size
                    print(f"  Already exists: {dest_path.name} ({file_size / 1024:.1f} KB)")
                    skipped += 1
                    continue
                
                url = build_url(paper_num, doc_type, paper_str)
                
                if download_file(url, dest_path):
                    downloaded += 1
                else:
                    failed += 1
                
                time.sleep(DELAY_BETWEEN_DOWNLOADS)
    
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Total files:      {total_files}")
    print(f"Downloaded:       {downloaded} ✓")
    print(f"Skipped:          {skipped} (already exist)")
    print(f"Failed:           {failed} ✗")
    print(f"Success rate:     {(downloaded / (downloaded + failed) * 100):.1f}%" if (downloaded + failed) > 0 else "N/A")
    print()
    print(f"Files saved to: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 80)


if __name__ == "__main__":
    main()