"""
Cambridge Past Papers URL Generator
Generates complete URL lists for batch operations
Exports to CSV for external download managers or audit trails
"""

import csv
from datetime import datetime

# Configuration
BASE_URL = "https://pastpapers.papacambridge.com/download_file.php?files=https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/"
SUBJECT = "0971"
PAPERS = ["21", "22", "41", "42", "61", "62"]
OUTPUT_CSV = 'cambridge_past_papers_urls.csv'


def generate_urls():
    """
    Generate all download URLs for papers from 2025 back to 2018.
    
    Returns:
        list: Complete list of generated URLs
    """
    urls = []
    
    for year in range(25, 17, -1):
        # Spring season (June)
        filename_ms = f"{SUBJECT}_s{year:02d}_ms"
        filename_qp = f"{SUBJECT}_s{year:02d}_qp"
        
        for paper in PAPERS:
            urls.append(BASE_URL + filename_ms + "_" + paper + ".pdf")
            urls.append(BASE_URL + filename_qp + "_" + paper + ".pdf")
        
        # Winter season (November) - skip year 25 if recent
        if year < 25:
            filename_ms = f"{SUBJECT}_w{year:02d}_ms"
            filename_qp = f"{SUBJECT}_w{year:02d}_qp"
            
            for paper in PAPERS:
                urls.append(BASE_URL + filename_ms + "_" + paper + ".pdf")
                urls.append(BASE_URL + filename_qp + "_" + paper + ".pdf")
    
    return urls


def save_to_csv(urls, filename):
    """
    Save URLs to CSV file.
    
    Args:
        urls (list): List of URLs to save
        filename (str): Output CSV filename
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])


def print_urls(urls):
    """
    Print all URLs to console.
    
    Args:
        urls (list): List of URLs to print
    """
    print(f"Total URLs generated: {len(urls)}\n")
    print("=" * 80)
    for i, url in enumerate(urls, 1):
        print(f"{i:4d}. {url}")
    print("=" * 80)


def main():
    """Main execution function."""
    print("=" * 80)
    print("Cambridge Past Papers URL Generator")
    print(f"Subject: {SUBJECT}")
    print("=" * 80)
    print()
    
    # Generate URLs
    urls = generate_urls()
    
    # Print to console
    print_urls(urls)
    
    # Save to CSV
    save_to_csv(urls, OUTPUT_CSV)
    print(f"\n✓ URLs saved to '{OUTPUT_CSV}'")
    
    # Print statistics
    print("\nStatistics:")
    print(f"  Total URLs:     {len(urls)}")
    print(f"  Mark Schemes:   {len([u for u in urls if '_ms_' in u])}")
    print(f"  Question Papers: {len([u for u in urls if '_qp_' in u])}")
    print(f"  Output file:    {OUTPUT_CSV}")


if __name__ == '__main__':
    main()