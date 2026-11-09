from django.core.management.base import BaseCommand
from apps.users.models import CustomUser, Profile, UserRole
from apps.courses.models import Category, Course, CourseLevel, CourseModule, Lesson, LessonType
from apps.learning.models import Assignment, AssignmentSubmission, SubmissionStatus, CoinTransaction
from apps.learning.services import enroll_user, mark_lesson_complete
from apps.certificates.services import create_or_get_certificate
from apps.blog.models import BlogCategory, Tag, Post, Comment


class Command(BaseCommand):
    help = "Demo ma'lumotlarni (Kategoriyalar, Kurslar, Darslar, Blog maqolalari, Talaba va Sertifikatlar) bazaga kiritish."

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

        # 2. Sinov talabasi
        student, s_created = CustomUser.objects.get_or_create(
            email="talaba@roziyev.dev",
            defaults={
                "username": "talaba",
                "first_name": "Jasur",
                "last_name": "Karimov",
                "role": UserRole.STUDENT,
            }
        )
        if s_created:
            student.set_password("password123")
            student.save()
            self.stdout.write(self.style.SUCCESS("Test talaba (talaba@roziyev.dev / password123) yaratildi."))

        s_profile, _ = Profile.objects.get_or_create(user=student)
        s_profile.headline = "Junior Mobile & Backend Dasturchi"
        s_profile.bio = "Algoritmlar va mobil dasturlashni chuqur o'rganmoqdaman."
        s_profile.save()

        # 3. Kurs Kategoriyalari
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

        # 4. Kurslar
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
                    "Kurs davomida FAANG darajasidagi intervyularda eng ko'p so'raladigan algoritmlar "
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

        # Kurs 3: PostgreSQL & SQL (Bepul kurs)
        course_db, _ = Course.objects.get_or_create(
            slug="postgresql-va-murakkab-sql-sorovlar-masterklassi",
            defaults={
                "title": "PostgreSQL va Murakkab SQL So'rovlar Masterklassi",
                "category": cat_db,
                "instructor": instructor,
                "short_description": "Noldan boshlab murakkab JOIN'lar, CTE, Window Functions, Indekslar va bazani tezlashtirish sirlari.",
                "description": (
                    "Ma'lumotlar bazasini to'g'ri loyihalash (Normalizatsiya), tranzaksiyalar (ACID), izolyatsiya darajalari, "
                    "indekslarning ichki ishlash mexanizmi va millionlab ma'lumotlar oqimida so'rovlarni optimallashtirish."
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
                    "Window Functions (ROW_NUMBER, RANK, DENSE_RANK)\n"
                    "Indekslar turlari va EXPLAIN ANALYZE bilan so'rovlarni tahlil qilish"
                ),
                "requirements": "Boshlang'ich kompyuter savodxonligi",
            }
        )

        # 5. Modullar va Darslarni kiritish (video URL va Markdown kontent bilan)
        m1, _ = CourseModule.objects.get_or_create(course=course_flutter, title="1-Modul: Dart Dasturlash Asoslari", order=1)
        l_dart1, _ = Lesson.objects.get_or_create(
            module=m1,
            title="1.1. Dart tiliga kirish va o'rnatish",
            defaults={
                "duration_minutes": 15,
                "is_preview": True,
                "order": 1,
                "video_url": "https://www.youtube.com/watch?v=Ej_Pcr4uC2Q",
                "content": (
                    "# Dart Dasturlash Tiliga Kirish\n\n"
                    "Dart — Google kompaniyasi tomonidan yaratilgan, client-side dasturlar uchun optimallashtirilgan tezkor til.\n\n"
                    "### Asosiy afzalliklari:\n"
                    "- **AOT (Ahead-of-Time) kompilatsiya:** Mashina kodiga tezkor kompilyatsiya qilinadi.\n"
                    "- **JIT (Just-in-Time) kompilatsiya:** Hot Reload imkoniyatini beradi.\n"
                    "- **Sound Null Safety:** Kodda `NullPointerException` xatoliklarini deyarli butunlay yo'q qiladi.\n\n"
                    "```dart\n"
                    "void main() {\n"
                    "  String greeting = 'Salom, RoziyevDev!';\n"
                    "  print(greeting);\n"
                    "}\n"
                    "```\n"
                )
            }
        )

        l_dart2, _ = Lesson.objects.get_or_create(
            module=m1,
            title="1.2. O'zgaruvchilar, Ma'lumot turlari va Null Safety",
            defaults={
                "duration_minutes": 25,
                "is_preview": True,
                "order": 2,
                "video_url": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                "content": (
                    "# O'zgaruvchilar va Null Safety\n\n"
                    "Dart tilida har bir qiymat obyekt hisoblanadi. Dart 2.12 versiyasidan boshlab rasmiy Null Safety joriy qilingan.\n\n"
                    "```dart\n"
                    "int age = 25;\n"
                    "String? optionalName; // Null bo'lishi mumkin\n"
                    "late final String config; // Keyinroq initsializatsiya qilinadi\n"
                    "```\n"
                )
            }
        )

        Lesson.objects.get_or_create(
            module=m1,
            title="1.3. Funksiyalar va OOP tamoyillari",
            defaults={
                "duration_minutes": 35,
                "is_preview": False,
                "order": 3,
                "video_url": "https://www.youtube.com/watch?v=Ej_Pcr4uC2Q",
                "content": "# OOP Tamoyillari\n\nKlasslar, konstruktorlar va interfeyslar haqida to'liq amaliy darslik."
            }
        )

        # SQL kursi darslari (bepul kurs)
        m_sql1, _ = CourseModule.objects.get_or_create(course=course_db, title="1-Modul: SQL Asoslari va Filtrlash", order=1)
        l_sql1, _ = Lesson.objects.get_or_create(
            module=m_sql1,
            title="1.1. PostgreSQL o'rnatish va DDL so'rovlar",
            defaults={
                "duration_minutes": 15,
                "is_preview": True,
                "order": 1,
                "video_url": "https://www.youtube.com/watch?v=qw--VYLpxG4",
                "content": (
                    "# PostgreSQL bilan ishlash\n\n"
                    "PostgreSQL — dunyodagi eng ilg'or ochiq kodli relyatsion ma'lumotlar bazasi tizimi.\n\n"
                    "```sql\n"
                    "CREATE TABLE users (\n"
                    "    id SERIAL PRIMARY KEY,\n"
                    "    name VARCHAR(100) NOT NULL,\n"
                    "    email VARCHAR(120) UNIQUE NOT NULL,\n"
                    "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
                    ");\n"
                    "```\n"
                )
            }
        )

        l_sql2, _ = Lesson.objects.get_or_create(
            module=m_sql1,
            title="1.2. SELECT, WHERE, GROUP BY va HAVING",
            defaults={
                "duration_minutes": 25,
                "is_preview": True,
                "order": 2,
                "video_url": "https://www.youtube.com/watch?v=qw--VYLpxG4",
                "content": (
                    "# Murakkab Ma'lumotlarni Tanlab Olish\n\n"
                    "```sql\n"
                    "SELECT department, COUNT(*), AVG(salary)\n"
                    "FROM employees\n"
                    "WHERE status = 'ACTIVE'\n"
                    "GROUP BY department\n"
                    "HAVING AVG(salary) > 5000000;\n"
                    "```\n"
                )
            }
        )

        # 6. Talabani PostgreSQL kursiga a'zo qilish va 100% tugatib sertifikat berish!
        enrollment_sql, _ = enroll_user(student, course_db)
        mark_lesson_complete(enrollment_sql, l_sql1)
        mark_lesson_complete(enrollment_sql, l_sql2)
        # Sertifikatni yaratish
        create_or_get_certificate(enrollment_sql)
        self.stdout.write(self.style.SUCCESS("Talaba uchun PostgreSQL kursi bo'yicha namunaviy sertifikat yaratildi!"))

        # 6.1. Darslarga amaliy vazifalar yaratish
        a_dart1, _ = Assignment.objects.get_or_create(
            lesson=l_dart1,
            defaults={
                "title": "1-Amaliy Vazifa: Dart tilida konsol dasturi",
                "description": "Dart tilida 'main' funksiyasini yozing va 1 dan 10 gacha bo'lgan sonlar yig'indisini konsolga chiqaring.",
                "starter_code": "void main() {\n  // 1 dan 10 gacha sonlar yig'indisini hisoblang\n  int sum = 0;\n  // davom ettiring...\n}",
                "coin_reward": 50,
                "passing_score": 70,
            }
        )

        a_dart2, _ = Assignment.objects.get_or_create(
            lesson=l_dart2,
            defaults={
                "title": "2-Amaliy Vazifa: Null Safety kalkulyator",
                "description": "Null bo'lishi mumkin bo'lgan ikkita sonni xavfsiz qo'shuvchi funksiya yozing.",
                "starter_code": "int safeAdd(int? a, int? b) {\n  // agar a yoki b null bo'lsa 0 deb hisoblang\n  return 0;\n}",
                "coin_reward": 60,
                "passing_score": 70,
            }
        )

        a_sql1, _ = Assignment.objects.get_or_create(
            lesson=l_sql1,
            defaults={
                "title": "1-Amaliy Vazifa: PostgreSQL jadval yaratish va blok-sxema",
                "description": "Talabalar (students) jadvali uchun SQL DDL so'rovini yozing va ma'lumotlar oqimi blok-sxemasini chizing.",
                "starter_code": "CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    full_name VARCHAR(120) NOT NULL,\n    email VARCHAR(120) UNIQUE NOT NULL,\n    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);",
                "coin_reward": 75,
                "passing_score": 70,
            }
        )

        # 6.2. Talaba uchun namunaviy topshiriq va admin tekshiruvi (tangachalar berish)
        sub_sql1, sub_created = AssignmentSubmission.objects.get_or_create(
            assignment=a_sql1,
            student=student,
            defaults={
                "submitted_code": "CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    full_name VARCHAR(120) NOT NULL,\n    email VARCHAR(120) UNIQUE NOT NULL\n);",
                "flowchart_data": "flowchart TD\n    Start([Boshlash]) --> Input[/Talaba ma'lumotlari/]\n    Input --> Save[(Bazada saqlash)]\n    Save --> End([Tugatish])",
                "status": SubmissionStatus.APPROVED,
                "score": 95,
                "instructor_feedback": "A'lo darajada yozilgan! DDL so'rovi to'liq sintaktik to'g'ri va blok-sxema mantiqan mos.",
                "reviewed_by": instructor,
            }
        )
        if sub_created or student.coins == 0:
            sub_sql1.approve(instructor, score=95, feedback="A'lo darajada yozilgan! DDL so'rovi to'liq to'g'ri.")
            self.stdout.write(self.style.SUCCESS(f"Talabaga vazifa uchun {a_sql1.coin_reward} tanga berildi!"))

        # 7. Blog Kategoriyalari va Teglar
        bcat_mobile, _ = BlogCategory.objects.get_or_create(
            slug="mobil-texnologiyalar",
            defaults={"name": "Mobil Texnologiyalar", "description": "Flutter, Dart, Android va iOS arxitekturasi."}
        )
        bcat_backend, _ = BlogCategory.objects.get_or_create(
            slug="backend-va-tizimlar",
            defaults={"name": "Backend va Arxitektura", "description": "Django, Python, API xavfsizligi va Highload tizimlar."}
        )
        bcat_algo, _ = BlogCategory.objects.get_or_create(
            slug="algoritmlar-va-tuzilmalar",
            defaults={"name": "Algoritmlar", "description": "LeetCode yechimlari va intervyuga tayyorgarlik."}
        )
        bcat_career, _ = BlogCategory.objects.get_or_create(
            slug="it-karyera",
            defaults={"name": "IT Karyera", "description": "Dasturchi bo'lish yo'li va maslahatlar."}
        )

        tag_flutter, _ = Tag.objects.get_or_create(name="Flutter", defaults={"slug": "flutter"})
        tag_django, _ = Tag.objects.get_or_create(name="Django", defaults={"slug": "django"})
        tag_python, _ = Tag.objects.get_or_create(name="Python", defaults={"slug": "python"})
        tag_sql, _ = Tag.objects.get_or_create(name="PostgreSQL", defaults={"slug": "postgresql"})
        tag_algo, _ = Tag.objects.get_or_create(name="Algoritmlar", defaults={"slug": "algoritmlar"})
        tag_clean, _ = Tag.objects.get_or_create(name="CleanArchitecture", defaults={"slug": "clean-architecture"})

        # 8. Blog Maqolalari
        # Maqola 1
        p1, _ = Post.objects.get_or_create(
            slug="2026-yilda-ozbekistonda-dasturchi-bolish-qaysi-yonalishni-tanlash-kerak",
            defaults={
                "title": "2026-yilda O'zbekistonda Dasturchi bo'lish: Qaysi yo'nalishni tanlash kerak?",
                "author": instructor,
                "category": bcat_career,
                "summary": "O'zbekiston IT bozorida eng talabgir bo'lgan mobil dasturlash, backend va sun'iy intellekt integratsiyalari tahlili.",
                "content": (
                    "Bugungi kunda texnologiyalar shiddat bilan rivojlanmoqda. Ko'pchilik yangi boshlayotgan yoshlarimiz qaysi sohadan boshlashni bilmay ikkilanadilar.\n\n"
                    "## 1. Mobil Dasturlash (Flutter & Kotlin)\n"
                    "O'zbekiston bozorida aholining aksariyati internetdan mobil ilovalar orqali foydalanadi: fintex (Click, Payme, Uzum), yetkazib berish xizmatlari va elektron tijorat.\n"
                    "Flutter bu o'rinda eng ommabop yechim: bitta kod bazasi bilan ham Android, ham iOS platformalariga yuqori unumdorlikka ega ilovalar yaratish imkonini beradi.\n\n"
                    "## 2. Backend Dasturlash (Python / Django / FastAPI)\n"
                    "Mobil ilovalar va veb-saytlarning 'miyasi' — backend tizimlardir. Ma'lumotlar bazasini to'g'ri loyihalash, xavfsiz REST API yaratish har qanday kompaniyada eng yuqori baholanadigan ko'nikmalardan biridir.\n\n"
                    "## Xulosa\n"
                    "Asosiysi — poydevor (algoritmlar va toza kodlash)ni mustahkam qurish. Qolgan freymvorklar va texnologiyalarni o'zlashtirish esa texnika masalasidir."
                ),
                "is_published": True,
                "views_count": 342,
            }
        )
        p1.tags.add(tag_flutter, tag_python)

        # Maqola 2
        p2, _ = Post.objects.get_or_create(
            slug="django-rest-framework-va-postgresql-yuqori-yuklamali-arxitektura-sirlari",
            defaults={
                "title": "Django REST Framework va PostgreSQL: Yuqori yuklamali arxitektura sirlari",
                "author": instructor,
                "category": bcat_backend,
                "summary": "Millionlab so'rovlar oqimida N+1 muammosini hal qilish, indeksatsiya, connection pooling va xotira keshidan unumli foydalanish.",
                "content": (
                    "Ko'p loyihalarda foydalanuvchilar soni ortishi bilan tizim sekinlashib qoladi. Buning 80% sababi — ma'lumotlar bazasiga noto'g'ri yo'llangan so'rovlardir.\n\n"
                    "### 1. N+1 Muammosi va Yechim\n"
                    "Django ORM `select_related` va `prefetch_related` imkoniyatlarini taqdim etadi.\n\n"
                    "```python\n"
                    "# Yomon amaliyot (Har bir kurs uchun alohida instruktor so'rovi ketadi)\n"
                    "courses = Course.objects.all()\n"
                    "for course in courses:\n"
                    "    print(course.instructor.name)\n\n"
                    "# To'g'ri amaliyot (1 ta SQL JOIN so'rovi)\n"
                    "courses = Course.objects.select_related('instructor').all()\n"
                    "```\n\n"
                    "### 2. PostgreSQL Indekslari\n"
                    "Keng tarqalgan `B-Tree` indekslari tenglik va diapazon so'rovlarida juda tez ishlaydi. Biroq ortiqcha indekslar yozish (`INSERT`/`UPDATE`) tezligini pasaytirishini unutmang."
                ),
                "is_published": True,
                "views_count": 512,
            }
        )
        p2.tags.add(tag_django, tag_python, tag_sql)

        # Maqola 3
        p3, _ = Post.objects.get_or_create(
            slug="flutter-3-va-clean-architecture-katta-loyihalarni-tashkil-qilish",
            defaults={
                "title": "Flutter 3.x va Clean Architecture: Katta loyihalarni to'g'ri tashkil qilish",
                "author": instructor,
                "category": bcat_mobile,
                "summary": "Data, Domain va Presentation qatlamlarini ajratish orqali testlanuvchan va kengaytiriluvchi mobil ilovalar yaratish.",
                "content": (
                    "Katta jamoalarda bitta kod bazasi ustida ishlaganda tartibsizlik kelib chiqmasligi uchun Clean Architecture zarur.\n\n"
                    "### Qatlamlar bo'linishi:\n"
                    "- **Domain:** Biznes mantiq (Entities, UseCases, Repositories interfeysi).\n"
                    "- **Data:** API so'rovlar, mahalliy ma'lumotlar bazasi (Hive/Isar/SharedPreferences), Models.\n"
                    "- **Presentation:** UI vidjetlar, Bloc/Cubit holat boshqaruvchilari.\n\n"
                    "Clean Architecture yordamida yozilgan ilovani test qilish va kelajakda boshqa kutubxonalarga almashtirish osonlashadi."
                ),
                "is_published": True,
                "views_count": 289,
            }
        )
        p3.tags.add(tag_flutter, tag_clean)

        # Maqola 4
        p4, _ = Post.objects.get_or_create(
            slug="algoritmlarni-chuqur-organish-boyicha-yol-xaritasi",
            defaults={
                "title": "Algoritmlarni chuqur o'rganish bo'yicha yo'l xaritasi (Roadmap)",
                "author": instructor,
                "category": bcat_algo,
                "summary": "LeetCode va texnik suhbatlardan muvaffaqiyatli o'tish uchun zarur bo'lgan bosqichma-bosqich o'rganish rejasi.",
                "content": (
                    "Dasturlashda muammolarni yechish qobiliyati — eng qimmatli fazilatdir.\n\n"
                    "### Bosqichlar:\n"
                    "1. **Big-O tahlili:** Kodning vaqt va xotira murakkabligini hisoblash.\n"
                    "2. **Two Pointers va Sliding Window:** Massivlar va satrlar bilan ishlash.\n"
                    "3. **Binary Search:** O(log N) qidiruv algoritmi.\n"
                    "4. **Trees & Graphs:** DFS, BFS, Dijkstra algoritmlari.\n"
                    "5. **Dynamic Programming:** Qiyin muammolarni kichik qismlarga bo'lib yechish."
                ),
                "is_published": True,
                "views_count": 420,
            }
        )
        p4.tags.add(tag_algo)

        # 9. Izohlar kiritish
        Comment.objects.get_or_create(
            post=p1,
            author_name="Jasur Karimov",
            user=student,
            defaults={
                "content": "Juda foydali va dolzarb maqola bo'libdi! Ayniqsa O'zbekiston bozori uchun Flutter tanlovi to'g'ri ta'riflangan.",
                "is_approved": True,
            }
        )
        Comment.objects.get_or_create(
            post=p2,
            author_name="Sardor",
            defaults={
                "content": "select_related va prefetch_related farqini aniq misollar bilan tushuntirib bera olasizmi?",
                "is_approved": True,
            }
        )

        # 10. Yangi kurslar kataloggi (Prompt Injiniring, Python, Web, UX/UI, Mobil, Telegram Bot)
        cat_ai, _ = Category.objects.get_or_create(
            slug="prompt-injiniring",
            defaults={
                "name": "Sun'iy Intellekt & Prompt Injiniring",
                "icon": "fa-solid fa-wand-magic-sparkles",
                "description": "ChatGPT, Claude va boshqa yirik til modellari bilan samarali muloqot qilish va ulardan ish jarayonlarida foydalanish.",
                "order": 5,
            }
        )
        cat_web, _ = Category.objects.get_or_create(
            slug="web-dasturlash",
            defaults={
                "name": "Web Dasturlash",
                "icon": "fa-solid fa-globe",
                "description": "HTML, CSS, JavaScript va zamonaviy freymvorklar yordamida veb-saytlar va veb-ilovalar yaratish.",
                "order": 6,
            }
        )
        cat_uxui, _ = Category.objects.get_or_create(
            slug="ux-ui-dizayn",
            defaults={
                "name": "UX/UI Dizayn",
                "icon": "fa-solid fa-pen-ruler",
                "description": "Foydalanuvchi uchun qulay va chiroyli interfeyslar loyihalash: Figma, dizayn tizimlari va prototiplash.",
                "order": 7,
            }
        )

        # Kurs: Prompt Injiniring
        course_prompt, _ = Course.objects.get_or_create(
            slug="prompt-injiniring-suniy-intellekt-bilan-samarali-ishlash",
            defaults={
                "title": "Prompt Injiniring: Sun'iy Intellekt bilan Samarali Ishlash",
                "category": cat_ai,
                "instructor": instructor,
                "short_description": "ChatGPT, Claude va boshqa yirik til modellaridan professional darajada foydalanish: aniq va samarali promptlar yozish san'ati.",
                "description": (
                    "Sun'iy intellekt modellari bugungi kunda ish unumdorligini bir necha barobar oshirish imkonini beradi, "
                    "biroq natija sifatini belgilovchi asosiy omil — to'g'ri so'rov (prompt) tuzish mahoratidir. "
                    "Ushbu kursda siz til modellarining ishlash tamoyillarini, rol berish (role prompting), zanjir fikrlash (chain-of-thought), "
                    "few-shot misollar va promptlarni tizimli optimallashtirish usullarini amaliy mashqlar orqali o'rganasiz."
                ),
                "level": CourseLevel.ALL_LEVELS,
                "price": 220000,
                "is_free": False,
                "duration_hours": 10,
                "students_count": 95,
                "rating": 4.80,
                "is_featured": False,
                "what_you_will_learn": (
                    "Yirik til modellari (LLM) qanday ishlashi haqida asosiy tushunchalar\n"
                    "Aniq, qisqa va natijali promptlar tuzish texnikalari\n"
                    "Rol berish, few-shot va chain-of-thought usullaridan foydalanish\n"
                    "Matn, kod va rasm generatsiyasi uchun maxsus promptlar yaratish\n"
                    "Ish jarayonlarini (workflow) AI yordamida avtomatlashtirish"
                ),
                "requirements": (
                    "Internetga ulangan kompyuter yoki telefon\n"
                    "ChatGPT yoki Claude kabi xizmatlardan foydalanish imkoniyati\n"
                    "Maxsus dasturlash bilimi talab qilinmaydi"
                ),
            }
        )
        m_prompt, _ = CourseModule.objects.get_or_create(course=course_prompt, title="1-Modul: Prompt Injiniring Asoslari", order=1)
        Lesson.objects.get_or_create(
            module=m_prompt,
            title="1.1. Til modeli qanday fikrlaydi?",
            defaults={
                "duration_minutes": 12,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Til Modeli Qanday Fikrlaydi?\n\n"
                    "Yirik til modellari (LLM) matnni token deb ataluvchi kichik bo'laklarga bo'lib, "
                    "har bir keyingi tokenni oldingi kontekst asosida ehtimollik bo'yicha tanlaydi.\n\n"
                    "### Muhim xulosa:\n"
                    "Model sizning so'rovingizdagi **har bir so'zni** kontekst sifatida hisobga oladi — "
                    "shuning uchun noaniq so'rov noaniq javobga olib keladi."
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_prompt,
            title="1.2. Aniq prompt tuzish formulasi (Rol + Vazifa + Format)",
            defaults={
                "duration_minutes": 18,
                "is_preview": False,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Aniq Prompt Tuzish Formulasi\n\n"
                    "Samarali prompt odatda uchta qismdan iborat bo'ladi:\n\n"
                    "1. **Rol** — modelga qanday mutaxassis sifatida javob berishini aytasiz.\n"
                    "2. **Vazifa** — aniq nima qilish kerakligini tushuntirasiz.\n"
                    "3. **Format** — javob qanday ko'rinishda bo'lishi kerakligini belgilaysiz.\n\n"
                    "```\n"
                    "Siz tajribali marketolog sifatida ishlang.\n"
                    "Quyidagi mahsulot uchun 3 ta sarlavha taklif qiling.\n"
                    "Javobni ro'yxat ko'rinishida bering.\n"
                    "```\n"
                )
            }
        )

        # Kurs: Python dasturlash tili asoslari
        course_py_basics, _ = Course.objects.get_or_create(
            slug="python-dasturlash-tili-asoslari",
            defaults={
                "title": "Python Dasturlash Tili Asoslari",
                "category": cat_backend,
                "instructor": instructor,
                "short_description": "Dasturlashni noldan boshlaydiganlar uchun Python tilining sintaksisi, ma'lumot turlari va amaliy mashqlar bilan mustahkam poydevor.",
                "description": (
                    "Python — soddaligi va keng qo'llanilishi bilan dasturlashni o'rganish uchun eng yaxshi tanlovlardan biri. "
                    "Ushbu kursda o'zgaruvchilar, shartli operatorlar, sikllar, funksiyalar, ro'yxatlar (list), lug'atlar (dict) "
                    "va obyektga yo'naltirilgan dasturlash (OOP) asoslarini amaliy misollar orqali bosqichma-bosqich o'rganasiz."
                ),
                "level": CourseLevel.BEGINNER,
                "price": 0,
                "is_free": True,
                "duration_hours": 20,
                "students_count": 310,
                "rating": 4.92,
                "is_featured": False,
                "what_you_will_learn": (
                    "Python sintaksisi, o'zgaruvchilar va ma'lumot turlari\n"
                    "Shartli operatorlar (if/elif/else) va takrorlash sikllari (for, while)\n"
                    "Funksiyalar yozish va argumentlar bilan ishlash\n"
                    "Ro'yxat (list), lug'at (dict) va to'plam (set) tuzilmalari\n"
                    "Obyektga yo'naltirilgan dasturlash (OOP) asoslari"
                ),
                "requirements": (
                    "Kompyuter (Windows, macOS yoki Linux)\n"
                    "Hech qanday oldindan dasturlash bilimi talab qilinmaydi"
                ),
            }
        )
        m_py1, _ = CourseModule.objects.get_or_create(course=course_py_basics, title="1-Modul: Python Sintaksisi va O'zgaruvchilar", order=1)
        Lesson.objects.get_or_create(
            module=m_py1,
            title="1.1. Python o'rnatish va birinchi dastur",
            defaults={
                "duration_minutes": 10,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Python O'rnatish va Birinchi Dastur\n\n"
                    "Python rasmiy saytidan (python.org) so'nggi versiyani yuklab oling va o'rnating.\n\n"
                    "```python\n"
                    "print('Salom, RoziyevDev!')\n"
                    "```\n\n"
                    "Ushbu bitta qator kod — sizning birinchi Python dasturingiz!"
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_py1,
            title="1.2. O'zgaruvchilar va ma'lumot turlari",
            defaults={
                "duration_minutes": 20,
                "is_preview": True,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# O'zgaruvchilar va Ma'lumot Turlari\n\n"
                    "```python\n"
                    "name = 'Ali'        # str\n"
                    "age = 25             # int\n"
                    "height = 1.75        # float\n"
                    "is_student = True    # bool\n"
                    "```\n\n"
                    "Python'da o'zgaruvchi turini alohida ko'rsatish shart emas — til buni avtomatik aniqlaydi."
                )
            }
        )

        # Kurs: Web dasturlash
        course_web, _ = Course.objects.get_or_create(
            slug="web-dasturlash-html-css-javascript",
            defaults={
                "title": "Web Dasturlash: HTML, CSS va JavaScript Asoslari",
                "category": cat_web,
                "instructor": instructor,
                "short_description": "Zamonaviy veb-saytlar yaratishning uchta ustuni — HTML, CSS va JavaScript'ni noldan amaliy loyihalar orqali o'rganing.",
                "description": (
                    "Ushbu kursda siz veb-sahifa tuzilishini HTML bilan shakllantirishni, CSS yordamida chiroyli va "
                    "moslashuvchan (responsive) dizayn yaratishni, hamda JavaScript bilan sahifaga interaktivlik qo'shishni "
                    "amaliy loyihalar asosida o'rganasiz."
                ),
                "level": CourseLevel.BEGINNER,
                "price": 280000,
                "is_free": False,
                "duration_hours": 24,
                "students_count": 210,
                "rating": 4.88,
                "is_featured": False,
                "what_you_will_learn": (
                    "HTML5 yordamida veb-sahifalar tuzilishini yaratish\n"
                    "CSS3 bilan zamonaviy va responsive dizayn (Flexbox, Grid)\n"
                    "JavaScript asoslari: o'zgaruvchilar, funksiyalar, DOM bilan ishlash\n"
                    "Formalar, animatsiyalar va interaktiv elementlar yaratish\n"
                    "Tayyor veb-sahifani hostingga joylashtirish"
                ),
                "requirements": (
                    "Kompyuter va zamonaviy brauzer\n"
                    "Dasturlashga qiziqish, oldindan bilim talab qilinmaydi"
                ),
            }
        )
        m_web1, _ = CourseModule.objects.get_or_create(course=course_web, title="1-Modul: HTML va CSS Asoslari", order=1)
        Lesson.objects.get_or_create(
            module=m_web1,
            title="1.1. HTML hujjat tuzilishi",
            defaults={
                "duration_minutes": 14,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# HTML Hujjat Tuzilishi\n\n"
                    "```html\n"
                    "<!DOCTYPE html>\n"
                    "<html lang=\"uz\">\n"
                    "<head>\n"
                    "    <meta charset=\"UTF-8\">\n"
                    "    <title>Mening Sahifam</title>\n"
                    "</head>\n"
                    "<body>\n"
                    "    <h1>Salom, Dunyo!</h1>\n"
                    "</body>\n"
                    "</html>\n"
                    "```\n"
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_web1,
            title="1.2. CSS bilan uslublashtirish",
            defaults={
                "duration_minutes": 22,
                "is_preview": False,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# CSS Bilan Uslublashtirish\n\n"
                    "```css\n"
                    "body {\n"
                    "    font-family: sans-serif;\n"
                    "    background-color: #f4f4f4;\n"
                    "}\n"
                    "h1 {\n"
                    "    color: #2563eb;\n"
                    "}\n"
                    "```\n"
                )
            }
        )

        # Kurs: UX/UI interfeys
        course_uxui, _ = Course.objects.get_or_create(
            slug="ux-ui-interfeys-dizayni-asoslari",
            defaults={
                "title": "UX/UI Interfeys Dizayni Asoslari",
                "category": cat_uxui,
                "instructor": instructor,
                "short_description": "Foydalanuvchi tajribasi (UX) va interfeys dizayni (UI) tamoyillari, Figma'da amaliy loyihalash va prototiplash.",
                "description": (
                    "Yaxshi mahsulot nafaqat to'g'ri ishlashi, balki foydalanuvchi uchun qulay va tushunarli bo'lishi ham kerak. "
                    "Ushbu kursda siz UX tadqiqot usullari, interfeys dizayni tamoyillari, rang va tipografika asoslarini, "
                    "hamda Figma dasturida interaktiv prototip yaratishni amaliy loyihalar orqali o'rganasiz."
                ),
                "level": CourseLevel.BEGINNER,
                "price": 260000,
                "is_free": False,
                "duration_hours": 18,
                "students_count": 140,
                "rating": 4.83,
                "is_featured": False,
                "what_you_will_learn": (
                    "UX tadqiqot asoslari: foydalanuvchi ehtiyojlarini aniqlash\n"
                    "UI dizayn tamoyillari: rang, tipografika, bo'shliq (spacing)\n"
                    "Figma dasturida interfeys komponentlari yaratish\n"
                    "Wireframe va interaktiv prototip tayyorlash\n"
                    "Dizayn tizimini (Design System) tashkil qilish"
                ),
                "requirements": (
                    "Kompyuter (Figma veb-brauzerda ham ishlaydi)\n"
                    "Vizual did va dizaynga qiziqish, oldindan tajriba shart emas"
                ),
            }
        )
        m_uxui1, _ = CourseModule.objects.get_or_create(course=course_uxui, title="1-Modul: UX/UI Asosiy Tushunchalar", order=1)
        Lesson.objects.get_or_create(
            module=m_uxui1,
            title="1.1. UX va UI o'rtasidagi farq",
            defaults={
                "duration_minutes": 11,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# UX va UI O'rtasidagi Farq\n\n"
                    "- **UX (User Experience)** — foydalanuvchining mahsulot bilan ishlash tajribasi: qulaylik, mantiqiylik, tezlik.\n"
                    "- **UI (User Interface)** — foydalanuvchi ko'rib turgan vizual qism: tugmalar, ranglar, shriftlar.\n\n"
                    "Yaxshi mahsulot — ham chiroyli (UI), ham qulay (UX) bo'lishi kerak."
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_uxui1,
            title="1.2. Rang va tipografika asoslari",
            defaults={
                "duration_minutes": 19,
                "is_preview": False,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Rang va Tipografika Asoslari\n\n"
                    "Interfeys uchun odatda 1 ta asosiy rang, 1-2 ta qo'shimcha rang va neytral kulrang palitradan foydalaniladi. "
                    "Matn uchun esa o'qilishi oson shrift tanlab, sarlavha va asosiy matn o'lchamlari orasida aniq ierarxiya yaratiladi."
                )
            }
        )

        # Kurs: Mobil dasturlash (Android/Kotlin — Flutter kursidan farqli, native yondashuv)
        course_mobile2, _ = Course.objects.get_or_create(
            slug="mobil-dasturlash-android-va-ios-asoslari",
            defaults={
                "title": "Mobil Dasturlash: Android va iOS Asoslari",
                "category": cat_mobile,
                "instructor": instructor,
                "short_description": "Mobil ilovalar dunyosiga kirish: platformalar farqi, UI komponentlar va birinchi mobil ilovangizni yaratish.",
                "description": (
                    "Mobil dasturlash sohasiga kirishni rejalashtirgan talabalar uchun mo'ljallangan ushbu kursda "
                    "Android va iOS platformalarining ishlash tamoyillari, mobil UI/UX qoidalari, hamda kross-platforma "
                    "yondashuvlar bilan tanishasiz va birinchi oddiy mobil ilovangizni yaratasiz."
                ),
                "level": CourseLevel.BEGINNER,
                "price": 240000,
                "is_free": False,
                "duration_hours": 16,
                "students_count": 175,
                "rating": 4.75,
                "is_featured": False,
                "what_you_will_learn": (
                    "Android va iOS platformalarining asosiy farqlari\n"
                    "Mobil interfeys (UI) loyihalash qoidalari\n"
                    "Native va kross-platforma (Flutter, React Native) yondashuvlar\n"
                    "Birinchi oddiy mobil ilovani yaratish va ishga tushirish\n"
                    "Ilovani do'konlarga (Google Play / App Store) joylashtirish bosqichlari"
                ),
                "requirements": (
                    "Kompyuter (Android Studio yoki Xcode o'rnatish imkoniyati)\n"
                    "Oldindan dasturlash bilimi shart emas, lekin mantiqiy fikrlash foydali"
                ),
            }
        )
        m_mob1, _ = CourseModule.objects.get_or_create(course=course_mobile2, title="1-Modul: Mobil Dasturlashga Kirish", order=1)
        Lesson.objects.get_or_create(
            module=m_mob1,
            title="1.1. Android va iOS: asosiy farqlar",
            defaults={
                "duration_minutes": 13,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Android va iOS: Asosiy Farqlar\n\n"
                    "- **Android** — Google tomonidan, ochiq manbali, Kotlin/Java tillarida ishlab chiqiladi.\n"
                    "- **iOS** — Apple tomonidan, yopiq ekotizim, Swift tilida ishlab chiqiladi.\n\n"
                    "Bitta kod bazasi bilan ikkala platformaga ilova yaratish uchun Flutter yoki React Native kabi "
                    "kross-platforma freymvorklaridan foydalaniladi."
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_mob1,
            title="1.2. Mobil UI loyihalash qoidalari",
            defaults={
                "duration_minutes": 17,
                "is_preview": False,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Mobil UI Loyihalash Qoidalari\n\n"
                    "Mobil interfeys kichik ekranga mo'ljallangani uchun tugmalar barmoq bosishga qulay o'lchamda "
                    "(kamida 44x44 piksel), matn o'qilishi oson va asosiy harakatlar ekranning pastki qismida joylashgan bo'lishi tavsiya etiladi."
                )
            }
        )

        # Kurs: Pythonda Telegram Bot Yaratish
        course_tg_bot, _ = Course.objects.get_or_create(
            slug="pythonda-telegram-bot-yaratish",
            defaults={
                "title": "Pythonda Telegram Bot Yaratish",
                "category": cat_backend,
                "instructor": instructor,
                "short_description": "python-telegram-bot kutubxonasi yordamida real loyihalar: buyruqlar, klaviaturalar, bazaga ulanish va botni serverga joylashtirish.",
                "description": (
                    "Telegram botlar — avtomatlashtirish, mijozlar bilan ishlash va shaxsiy loyihalar uchun eng qulay vositalardan biri. "
                    "Ushbu kursda siz Python tilida Telegram Bot API bilan ishlashni, buyruqlar va inline klaviaturalar yaratishni, "
                    "botni ma'lumotlar bazasiga ulashni va uni serverga joylashtirib doimiy ishlashini ta'minlashni o'rganasiz."
                ),
                "level": CourseLevel.INTERMEDIATE,
                "price": 250000,
                "is_free": False,
                "duration_hours": 14,
                "students_count": 130,
                "rating": 4.87,
                "is_featured": False,
                "what_you_will_learn": (
                    "Telegram Bot API va BotFather orqali bot yaratish\n"
                    "python-telegram-bot kutubxonasi bilan buyruqlar yozish\n"
                    "Inline va oddiy klaviaturalar yaratish\n"
                    "Botni ma'lumotlar bazasi (SQLite/PostgreSQL) bilan bog'lash\n"
                    "Botni serverga joylashtirish va 24/7 ishlashini ta'minlash"
                ),
                "requirements": (
                    "Python tilining asoslarini bilish (o'zgaruvchilar, funksiyalar)\n"
                    "Telegram akkaunti"
                ),
            }
        )
        m_tg1, _ = CourseModule.objects.get_or_create(course=course_tg_bot, title="1-Modul: Birinchi Telegram Bot", order=1)
        Lesson.objects.get_or_create(
            module=m_tg1,
            title="1.1. BotFather orqali bot yaratish",
            defaults={
                "duration_minutes": 10,
                "is_preview": True,
                "order": 1,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# BotFather Orqali Bot Yaratish\n\n"
                    "Telegram'da @BotFather'ga yozib, `/newbot` buyrug'i orqali yangi bot yaratasiz va undan olingan "
                    "**API token**ni xavfsiz joyda saqlaysiz — bu token orqali dasturingiz bot bilan bog'lanadi."
                )
            }
        )
        Lesson.objects.get_or_create(
            module=m_tg1,
            title="1.2. Birinchi /start buyrug'ini yozish",
            defaults={
                "duration_minutes": 20,
                "is_preview": True,
                "order": 2,
                "lesson_type": LessonType.TEXT,
                "content": (
                    "# Birinchi /start Buyrug'ini Yozish\n\n"
                    "```python\n"
                    "from telegram import Update\n"
                    "from telegram.ext import Application, CommandHandler, ContextTypes\n\n"
                    "async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):\n"
                    "    await update.message.reply_text('Salom! Men roziyev.dev botiman.')\n\n"
                    "app = Application.builder().token('TOKEN').build()\n"
                    "app.add_handler(CommandHandler('start', start))\n"
                    "app.run_polling()\n"
                    "```\n"
                )
            }
        )

        self.stdout.write(self.style.SUCCESS("Yangi kurslar (Prompt Injiniring, Python, Web, UX/UI, Mobil, Telegram Bot) kiritildi!"))
        self.stdout.write(self.style.SUCCESS("Barcha demo ma'lumotlar va blog maqolalari muvaffaqiyatli kiritildi!"))
