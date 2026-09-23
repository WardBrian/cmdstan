from audioop import add
import os
import argparse
from typing import Any
from pathlib import Path
import warnings

BUILD_DIR = Path(__file__).parent
validate_path = lambda p: Path(p).exists()

cli = argparse.ArgumentParser()
cli.add_argument("model", action="store")

# dictionary which maps variable names to functions which get their values
# this is lazy to allow both environment variables and command line arguments
MAKE_VARIABLES = dict()

def populate_globals(args):
    for name, getter in MAKE_VARIABLES.items():
        globals()[name] = getter(args)

def user_supplied_or(name: str, dflt: Any,*, check: callable = lambda _: True):
    cli.add_argument(f"--{name}", action="store", required=False, default=None)

    def get(args):
        value = getattr(args, name)
        default = dflt() if callable(dflt) else dflt
        if value is None:
            value = os.getenv(name, default)
        if not check(value):
            warnings.warn(f"Invalid value for {name}: {value}.\n\tUsing default: {default}", stacklevel=2)
            value = default
        return type(default)(value)

    MAKE_VARIABLES[name] = get

user_supplied_or("CXX", "g++")
user_supplied_or("CC", "gcc")
user_supplied_or("O", "3", check=lambda v: v in "0123gs")
user_supplied_or("CXXFLAGS", "")

# paths
user_supplied_or("STAN", BUILD_DIR / "stan", check=validate_path)
# lazy because it depends on STAN
user_supplied_or("MATH", lambda: STAN / "lib" / "stan_math", check=validate_path)


def get_dependencies(file: str) -> set[str]:
    # generate .d file, read
    pass

def rebuild_needed() -> bool:
    pass


if __name__ == "__main__":
    args = cli.parse_args()
    print(MAKE_VARIABLES.keys())
    populate_globals(args)

    CXXFLAGS += f"-std=c++1y -Wno-sign-compare -Wno-ignored-attributes -D_REENTRANT -DBOOST_DISABLE_ASSERTS -O{O}"
    print(CXXFLAGS)
    print(MATH)

