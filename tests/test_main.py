import unittest
from unittest.mock import Mock

from app import main


class TestAcmeRecord(unittest.TestCase):

    def test_update_challenge_record(self):
        api_client = Mock()
        api_client.update_address.return_value = True

        result = main.update_challenge_record(api_client, "new-challenge-value")

        self.assertTrue(result)
        api_client.update_address.assert_called_once_with(
            "_acme-challenge", "TXT", "new-challenge-value"
        )


if __name__ == "__main__":
    unittest.main()