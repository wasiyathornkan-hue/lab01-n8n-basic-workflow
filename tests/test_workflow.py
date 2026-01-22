"""
Lab 01: n8n Basic Workflow - Auto-grading Tests
================================================

Test cases สำหรับตรวจสอบ Student Grade Calculator Workflow

การรัน tests:
    pytest tests/test_workflow.py -v

หมายเหตุ:
    - ต้องรัน n8n ที่ localhost:5678 ก่อนรัน tests
    - Webhook path ต้องเป็น /webhook-test/lab01
"""

import pytest
import requests
import json
import os
import time

# Configuration
N8N_BASE_URL = os.environ.get("N8N_BASE_URL", "http://localhost:5678")
WEBHOOK_PATH = "/webhook-test/lab01"
WEBHOOK_URL = f"{N8N_BASE_URL}{WEBHOOK_PATH}"

# Timeout for requests
REQUEST_TIMEOUT = 30


class TestLab01BasicWorkflow:
    """Test cases สำหรับ Lab 01: Student Grade Calculator"""

    # ==================== Helper Methods ====================
    
    def send_request(self, data: dict) -> requests.Response:
        """ส่ง POST request ไปยัง Webhook"""
        return requests.post(
            WEBHOOK_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )

    # ==================== Test Cases ====================

    def test_01_webhook_accepts_post(self):
        """
        Test 1: Webhook รับ POST request ได้ (10 คะแนน)
        
        ตรวจสอบว่า Webhook endpoint ทำงานและตอบกลับ status 200
        """
        data = {
            "student_id": "test001",
            "name": "Test User",
            "scores": [80]
        }
        
        try:
            response = self.send_request(data)
            assert response.status_code == 200, \
                f"Expected status 200, got {response.status_code}"
        except requests.exceptions.ConnectionError:
            pytest.fail(
                f"ไม่สามารถเชื่อมต่อ n8n ได้ที่ {WEBHOOK_URL}\n"
                "กรุณาตรวจสอบว่า:\n"
                "1. n8n กำลังทำงานอยู่\n"
                "2. Webhook path ถูกต้อง (/webhook-test/lab01)\n"
                "3. Workflow ถูก activate แล้ว"
            )
        except requests.exceptions.Timeout:
            pytest.fail(f"Request timeout หลังจาก {REQUEST_TIMEOUT} วินาที")

    def test_02_returns_json(self):
        """
        Test 2: Response เป็น JSON format (10 คะแนน)
        
        ตรวจสอบว่า Response มี Content-Type เป็น application/json
        """
        data = {
            "student_id": "test002",
            "name": "Test User",
            "scores": [80]
        }
        
        response = self.send_request(data)
        content_type = response.headers.get('Content-Type', '')
        
        assert 'application/json' in content_type.lower(), \
            f"Expected Content-Type to contain 'application/json', got '{content_type}'"
        
        # ตรวจสอบว่า parse JSON ได้
        try:
            response.json()
        except json.JSONDecodeError:
            pytest.fail("Response ไม่สามารถ parse เป็น JSON ได้")

    def test_03_student_id_preserved(self):
        """
        Test 3: student_id ถูกส่งกลับมาถูกต้อง (10 คะแนน)
        
        ตรวจสอบว่า student_id ใน response ตรงกับ input
        """
        test_id = "65001234"
        data = {
            "student_id": test_id,
            "name": "Test User",
            "scores": [80]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("student_id") == test_id, \
            f"Expected student_id '{test_id}', got '{result.get('student_id')}'"

    def test_04_name_preserved(self):
        """
        Test 4: name ถูกส่งกลับมาถูกต้อง (10 คะแนน)
        
        ตรวจสอบว่า name ใน response ตรงกับ input (รวมถึงภาษาไทย)
        """
        test_name = "สมชาย ใจดี"
        data = {
            "student_id": "test004",
            "name": test_name,
            "scores": [80]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("name") == test_name, \
            f"Expected name '{test_name}', got '{result.get('name')}'"

    def test_05_total_calculation(self):
        """
        Test 5: คำนวณ total ถูกต้อง (15 คะแนน)
        
        ตรวจสอบว่าผลรวมของ scores ถูกต้อง
        """
        scores = [85, 90, 78, 92, 88]
        expected_total = sum(scores)  # 433
        
        data = {
            "student_id": "test005",
            "name": "Test User",
            "scores": scores
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("total") == expected_total, \
            f"Expected total {expected_total}, got {result.get('total')}"

    def test_06_average_calculation(self):
        """
        Test 6: คำนวณ average ถูกต้อง (15 คะแนน)
        
        ตรวจสอบว่าค่าเฉลี่ยถูกต้อง (ทศนิยม 1 ตำแหน่ง)
        """
        scores = [80, 90, 100]
        expected_average = 90.0
        
        data = {
            "student_id": "test006",
            "name": "Test User",
            "scores": scores
        }
        
        response = self.send_request(data)
        result = response.json()
        
        actual_average = result.get("average")
        
        # ยอมรับความคลาดเคลื่อนเล็กน้อยจากการปัดเศษ
        assert abs(actual_average - expected_average) < 0.1, \
            f"Expected average {expected_average}, got {actual_average}"

    def test_07_grade_a(self):
        """
        Test 7: ตัดเกรด A ถูกต้อง (10 คะแนน)
        
        เมื่อ average >= 80 ต้องได้เกรด A
        """
        # average = 86.67 (ควรได้ A)
        data = {
            "student_id": "test007",
            "name": "Test User",
            "scores": [85, 90, 85]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("grade") == "A", \
            f"Expected grade 'A' for average >= 80, got '{result.get('grade')}'"

    def test_08_grade_b(self):
        """
        Test 8: ตัดเกรด B ถูกต้อง (5 คะแนน)
        
        เมื่อ 70 <= average < 80 ต้องได้เกรด B
        """
        # average = 74.33 (ควรได้ B)
        data = {
            "student_id": "test008",
            "name": "Test User",
            "scores": [70, 75, 78]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("grade") == "B", \
            f"Expected grade 'B' for 70 <= average < 80, got '{result.get('grade')}'"

    def test_09_status_passed(self):
        """
        Test 9: status passed ถูกต้อง (10 คะแนน)
        
        เมื่อ average >= 50 ต้องได้ status "passed"
        """
        # average = 55.0 (ควรได้ passed)
        data = {
            "student_id": "test009",
            "name": "Test User",
            "scores": [50, 60, 55]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("status") == "passed", \
            f"Expected status 'passed' for average >= 50, got '{result.get('status')}'"

    def test_10_status_failed(self):
        """
        Test 10: status failed ถูกต้อง (5 คะแนน)
        
        เมื่อ average < 50 ต้องได้ status "failed"
        """
        # average = 38.33 (ควรได้ failed)
        data = {
            "student_id": "test010",
            "name": "Test User",
            "scores": [30, 40, 45]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("status") == "failed", \
            f"Expected status 'failed' for average < 50, got '{result.get('status')}'"


class TestWorkflowFile:
    """Test cases สำหรับตรวจสอบไฟล์ workflow.json"""

    def test_workflow_file_exists(self):
        """
        Bonus: ตรวจสอบว่ามีไฟล์ workflow.json
        """
        assert os.path.exists('workflow.json'), \
            "ไม่พบไฟล์ workflow.json - กรุณา export workflow จาก n8n"

    def test_workflow_valid_json(self):
        """
        Bonus: ตรวจสอบว่า workflow.json เป็น valid JSON
        """
        if not os.path.exists('workflow.json'):
            pytest.skip("ไม่พบไฟล์ workflow.json")
        
        with open('workflow.json', 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"workflow.json ไม่ใช่ valid JSON: {e}")
        
        # ตรวจสอบว่ามี nodes
        assert 'nodes' in data, "workflow.json ไม่มี 'nodes' key"

    def test_workflow_has_webhook(self):
        """
        Bonus: ตรวจสอบว่า workflow มี Webhook node
        """
        if not os.path.exists('workflow.json'):
            pytest.skip("ไม่พบไฟล์ workflow.json")
        
        with open('workflow.json', 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        
        nodes = workflow.get('nodes', [])
        node_types = [node.get('type', '').lower() for node in nodes]
        
        has_webhook = any('webhook' in t for t in node_types)
        assert has_webhook, "Workflow ไม่มี Webhook node"


# ==================== Additional Test Cases (Edge Cases) ====================

class TestEdgeCases:
    """Test cases สำหรับ edge cases"""

    def send_request(self, data: dict) -> requests.Response:
        """ส่ง POST request ไปยัง Webhook"""
        return requests.post(
            WEBHOOK_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )

    def test_single_score(self):
        """
        Edge Case: มีคะแนนแค่ 1 ตัว
        """
        data = {
            "student_id": "edge001",
            "name": "Single Score",
            "scores": [75]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("total") == 75
        assert result.get("average") == 75.0
        assert result.get("grade") == "B"

    def test_perfect_score(self):
        """
        Edge Case: คะแนนเต็ม 100 ทุกวิชา
        """
        data = {
            "student_id": "edge002",
            "name": "Perfect Score",
            "scores": [100, 100, 100, 100, 100]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("total") == 500
        assert result.get("average") == 100.0
        assert result.get("grade") == "A"
        assert result.get("status") == "passed"

    def test_zero_score(self):
        """
        Edge Case: คะแนน 0 ทุกวิชา
        """
        data = {
            "student_id": "edge003",
            "name": "Zero Score",
            "scores": [0, 0, 0]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("total") == 0
        assert result.get("average") == 0.0
        assert result.get("grade") == "F"
        assert result.get("status") == "failed"

    def test_boundary_grade_a(self):
        """
        Edge Case: คะแนนพอดี 80 (boundary ของ A)
        """
        data = {
            "student_id": "edge004",
            "name": "Boundary A",
            "scores": [80, 80, 80]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("grade") == "A", \
            "average = 80 ควรได้เกรด A"

    def test_boundary_pass(self):
        """
        Edge Case: คะแนนพอดี 50 (boundary ของ pass)
        """
        data = {
            "student_id": "edge005",
            "name": "Boundary Pass",
            "scores": [50, 50, 50]
        }
        
        response = self.send_request(data)
        result = response.json()
        
        assert result.get("status") == "passed", \
            "average = 50 ควรได้ status passed"
        assert result.get("grade") == "D", \
            "average = 50 ควรได้เกรด D"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
