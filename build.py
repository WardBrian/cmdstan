#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys
import os
import argparse
import platform

# note: since we'd be using system python,
# we'd want to probably avoid using pathlib
# and subprocess.run
WINDOWS = platform.system() == "Windows"

HERE = Path(__file__).parent
BUILD = Path(os.getenv("CMDSTAN_BUILD_DIR", HERE/"build"))
EXE = ".exe" if WINDOWS else ""
EXTRA_WINDOWS_ARGS = ["-A", "x64", "-T" "ClangCL"] if WINDOWS else []
EXTRA_WINDOWS_BUILD_ARGS = ["--config", "Release"] if WINDOWS else []
BIN = BUILD/"bin"/"Release" if platform.system() == "Windows" else BUILD/"bin"


cli = argparse.ArgumentParser()
cli.add_argument("stan_file", help="stan file to build")

def main(argparsed):
    args, cmake_args = argparsed
    BUILD.mkdir(exist_ok=True,parents=True)

    STAN_FILE = Path(args.stan_file).with_suffix(".stan")
    if not STAN_FILE.exists():
        raise FileNotFoundError(f"Cannot find file '{STAN_FILE}'")

    print(f"Generating CMakeLists-model.txt for {STAN_FILE}")
    with open(HERE/"CMakeLists-model.txt", "w") as f:
        f.write(f"stan_model({STAN_FILE.stem})\n")
    # also need to handle includes
    shutil.copy2(STAN_FILE, BUILD/STAN_FILE.name)
    # copy executable to build folder to avoid recompilation if we can
    if (STAN_FILE.with_suffix(EXE).exists()):
        shutil.copy2(STAN_FILE.with_suffix(EXE), BIN/STAN_FILE.with_suffix(EXE).name)

    print("Runing cmake")
    subprocess.run(["cmake", "-S", str(HERE), "-B", str(BUILD), "-Wno-dev"] + EXTRA_WINDOWS_ARGS + cmake_args, check=True)

    print("Building")
    subprocess.run(["cmake", "--build", str(BUILD), '-j', '10', '-t' ,str(STAN_FILE.stem)] + EXTRA_WINDOWS_BUILD_ARGS, check=True)

    # copy build executable back to original folder, clean up
    shutil.copy2(BIN/STAN_FILE.with_suffix(EXE).name, STAN_FILE.with_suffix(EXE))
    (BIN/STAN_FILE.with_suffix(EXE)).unlink(missing_ok=True)

    print("Done!")

if __name__ == "__main__":
    try:
        main(cli.parse_known_args())
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        (HERE / "CMakeLists-model.txt").unlink(missing_ok=True)

