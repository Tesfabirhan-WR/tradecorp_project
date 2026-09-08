import pandas as pd
import os
from io import StringIO
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

def get_blob_service_client(account_name: str, account_key: str) -> BlobServiceClient:
    """Create and return a BlobServiceClient for ADLS Gen2."""
    connect_str = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={os.getenv('STORAGE_ACCOUNT_NAME')};"
        f"AccountKey={os.getenv('STORAGE_ACCOUNT_KEY')};"
        f"EndpointSuffix=core.windows.net"
    )
    return BlobServiceClient.from_connection_string(connect_str)

def read_csv_from_blob(blob_service_client: BlobServiceClient, container_name: str, blob_name: str) -> pd.DataFrame:
    """Read a single CSV file from ADLS Gen2."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    csv_bytes = blob_client.download_blob().readall()
    csv_text = csv_bytes.decode("utf-8")
    return pd.read_csv(StringIO(csv_text))

def load_all_csvs_from_container(blob_service_client: BlobServiceClient, container_name: str):
    """Load all CSV files from a container and return a dict of DataFrames."""
    container_client = blob_service_client.get_container_client(container_name)
    
    dfs = {}
    for blob in container_client.list_blobs():
        if blob.name.lower().endswith(".csv"):
            print(f"Loading: {blob.name}")
            dfs[blob.name] = read_csv_from_blob(blob_service_client, container_name, blob.name)
    
    return dfs

if __name__ == "__main__":
    # Example usage
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("STORAGE_ACCOUNT_KEY")
    container_name = os.getenv("CONTAINER_NAME")

    blob_service_client = get_blob_service_client(account_name, account_key)
    dfs = load_all_csvs_from_container(blob_service_client, container_name)

    print(dfs.keys())  # list of CSV filenames


