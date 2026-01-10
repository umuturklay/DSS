import pandas as pd
import numpy as np

print("📊 Dataset analizi başlıyor...\n")

df = pd.read_csv('data/raw/Student success data.csv')

print(f"Toplam öğrenci sayısı: {len(df)}")
print(f"Toplam kolon sayısı: {len(df.columns)}\n")

print("🔍 İlk 5 satır:")
print(df.head())

print("\n📈 Önemli kolonlar:")
important_cols = ['course', 'previous_qualification_grade', 'gender',
                  'scholarship_holder', 'age_at_enrollment', 'international',
                  'curricular_units_1st_sem_grade', 'curricular_units_2nd_sem_grade',
                  'target', 'nacionality']

for col in important_cols:
    if col in df.columns:
        print(f"\n{col}:")
        if df[col].dtype == 'object':
            print(df[col].value_counts().head())
        else:
            print(f"  Min: {df[col].min()}, Max: {df[col].max()}, Mean: {df[col].mean():.2f}")

print("\n📊 Burs alanlar:")
print(df['scholarship_holder'].value_counts())

print("\n🌍 Uyruk dağılımı:")
print(df['nacionality'].value_counts().head(10))

print("\n✅ Analiz tamamlandı!")
