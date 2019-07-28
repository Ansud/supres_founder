"""

Main executable file used to start project

"""

import asyncio

from source.core import run_project


def main():
    asyncio.run(run_project())


if __name__ == "__main__":
    main()
