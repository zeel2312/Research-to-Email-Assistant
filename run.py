#!/usr/bin/env python

from __future__ import annotations

import sys
from dotenv import load_dotenv
load_dotenv()

from agent.main_agent import run_agent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run.py <topic>")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    email = run_agent(topic)
    print("\n=== Draft Email ===\n")
    print(email)


if __name__ == "__main__":
    main()