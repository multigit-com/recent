import os
import sys
from datetime import datetime, timedelta
import argparse


def list_recent_readmes(search_path, max_depth):
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    results = []

    for root, dirs, files in os.walk(search_path):
        # Check if we've exceeded the max depth
        if root[len(search_path):].count(os.sep) >= max_depth:
            del dirs[:]  # Don't go deeper
            continue

        if 'README.md' in files:
            readme_path = os.path.join(root, 'README.md')
            mod_time = datetime.fromtimestamp(os.path.getmtime(readme_path))
            if mod_time > one_month_ago:
                results.append((mod_time, root))

    # Sort results by date
    results.sort(key=lambda x: x[0])

    # Print sorted results
    for mod_time, folder in results:
        print(f"{mod_time.strftime('%Y-%m-%d')} {folder}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List folders with recently updated README.md files.")
    parser.add_argument("search_path", nargs="?", default="github", help="Path to search (default: github)")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth to search (default: 3)")

    args = parser.parse_args()

    if not os.path.isdir(args.search_path):
        print(f"Error: Directory '{args.search_path}' does not exist.")
        sys.exit(1)

    list_recent_readmes(args.search_path, args.max_depth)
