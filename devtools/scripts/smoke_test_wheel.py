#!/usr/bin/env python

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def run_cli_smoke() -> None:
    psi4_exe = shutil.which("psi4")
    if psi4_exe is None:
        psi4_exe = shutil.which("psi4.exe")
    if psi4_exe is None:
        raise SystemExit("psi4 executable not found on PATH")

    cli_input = """molecule h2 {
  H
  H 1 0.74
}

set {
  basis sto-3g
}

energy('scf')
"""

    with tempfile.TemporaryDirectory(prefix="psi4-wheel-smoke-") as tmpdir:
        tmp_path = Path(tmpdir)
        input_path = tmp_path / "smoke.dat"
        output_path = tmp_path / "smoke.out"
        input_path.write_text(cli_input, encoding="utf-8")
        subprocess.run(
            [psi4_exe, str(input_path), "-o", str(output_path)],
            check=True,
            cwd=tmpdir,
        )
        output_text = output_path.read_text(encoding="utf-8")
        if "Psi4 exiting successfully" not in output_text:
            raise SystemExit("psi4 CLI smoke test did not reach a successful exit marker")


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test an installed psi4 wheel.")
    parser.add_argument("--expect-version", help="Assert that psi4.__version__ matches this value.")
    parser.add_argument("--skip-cli", action="store_true", help="Skip the psi4 executable smoke test.")
    args = parser.parse_args()

    import psi4
    from psi4 import core

    print(f"psi4 module: {psi4.__file__}")
    print(f"psi4 version: {psi4.__version__}")

    if args.expect_version and psi4.__version__ != args.expect_version:
        raise SystemExit(f"expected psi4.__version__={args.expect_version}, got {psi4.__version__}")

    core.set_num_threads(2)
    if core.get_num_threads() != 2:
        raise SystemExit("OpenMP smoke test failed to set Psi4 thread count to 2")

    molecule = psi4.geometry(
        """
        H
        H 1 0.74
        """
    )
    energy = psi4.energy("scf/sto-3g", molecule=molecule)
    print(f"SCF energy: {energy:.12f}")

    if not args.skip_cli:
        run_cli_smoke()


if __name__ == "__main__":
    main()
