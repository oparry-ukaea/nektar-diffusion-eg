#!/bin/env bash

# Defaults - run in debug and output to a subdirectory tagged with the current date and time
MODE="DEBUG"
RUN_SUBDIR="$(date +%Y-%m-%d_%H-%M)"
TEMPLATE_SUBDIR="file-based_sin"
# Parse command line args
for arg in $*; do
    case "$arg" in
        mode=*)
            MODE=${arg:5};;
        subdir=*)
            RUN_SUBDIR=${arg:7};;
        template=*)
            TEMPLATE_SUBDIR=${arg:9};;
        *)
            echo "Unrecognised argument: $arg"
            echo "Usage:"
            echo " $0 <mode=mode_str> <subdir=label> <template=template_name>"
            echo "    mode_str      : 'DEBUG' or 'RELEASE' (default='DEBUG'; case insensitive)"
            echo "    label         : name of the subdirectory in ./runs/ in which to execute solver (default is YY-mm-DD_HH-MM)"
            echo "    template_name : name of a subdirectory in runs/templates on which to base this run"
            exit 1
    esac
done

# Set mode-dependent options
case "${MODE^^}" in
    DEBUG)
        BUILD_SUBDIR="buildDebug";;
    RELEASE)
        BUILD_SUBDIR="build";;
    *)
        echo "'$MODE' is not a valid mode, choose 'DEBUG' or 'RELEASE' (case insensitive)"
        exit 2;;
esac

REPO_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BIN_DIR="$REPO_ROOT/$BUILD_SUBDIR/dist"
RUNS_DIR="$REPO_ROOT/runs"
RUN_TEMPLATE="$RUNS_DIR/templates/$TEMPLATE_SUBDIR"
EXEC_PATH="$BIN_DIR/ADRSolver"

# Check template exists
if [ ! -d "$RUN_TEMPLATE" ]; then
    echo "No run template at $RUN_TEMPLATE"
    exit 3
fi

# Check executable exists
if [ ! -e "$EXEC_PATH" ]; then
    echo "No solver executable at $EXEC_PATH"
    exit 4
fi

# Set run directory and confirm overwrite if it exists
run_dir="$RUNS_DIR/$RUN_SUBDIR"
if [ -e "$run_dir" ]; then
    read -p "Overwrite existing run directory at $run_dir? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
    \rm -rf "$run_dir"
fi

cp -r "$RUN_TEMPLATE" "$run_dir"
cd "$run_dir" 
mpirun -np 4 "$EXEC_PATH" session.xml
cd -