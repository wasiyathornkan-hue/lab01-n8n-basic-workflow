# 🔬 Lab 01: n8n Basic Workflow - JSON Processing

## 📋 ข้อมูลทั่วไป

| รายการ | รายละเอียด |
|--------|------------|
| **วิชา** | n8n Workflow Automation |
| **สัปดาห์** | 1 - n8n Fundamental |
| **คะแนนเต็ม** | 100 คะแนน |
| **เวลา** | 2 ชั่วโมง |

## 🎯 วัตถุประสงค์การเรียนรู้

หลังจากทำ Lab นี้เสร็จ นักศึกษาจะสามารถ:

1. สร้าง Workflow พื้นฐานใน n8n ได้
2. ใช้ Webhook Node รับข้อมูล JSON ได้
3. ใช้ Edit Fields Node แปลงและประมวลผลข้อมูลได้
4. เข้าใจ Data Flow และ Expression ใน n8n
5. Export Workflow เป็นไฟล์ JSON ได้

## 📝 โจทย์

สร้าง **Student Grade Calculator Workflow** ที่ทำหน้าที่:

1. รับข้อมูลนักศึกษาผ่าน Webhook (POST request)
2. คำนวณคะแนนรวม (total) และค่าเฉลี่ย (average)
3. ตัดเกรดตามเกณฑ์ที่กำหนด
4. กำหนดสถานะ passed/failed
5. ส่ง Response กลับในรูปแบบ JSON

## 📥 Input Format

Webhook จะรับ POST request พร้อม JSON body ดังนี้:

```json
{
  "student_id": "65001234",
  "name": "สมชาย ใจดี",
  "scores": [85, 90, 78, 92, 88]
}
```

### Input Fields:
| Field | Type | Description |
|-------|------|-------------|
| `student_id` | string | รหัสนักศึกษา |
| `name` | string | ชื่อ-นามสกุล |
| `scores` | array of numbers | คะแนนสอบแต่ละครั้ง |

## 📤 Expected Output Format

Workflow ต้อง Response กลับในรูปแบบ JSON ดังนี้:

```json
{
  "student_id": "65001234",
  "name": "สมชาย ใจดี",
  "total": 433,
  "average": 86.6,
  "grade": "A",
  "status": "passed"
}
```

### Output Fields:
| Field | Type | Description |
|-------|------|-------------|
| `student_id` | string | รหัสนักศึกษา (เหมือน input) |
| `name` | string | ชื่อ-นามสกุล (เหมือน input) |
| `total` | number | ผลรวมคะแนนทั้งหมด |
| `average` | number | ค่าเฉลี่ยคะแนน (ทศนิยม 1 ตำแหน่ง) |
| `grade` | string | เกรด (A, B, C, D, F) |
| `status` | string | สถานะ ("passed" หรือ "failed") |

## 📊 เกณฑ์การตัดเกรด

| ค่าเฉลี่ย | เกรด |
|-----------|------|
| >= 80 | A |
| >= 70 | B |
| >= 60 | C |
| >= 50 | D |
| < 50 | F |

## 📊 เกณฑ์สถานะ

| ค่าเฉลี่ย | สถานะ |
|-----------|--------|
| >= 50 | passed |
| < 50 | failed |

## 🔧 ขั้นตอนการทำ Lab

