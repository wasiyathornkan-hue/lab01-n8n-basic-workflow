"""
Lab 01: n8n Basic Workflow - Auto-grading Tests
================================================

Test cases สำหรับตรวจสอบ Student Grade Calculator Workflow
ตรวจสอบจากไฟล์ workflow.json โดยไม่ต้องรัน n8n

การรัน tests:
    pytest tests/test_workflow.py -v
"""

import pytest
import json
import os
import re

# Configuration
WORKFLOW_FILE = 'workflow.json'


class TestWorkflowStructure:
    """Test cases สำหรับตรวจสอบโครงสร้าง workflow.json (40 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        """Load workflow.json before each test"""
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                self.connections = self.workflow.get('connections', {})
        else:
            self.workflow = None
            self.nodes = []
            self.connections = {}

    def test_01_workflow_file_exists(self):
        """
        Test 1: ตรวจสอบว่ามีไฟล์ workflow.json (10 คะแนน)
        """
        assert os.path.exists(WORKFLOW_FILE), \
            "workflow.json not found - please export workflow from n8n"

    def test_02_workflow_valid_json(self):
        """
        Test 2: ตรวจสอบว่า workflow.json เป็น valid JSON (10 คะแนน)
        """
        assert self.workflow is not None, \
            "workflow.json is not valid JSON"
        assert 'nodes' in self.workflow, \
            "workflow.json missing 'nodes' key"

    def test_03_has_webhook_node(self):
        """
        Test 3: ตรวจสอบว่ามี Webhook Node (10 คะแนน)
        """
        webhook_nodes = [n for n in self.nodes if 'webhook' in n.get('type', '').lower()]
        assert len(webhook_nodes) > 0, \
            "Workflow does not have Webhook node"

    def test_04_has_code_node(self):
        """
        Test 4: ตรวจสอบว่ามี Code Node (10 คะแนน)
        """
        code_nodes = [n for n in self.nodes if 'code' in n.get('type', '').lower()]
        assert len(code_nodes) > 0, \
            "Workflow does not have Code node"


class TestWebhookConfiguration:
    """Test cases สำหรับตรวจสอบการตั้งค่า Webhook (20 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        """Load workflow.json before each test"""
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                # Find webhook node
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
        """
        Test 5: ตรวจสอบว่า Webhook ใช้ POST method (10 คะแนน)
        """
        if self.webhook_node is None:
            pytest.skip("No webhook node found")
        
        params = self.webhook_node.get('parameters', {})
        http_method = params.get('httpMethod', '').upper()
        
        assert http_method == 'POST', \
            f"Webhook should use POST method, got '{http_method}'"

    def test_06_webhook_path_lab01(self):
        """
        Test 6: ตรวจสอบว่า Webhook path เป็น 'lab01' (10 คะแนน)
        """
        if self.webhook_node is None:
            pytest.skip("No webhook node found")
        
        params = self.webhook_node.get('parameters', {})
        path = params.get('path', '')
        
        assert path == 'lab01', \
            f"Webhook path should be 'lab01', got '{path}'"


class TestCodeNodeLogic:
    """Test cases สำหรับตรวจสอบ Code Node (40 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        """Load workflow.json before each test"""
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                # Find code node
                self.code_node = None
                self.js_code = ""
                for node in self.nodes:
                    if 'code' in node.get('type', '').lower():
                        self.code_node = node
                        self.js_code = node.get('parameters', {}).get('jsCode', '')
                        break
        else:
            self.workflow = None
            self.nodes = []
            self.code_node = None
            self.js_code = ""

    def test_07_code_calculates_total(self):
        """
        Test 7: ตรวจสอบว่า Code คำนวณ total (10 คะแนน)
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        # Check for total calculation patterns
        has_total = any([
            'reduce' in self.js_code,
            'total' in self.js_code.lower(),
            '.sum' in self.js_code,
        ])
        
        assert has_total, \
            "Code should calculate total (sum of scores)"

    def test_08_code_calculates_average(self):
        """
        Test 8: ตรวจสอบว่า Code คำนวณ average (10 คะแนน)
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        # Check for average calculation patterns
        has_average = any([
            'average' in self.js_code.lower(),
            '/ ' in self.js_code and 'length' in self.js_code,
            '/input.scores.length' in self.js_code,
        ])
        
        assert has_average, \
            "Code should calculate average"

    def test_09_code_has_grade_logic(self):
        """
        Test 9: ตรวจสอบว่า Code มีการตัดเกรด (10 คะแนน)
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        # Check for grade assignment
        has_grade = any([
            'grade' in self.js_code.lower(),
            "'A'" in self.js_code or '"A"' in self.js_code,
            "'B'" in self.js_code or '"B"' in self.js_code,
        ])
        
        # Check for conditional logic
        has_conditions = any([
            '>= 80' in self.js_code or '>=80' in self.js_code,
            '>= 70' in self.js_code or '>=70' in self.js_code,
        ])
        
        assert has_grade and has_conditions, \
            "Code should have grade calculation logic (A, B, C, D, F)"

    def test_10_code_has_status_logic(self):
        """
        Test 10: ตรวจสอบว่า Code มีการกำหนด status (10 คะแนน)
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        # Check for status assignment
        has_status = any([
            'status' in self.js_code.lower(),
            "'passed'" in self.js_code or '"passed"' in self.js_code,
            "'failed'" in self.js_code or '"failed"' in self.js_code,
        ])
        
        assert has_status, \
            "Code should have status logic (passed/failed)"


class TestOutputFields:
    """Bonus tests สำหรับตรวจสอบ output fields"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        """Load workflow.json before each test"""
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
                # Find code node
                self.code_node = None
                self.js_code = ""
                for node in self.nodes:
                    if 'code' in node.get('type', '').lower():
                        self.code_node = node
                        self.js_code = node.get('parameters', {}).get('jsCode', '')
                        break
        else:
            self.workflow = None
            self.nodes = []
            self.code_node = None
            self.js_code = ""

    def test_output_has_student_id(self):
        """
        Bonus: ตรวจสอบว่า output มี student_id
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        assert 'student_id' in self.js_code, \
            "Output should include student_id"

    def test_output_has_name(self):
        """
        Bonus: ตรวจสอบว่า output มี name
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        assert 'name' in self.js_code, \
            "Output should include name"

    def test_output_returns_json(self):
        """
        Bonus: ตรวจสอบว่า return เป็น JSON format
        """
        if not self.js_code:
            pytest.skip("No code node found")
        
        has_return = 'return' in self.js_code and 'json' in self.js_code.lower()
        
        assert has_return, \
            "Code should return JSON object"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
