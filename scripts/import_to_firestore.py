import json
from app import create_app
import app as app_module

print("🔥 Firestore import başlıyor...\n")

application = create_app()

with application.app_context():
    db = app_module.db

    print("📚 Scholarships import ediliyor...")
    with open('data/processed/scholarships.json', 'r') as f:
        scholarships = json.load(f)

    for sch in scholarships:
        doc_ref = db.collection('scholarships').document()
        sch['id'] = doc_ref.id
        doc_ref.set(sch)
        print(f"  ✅ {sch['name']}")

    print(f"\n✅ {len(scholarships)} scholarship Firestore'a eklendi\n")

    print("👥 Students import ediliyor...")
    with open('data/processed/students_sample.json', 'r') as f:
        students = json.load(f)

    batch_size = 50
    for i in range(0, len(students), batch_size):
        batch = db.batch()
        batch_students = students[i:i+batch_size]

        for student in batch_students:
            doc_ref = db.collection('students').document(student['student_id'])
            batch.set(doc_ref, student)

        batch.commit()
        print(f"  ✅ Batch {i//batch_size + 1}: {len(batch_students)} student eklendi")

    print(f"\n✅ {len(students)} student Firestore'a eklendi\n")

    print("🔍 Firestore durumu kontrol ediliyor...")
    sch_count = len(list(db.collection('scholarships').limit(100).stream()))
    stu_count = len(list(db.collection('students').limit(100).stream()))

    print(f"  Scholarships collection: {sch_count} doküman")
    print(f"  Students collection: {stu_count} doküman")

    print("\n🎉 Import tamamlandı!")
