from pathlib import Path


def generate_mock_file(file_name, size_in_mb):
    """
    Generate a mock file of specified size in MB.

    Parameters:
    - file_name (str): Name of the file to be generated.
    - size_in_mb (int): Size of the file in megabytes.
    """
    size_in_bytes = size_in_mb * 1024 * 1024  # Convert MB to bytes
    with open(file_name, "wb") as f:
        f.write(b"0" * size_in_bytes)
    return f"{file_name} of size {size_in_mb} MB created successfully."


mb_li = [100*n for n in range(1, 21)]

for mb in mb_li:
    print(mb)
    folder = Path("mock_files")
    if not folder.exists():
        folder.mkdir()
    file_name = f"mock_file_{mb}mb.txt"
    size_in_mb = mb  # Change this to the desired file size in MB
    generate_mock_file(folder / file_name, size_in_mb)