### Step 1: สร้าง Workflow ใหม่
1. เปิด n8n (http://localhost:5678)
2. คลิก "Create new workflow"
3. ตั้งชื่อ Workflow: `Lab01-Student-Grade-Calculator`

### Step 2: เพิ่ม Webhook Node
1. คลิก "+" เพื่อเพิ่ม Node
2. ค้นหา "Webhook" แล้วเลือก
3. ตั้งค่า:
   - **HTTP Method**: POST
   - **Path**: `lab01` (URL จะเป็น `/webhook-test/lab01`)
   - **Response Mode**: Last Node

### Step 3: เพิ่ม Code Node สำหรับคำนวณ
1. เพิ่ม Node "Code"
2. เขียน JavaScript เพื่อ:
   - คำนวณ total (ผลรวม scores)
   - คำนวณ average (ค่าเฉลี่ย)
   - ตัดเกรดตามเกณฑ์
   - กำหนดสถานะ

### Step 4: ทดสอบ Workflow
1. คลิก "Test workflow"
2. ใช้ Postman หรือ curl ส่ง POST request:

```bash
curl -X POST http://localhost:5678/webhook-test/lab01 \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "65001234",
    "name": "สมชาย ใจดี",
    "scores": [85, 90, 78, 92, 88]
  }'
```

### Step 5: Export Workflow
1. คลิกที่ Menu (⋮) ของ Workflow
2. เลือก "Download"
3. บันทึกไฟล์เป็น `workflow.json`
4. วางไฟล์ใน root ของ repository นี้

## 📁 ไฟล์ที่ต้องส่ง

```
lab01-n8n-basic-workflow/
├── workflow.json          ← Export จาก n8n (จำเป็น)
└── screenshots/
    └── workflow-result.png  ← Screenshot ผลการทำงาน (optional)
```

## ✅ เกณฑ์การให้คะแนน (100 คะแนน)

| Test Case | คะแนน | รายละเอียด |
|-----------|--------|------------|
| Webhook รับ POST ได้ | 10 | Webhook ตอบ status 200 |
| Response เป็น JSON | 10 | Content-Type เป็น application/json |
| student_id ถูกต้อง | 10 | ส่ง student_id กลับมาตรงกับ input |
| name ถูกต้อง | 10 | ส่ง name กลับมาตรงกับ input |
| คำนวณ total ถูกต้อง | 15 | ผลรวมของ scores ถูกต้อง |
| คำนวณ average ถูกต้อง | 15 | ค่าเฉลี่ยถูกต้อง |
| ตัดเกรด A ถูกต้อง | 10 | average >= 80 → "A" |
| ตัดเกรด B ถูกต้อง | 5 | 70 <= average < 80 → "B" |
| status passed ถูกต้อง | 10 | average >= 50 → "passed" |
| status failed ถูกต้อง | 5 | average < 50 → "failed" |
| **รวม** | **100** | |

## 💡 คำแนะนำ

### การคำนวณใน Code Node:

```javascript
// ตัวอย่าง Code Node
const input = $input.first().json;

// คำนวณ total
const total = input.scores.reduce((sum, score) => sum + score, 0);

// คำนวณ average
const average = Math.round((total / input.scores.length) * 10) / 10;

// ตัดเกรด
let grade;
if (average >= 80) grade = 'A';
else if (average >= 70) grade = 'B';
else if (average >= 60) grade = 'C';
else if (average >= 50) grade = 'D';
else grade = 'F';

// กำหนด status
const status = average >= 50 ? 'passed' : 'failed';

return [{
  json: {
    student_id: input.student_id,
    name: input.name,
    total: total,
    average: average,
    grade: grade,
    status: status
  }
}];
```

### Expression ที่มีประโยชน์:
- `{{ $json.scores }}` - เข้าถึง array scores
- `{{ $json.scores.reduce((a,b) => a+b, 0) }}` - รวมค่าใน array
- `{{ $json.scores.length }}` - นับจำนวน items

## 🧪 การทดสอบในเครื่อง

ก่อนส่งงาน สามารถทดสอบด้วย test cases เหล่านี้:

### Test Case 1: Basic
```json
{"student_id": "001", "name": "Test", "scores": [80, 80, 80]}
```
Expected: total=240, average=80.0, grade="A", status="passed"

### Test Case 2: Grade B
```json
{"student_id": "002", "name": "Test", "scores": [70, 75, 78]}
```
Expected: total=223, average=74.3, grade="B", status="passed"

### Test Case 3: Failed
```json
{"student_id": "003", "name": "Test", "scores": [30, 40, 45]}
```
Expected: total=115, average=38.3, grade="F", status="failed"

## 🆘 การขอความช่วยเหลือ

หากมีปัญหา:
1. ตรวจสอบว่า n8n ทำงานอยู่ที่ port 5678
2. ตรวจสอบ Webhook path ว่าถูกต้อง (`/webhook-test/lab01`)
3. ดู Execution log ใน n8n เพื่อหา error
4. ถามใน Discord หรือ Issue ของ repository นี้

## 📚 แหล่งข้อมูลเพิ่มเติม

- [n8n Documentation](https://docs.n8n.io/)
- [Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [Code Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Expressions](https://docs.n8n.io/code-examples/expressions/)

---

**Good luck! 🍀**
