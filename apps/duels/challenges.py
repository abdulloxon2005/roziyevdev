"""Boshlang'ich duel topshiriqlari (bo'sh bo'lsa avtomatik yaratiladi)."""

DEFAULTS = [
    # (sarlavha, tavsif, qiyinlik, testlar)
    ("Ikki son yig'indisi", "solve(a, b) funksiyasi a va b ning yig'indisini qaytarsin.", 'easy',
     [[[1, 2], 3], [[-5, 5], 0], [[100, 250], 350]]),
    ("Juft yoki toq", "solve(n) funksiyasi n juft bo'lsa 'juft', aks holda 'toq' qaytarsin.", 'easy',
     [[[4], 'juft'], [[7], 'toq'], [[0], 'juft']]),
    ("Eng katta son", "solve(nums) ro'yxatdagi eng katta sonni qaytarsin.", 'easy',
     [[[[1, 9, 3]], 9], [[[-4, -2, -8]], -2], [[[5]], 5]]),
    ("Faktorial", "solve(n) funksiyasi n! ni qaytarsin (0! = 1).", 'medium',
     [[[0], 1], [[5], 120], [[10], 3628800]]),
    ("Palindrom", "solve(s) satr palindrom bo'lsa True, aks holda False qaytarsin (harf registri e'tiborsiz).", 'medium',
     [[['Level'], True], [['salom'], False], [['Anna'], True]]),
    ("Unli harflar soni", "solve(s) satrdagi unli harflar (a, e, i, o, u) sonini qaytarsin.", 'medium',
     [[['hello'], 2], [['rhythm'], 0], [['Education'], 5]]),
    ("Fibonachchi", "solve(n) n-chi Fibonachchi sonini qaytarsin (F0=0, F1=1).", 'hard',
     [[[0], 0], [[1], 1], [[10], 55], [[30], 832040]]),
    ("Tub sonlar soni", "solve(n) funksiyasi 1 dan n gacha (n ham kiradi) nechta tub son borligini qaytarsin.", 'hard',
     [[[10], 4], [[1], 0], [[50], 15]]),
    ("Qavslar balansi", "solve(s) faqat ()[]{} dan iborat satrdagi qavslar to'g'ri joylashgan bo'lsa True qaytarsin.", 'hard',
     [[['([]{})'], True], [['(]'], False], [[''], True], [['((('], False]]),
]


def ensure_challenges():
    from .models import DuelChallenge
    if DuelChallenge.objects.exists():
        return
    DuelChallenge.objects.bulk_create([
        DuelChallenge(title=t, description=d, difficulty=diff, tests=tests)
        for t, d, diff, tests in DEFAULTS
    ])
