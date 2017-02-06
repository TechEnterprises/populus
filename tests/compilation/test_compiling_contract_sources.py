import pytest
import textwrap
import json

import os

from populus import Project
from populus.compilation import (
    compile_project_contracts,
)


BASE_DIR= os.path.abspath(os.path.dirname(__file__))

project_dir = os.path.join(BASE_DIR, 'projects', 'test-01')


CONTRACT_A_SOURCE = textwrap.dedent(("""pragma solidity ^0.4.0;

    import "contracts/ContractB.sol";
    import "contracts/ContractC.sol";

    contract A is C {
        function A() {
            B.doit();
        }
    }
"""))


CONTRACT_B_SOURCE = textwrap.dedent(("""pragma solidity ^0.4.0;

    library B {
        function doit() {}
    }
"""))


CONTRACT_C_SOURCE = textwrap.dedent(("""pragma solidity ^0.4.0;

    contract C {
        function C() {}
    }
"""))


def test_compiling_with_single_contract(project_dir, write_project_file):
    write_project_file('contracts/Math.sol', CONTRACT_C_SOURCE)

    project = Project()

    source_paths, contract_data = compile_project_contracts(project)

    assert 'contracts/Math.sol' in source_paths

    assert 'Math' in contract_data


def test_compilation_with_imports(project_dir, write_project_file):
    write_project_file('contracts/ContractA.sol', CONTRACT_A_SOURCE)
    write_project_file('contracts/ContractB.sol', CONTRACT_B_SOURCE)
    write_project_file('contracts/ContractC.sol', CONTRACT_C_SOURCE)

    project = Project()

    source_paths, contract_data = compile_project_contracts(project)

    assert 'A' in contract_data
    assert 'B' in contract_data
    assert 'C' in contract_data


def test_compiling_with_instaled_package(project_dir, write_project_file):
    # TODO: make it easier to have an installed package.
    assert False
