"""Wheel console entry point for Psi4."""

from __future__ import annotations

import runpy


def main() -> None:
    runpy.run_module("psi4.run_psi4", run_name="__main__")
