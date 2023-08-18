from pathlib import Path
import shutil
import subprocess
import sys
import os

# note: since we'd be using system python,
# we'd want to probably avoid using pathlib
# and subprocess.run

HERE = Path(__file__).parent
BUILD = Path(os.getenv("CMDSTAN_BUILD_DIR", HERE/"build"))

def main():
    BUILD.mkdir(exist_ok=True,parents=True)

    if len(sys.argv) < 2:
        raise ValueError("Must provide a stan file as first argument")

    STAN_FILE = Path(sys.argv[1]).with_suffix(".stan")
    if not STAN_FILE.exists():
        raise FileNotFoundError(f"Cannot find file '{STAN_FILE}'")

    print(f"Generating CMakeLists-model.txt for {STAN_FILE}")
    with open(HERE/"CMakeLists-model.txt", "w") as f:
        f.write(f"stan_model({STAN_FILE.stem})\n")
    # also need to handle includes
    shutil.copyfile(STAN_FILE, BUILD/STAN_FILE.name)

    print("Runing cmake")
    subprocess.run(["cmake", "-S", str(HERE), "-B", str(BUILD), "-Wno-dev"] + sys.argv[2:], check=True)

    print("Building")
    subprocess.run(["cmake", "--build", str(BUILD), '-j', '10', '-t' ,str(STAN_FILE.stem)], check=True)

    shutil.copyfile(BUILD/"bin"/STAN_FILE.stem, STAN_FILE.with_suffix(""))
    print("Done!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        (HERE / "CMakeLists-model.txt").unlink(missing_ok=True)

