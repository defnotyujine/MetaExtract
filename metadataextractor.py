from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys
import magic  # For detecting MIME type

__authors__ = ["Eugene S. Garces", "Alexandra Ashley A. Fernandez", "John Carl Arroza", "Alfie Celeste"]
__date__ = "2024/9/25"
__description__ = "Gather filesystem metadata of provided file"

# Argument parser for input file path
parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument("FILE_PATH", help="Path to file to gather metadata for")
args = parser.parse_args()
file_path = args.FILE_PATH

# Attempt to gather the file statistics
try:
    stat_info = os.stat(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' does not exist.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while accessing the file: {e}")
    sys.exit(1)

metadata = []

# Platform-specific file time information
if "linux" in sys.platform or "darwin" in sys.platform:
    metadata.append(f"<strong>Change time:</strong> {dt.fromtimestamp(stat_info.st_ctime)}")
elif "win" in sys.platform:
    metadata.append(f"<strong>Creation time:</strong> {dt.fromtimestamp(stat_info.st_ctime)}")
else:
    metadata.append(f"<strong>Platform Unsupported:</strong> {sys.platform} cannot interpret timestamps.")

# Gathering basic metadata
metadata.extend([
    f"<strong>Modification time:</strong> {dt.fromtimestamp(stat_info.st_mtime)}",
    f"<strong>Access time:</strong> {dt.fromtimestamp(stat_info.st_atime)}",
    f"<strong>File mode:</strong> {stat_info.st_mode}",
    f"<strong>File inode:</strong> {stat_info.st_ino}",
    f"<strong>Device ID:</strong> {stat_info.st_dev}",
    f"<strong>Number of hard links:</strong> {stat_info.st_nlink}",
    f"<strong>Owner User ID:</strong> {stat_info.st_uid}",
    f"<strong>Group ID:</strong> {stat_info.st_gid}",
    f"<strong>File Size:</strong> {stat_info.st_size} bytes",
    f"<strong>File Size in KB:</strong> {stat_info.st_size / 1024:.2f} KB",
    f"<strong>File Extension:</strong> {os.path.splitext(file_path)[1]}",
    f"<strong>File Type:</strong> {os.path.splitext(file_path)[1][1:].upper() if os.path.splitext(file_path)[1] else 'Unknown'}",
    f"<strong>File Permissions:</strong> {oct(stat_info.st_mode)}",
    f"<strong>Last Accessed By:</strong> {stat_info.st_uid}",
    f"<strong>Is a symlink:</strong> {os.path.islink(file_path)}",
    f"<strong>Absolute Path:</strong> {os.path.abspath(file_path)}",
    f"<strong>File exists:</strong> {os.path.exists(file_path)}",
    f"<strong>Parent directory:</strong> {os.path.dirname(file_path)}",
    f"<strong>File name:</strong> {os.path.basename(file_path)}"
])

# Detect MIME type using magic numbers
mime = magic.Magic(mime=True)
file_mime = mime.from_file(file_path)
metadata.append(f"<strong>Detected MIME Type:</strong> {file_mime}")

# Generate timestamp for file output
timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
output_file = f"file_metadata_{timestamp}.html"

# Writing metadata to the HTML file
try:
    with open(output_file, "w") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Metadata Report</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            color: #333;
            animation: fadeIn 1s ease-in;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            animation: slideIn 0.8s ease-out;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 5px;
            animation: slideIn 0.8s ease-out;
        }}
        .metadata {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
            max-width: 600px;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 1s forwards;
        }}
        .metadata p {{
            margin: 10px 0;
        }}
        .metadata ul {{
            list-style-type: none;
            padding: 0;
        }}
        .metadata li {{
            background: #ecf0f1;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            transition: background 0.3s ease;
            animation: fadeIn 0.5s forwards;
            opacity: 0;
        }}
        .metadata li:hover {{
            background: #d5dbdb;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        button {{
            padding: 10px 15px;
            border: none;
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        button:hover {{
            background-color: #34495e;
        }}
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes slideIn {{
            from {{ transform: translateY(-20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <h1>File Metadata Report</h1>
    <div class="metadata">
        <h2>Report Summary</h2>
        <p><strong>Generated on:</strong> {dt.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>File Analyzed:</strong> {file_path}</p>
        <h2>Metadata Details</h2>
        <ul>
""")
        # Writing metadata into the HTML file
        for index, item in enumerate(metadata):
            f.write(f"            <li style='animation-delay: {index * 0.1}s;'>{item}</li>\n")

        f.write(f"""
        </ul>
        <button onclick="window.print()">Print this report</button>
    </div>
    <div class="footer">
        <p>Developed by {', '.join(__authors__)} on {__date__}</p>
    </div>
</body>
</html>
""")

    print(f"Metadata has been written to {output_file}")
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")
