import pandas as pd
import numpy as np
import json

print("🔄 Student data preprocessing başlıyor...\n")

df = pd.read_csv('data/raw/Student success data.csv')

print(f"Toplam öğrenci: {len(df)}")

def normalize_gpa(grade):
    """Normalize GPA to 4.0 scale
    Original range: 95-190
    Target range: 0.0-4.0
    """
    min_grade = 95
    max_grade = 190
    return round(((grade - min_grade) / (max_grade - min_grade)) * 4.0, 2)

def calculate_semester_gpa(row):
    """Calculate average GPA from both semesters"""
    sem1 = row['curricular_units_1st_sem_grade']
    sem2 = row['curricular_units_2nd_sem_grade']

    if sem1 == 0 and sem2 == 0:
        return 0.0
    elif sem1 == 0:
        return round((sem2 / 20.0) * 4.0, 2)
    elif sem2 == 0:
        return round((sem1 / 20.0) * 4.0, 2)
    else:
        avg = (sem1 + sem2) / 2
        return round((avg / 20.0) * 4.0, 2)

print("📊 GPA normalizasyonu yapılıyor...")

df['gpa_normalized'] = df['previous_qualification_grade'].apply(normalize_gpa)
df['current_gpa'] = df.apply(calculate_semester_gpa, axis=1)

df['gpa_final'] = df.apply(
    lambda row: row['current_gpa'] if row['current_gpa'] > 0 else row['gpa_normalized'],
    axis=1
)

print(f"GPA range: {df['gpa_final'].min():.2f} - {df['gpa_final'].max():.2f}")
print(f"GPA mean: {df['gpa_final'].mean():.2f}\n")

students = []

for idx, row in df.iterrows():
    student = {
        "student_id": f"STU_{idx:05d}",
        "gpa": round(row['gpa_final'], 2),
        "course": int(row['course']),
        "gender": int(row['gender']),
        "age": int(row['age_at_enrollment']),
        "nationality": int(row['nacionality']),
        "is_international": bool(row['international']),
        "current_scholarship_holder": bool(row['scholarship_holder']),
        "marital_status": int(row['marital_status']),
        "status": row['target'],
        "keywords": []
    }

    course_keywords = {
        9991: ["computer science", "technology", "programming"],
        9500: ["engineering", "technical", "science"],
        9119: ["business", "management", "economics"],
        9070: ["design", "creative", "arts"],
        9773: ["economics", "finance", "business"],
        9254: ["education", "teaching", "pedagogy"],
        9853: ["management", "leadership", "business"],
        9238: ["mathematics", "statistics", "data"]
    }

    student['keywords'] = course_keywords.get(student['course'], ["general", "studies"])

    if student['gender'] == 0:
        student['keywords'].append("women")

    if student['is_international']:
        student['keywords'].append("international")

    if student['gpa'] >= 3.5:
        student['keywords'].append("high achiever")
    elif student['gpa'] >= 3.0:
        student['keywords'].append("merit")

    students.append(student)

sample_size = 500
sample_students = students[:sample_size]

print(f"✅ {len(sample_students)} öğrenci profili oluşturuldu (sample)\n")

print("📊 Sample istatistikleri:")
sample_df = pd.DataFrame(sample_students)
print(f"GPA ortalaması: {sample_df['gpa'].mean():.2f}")
print(f"International öğrenci: {sample_df['is_international'].sum()}")
print(f"Burs sahibi: {sample_df['current_scholarship_holder'].sum()}")
print(f"Kadın öğrenci: {(sample_df['gender'] == 0).sum()}")

with open('data/processed/students_sample.json', 'w') as f:
    json.dump(sample_students, f, indent=2)

print("\n💾 Students saved to: data/processed/students_sample.json")
print(f"📦 Full dataset ({len(students)} students) hazır, gerekirse kullanılabilir")
