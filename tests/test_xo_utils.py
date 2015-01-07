import os

import xo_server.common.utils as utils


INPUT_FILES_DIR = "tests/input_files/test_xo_utils"
ETALON_FILES_DIR = "tests/etalon_files/test_xo_utils"

class TestSuperInclude(object):
    def test_simple_load(self):
        input_file_path = os.path.join(INPUT_FILES_DIR, "common.yml")
        data = open(input_file_path).read()
        data_after_include = utils.super_include(data)

        etalon_file_path = os.path.join(ETALON_FILES_DIR, "test_simple_load_etalon.yml")
        etalon_data = open(etalon_file_path).read()
        assert data_after_include == etalon_data

    def test_cascade_load(self):
        input_file_path = os.path.join(INPUT_FILES_DIR, "game_service1.yml")
        data = open(input_file_path).read()
        data_after_include = utils.super_include(data)

        etalon_file_path = os.path.join(ETALON_FILES_DIR, "test_cascade_load_etalon.yml")
        etalon_data = open(etalon_file_path).read()
        assert data_after_include == etalon_data
