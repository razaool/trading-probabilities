"""
Add missing exchange column to tickers table
Run this via: railway run python backend/scripts/fix_exchange_column.py
"""

import sys
import os
from sqlalchemy import create_engine, text, inspect

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings


def fix_schema():
    """Add missing exchange column if it doesn't exist"""

    print("=" * 60)
    print("FIXING TICKERS TABLE SCHEMA")
    print("=" * 60)

    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # Check current columns
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('tickers')]
        print(f"\nCurrent columns: {columns}")

        if 'exchange' not in columns:
            print("\n⚠️  Missing 'exchange' column - adding it now...")

            # Add the missing column
            conn.execute(text("ALTER TABLE tickers ADD COLUMN exchange VARCHAR(50)"))
            conn.commit()

            print("✅ Added 'exchange' column to tickers table")
        else:
            print("\n✅ 'exchange' column already exists")

        # Verify the fix
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('tickers')]
        print(f"\nUpdated columns: {columns}")

    print("\n" + "=" * 60)
    print("SCHEMA FIX COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    fix_schema()
