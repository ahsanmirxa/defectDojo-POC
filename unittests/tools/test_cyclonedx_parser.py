import datetime
from ..dojo_test_case import DojoTestCase

from dojo.models import Test, Finding
from dojo.tools.cyclonedx.parser import CycloneDXParser


class TestParser(DojoTestCase):

    def test_grype_report(self):
        with open("unittests/scans/cyclonedx/grype_dd_1_14_1.xml") as file:
            parser = CycloneDXParser()
            findings = list(parser.get_findings(file, Test()))
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(619, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Deprecated", finding.component_name)
                self.assertEqual("1.2.12", finding.component_version)
                self.assertEqual(datetime.date(2021, 4, 13), datetime.datetime.date(finding.date))
            with self.subTest(i=200):
                finding = findings[200]
                self.assertEqual("High", finding.severity)
                self.assertEqual("jira", finding.component_name)
                self.assertEqual("2.0.0", finding.component_version)
                self.assertEqual("CVE-2019-8443", finding.cve)
                self.assertEqual(datetime.date(2021, 4, 13), datetime.datetime.date(finding.date))

    def test_spec1_report(self):
        """Test a report from the spec itself"""
        with open("unittests/scans/cyclonedx/spec1.xml") as file:
            parser = CycloneDXParser()
            findings = list(parser.get_findings(file, Test()))
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(2, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertIsNone(finding.cve)
                self.assertEqual("Info", finding.severity)
            with self.subTest(i=1):
                finding = findings[1]
                self.assertEqual("CVE-2018-7489", finding.cve)
                self.assertEqual("Critical", finding.severity)
                self.assertIn(finding.cwe, [184, 502])  # there is 2 CWE in the report
                self.assertEqual("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", finding.cvssv3)
                self.assertEqual("jackson-databind", finding.component_name)
                self.assertEqual("2.9.9", finding.component_version)
                self.assertEqual("CVE-2018-7489", finding.vuln_id_from_tool)

    def test_cyclonedx_bom_report(self):
        with open("unittests/scans/cyclonedx/cyclonedx_bom.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(73, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("asteval", finding.component_name)
                self.assertEqual("0.9.23", finding.component_version)

    def test_cyclonedx_jake_report(self):
        """Test a report generated by Jake"""
        with open("unittests/scans/cyclonedx/jake.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(204, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("yaspin", finding.component_name)
                self.assertEqual("0.16.0", finding.component_version)

    def test_cyclonedx_retirejs_report(self):
        """Test a report generated by RetireJS"""
        with open("unittests/scans/cyclonedx/retirejs.latest.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(6, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("handlebars", finding.component_name)
                self.assertEqual("3.0.0", finding.component_version)
            with self.subTest(i=5):
                finding = findings[5]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("jquery", finding.component_name)
                self.assertEqual("1.8.0", finding.component_version)

    def test_cyclonedx_grype_11_report(self):
        """Test a report generated by Grype 0.11"""
        with open("unittests/scans/cyclonedx/dd_1_15_0.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(689, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Deprecated", finding.component_name)
                self.assertEqual("1.2.12", finding.component_version)
            with self.subTest(i=5):
                finding = findings[5]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Jinja2", finding.component_name)
                self.assertEqual("2.11.3", finding.component_version)
            with self.subTest(i=640):
                finding = findings[640]
                self.assertEqual("High", finding.severity)
                self.assertEqual("redis", finding.component_name)
                self.assertEqual("3.5.3", finding.component_version)
                self.assertEqual("CVE-2018-12326", finding.cve)
                self.assertEqual("CVSS:3.0/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", finding.cvssv3)
                self.assertIn("Buffer overflow in redis-cli of Redis before 4.0.10 and 5.x before 5.0 RC3", finding.description)
                self.assertEqual("CVE-2018-12326", finding.vuln_id_from_tool)
            with self.subTest(i=641):
                finding = findings[641]
                self.assertEqual("High", finding.severity)
                self.assertEqual("redis", finding.component_name)
                self.assertEqual("3.5.3", finding.component_version)
                self.assertEqual("CVE-2018-12453", finding.cve)
                self.assertEqual("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H", finding.cvssv3)
                self.assertEqual(
                    "Type confusion in the xgroupCommand function in t_stream.c in redis-server in Redis before 5.0 allows"
                    " remote attackers to cause denial-of-service via an XGROUP command in which the key is not a stream.",
                    finding.description)
                self.assertEqual("CVE-2018-12453", finding.vuln_id_from_tool)
