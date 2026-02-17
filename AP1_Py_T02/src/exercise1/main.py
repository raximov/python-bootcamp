#!/usr/bin/env python3
"""Task 2 — Asynchronous Image Downloader."""

import asyncio
import os
import sys

try:
    import aiohttp
except ImportError:
    print("Installing aiohttp…")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp


# ---------------------------------------------------------------------------
# Table formatting
# ---------------------------------------------------------------------------

def format_table(headers, rows, alignments=None):
    ncols = len(headers)
    if alignments is None:
        alignments = ["left"] * ncols
    widths = [len(h) + 2 for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)) + 2)

    def _cell(text, w, align):
        s = str(text)
        if align == "left":
            return " " + s.ljust(w - 1)
        if align == "right":
            return s.rjust(w - 1) + " "
        return s.center(w)

    sep = "+" + "+".join("-" * w for w in widths) + "+"
    lines = [sep]
    lines.append("|" + "|".join(_cell(h, widths[i], alignments[i])
                                for i, h in enumerate(headers)) + "|")
    lines.append(sep)
    for row in rows:
        lines.append("|" + "|".join(_cell(c, widths[i], alignments[i])
                                    for i, c in enumerate(row)) + "|")
    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Download logic
# ---------------------------------------------------------------------------

async def download_image(session, url, save_dir, results, index):
    """Download a single image and record the result."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                results[index] = (url, "Error")
                return
            filename = url.rstrip("/").split("/")[-1]
            if not filename:
                filename = f"image_{index}"
            filepath = os.path.join(save_dir, filename)
            content = await resp.read()
            with open(filepath, "wb") as f:
                f.write(content)
            results[index] = (url, "Success")
    except Exception:
        results[index] = (url, "Error")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    # Ask for save directory (re-prompt until valid)
    while True:
        save_dir = input("Enter path to save images: ").strip()
        if not save_dir:
            print("Path cannot be empty.")
            continue
        try:
            os.makedirs(save_dir, exist_ok=True)
            # Test write access
            test_file = os.path.join(save_dir, ".write_test")
            with open(test_file, "w") as f:
                f.write("")
            os.remove(test_file)
            break
        except (OSError, PermissionError):
            print("Invalid path or no write access. Please try again.")

    results = {}
    tasks = []
    idx = 0

    async with aiohttp.ClientSession() as session:
        while True:
            url = input().strip()
            if not url:
                break
            results[idx] = (url, "Pending")
            task = asyncio.create_task(
                download_image(session, url, save_dir, results, idx)
            )
            tasks.append(task)
            idx += 1

        if tasks:
            pending = [t for t in tasks if not t.done()]
            if pending:
                print(f"\nWaiting for {len(pending)} download(s) to finish...")
            await asyncio.gather(*tasks, return_exceptions=True)

    # Print summary
    print()
    rows = [(results[i][0], results[i][1]) for i in sorted(results)]
    print(format_table(["Link", "Status"], rows, ["left", "left"]))


if __name__ == "__main__":
    asyncio.run(main())
