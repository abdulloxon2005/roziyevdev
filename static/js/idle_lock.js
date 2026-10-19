/**
 * RoziyevDev LMS — Harakatsizlik Taymeri va Xavfsizlik Qulfi (Idle Session Lock)
 */
(function() {
    'use strict';

    const TIMEOUT_SECONDS = parseInt(window.SESSION_IDLE_TIMEOUT, 10) || 900; // 15 daqiqa
    const WARNING_SECONDS = 60; // 60 soniya oldin ogohlantirish

    let secondsLeft = TIMEOUT_SECONDS;
    let isLocked = false;
    let timerInterval = null;

    const overlay = document.getElementById('session-lock-overlay');
    const warningToast = document.getElementById('idle-warning-toast');
    const countdownEl = document.getElementById('idle-warning-countdown');
    const unlockForm = document.getElementById('session-unlock-form');
    const passwordInput = document.getElementById('lock-password-input');
    const errorMsg = document.getElementById('lock-error-msg');
    const submitBtn = document.getElementById('unlock-submit-btn');
    const btnText = document.getElementById('unlock-btn-text');

    if (!overlay || !unlockForm) {
        return;
    }

    // Foydalanuvchi faolligini qayd qilish (Faqat qulf ochilmagan paytda)
    function onUserActivity() {
        if (isLocked) return;

        // Agar ogohlantirish ko'rsatilgan bo'lsa, uni yashirish
        if (secondsLeft <= WARNING_SECONDS) {
            hideWarning();
        }

        secondsLeft = TIMEOUT_SECONDS;
    }

    // Hodisalarni tinglash (Trotling bilan)
    let lastActivityCall = 0;
    function throttledActivity() {
        const now = Date.now();
        if (now - lastActivityCall > 1000) {
            lastActivityCall = now;
            onUserActivity();
        }
    }

    ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart'].forEach(evt => {
        window.addEventListener(evt, throttledActivity, { passive: true });
    });

    // Ogohlantirishni ko'rsatish
    function showWarning(left) {
        if (!warningToast) return;
        if (countdownEl) countdownEl.textContent = left;
        warningToast.classList.remove('translate-y-32', 'opacity-0', 'pointer-events-none');
    }

    // Ogohlantirishni yashirish
    function hideWarning() {
        if (!warningToast) return;
        warningToast.classList.add('translate-y-32', 'opacity-0', 'pointer-events-none');
    }

    // Ekranni qulflash
    function lockScreen() {
        if (isLocked) return;
        isLocked = true;
        hideWarning();

        overlay.classList.remove('hidden');
        // Force reflow
        void overlay.offsetWidth;
        overlay.classList.remove('opacity-0');
        const modal = overlay.querySelector('div');
        if (modal) {
            modal.classList.remove('scale-95');
            modal.classList.add('scale-100');
        }

        if (passwordInput) {
            passwordInput.value = '';
            passwordInput.focus();
        }
        if (errorMsg) {
            errorMsg.classList.add('hidden');
            errorMsg.textContent = '';
        }
    }

    // Ekranni qulfdan chiqarish
    function unlockScreen() {
        isLocked = false;
        secondsLeft = TIMEOUT_SECONDS;

        overlay.classList.add('opacity-0');
        const modal = overlay.querySelector('div');
        if (modal) {
            modal.classList.remove('scale-100');
            modal.classList.add('scale-95');
        }

        setTimeout(() => {
            overlay.classList.add('hidden');
        }, 300);

        if (passwordInput) {
            passwordInput.value = '';
        }
        if (errorMsg) {
            errorMsg.classList.add('hidden');
        }
    }

    // Taymer sikli (har 1 soniyada)
    timerInterval = setInterval(() => {
        if (isLocked) return;

        secondsLeft--;

        if (secondsLeft <= 0) {
            lockScreen();
        } else if (secondsLeft <= WARNING_SECONDS) {
            showWarning(secondsLeft);
        }
    }, 1000);

    // Qulfni ochish formasini yuborish (AJAX)
    unlockForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const password = passwordInput.value.trim();
        if (!password) {
            showError("Iltimos, parolingizni kiriting!");
            return;
        }

        // Yuklanish holati
        submitBtn.disabled = true;
        btnText.textContent = "Tekshirilmoqda...";

        const csrfToken = unlockForm.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('password', password);
        formData.append('next', window.CURRENT_PATH || '/');

        fetch(window.UNLOCK_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(async (response) => {
            const data = await response.json();
            if (response.ok && data.success) {
                unlockScreen();
            } else if (data.expired && data.redirect) {
                window.location.href = data.redirect;
            } else {
                showError(data.error || "Parol noto'g'ri kiritildi!");
            }
        })
        .catch(err => {
            console.error('Unlock error:', err);
            showError("Tarmoq xatosi yoki seans muddati tugagan. Qaytadan kiring.");
        })
        .finally(() => {
            submitBtn.disabled = false;
            btnText.textContent = "Qulfni Ochish";
        });
    });

    function showError(msg) {
        if (errorMsg) {
            errorMsg.textContent = msg;
            errorMsg.classList.remove('hidden');
        }
        if (passwordInput) {
            passwordInput.classList.add('border-rose-500', 'ring-1', 'ring-rose-500');
            passwordInput.focus();
            setTimeout(() => {
                passwordInput.classList.remove('border-rose-500', 'ring-1', 'ring-rose-500');
            }, 3000);
        }
    }

    // Parolni ko'rsatish / yashirish
    window.toggleLockPasswordVisibility = function() {
        if (!passwordInput) return;
        const eyeIcon = document.getElementById('lock-pass-eye');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            if (eyeIcon) {
                eyeIcon.classList.remove('fa-eye');
                eyeIcon.classList.add('fa-eye-slash');
            }
        } else {
            passwordInput.type = 'password';
            if (eyeIcon) {
                eyeIcon.classList.remove('fa-eye-slash');
                eyeIcon.classList.add('fa-eye');
            }
        }
    };

})();
