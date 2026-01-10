from app import create_app
import app as app_module

application = create_app()

with application.app_context():
    print("🔥 Firebase bağlantısı test ediliyor...")

    try:
        test_doc = app_module.db.collection('test').document('connection_test')
        test_doc.set({'status': 'connected', 'message': 'Firebase bağlantısı başarılı!'})

        result = test_doc.get()
        if result.exists:
            print("✅ Firebase Firestore bağlantısı BAŞARILI!")
            print(f"✅ Test data: {result.to_dict()}")

            test_doc.delete()
            print("✅ Test dokümanı temizlendi")
        else:
            print("❌ Test dokümanı okunamadı")

    except Exception as e:
        print(f"❌ HATA: {e}")
