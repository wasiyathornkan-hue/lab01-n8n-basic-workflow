"""
Lab 01: n8n Basic Workflow - Auto-grading Tests
ตรวจสอบจากไฟล์ workflow.json โดยไม่ต้องรัน n8n
"""

import pytest
import json
import os

WORKFLOW_FILE = 'workflow.json'


class TestWorkflowStructure:
    """ตรวจสอบโครงสร้าง workflow.json (40 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
        else:
            self.workflow = None
            self.nodes = []

    def test_01_workflow_file_exists(self):
        """Test 1: มีไฟล์ workflow.json (10 คะแนน)"""
        assert os.path.exists(WORKFLOW_FILE), \
            "workflow.json not found - please export workflow from n8n"

    def test_02_workflow_valid_json(self):
        """Test 2: เป็น valid JSON (10 คะแนน)"""
        assert self.workflow is not None, "workflow.json is not valid JSON"
        assert 'nodes' in self.workflow, "workflow.json missing 'nodes' key"

    def test_03_has_webhook_node(self):
        """Test 3: มี Webhook Node (10 คะแนน)"""
        webhook_nodes = [n for n in self.nodes if 'webhook' in n.get('type', '').lower()]
        assert len(webhook_nodes) > 0, "Workflow does not have Webhook node"

    def test_04_has_code_node(self):
        """Test 4: มี Code Node (10 คะแนน)"""
        code_nodes = [n for n in self.nodes if 'code' in n.get('type', '').lower()]
        assert len(code_nodes) > 0, "Workflow does not have Code node"


class TestWebhookConfiguration:
    """ตรวจสอบการตั้งค่า Webhook (20 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                self.webhook_node = None
                for node in self.nodes:
                    if 'webhook' in node.get('type', '').lower():
                        self.webhook_node = node
                        break
        else:
            self.workflow = None
            self.nodes = []
            self.webhook_node = None

    def test_05_webhook_method_post(self):
        """Test 5: Webhook ใช้ POST method (10 คะแนน)"""
        if self.webhook_node is None:
            pytest.skip("No webhook node found")
        params = self.webhook_node.get('parameters', {})
        http_method = params.get('httpMethod', '').upper()
        assert http_method == 'POST', f"Webhook should use POST method, got '{http_method}'"

    def test_06_webhook_path_lab01(self):
        """Test 6: Webhook path เป็น 'lab01' (10 คะแนน)"""
        if self.webhook_node is None:
            pytest.skip("No webhook node found")
        params = self.webhook_node.get('parameters', {})
        path = params.get('path', '')
        assert path == 'lab01', f"Webhook path should be 'lab01', got '{path}'"


class TestCodeNodeLogic:
    """ตรวจสอบ Code Node (40 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                self.js_code = ""
                for node in self.nodes:
                    if 'code' in node.get('type', '').lower():
                        self.js_code = node.get('parameters', {}).get('jsCode', '')
                        break
        else:
            self.workflow = None
            self.nodes = []
            self.js_code = ""

    def test_07_code_calculates_total(self):
        """Test 7: Code คำนวณ total (10 คะแนน)"""
        if not self.js_code:
            pytest.skip("No code node found")
        has_total = 'reduce' in self.js_code or 'total' in self.js_code.lower()
        assert has_total, "Code should calculate total (sum of scores)"

    def test_08_code_calculates_average(self):
        """Test 8: Code คำนวณ average (10 คะแนน)"""
        if not self.js_code:
            pytest.skip("No code node found")
        has_average = 'average' in self.js_code.lower() or ('/' in self.js_code and 'length' in self.js_code)
        assert has_average, "Code should calculate average"

    def test_09_code_has_grade_logic(self):
        """Test 9: Code มีการตัดเกรด (10 คะแนน)"""
        if not self.js_code:
            pytest.skip("No code node found")
        has_grade = 'grade' in self.js_code.lower()
        has_conditions = '>= 80' in self.js_code or '>=80' in self.js_code
        assert has_grade and has_conditions, "Code should have grade calculation logic"

    def test_10_code_has_status_logic(self):
        """Test 10: Code มี status logic (10 คะแนน)"""
        if not self.js_code:
            pytest.skip("No code node found")
        has_status = 'passed' in self.js_code or 'failed' in self.js_code
        assert has_status, "Code should have status logic (passed/failed)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
