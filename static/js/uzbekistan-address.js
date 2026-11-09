/**
 * O'zbekiston Respublikasi viloyatlari va tumanlari ro'yxati.
 * Ro'yxatdan o'tish formasida "Viloyat" tanlangach, shu viloyatga tegishli
 * tumanlar/shaharlar ro'yxati avtomatik to'ldiriladi.
 */
const UZBEKISTAN_REGIONS = {
    "Andijon viloyati": [
        "Andijon shahri", "Xonobod shahri", "Andijon tumani", "Asaka tumani",
        "Baliqchi tumani", "Bo'z tumani", "Buloqboshi tumani", "Izboskan tumani",
        "Jalaquduq tumani", "Marhamat tumani", "Oltinko'l tumani", "Paxtaobod tumani",
        "Shahrixon tumani", "Xo'jaobod tumani", "Qo'rg'ontepa tumani"
    ],
    "Buxoro viloyati": [
        "Buxoro shahri", "Kogon shahri", "Buxoro tumani", "G'ijduvon tumani",
        "Jondor tumani", "Kogon tumani", "Olot tumani", "Peshku tumani",
        "Qorako'l tumani", "Qorovulbozor tumani", "Romitan tumani", "Shofirkon tumani",
        "Vobkent tumani"
    ],
    "Farg'ona viloyati": [
        "Farg'ona shahri", "Marg'ilon shahri", "Qo'qon shahri", "Quvasoy shahri",
        "Farg'ona tumani", "Bag'dod tumani", "Beshariq tumani", "Buvayda tumani",
        "Dang'ara tumani", "Furqat tumani", "Qo'shtepa tumani", "Oltiariq tumani",
        "Quva tumani", "Rishton tumani", "So'x tumani", "Toshloq tumani",
        "O'zbekiston tumani", "Uchko'prik tumani", "Yozyovon tumani"
    ],
    "Jizzax viloyati": [
        "Jizzax shahri", "Jizzax tumani", "Arnasoy tumani", "Baxmal tumani",
        "Do'stlik tumani", "Forish tumani", "G'allaorol tumani", "Zafarobod tumani",
        "Zarbdor tumani", "Zomin tumani", "Mirzachul tumani", "Paxtakor tumani",
        "Sharof Rashidov tumani", "Yangiobod tumani"
    ],
    "Namangan viloyati": [
        "Namangan shahri", "Namangan tumani", "Chortoq tumani", "Chust tumani",
        "Kosonsoy tumani", "Mingbuloq tumani", "Norin tumani", "Pop tumani",
        "To'raqo'rg'on tumani", "Uchqo'rg'on tumani", "Uychi tumani", "Yangiqo'rg'on tumani"
    ],
    "Navoiy viloyati": [
        "Navoiy shahri", "Zarafshon shahri", "Uchquduq tumani", "Konimex tumani",
        "Karmana tumani", "Qiziltepa tumani", "Navbahor tumani", "Nurota tumani",
        "Tomdi tumani", "Xatirchi tumani"
    ],
    "Qashqadaryo viloyati": [
        "Qarshi shahri", "Shahrisabz shahri", "Qamashi tumani", "Qarshi tumani",
        "Kasbi tumani", "Kitob tumani", "Koson tumani", "Mirishkor tumani",
        "Muborak tumani", "Nishon tumani", "Chiroqchi tumani", "Shahrisabz tumani",
        "Yakkabog' tumani", "Dehqonobod tumani", "G'uzor tumani"
    ],
    "Qoraqalpog'iston Respublikasi": [
        "Nukus shahri", "Amudaryo tumani", "Beruniy tumani", "Chimboy tumani",
        "Ellikqal'a tumani", "Kegeyli tumani", "Mo'ynoq tumani", "Nukus tumani",
        "Qanliko'l tumani", "Qo'ng'irot tumani", "Qoraozak tumani", "Shumanay tumani",
        "Taxtako'pir tumani", "To'rtko'l tumani", "Xo'jayli tumani"
    ],
    "Samarqand viloyati": [
        "Samarqand shahri", "Kattaqo'rg'on shahri", "Bulung'ur tumani", "Ishtixon tumani",
        "Jomboy tumani", "Kattaqo'rg'on tumani", "Qo'shrabot tumani", "Narpay tumani",
        "Nurobod tumani", "Oqdaryo tumani", "Paxtachi tumani", "Payariq tumani",
        "Pastdarg'om tumani", "Samarqand tumani", "Toyloq tumani", "Urgut tumani"
    ],
    "Sirdaryo viloyati": [
        "Guliston shahri", "Shirin shahri", "Boyovut tumani", "Guliston tumani",
        "Mirzaobod tumani", "Oqoltin tumani", "Sardoba tumani", "Sayxunobod tumani",
        "Sirdaryo tumani", "Xovos tumani"
    ],
    "Surxondaryo viloyati": [
        "Termiz shahri", "Angor tumani", "Bandixon tumani", "Boysun tumani",
        "Denov tumani", "Jarqo'rg'on tumani", "Qiziriq tumani", "Qumqo'rg'on tumani",
        "Muzrabot tumani", "Oltinsoy tumani", "Sariosiyo tumani", "Sherobod tumani",
        "Shurchi tumani", "Termiz tumani", "Uzun tumani"
    ],
    "Toshkent shahri": [
        "Bektemir tumani", "Chilonzor tumani", "Mirobod tumani", "Mirzo Ulug'bek tumani",
        "Olmazor tumani", "Sergeli tumani", "Shayxontohur tumani", "Uchtepa tumani",
        "Yakkasaroy tumani", "Yashnobod tumani", "Yunusobod tumani", "Yangihayot tumani"
    ],
    "Toshkent viloyati": [
        "Nurafshon shahri", "Angren shahri", "Bekobod shahri", "Olmaliq shahri",
        "Chirchiq shahri", "Yangiyul shahri", "Bekobod tumani", "Bo'ka tumani",
        "Bo'stonliq tumani", "Chinoz tumani", "Qibray tumani", "Oqqo'rg'on tumani",
        "Ohangaron tumani", "Parkent tumani", "Piskent tumani", "Quyichirchiq tumani",
        "O'rtachirchiq tumani", "Yuqorichirchiq tumani", "Yangiyul tumani", "Zangiota tumani"
    ],
    "Xorazm viloyati": [
        "Urganch shahri", "Xiva shahri", "Bog'ot tumani", "Gurlan tumani",
        "Qo'shko'pir tumani", "Shovot tumani", "Urganch tumani", "Xazorasp tumani",
        "Xiva tumani", "Xonqa tumani", "Yangiariq tumani", "Yangibozor tumani"
    ]
};

/**
 * Berilgan <select> elementlarini O'zbekiston viloyat/tuman ma'lumotlari bilan bog'laydi.
 * @param {HTMLSelectElement} regionSelect - Viloyat tanlash select elementi
 * @param {HTMLSelectElement} districtSelect - Tuman/shahar tanlash select elementi
 */
function initUzbekistanAddressSelects(regionSelect, districtSelect) {
    if (!regionSelect || !districtSelect) return;

    const regionNames = Object.keys(UZBEKISTAN_REGIONS).sort((a, b) => a.localeCompare(b, 'uz'));
    regionNames.forEach((name) => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        regionSelect.appendChild(option);
    });

    function fillDistricts(regionName) {
        districtSelect.innerHTML = '<option value="">Tumanni tanlang</option>';
        const districts = UZBEKISTAN_REGIONS[regionName] || [];
        districts.forEach((district) => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = district;
            districtSelect.appendChild(option);
        });
        districtSelect.disabled = districts.length === 0;
    }

    regionSelect.addEventListener('change', () => fillDistricts(regionSelect.value));
    districtSelect.disabled = true;
}
