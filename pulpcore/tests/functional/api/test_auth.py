# coding=utf-8
"""Tests for Pulp 3's authentication API.

For more information, see the documentation on `Authentication
<http://docs.pulpproject.org/en/3.0/nightly/integration_guide/rest_api/authentication.html>`_.
"""
import unittest

from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import BASE_PATH

from tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class AuthTestCase(unittest.TestCase):
    """Test Pulp3 Authentication."""

    def setUp(self):
        """Create class-wide variables."""
        self.cfg = config.get_config()

    def test_base_auth_success(self):
        """Perform HTTP basic authentication with valid credentials.

        Assert that a response indicating success is returned.
        """
        api.Client(self.cfg, api.json_handler).get(
            BASE_PATH,
            auth=HTTPBasicAuth(*self.cfg.pulp_auth),
        )

    def test_base_auth_failure(self):
        """Perform HTTP basic authentication with invalid credentials.

        Assert that a response indicating failure is returned.
        """
        self.cfg.pulp_auth[1] = utils.uuid4()  # randomize password
        with self.assertRaises(HTTPError):
            api.Client(self.cfg, api.json_handler).get(
                BASE_PATH,
                auth=HTTPBasicAuth(*self.cfg.pulp_auth),
            )
