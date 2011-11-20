#!/bin/bash
CODEBASE="${HOME}/lumberyard"
export PYTHONPATH="${CODEBASE}"

pushd "${CODEBASE}/docs"
make html
popd
