"""
Cambridge Past Papers Downloader - Subject 0971
Downloads past papers from papacambridge.com for subject 0971 (Computer Science)
Organizes files by year and season (June/November)
"""

import os
import time
import requests
from pathlib import Path
from urllib.parse import urlparse

# Configuration
BASE_URL = "https://pastpapers.papacambridge.com/download_file.php?files=https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/"
SUBJECT = "0971"
PAPERS = ["21", "22", "41", "42", "61", "62"]
PARENT_FOLDER = "Cambridge_Past_Papers_0971"
DELAY_BETWEEN_DOWNLOADS = 0.5  # seconds


def download_file(url, filepath):
    """
    Download a file from the given URL to the specified filepath.
    
    Args:
        url (str): URL to download from
        filepath (str): Local path to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(filepath):
            print(f"  Downloading: {os.path.basename(filepath)}", end=" ... ")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print("✓")
                return True
            else:
                print(f"✗ (Status: {response.status_code})")
                return False
        else:
            print(f"  Skipping: {os.path.basename(filepath)} (already exists)")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def create_directory_structure(year, season):
    """
    Create directory structure for organizing downloaded papers.
    
    Args:
        year (int): Full year (e.g., 2025)
        season (str): Season name ("June" or "November")
        
    Returns:
        str: Path to the season folder
    """
    year_folder = os.path.join(PARENT_FOLDER, f"{year}")
    season_folder = os.path.join(year_folder, season)
    Path(season_folder).mkdir(parents=True, exist_ok=True)
    return season_folder


def download_papers_for_session(year, year_code, session_code, session_name):
    """
    Download all papers for a specific examination session.
    
    Args:
        year (int): Full year
        year_code (int): Two-digit year code
        session_code (str): Session code ('s' for June, 'w' for November)
        session_name (str): Human-readable session name
    """
    session_folder = create_directory_structure(year, session_name)
    print(f"Processing {year} - {session_name}...")
    
    filename_ms = f"{SUBJECT}_{session_code}{year_code:02d}_ms"
    filename_qp = f"{SUBJECT}_{session_code}{year_code:02d}_qp"
    
    for paper in PAPERS:
        # Download mark scheme
        ms_filename = f"{filename_ms}_{paper}.pdf"
        ms_url = BASE_URL + ms_filename
        ms_filepath = os.path.join(session_folder, ms_filename)
        download_file(ms_url, ms_filepath)
        time.sleep(DELAY_BETWEEN_DOWNLOADS)
        
        # Download question paper
        qp_filename = f"{filename_qp}_{paper}.pdf"
        qp_url = BASE_URL + qp_filename
        qp_filepath = os.path.join(session_folder, qp_filename)
        download_file(qp_url, qp_filepath)
        time.sleep(DELAY_BETWEEN_DOWNLOADS)


def main():
    """Main execution function."""
    # Create parent folder
    Path(PARENT_FOLDER).mkdir(exist_ok=True)
    
    print(f"Starting downloads to: {PARENT_FOLDER}\n")
    
    # Download papers from 2025 back to 2018
    for year in range(25, 17, -1):
        full_year = 2000 + year
        
        # Spring season (June)
        download_papers_for_session(full_year, year, 's', 'June')
        
        # Winter season (November) - skip for 2025 if not yet available
        if year < 25:
            download_papers_for_session(full_year, year, 'w', 'November')
        
        print()
    
    # Print completion message
    print("✓ Download complete!")
    print(f"\nFolder structure created in: {PARENT_FOLDER}")
    print("\nStructure:")
    print("Cambridge_Past_Papers_0971/")
    print("├── 2025/")
    print("│   └── June/")
    print("│       ├── 0971_s25_ms_21.pdf")
    print("│       ├── 0971_s25_qp_21.pdf")
    print("│       └── ...")
    print("├── 2024/")
    print("│   ├── June/")
    print("│   │   └── ...")
    print("│   └── November/")
    print("│       └── ...")
    print("└── ...")


if __name__ == '__main__':
    main()