import os
import requests

def download_files(urls, local_directory='datasets/'):
    """
    Downloads files from the specified URLs and saves them to a local directory.

    Args:
    - urls (list of str): List of URLs to download files from.
    - local_directory (str): The local directory to save the downloaded files.

    Returns:
    - list of str: List of local file paths where the files were saved.
    """
    # Ensure the local directory exists
    os.makedirs(local_directory, exist_ok=True)

    # List to store the local paths of the downloaded files
    local_paths = []

    for url in urls:
        try:
            # Extract file name from URL
            file_name = url.split('/')[-1]
            local_path = os.path.join(local_directory, file_name)
            
            # Download the file
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            
            with open(local_path, 'wb') as file:
                file.write(response.content)
            
            # Append the local path to the list
            local_paths.append(local_path)
            print(f"Downloaded {file_name} to {local_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

    return local_paths