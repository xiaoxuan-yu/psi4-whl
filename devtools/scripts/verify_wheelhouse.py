#!/usr/bin/env python

from __future__ import annotations

import argparse
import email
import zipfile
from pathlib import Path

from packaging.utils import parse_wheel_filename


EXPECTED_LANES = {
    "linux-x86_64",
    "windows-x86_64",
    "macos-x86_64",
    "macos-arm64",
}


def classify_lane(filename: str) -> str:
    if "manylinux" in filename and "x86_64" in filename:
        return "linux-x86_64"
    if "win_amd64" in filename:
        return "windows-x86_64"
    if "macosx" in filename and "arm64" in filename and "x86_64" not in filename:
        return "macos-arm64"
    if "macosx" in filename and "x86_64" in filename and "arm64" not in filename:
        return "macos-x86_64"
    raise ValueError(f"unable to classify wheel lane from filename: {filename}")


def read_metadata_fields(wheel_path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(wheel_path) as zf:
        metadata_name = next(name for name in zf.namelist() if name.endswith(".dist-info/METADATA"))
        metadata = email.message_from_bytes(zf.read(metadata_name))
    return metadata["Name"], metadata["Version"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a release wheelhouse before publishing.")
    parser.add_argument("wheelhouse", help="Directory containing repaired wheel artifacts.")
    parser.add_argument("--expect-version", required=True, help="Expected Psi4 version, e.g. 1.10")
    parser.add_argument("--expect-count", type=int, default=4, help="Expected number of wheels.")
    args = parser.parse_args()

    wheelhouse = Path(args.wheelhouse).resolve()
    if not wheelhouse.is_dir():
        raise SystemExit(f"wheelhouse directory not found: {wheelhouse}")

    sdists = sorted(wheelhouse.glob("*.tar.gz")) + sorted(wheelhouse.glob("*.zip"))
    if sdists:
        raise SystemExit(f"sdist artifacts are not allowed: {[path.name for path in sdists]}")

    wheels = sorted(wheelhouse.glob("*.whl"))
    if len(wheels) != args.expect_count:
        raise SystemExit(f"expected {args.expect_count} wheels, found {len(wheels)}: {[path.name for path in wheels]}")

    lanes = set()
    for wheel_path in wheels:
        distribution, version, _, _ = parse_wheel_filename(wheel_path.name)
        metadata_name, metadata_version = read_metadata_fields(wheel_path)

        if distribution != "psi4_whl":
            raise SystemExit(f"unexpected wheel distribution name: {wheel_path.name}")
        if str(version) != args.expect_version:
            raise SystemExit(f"unexpected wheel version in filename: {wheel_path.name}")
        if metadata_name != "psi4-whl":
            raise SystemExit(f"unexpected METADATA Name in {wheel_path.name}: {metadata_name}")
        if metadata_version != args.expect_version:
            raise SystemExit(f"unexpected METADATA Version in {wheel_path.name}: {metadata_version}")

        lanes.add(classify_lane(wheel_path.name))

    if lanes != EXPECTED_LANES:
        missing = sorted(EXPECTED_LANES - lanes)
        extra = sorted(lanes - EXPECTED_LANES)
        raise SystemExit(f"wheel lane mismatch; missing={missing} extra={extra}")

    print("Validated wheels:")
    for wheel_path in wheels:
        print(f"  {wheel_path.name}")


if __name__ == "__main__":
    main()
