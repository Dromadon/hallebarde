import os
import subprocess
from typing import List
from unittest import TestCase


class TestMakePackage(TestCase):

    def setUp(self) -> None:
        path_to_current_test_file = os.path.dirname(os.path.realpath(__file__))
        self.path_to_package = path_to_current_test_file + "/../../app/package/"
        self.path_to_makefile: str = path_to_current_test_file + "/../.."

    def test_make_package_should_clean_package_folder_in_app_directory(self):
        # Given
        file_to_clean = "old_package.zip"
        subprocess.check_output(["touch", file_to_clean], cwd=self.path_to_package)

        # When
        subprocess.check_output(["make", "package"], cwd=self.path_to_makefile)

        # Then
        list_of_files_in_package_folder: List[str] = os.listdir(self.path_to_package)
        assert file_to_clean not in list_of_files_in_package_folder

    def test_make_package_should_generate_lambda_artifacts_as_unit_zip_files(self):
        # Given
        expected_zip_artifacts = ["get_token.zip", "get_presigned_url.zip", "authorizer.zip"]

        # When
        subprocess.check_output(["make", "package"], cwd=self.path_to_makefile)

        # Then
        files_in_package_folder: List[str] = os.listdir(self.path_to_package)
        zip_files_in_package_folder = [file for file in files_in_package_folder if file.endswith('.zip')]
        assert set(expected_zip_artifacts) == set(zip_files_in_package_folder)
