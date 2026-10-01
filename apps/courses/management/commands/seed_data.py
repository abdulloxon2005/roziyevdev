from django.core.management.base import BaseCommand
from apps.users.models import CustomUser, Profile, UserRole
from apps.courses.models import Category, Course, CourseLevel, CourseModule, Lesson


class Command(BaseCommand):
    help = "Demo ma'lumotlarni (Kategoriyalar, Kurslar, O'qituvchi va Darslar) bazaga kiritish."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Demo ma'lumotlar kiritilmoqda..."))

        # 1. Admin & Instruktor yaratish
        instructor, created = CustomUser.objects.get_or_create(
            email="admin@roziyev.dev",
            defaults={
                "username": "roziyevdev",
                "first_name": "Abdulloh",
                "last_name": "Roziyev",
                "role": UserRole.INSTRUCTOR,
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            instructor.set_password("AdminPassword123!")
            instructor.save()
            self.stdout.write(self.style.SUCCESS("O'qituvchi (admin@roziyev.dev) yaratildi."))

        profile, _ = Profile.objects.get_or_create(user=instructor)
        profile.headline = "Senior Software Engineer & Mobile Developer"
        profile.bio = "5+ yillik tajribaga ega dasturchi. Mobil dasturlash (Flutter, Android), algoritmlar va yuqori yuklamali backend tizimlari bo'yicha mutaxassis. 1000 dan ortiq o'quvchilarga ta'lim bergan."
        profile.github = "https://github.com/roziyevdev"
        profile.linkedin = "https://linkedin.com/in/roziyevdev"
        profile.telegram = "@roziyevdev"
        profile.website = "https://roziyev.dev"
        profile.save()

        # 2. Kategoriyalarni yaratish
        cat_mobile, _ = Category.objects.get_or_create(
            slug="mobil-dasturlash",
            defaults={
                "name": "Mobil Dasturlash",
                "icon": "fa-solid fa-mobile-screen-button",
                "description": "Flutter, Kotlin va iOS texnologiyalarida zamonaviy krossplatform va nativ mobil ilovalar yaratish.",
                "order": 1,
            }
        )

        cat_algo, _ = Category.objects.get_or_create(
            slug="algoritmlar-va-malumotlar-tuzilmasi",
            defaults={
                "name": "Algoritmlar & Ma'lumotlar Tuzilmasi",
                "icon": "fa-solid fa-diagram-project",
                "description": "Texnik intervyulardan muvaffaqiyatli o'tish, Big-O tahlili va LeetCode masalalarini oson yechish.",
                "order": 2,
            }
        )

        cat_db, _ = Category.objects.get_or_create(
            slug="malumotlar-bazasi-va-sql",
            defaults={
                "name": "Ma'lumotlar Bazasi & SQL",
                "icon": "fa-solid fa-database",
                "description": "Relatsion ma'lumotlar bazasi (PostgreSQL), murakkab SQL so'rovlar, indeksatsiya va optimizatsiya.",
                "order": 3,
            }
        )

        cat_backend, _ = Category.objects.get_or_create(
            slug="backend-dasturlash",
            defaults={
                "name": "Backend & Python Dasturlash",
                "icon": "fa-solid fa-server",
                "description": "Django, Django REST Framework, xavfsiz JWT, mikroservislar va RESTful API ishlab chiqish.",
                "order": 4,
            }
        )

        # 3. Kurslarni yaratish
        # Kurs 1: Flutter
        course_flutter, _ = Course.objects.get_or_create(
            slug="flutter-va-dart-noldan-professionalgacha",
            defaults={
                "title": "Flutter va Dart: Noldan Professional Darajagacha",
                "category": cat_mobile,
                "instructor": instructor,
                "short_description": "Android va iOS uchun bitta kod bazasida chiroyli va tez ishlaydigan mobil ilovalar yaratishni to'liq o'rganing.",
                "description": (
                    "Ushbu kursda siz Dart dasturlash tilining nozik jihatlaridan boshlab, "
                    "Flutter fremvorkida Clean Architecture, Bloc/Provider/Riverpod arxitekturalari, "
                    "REST API integratsiyasi, offline kesh, push-bildirishnomalar va ilovani Google Play / App Store'ga yuklashgacha bo'lgan "
                    "barcha bosqichlarni to'liq amaliy loyihalar orqali o'rganasiz."
                ),
                "level": CourseLevel.BEGINNER,
                "price": 350000,
                "is_free": False,
                "duration_hours": 36,
                "students_count": 480,
                "rating": 4.95,
                "is_featured": True,
                "what_you_will_learn": (
                    "Dart asoslari va OOP tamoyillari\n"
                    "Flutter vidjetlari va zamonaviy UI/UX dizayn yaratish\n"
                    "Bloc & Cubit yordamida professional holat boshqaruvi (State Management)\n"
                    "REST API va HTTP/Dio orqali backend bilan bog'lanish\n"
                    "Ilovalarni Google Play va Apple App Store do'konlariga nashr qilish"
                ),
                "requirements": (
                    "Kompyuter (Windows, macOS yoki Linux)\n"
                    "Dasturlashga bo'lgan qiziqish va boshlang'ich mantiqiy fikrlash\n"
                    "Hech qanday oldindan maxsus bilim talab qilinmaydi"
                ),
            }
        )

        # Kurs 2: Algoritmlar
        course_algo, _ = Course.objects.get_or_create(
            slug="algoritmlar-va-malumotlar-tuzilmalari-masterklass",
            defaults={
                "title": "Algoritmlar va Ma'lumotlar Tuzilmasi: Amaliy Dasturlash",
                "category": cat_algo,
                "instructor": instructor,
                "short_description": "Big-O tahlili, massivlar, bog'langan ro'yxatlar, daraxtlar, graflar va LeetCode'dagi 100+ saralangan masalalar yechimi.",
                "description": (
                    "Har qanday kuchli dasturchining asosini algoritmlar va to'g'ri ma'lumotlar tuzilmalarini tanlash tashkil etadi. "
                    "Kurs davomida FAANG darajasidagi intervyularda eng ko'p so'raladigan algoritmlar (Binary Search, Two Pointers, Sliding Window, DFS/BFS, Dynamic Programming) "
                    "vizual va tushunarli tarzda amalda ko'rsatiladi."
                ),
                "level": CourseLevel.INTERMEDIATE,
                "price": 290000,
                "is_free": False,
                "duration_hours": 28,
                "students_count": 620,
                "rating": 4.98,
                "is_featured": True,
                "what_you_will_learn": (
                    "Vaqt va xotira murakkabligi (Big-O notation) tahlili\n"
                    "Qidiruv va saralash algoritmlarini mustaqil amalga oshirish\n"
                    "Daraxtlar (Trees) va Graflar (Graphs) bilan professional ishlash\n"
                    "Dinamik dasturlash (Dynamic Programming) usullari\n"
                    "Texnik intervyulardan muvaffaqiyatli o'tish strategiyalari"
                ),
                "requirements": (
                    "Ixtiyoriy bitta dasturlash tilining asoslarini bilish (Python, Java, Dart, C++ yoki JS)"
                ),
            }
        )

        # Kurs 3: Ma'lumotlar bazasi
        course_db, _ = Course.objects.get_or_create(
            slug="postgresql-va-murakkab-sql-sorovlar-masterklassi",
            defaults={
                "title": "PostgreSQL va Murakkab SQL So'rovlar Masterklassi",
                "category": cat_db,
                "instructor": instructor,
                "short_description": "Noldan boshlab murakkab JOIN'lar, CTE, Window Functions, Indekslar va bazani tezlashtirish sirlari.",
                "description": (
                    "Ma'lumotlar bazasini to'g'ri loyihalash (Normalizatsiya), tranzaksiyalar (ACID), izolyatsiya darajalari, "
                    "indekslarning ichki ishlash mexanizmi (B-tree, GIN) va millionlab ma'lumotlar oqimida so'rovlarni optimallashtirish bo'yicha to'liq qo'llanma."
                ),
                "level": CourseLevel.ALL_LEVELS,
                "price": 0,
                "is_free": True,
                "duration_hours": 16,
                "students_count": 890,
                "rating": 4.90,
                "is_featured": True,
                "what_you_will_learn": (
                    "SQL sintaksisi va DDL/DML asoslari\n"
                    "Murakkab JOIN, subquery va Common Table Expressions (CTE)\n"
                    "Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)\n"
                    "Indekslar turlari va EXPLAIN ANALYZE bilan so'rovlarni tahlil qilish\n"
                    "Tranzaksiyalar va qulflashlar (Locks, Concurrency)"
                ),
                "requirements": (
                    "Boshlang'ich kompyuter savodxonligi"
                ),
            }
        )

        # Kurs 4: Django REST Framework
        course_drf, _ = Course.objects.get_or_create(
            slug="django-rest-framework-bilan-xavfsiz-api-yaratish",
            defaults={
                "title": "Django REST Framework: Kuchli va Xavfsiz Backend API",
                "category": cat_backend,
                "instructor": instructor,
                "short_description": "JWT autentifikatsiya, ruxsatlar, testlash, Swagger hujjati va Docker konteynerlashtirish.",
                "description": (
                    "Frontend (React/Flutter/Vue) ilovalar uchun xavfsiz, tezkor va arxitekturaviy to'g'ri REST API ishlab chiqish kursi."
                ),
                "level": CourseLevel.INTERMEDIATE,
                "price": 320000,
                "is_free": False,
                "duration_hours": 24,
                "students_count": 340,
                "rating": 4.92,
                "is_featured": True,
                "what_you_will_learn": (
                    "Django ORM optimallashtirish (select_related, prefetch_related)\n"
                    "DRF Serializers, ViewSets va Generics\n"
                    "JWT (JSON Web Token) xavfsiz autentifikatsiya\n"
                    "Swagger va OpenAPI 3.0 hujjatlashtirish\n"
                    "Docker va Nginx orqali serverga o'rnatish"
                ),
                "requirements": (
                    "Python dasturlash tili asoslari\n"
                    "Boshlang'ich Django bilimi"
                ),
            }
        )

        # 4. Modullar va Darslarni kiritish (Flutter kursi uchun namunaviy)
        m1, _ = CourseModule.objects.get_or_create(course=course_flutter, title="1-Modul: Dart Dasturlash Asoslari", order=1)
        Lesson.objects.get_or_create(module=m1, title="1.1. Dart tiliga kirish va o'rnatish", duration_minutes=15, is_preview=True, order=1)
        Lesson.objects.get_or_create(module=m1, title="1.2. O'zgaruvchilar, Ma'lumot turlari va Null Safety", duration_minutes=25, is_preview=True, order=2)
        Lesson.objects.get_or_create(module=m1, title="1.3. Funksiyalar va OOP tamoyillari (Classes & Interfaces)", duration_minutes=35, is_preview=False, order=3)

        m2, _ = CourseModule.objects.get_or_create(course=course_flutter, title="2-Modul: Flutter Asoslari va Zamonaviy UI", order=2)
        Lesson.objects.get_or_create(module=m2, title="2.1. Flutter arxitekturasi: Widget Tree", duration_minutes=20, is_preview=False, order=1)
        Lesson.objects.get_or_create(module=m2, title="2.2. Stateless vs Stateful vidjetlar", duration_minutes=30, is_preview=False, order=2)
        Lesson.objects.get_or_create(module=m2, title="2.3. Chiroyli dizayn: Responsive va adaptiv tartiblar", duration_minutes=45, is_preview=False, order=3)

        m3, _ = CourseModule.objects.get_or_create(course=course_flutter, title="3-Modul: State Management va API Integratsiyasi", order=3)
        Lesson.objects.get_or_create(module=m3, title="3.1. Bloc va Cubit arxitekturasi bilan tanishuv", duration_minutes=40, is_preview=False, order=1)
        Lesson.objects.get_or_create(module=m3, title="3.2. Dio kutubxonasi orqali REST API ga so'rovlar", duration_minutes=45, is_preview=False, order=2)

        # Algoritm kursi uchun modullar
        m_algo1, _ = CourseModule.objects.get_or_create(course=course_algo, title="1-Modul: Murakkablik tahlili (Big-O)", order=1)
        Lesson.objects.get_or_create(module=m_algo1, title="1.1. Big-O, Big-Omega va Big-Theta nima?", duration_minutes=20, is_preview=True, order=1)
        Lesson.objects.get_or_create(module=m_algo1, title="1.2. Xotira va vaqt bo'yicha masalalarni tahlil qilish", duration_minutes=30, is_preview=True, order=2)

        m_algo2, _ = CourseModule.objects.get_or_create(course=course_algo, title="2-Modul: Chiziqli Ma'lumot Tuzilmalari", order=2)
        Lesson.objects.get_or_create(module=m_algo2, title="2.1. Massivlar va Stringlar: Two Pointers texnikasi", duration_minutes=35, is_preview=False, order=1)
        Lesson.objects.get_or_create(module=m_algo2, title="2.2. Bog'langan ro'yxatlar (Linked Lists)", duration_minutes=40, is_preview=False, order=2)

        # SQL kursi uchun modullar
        m_sql1, _ = CourseModule.objects.get_or_create(course=course_db, title="1-Modul: SQL Asoslari va Ma'lumotlarni Filtrlash", order=1)
        Lesson.objects.get_or_create(module=m_sql1, title="1.1. PostgreSQL o'rnatish va DDL so'rovlar", duration_minutes=15, is_preview=True, order=1)
        Lesson.objects.get_or_create(module=m_sql1, title="1.2. SELECT, WHERE, GROUP BY va HAVING", duration_minutes=25, is_preview=True, order=2)

        self.stdout.write(self.style.SUCCESS("Barcha demo ma'lumotlar muvaffaqiyatli kiritildi!"))
