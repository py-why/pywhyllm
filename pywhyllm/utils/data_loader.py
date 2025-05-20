import bz2
import json
import os
import requests
from tqdm import tqdm
import logging


def download_causenet(url: str, file_path: str) -> bool:
    """
    Download the CauseNet-Precision dataset from causenet.org and save it to the specified path.

    The CauseNet-Precision dataset is a subset of the CauseNet
    knowledge base containing high-precision causal relations extracted from web sources.
    The dataset is described in the following paper:

    Citation:
    Stefan Heindorf, Yan Scholten, Henning Wachsmuth, Axel-Cyrille Ngonga Ngomo, and Martin Potthast.
    2020. CauseNet: Towards a Causality Graph Extracted from the Web. In Proceedings of the 29th ACM
    International Conference on Information &amp; Knowledge Management (CIKM '20). Association for
    Computing Machinery, New York, NY, USA, 3023–3030. https://doi.org/10.1145/3340531.3412763

    TODO: Add license

    Args:
        url (str): The URL of the file to download.
        file_path (str): The local path where the file will be saved.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Send a GET request to the URL
        response = requests.get(url, stream=True)

        # Check if the request was successful
        if response.status_code != 200:
            logging.error(f"Failed to download file from {url}. Status code: {response.status_code}")
            return False

        # Get the total file size for progress bar (if available)
        total_size = int(response.headers.get("content-length", 0))

        # Download and save the file with a progress bar
        with open(file_path, "wb") as file, tqdm(
                desc="Downloading",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        logging.info(f"File downloaded successfully to {file_path}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file from {url}: {e}")
        return False
    except OSError as e:
        logging.error(f"Error saving file to {file_path}: {e}")
        return False


def load_causenet_json(file_path):
    json_data = []
    print("Loading CauseNet using json")
    with bz2.open(file_path, 'rt',
                  encoding='utf-8') as file:
        # Read each line and parse as JSON
        for line in file:
            line = line.strip()  # Remove trailing newlines
            if line:  # Skip empty lines
                json_obj = json.loads(line)  # Parse the line as JSON
                json_data.append(json_obj)  # Add to list
    print("Done loading CauseNet using json")
    return json_data


def create_causenet_dict(json_data):
    causenet_dict = {}
    print("Creating dictionary from CauseNet json data")
    for item in json_data:
        cause = item['causal_relation']['cause']['concept']
        effect = item['causal_relation']['effect']['concept']
        key = cause + "-" + effect

        if key not in causenet_dict:
            causenet_dict[key] = {
                'causal_relation': {'cause': cause, 'effect': effect},
                'sources': item['sources']
            }
        else:
            # Append sources to existing list
            causenet_dict[key]['sources'].extend(item['sources'])
    print("Done creating dictionary from CauseNet json data")
    return causenet_dict
