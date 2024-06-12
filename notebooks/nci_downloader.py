import requests
from tqdm.auto import tqdm
import os
import zipfile


def download_product_thredds(product, storage_path, extract=True):
    """
    A custom downloader  to download an an equivalent product from NCI
    Parameters
    ----------
    product : eodag.api.product.EOProduct
        an EODAG product object
    raw_data_path : str
        The path to the directory where the downloaded product will be saved.

    Returns
    -------
    None
    """
    nci_base_url = "https://dapds00.nci.org.au/thredds/fileServer/fj7/Copernicus/"
    nci_url = (
        "/".join([nci_base_url, *product.properties["quicklook"].split("/")[4:]])[:-4] + ".zip"
    )
    local_basename = os.path.basename(nci_url)
    local_filepath = os.path.join(storage_path, local_basename)

    response = requests.get(nci_url, stream=True)

    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    os.makedirs(
        os.path.dirname(local_filepath), exist_ok=True
    )  # Make the directory structure in advance so python doesnt complain if it doesnt exist
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(local_filepath, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if extract:
        print("Unzipping file!")
        unzipped_filepath = local_filepath[:-4]
        with zipfile.ZipFile(local_filepath, "r") as zip_ref:
            zip_ref.extractall(unzipped_filepath)
        local_filepath = unzipped_filepath
        # Get the SAFE file as eodag does
        local_filepath = os.path.join(local_filepath, os.listdir(local_filepath)[0])
        print("Done unzipping!")

    return local_filepath
