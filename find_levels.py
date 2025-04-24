"""
Main executable file used to start the project
"""

import asyncio

from source.core import run_project

if __name__ == "__main__":
    asyncio.run(run_project())
