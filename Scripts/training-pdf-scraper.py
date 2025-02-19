import os
import requests
import urllib3
from googlesearch import search
from urllib.parse import urlparse

# --- Monkey-patch requests to disable SSL certificate verification ---
old_request = requests.Session.request

def new_request(self, method, url, *args, **kwargs):
    kwargs['verify'] = False  # Force bypass SSL verification
    return old_request(self, method, url, *args, **kwargs)

requests.Session.request = new_request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# -------------------------------------------------------------------------

def download_pdf(url, download_folder):
    """Attempts to download a PDF from the given URL.
       Returns True if successful, otherwise False."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for HTTP issues
        
        # Create a filename based on the URL
        filename = os.path.basename(urlparse(url).path)
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        file_path = os.path.join(download_folder, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def get_pdf_urls(query, num_results=100):
    """Returns a list of PDF URLs from a Google search using the given query."""
    urls = []
    for url in search(query, num_results=num_results):
        if url.lower().endswith(".pdf"):
            urls.append(url)
    return urls

def main():
    query = "menu del dia filetype:pdf"
    download_folder = "downloaded_pdfs"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Retrieve more URLs than needed in case some downloads fail
    pdf_urls = get_pdf_urls(query, num_results=100)
    print(f"Found {len(pdf_urls)} PDF URLs. Attempting to download 50 successful PDFs...")
    
    successful_downloads = 0
    for url in pdf_urls:
        if successful_downloads >= 50:
            break
        if download_pdf(url, download_folder):
            successful_downloads += 1

    print(f"Download complete! {successful_downloads} PDFs successfully saved in '{download_folder}'.")

if __name__ == "__main__":
    main()
