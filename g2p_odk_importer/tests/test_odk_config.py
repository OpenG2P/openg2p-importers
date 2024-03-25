from unittest.mock import patch

from odoo.tests.common import TransactionCase

from odoo.addons.g2p_odk_importer.models.odk_client import ODKClient


class TestOdkConfig(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_url = "http://example.com"
        self.username = "test_user"
        self.password = "test_password"
        self.project_id = 5
        self.form_id = "test_form_id"
        self.target_registry = "group"
        self.json_formatter = "{ name: .name, age: .age }"

    @patch.object(ODKClient, "login")
    @patch.object(ODKClient, "test_connection")
    def test_test_connection(self, mock_test_connection, mock_login):
        mock_test_connection.return_value = True
        mock_login.return_value = None

        odk_config = self.env["odk.config"].create(
            {
                "name": "Test ODK Config",
                "base_url": self.base_url,
                "username": self.username,
                "password": self.password,
                "project": self.project_id,
                "form_id": self.form_id,
                "target_registry": self.target_registry,
                "json_formatter": self.json_formatter,
            }
        )

        result = odk_config.test_connection()

        self.assertTrue(mock_login.called)
        self.assertTrue(mock_test_connection.called)
        self.assertEqual(result["params"]["type"], "success")
        self.assertEqual(result["params"]["message"], "Tested successfully.")

    @patch.object(ODKClient, "login")
    @patch.object(ODKClient, "import_delta_records")
    def test_import_records(self, mock_import_delta_records, mock_login):
        mock_import_delta_records.return_value = {"form_updated": True}
        mock_login.return_value = None

        odk_config = self.env["odk.config"].create(
            {
                "name": "Test ODK Config",
                "base_url": self.base_url,
                "username": self.username,
                "password": self.password,
                "project": self.project_id,
                "form_id": self.form_id,
                "target_registry": self.target_registry,
                "json_formatter": self.json_formatter,
            }
        )

        result = odk_config.import_records()

        self.assertTrue(mock_login.called)
        self.assertTrue(mock_import_delta_records.called)
        self.assertEqual(result["params"]["type"], "success")
        self.assertEqual(
            result["params"]["message"], "ODK form records were imported successfully."
        )

    @patch.object(ODKClient, "login")
    @patch.object(ODKClient, "import_delta_records")
    def test_import_records_no_updates(self, mock_import_delta_records, mock_login):
        mock_login.return_value = None

        odk_config = self.env["odk.config"].create(
            {
                "name": "Test ODK Config",
                "base_url": self.base_url,
                "username": self.username,
                "password": self.password,
                "project": self.project_id,
                "form_id": self.form_id,
                "target_registry": self.target_registry,
                "json_formatter": self.json_formatter,
            }
        )

        result = odk_config.import_records()

        self.assertTrue(mock_login.called)
        self.assertTrue(mock_import_delta_records.called)
        self.assertEqual(result["params"]["type"], "warning")
        self.assertEqual(
            result["params"]["message"], "No new form records were submitted."
        )
