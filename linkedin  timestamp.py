#!/usr/bin/env python3
"""
LinkedIn Post Timestamp Extractor
Extracts the real post time from a LinkedIn post URL using the embedded snowflake ID.

Pipeline:
  URL → extract decimal ID → binary → first 41 bits → decimal → Unix time → human time
"""

import re
import sys
from datetime import datetime, timezone


def extract_post_id(url: str) -> str:
    """Extract the large decimal post ID from a LinkedIn URL."""
    match = re.search(r'-(\d{15,})-', url)
    if not match:
        raise ValueError(
            "Could not find a LinkedIn post ID in the URL.\n"
            "Expected format: https://www.linkedin.com/posts/...-<ID>-XXXX"
        )
    return match.group(1)


def decimal_to_binary(decimal: int) -> str:
    """Convert decimal to binary string (no '0b' prefix)."""
    return bin(decimal)[2:]


def extract_timestamp_bits(binary_str: str, num_bits: int = 41) -> str:
    """Take the first N bits (most significant) from the binary string."""
    if len(binary_str) < num_bits:
        # Shouldn't happen for valid LinkedIn IDs, but handle gracefully
        return binary_str
    return binary_str[:num_bits]


def binary_to_decimal(binary_str: str) -> int:
    """Convert binary string back to decimal."""
    return int(binary_str, 2)


def unix_ms_to_datetime(unix_ms: int) -> datetime:
    """Convert Unix time in milliseconds to a UTC datetime object."""
    return datetime.fromtimestamp(unix_ms / 1000, tz=timezone.utc)


def main():
    # --- Get URL input ---
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:]).strip()
    else:
        print("=" * 60)
        print("  LinkedIn Post Timestamp Extractor")
        print("=" * 60)
        url = input("\nPaste your LinkedIn post URL:\n> ").strip()

    if not url:
        print("Error: No URL provided.")
        sys.exit(1)

    print()

    try:
        # Step 1: Extract post ID
        post_id_str = extract_post_id(url)
        post_id = int(post_id_str)
        print(f"Step 1 │ Extracted decimal ID : {post_id}")

        # Step 2: Convert to binary
        binary = decimal_to_binary(post_id)
        print(f"Step 2 │ Full binary ({len(binary)} bits)  : {binary}")

        # Step 3: Take first 41 bits (timestamp portion of LinkedIn snowflake ID)
        timestamp_bits = extract_timestamp_bits(binary, num_bits=41)
        print(f"Step 3 │ First 41 bits         : {timestamp_bits}")

        # Step 4: Convert those bits back to decimal → Unix time in milliseconds
        unix_ms = binary_to_decimal(timestamp_bits)
        print(f"Step 4 │ Decimal (Unix ms)     : {unix_ms}")

        # Step 5: Convert to human-readable time
        post_time_utc = unix_ms_to_datetime(unix_ms)
        print(f"Step 5 │ UTC datetime          : {post_time_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # Also show in IST (UTC+5:30) since the user is in India
        from datetime import timedelta
        ist_offset = timedelta(hours=5, minutes=30)
        post_time_ist = post_time_utc + ist_offset
        print(f"       │ IST datetime          : {post_time_ist.strftime('%Y-%m-%d %H:%M:%S')} IST")

        print()
        print("─" * 60)
        print(f"  Post published at: {post_time_utc.strftime('%d %B %Y, %H:%M UTC')}")
        print(f"                     {post_time_ist.strftime('%d %B %Y, %H:%M IST')}")
        print("─" * 60)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()