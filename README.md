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
3. ใช้ Code Node แปลงและประมวลผลข้อมูลได้
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

```json
{
  "student_id": "65001234",
  "name": "Somchai Jaidee",
  "scores": [85, 90, 78, 92, 88]
}
```

## 📤 Expected Output Format

```json
{
  "student_id": "65001234",
  "name": "Somchai Jaidee",
  "total": 433,
  "average": 86.6,
  "grade": "A",
  "status": "passed"
}
```

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
3. ตั้งชื่อ: `Lab01-Student-Grade-Calculator`

### Step 2: เพิ่ม Webhook Node
- **HTTP Method**: POST
- **Path**: `lab01`
- **Response Mode**: Last Node

### Step 3: เพิ่ม Code Node
ใส่โค้ด JavaScript:

```javascript
const item = $input.first().json;
const input = item.body || item;

const total = input.scores.reduce((sum, score) => sum + score, 0);
const average = Math.round((total / input.scores.length) * 10) / 10;

let grade;
if (average >= 80) grade = 'A';
else if (average >= 70) grade = 'B';
else if (average >= 60) grade = 'C';
else if (average >= 50) grade = 'D';
else grade = 'F';

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

### Step 4: ทดสอบ Workflow
```bash
curl -X POST http://localhost:5678/webhook-test/lab01 \
  -H "Content-Type: application/json" \
  -d '{"student_id": "65001234", "name": "Somchai Jaidee", "scores": [85, 90, 78, 92, 88]}'
```

### Step 5: Export และส่งงาน
1. คลิก Menu (⋮) > Download
2. บันทึกเป็น `workflow.json`
3. แทนที่ไฟล์ในโปรเจค
4. `git add . && git commit -m "Add workflow" && git push`

## ✅ เกณฑ์การให้คะแนน (100 คะแนน)

| Test | คะแนน | ตรวจอะไร |
|------|-------|----------|
| มีไฟล์ workflow.json | 10 | ส่งไฟล์มา |
| เป็น valid JSON | 10 | ไฟล์ถูกต้อง |
| มี Webhook Node | 10 | มี node รับข้อมูล |
| มี Code Node | 10 | มี node ประมวลผล |
| Webhook ใช้ POST | 10 | ตั้งค่าถูกต้อง |
| Webhook path = "lab01" | 10 | ตั้งค่าถูกต้อง |
| คำนวณ total | 10 | มีโค้ดคำนวณ |
| คำนวณ average | 10 | มีโค้ดคำนวณ |
| มีตัดเกรด A-F | 10 | มี logic ตัดเกรด |
| มี status passed/failed | 10 | มี logic status |
| **รวม** | **100** | |

---

**Good luck! 🍀**
