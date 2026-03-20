"""
users: add lastname column
"""

from yoyo import step

__depends__ = {'20260320_01_k7bqX-users-create-table'}

steps = [
    step(
        "ALTER TABLE users ADD COLUMN lastname VARCHAR(100)",
        "ALTER TABLE users DROP COLUMN lastname"
    )
]
