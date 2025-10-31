"""Fix encoding issues in precommit_errors.txt file."""

import sys
from pathlib import Path


def fix_encoding(input_file: str, output_file: str = None):
    """
    Fix encoding issues by removing null bytes and normalizing text.

    Args:
        input_file: Path to file with encoding issues
        output_file: Path to output file (defaults to input_file)
    """
    if output_file is None:
        output_file = input_file

    # Read the file in binary mode
    with open(input_file, 'rb') as f:
        content = f.read()

    # Remove null bytes
    content = content.replace(b'\x00', b'')

    # Try to decode as UTF-16LE (common Windows encoding issue)
    try:
        text = content.decode('utf-16le')
        print(f"✓ Detected UTF-16LE encoding")
    except UnicodeDecodeError:
        # Try UTF-8
        try:
            text = content.decode('utf-8')
            print(f"✓ Detected UTF-8 encoding")
        except UnicodeDecodeError:
            # Try Latin-1 as fallback
            text = content.decode('latin-1')
            print(f"✓ Detected Latin-1 encoding")

    # Write back as clean UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"✓ Fixed encoding: {output_file}")
    print(f"✓ File size: {len(text)} characters")

    return text


if __name__ == "__main__":
    # Default file path
    error_file = Path(__file__).parent.parent / "precommit_errors.txt"

    if len(sys.argv) > 1:
        error_file = Path(sys.argv[1])

    if not error_file.exists():
        print(f"❌ Error: File not found: {error_file}")
        sys.exit(1)

    print(f"Fixing encoding for: {error_file}")

    # Create a backup
    backup_file = error_file.with_suffix('.txt.bak')
    import shutil
    shutil.copy2(error_file, backup_file)
    print(f"✓ Created backup: {backup_file}")

    # Fix encoding
    fixed_text = fix_encoding(str(error_file))

    # Show first few lines
    lines = fixed_text.split('\n')[:10]
    print(f"\n✓ First 10 lines of fixed file:")
    print("=" * 80)
    for i, line in enumerate(lines, 1):
        print(f"{i:2}. {line[:75]}")

    print(f"\n✅ Encoding fixed successfully!")
    print(f"   Original backed up to: {backup_file}")
    print(f"   Fixed file: {error_file}")
