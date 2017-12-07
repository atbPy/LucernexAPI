import report_builder
import unittest
from collections import defaultdict

class ReportBuilderTest(unittest.TestCase):
    def setUp(self):
        self.current_working_directory = "C:/Users/abednar/PycharmProjects/LucernexAPI/"

        self.data = defaultdict(dict)

        self.data = {'68701': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'},
                          'CustomCodeFieldName': 'Kilometer(s)'},
                '68702': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'},
                          'CustomCodeFieldName': 'Meter(s)'},
                '68703': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'},
                          'CustomCodeFieldName': 'Mile(s)'}}

    def test_create_report_file_name(self):
        name = "ReportTest"
        expected = "C:\\Users\\abednar\\PycharmProjects\\LucernexAPI\\Reports\\ReportTest.xlsx"
        actual = report_builder.create_report_file_name("ReportTest")
        self.assertEqual(expected, actual)

    def test_create_report_file_name_bad_input(self):
        with self.assertRaises(TypeError):
            report_builder.create_report_file_name(None)


if __name__ == '__main__':
    unittest.main()