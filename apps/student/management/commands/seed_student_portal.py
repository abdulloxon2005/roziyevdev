import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import CustomUser
from apps.courses.models import Course, Lesson
from apps.contests.models import Contest, ContestProblem, ContestCategory
from apps.projects.models import Project, ProjectStatus, ProjectType
from apps.roadmaps.models import RoadmapTrack, RoadmapStage, RoadmapNode, NodeImportance


class Command(BaseCommand):
    help = "O'quvchi Paneli uchun demo ma'lumotlarni (Musobaqalar, Loyihalar, Dasturchi Yo'li) bazaga kiritadi."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Dasturchi Yo'li (Roadmaps) ma'lumotlari kiritilmoqda..."))

        # 1. ROADMAP TRACKS
        flutter_course = Course.objects.filter(category__slug='mobil-dasturlash').first() or Course.objects.first()
        backend_course = Course.objects.filter(category__slug='backend-python').first() or Course.objects.first()
        algo_course = Course.objects.filter(category__slug='algoritmlar-va-malumotlar-tuzilmasi').first() or Course.objects.first()

        # Track 1: Flutter
        track_flutter, _ = RoadmapTrack.objects.get_or_create(
            slug='flutter-mobil-dasturchi',
            defaults={
                'title': "Flutter & Dart Mobil Dasturchi",
                'icon': 'fa-solid fa-mobile-screen',
                'accent_color': 'blue',
                'short_description': "Noldan boshlab professional Flutter dasturchi bo'lishgacha bo'lgan barcha bosqichlar.",
                'estimated_months': 6,
                'order': 1,
                'is_active': True,
            }
        )

        st1, _ = RoadmapStage.objects.get_or_create(
            track=track_flutter, order=1,
            defaults={'title': "1-Bosqich: Dart Tili va Asoslari", 'description': "Dart sintaksisi, o'zgaruvchilar, funksiyalar va OOP tamoyillari."}
        )
        RoadmapNode.objects.get_or_create(
            stage=st1, order=1,
            defaults={
                'title': "Dart Sintaksisi va Tiplar",
                'summary': "O'zgaruvchilar (var, final, const), tiplar tizimi va null-safety xususiyatlari.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
                'external_docs_url': 'https://dart.dev/guides'
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=st1, order=2,
            defaults={
                'title': "OOP: Klasslar, Merosxo'rlik va Mixinlar",
                'summary': "Ob'ektga yo'naltirilgan dasturlash, enkapsulyatsiya, abstraksiya va mixinlar bilan ishlash.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
                'external_docs_url': 'https://dart.dev/language/classes'
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=st1, order=3,
            defaults={
                'title': "Asinxron Dasturlash (Future, Streams)",
                'summary': "async/await, Future ob'ektlari va oqimlar (Stream) bilan ishlash.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
            }
        )

        st2, _ = RoadmapStage.objects.get_or_create(
            track=track_flutter, order=2,
            defaults={'title': "2-Bosqich: Flutter Framework va UI", 'description': "Vidjetlar daraxti, tartiblash va moslashuvchan dizayn."}
        )
        RoadmapNode.objects.get_or_create(
            stage=st2, order=1,
            defaults={
                'title': "Widgetlar Daraxti (Stateless vs Stateful)",
                'summary': "Flutterda hamma narsa vidjet. Vidjet hayot davri va reaktiv chizilish tamoyili.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=st2, order=2,
            defaults={
                'title': "Responsive Dizayn va Layoutlar",
                'summary': "LayoutBuilder, MediaQuery va har xil ekran o'lchamlariga moslashish.",
                'importance': NodeImportance.RECOMMENDED,
                'linked_course': flutter_course,
            }
        )

        st3, _ = RoadmapStage.objects.get_or_create(
            track=track_flutter, order=3,
            defaults={'title': "3-Bosqich: Arxitektura va State Management", 'description': "BLoC, Clean Architecture va mahalliy kesh."}
        )
        RoadmapNode.objects.get_or_create(
            stage=st3, order=1,
            defaults={
                'title': "BLoC & Cubit State Management",
                'summary': "Holatni hodisalar va oqimlar orqali markazlashgan holda boshqarish.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=st3, order=2,
            defaults={
                'title': "REST API & Offline Kesh (Dio, Hive)",
                'summary': "Server bilan muloqot, tokenlarni saqlash va oflayn rejimni tashkillashtirish.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': flutter_course,
            }
        )

        # Track 2: Python Backend
        track_py, _ = RoadmapTrack.objects.get_or_create(
            slug='python-backend-muhandisi',
            defaults={
                'title': "Python & Django Backend Muhandisi",
                'icon': 'fa-brands fa-python',
                'accent_color': 'emerald',
                'short_description': "Murakkab veb-servislar, REST API va ma'lumotlar bazalari arxitekturasi.",
                'estimated_months': 6,
                'order': 2,
                'is_active': True,
            }
        )
        py_st1, _ = RoadmapStage.objects.get_or_create(
            track=track_py, order=1,
            defaults={'title': "1-Bosqich: Python Chuqurlashtirilgan", 'description': "Dekoratorlar, generatorlar, OOP va paketlar."}
        )
        RoadmapNode.objects.get_or_create(
            stage=py_st1, order=1,
            defaults={
                'title': "Python Ma'lumotlar Tuzilmalari va OOP",
                'summary': "Lug'atlar, to'plamlar, dunder metodlar va xotira boshqaruvi.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': backend_course,
            }
        )
        py_st2, _ = RoadmapStage.objects.get_or_create(
            track=track_py, order=2,
            defaults={'title': "2-Bosqich: Django & REST Framework", 'description': "Web arxitekturasi, ORM va API dizayni."}
        )
        RoadmapNode.objects.get_or_create(
            stage=py_st2, order=1,
            defaults={
                'title': "Django ORM va PostgreSQL",
                'summary': "Murakkab so'rovlar, indeksatsiya, tranzaksiyalar va migratsiyalar.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': backend_course,
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=py_st2, order=2,
            defaults={
                'title': "DRF: Serializers, ViewSets & JWT",
                'summary': "Xavfsiz RESTful API ishlab chiqish va OpenAPI hujjatlashtirish.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': backend_course,
            }
        )

        # Track 3: Algoritmlar
        track_algo, _ = RoadmapTrack.objects.get_or_create(
            slug='algoritmlar-va-muhandislik',
            defaults={
                'title': "Algoritmlar & Ma'lumotlar Tuzilmasi",
                'icon': 'fa-solid fa-code-branch',
                'accent_color': 'purple',
                'short_description': "Dasturiy mantiq, Big-O tahlili va samarali kod yozish madaniyati.",
                'estimated_months': 4,
                'order': 3,
                'is_active': True,
            }
        )
        algo_st1, _ = RoadmapStage.objects.get_or_create(
            track=track_algo, order=1,
            defaults={'title': "1-Bosqich: Asosiy Algoritmik Tushunchalar", 'description': "Big-O, saralash va qidiruv algoritmlari."}
        )
        RoadmapNode.objects.get_or_create(
            stage=algo_st1, order=1,
            defaults={
                'title': "Vaqt Murakkabligi va Big-O Notatsiyasi",
                'summary': "Algoritm tezligini xotira va vaqt bo'yicha matematik baholash.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': algo_course,
            }
        )
        RoadmapNode.objects.get_or_create(
            stage=algo_st1, order=2,
            defaults={
                'title': "Binar Qidiruv va Tezkor Saralash (QuickSort)",
                'summary': "Bo'lib tashla va hukmronlik qil tamoyili asosidagi klassik algoritmlar.",
                'importance': NodeImportance.ESSENTIAL,
                'linked_course': algo_course,
            }
        )

        self.stdout.write(self.style.SUCCESS("Dasturchi Yo'li ma'lumotlari muvaffaqiyatli saqlandi!"))

        # 2. CONTESTS
        self.stdout.write(self.style.NOTICE("Musobaqalar (Contests) ma'lumotlari kiritilmoqda..."))
        now = timezone.now()

        # Active contest
        c1, _ = Contest.objects.get_or_create(
            slug='algoritmik-kodlash-chempionati-1',
            defaults={
                'title': "Haftalik Algoritmik Kodlash Bellashuvi #1",
                'category': ContestCategory.ALGORITHMIC,
                'description': "Ushbu musobaqada algoritmlar va ma'lumotlar tuzilmalariga oid 3 ta masala berilgan. Eng tez va aniq yechim egalari tangalar bilan taqdirlanadi.",
                'rules': "Barcha yechimlar tekshiriladi. Begona yechimlarni ko'chirish taqiqlanadi.",
                'start_time': now - datetime.timedelta(hours=12),
                'end_time': now + datetime.timedelta(days=2),
                'coin_prize_pool': 500,
                'first_place_reward': "300 tanga + Diplom",
                'second_place_reward': "150 tanga",
                'third_place_reward': "50 tanga",
                'is_published': True,
            }
        )
        ContestProblem.objects.get_or_create(
            contest=c1, order=1,
            defaults={
                'title': "Massivdagi Ikki Son Yig'indisi (Two Sum)",
                'description': "Berilgan butun sonlar massividan yig'indisi maqsadli `target` soniga teng bo'lgan ikkita sonning indekslarini toping.",
                'points': 100,
                'difficulty': 'easy',
                'starter_code': "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Kodingizni yozing\n    pass\n"
            }
        )
        ContestProblem.objects.get_or_create(
            contest=c1, order=2,
            defaults={
                'title': "Palindromik Qatorni Tekshirish",
                'description': "Berilgan satr faqat harf va raqamlarni hisobga olganda chapdan ham, o'ngdan ham bir xil o'qilishini tekshiruvchi funksiya yozing.",
                'points': 150,
                'difficulty': 'medium',
                'starter_code': "def is_palindrome(s: str) -> bool:\n    # Kodingizni yozing\n    pass\n"
            }
        )

        # Upcoming contest
        c2, _ = Contest.objects.get_or_create(
            slug='flutter-clean-architecture-hackathon',
            defaults={
                'title': "Flutter UI & Clean Architecture Hackathon",
                'category': ContestCategory.MOBILE,
                'description': "48 soatlik mobil dasturlash xakatoni. Berilgan dizayn bo'yicha to'liq ishlovchi ilova tayyorlang va hakamlar bahosiga yuboring.",
                'rules': "Flutter 3.x, BLoC yoki Riverpod bilan Clean Architecture talab qilinadi.",
                'start_time': now + datetime.timedelta(days=3),
                'end_time': now + datetime.timedelta(days=5),
                'coin_prize_pool': 1000,
                'first_place_reward': "600 tanga + Premium Sertifikat",
                'second_place_reward': "300 tanga",
                'third_place_reward': "100 tanga",
                'is_published': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("Musobaqalar muvaffaqiyatli yaratildi!"))

        # 3. STUDENT PROJECTS
        self.stdout.write(self.style.NOTICE("Talabalar loyihalari (Projects) kiritilmoqda..."))
        admin_user = CustomUser.objects.filter(is_superuser=True).first() or CustomUser.objects.first()

        if admin_user:
            Project.objects.get_or_create(
                slug='e-bozor-yetkazib-berish-mobil-ilovasi',
                defaults={
                    'author': admin_user,
                    'course': flutter_course,
                    'title': "E-Bozor — Mobil Yetkazib Berish Ilovasi",
                    'tagline': "Flutter va BLoC arxitekturasida yaratilgan zamonaviy online do'kon va kuryer ilovasi",
                    'description': "Ushbu loyiha Flutter kursining bitiruv amaliy ishi hisoblanadi. Real vaqt rejimida buyurtmalarni kuzatish, savatcha va to'lov tizimlari integratsiya qilingan.",
                    'tech_stack': "Flutter, BLoC, Django REST, PostgreSQL, Docker",
                    'github_url': "https://github.com/roziyevdev/ebozor-flutter",
                    'demo_url': "https://roziyev.dev",
                    'project_type': ProjectType.CAPSTONE,
                    'status': ProjectStatus.FEATURED,
                    'score': 98,
                    'instructor_review': "Dastur arxitekturasi juda yuqori saviyada qurilgan. Clean Architecture prinsiplari to'liq qo'llangan.",
                    'likes_count': 18,
                    'views_count': 140,
                }
            )

            Project.objects.get_or_create(
                slug='edubot-telegram-crm-tizimi',
                defaults={
                    'author': admin_user,
                    'course': backend_course,
                    'title': "EduBot — O'quv Markazlari CRM Tizimi",
                    'tagline': "Telegram bot va Django admin orqali boshqariluvchi to'liq avtomatlashtirilgan ta'lim platformasi",
                    'description': "O'quvchilarni ro'yxatga olish, dars jadvallarini yuborish, to'lovlarni tekshirish va dars eslatmalarini jo'natuvchi aqlli bot.",
                    'tech_stack': "Python, Aiogram, Django, PostgreSQL, Redis",
                    'github_url': "https://github.com/roziyevdev/edubot-crm",
                    'demo_url': "https://t.me/roziyevdev_bot",
                    'project_type': ProjectType.PERSONAL,
                    'status': ProjectStatus.APPROVED,
                    'score': 94,
                    'instructor_review': "Asinxron arxitektura va Redis keshlash tizimi to'g'ri tashkil etilgan.",
                    'likes_count': 12,
                    'views_count': 85,
                }
            )

        self.stdout.write(self.style.SUCCESS("O'quvchi Paneli demo ma'lumotlari muvaffaqiyatli kiritildi!"))
