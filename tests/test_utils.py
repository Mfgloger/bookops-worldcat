# -*- coding: utf-8 -*-

import pytest

from bookops_worldcat.utils import (
    _str2list,
    _parse_error_response,
    verify_oclc_number,
    verify_oclc_numbers,
)
from bookops_worldcat.errors import InvalidOclcNumber


class MockServiceErrorResponse:
    """Simulates error response from the web service"""

    def __init__(self):
        self.status_code = 400
        self.url = "https://test.org/some_endpoint"
        self.text = "{'type': 'MISSING_QUERY_PARAMETER', 'title': 'Validation Failure', 'detail': 'details here'}"

    def json(self):
        return {
            "type": "MISSING_QUERY_PARAMETER",
            "title": "Validation Failure",
            "detail": "details here",
        }


class TestUtils:
    """Tests various methods in utils module"""

    @pytest.mark.parametrize(
        "argm,expectation",
        [
            ("12345", ["12345"]),
            ("12345,67890", ["12345", "67890"]),
            ("12345, 67890", ["12345", "67890"]),
        ],
    )
    def test_str2list(self, argm, expectation):
        assert _str2list(argm) == expectation

    @pytest.mark.parametrize(
        "argm,expectation,msg",
        [
            (
                None,
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclc_number' is missing.",
            ),
            (
                [12345],
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclc_number' is of invalid type.",
            ),
            (
                12345.5,
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclc_number' is of invalid type.",
            ),
            (
                "bt12345",
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclc_number' does not look like real OCLC #.",
            ),
            (
                "odn12345",
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclc_number' does not look like real OCLC #.",
            ),
        ],
    )
    def test_verify_oclc_number_exceptions(self, argm, expectation, msg):
        with expectation as exp:
            verify_oclc_number(argm)
            assert msg == str(exp.value)

    @pytest.mark.parametrize(
        "argm,expectation",
        [
            ("000012345", 12345),
            (12345, 12345),
            ("ocm00012345", 12345),
            ("ocn00012345", 12345),
            ("ocn12345", 12345),
            (" on12345 \n", 12345),
        ],
    )
    def test_verify_oclc_number_success(self, argm, expectation):
        assert verify_oclc_number(argm) == expectation

    @pytest.mark.parametrize(
        "argm,expectation,msg",
        [
            (
                None,
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclcNumbers' must be a list or comma separated string of valid OCLC #.",
            ),
            (
                "",
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclcNumbers' must be a list or comma separated string of valid OCLC #.",
            ),
            (
                [],
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclcNumbers' must be a list or comma separated string of valid OCLC #.",
            ),
            (
                ",,",
                pytest.raises(InvalidOclcNumber),
                "Argument 'oclcNumbers' must be a list or comma separated string of valid OCLC #.",
            ),
            (
                12345.5,
                pytest.raises(InvalidOclcNumber),
                "One of passed OCLC #s is invalid.",
            ),
            (
                "bt12345",
                pytest.raises(InvalidOclcNumber),
                "One of passed OCLC #s is invalid.",
            ),
            (
                "odn12345",
                pytest.raises(InvalidOclcNumber),
                "One of passed OCLC #s is invalid.",
            ),
        ],
    )
    def test_verify_oclc_numbers_exceptions(self, argm, expectation, msg):
        with expectation as exp:
            verify_oclc_numbers(argm)
            assert msg == str(exp.value)

    @pytest.mark.parametrize(
        "argm,expectation",
        [
            ("12345", ["12345"]),
            ("12345,67890", ["12345", "67890"]),
            ("ocm12345, ocm67890", ["12345", "67890"]),
            ([12345, 67890], ["12345", "67890"]),
            (["ocn12345", "on67890"], ["12345", "67890"]),
        ],
    )
    def test_verify_oclc_numbers_parsing(self, argm, expectation):
        assert verify_oclc_numbers(argm) == expectation

    def test_parse_error_response(self):
        response = MockServiceErrorResponse()
        assert (
            _parse_error_response(response)
            == "Web service returned 400 error: {'type': 'MISSING_QUERY_PARAMETER', 'title': 'Validation Failure', 'detail': 'details here'}; https://test.org/some_endpoint"
        )
