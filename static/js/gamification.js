/**
 * roziyevdev - Gamification Audio & Coin Animation Engine
 * Uses Web Audio API for zero-latency, cross-browser coin chimes without external audio assets.
 */
(function() {
    // 1. Web Audio API Coin Synthesizer
    let audioCtx = null;

    function getAudioContext() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                audioCtx = new AudioContext();
            }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    window.playCoinSound = function() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;

            // Tone 1: B5 (987.77 Hz)
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(987.77, now);
            gain1.gain.setValueAtTime(0.3, now);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.12);

            // Tone 2: E6 (1318.51 Hz) - high energetic bell
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(1318.51, now + 0.08);
            gain2.gain.setValueAtTime(0.35, now + 0.08);
            gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.08);
            osc2.stop(now + 0.45);
        } catch (e) {
            console.warn("AudioContext error:", e);
        }
    };

    // 2. Floating Coin Celebration Animation
    window.celebrateCoins = function(amount = 25, message = "Tangachalar qo'shildi!") {
        window.playCoinSound();

        const container = document.createElement('div');
        container.className = 'fixed inset-0 pointer-events-none z-[9999] flex items-center justify-center overflow-hidden';
        document.body.appendChild(container);

        // Center celebration badge
        const badge = document.createElement('div');
        badge.className = 'px-6 py-4 rounded-2xl bg-amber-500/90 text-slate-950 font-black text-lg shadow-2xl backdrop-blur-md flex items-center gap-3 transform scale-50 opacity-0 transition-all duration-300 pointer-events-auto border-2 border-yellow-300';
        badge.innerHTML = `
            <span class="material-symbols-outlined text-slate-950 text-4xl animate-bounce">monetization_on</span>
            <div>
                <div class="text-xl font-extrabold leading-none">+${amount} Tanga!</div>
                <div class="text-xs font-semibold text-slate-900 mt-1">${message}</div>
            </div>
        `;
        container.appendChild(badge);

        requestAnimationFrame(() => {
            badge.style.transform = 'scale(1)';
            badge.style.opacity = '1';
        });

        // Spawn 16 floating coins with random physics
        const numCoins = 16;
        for (let i = 0; i < numCoins; i++) {
            const coin = document.createElement('div');
            coin.innerHTML = '<span class="material-symbols-outlined text-amber-400 text-3xl drop-shadow-md">monetization_on</span>';
            coin.className = 'absolute select-none';
            coin.style.left = '50%';
            coin.style.top = '50%';
            coin.style.transform = 'translate(-50%, -50%)';

            const angle = (Math.PI * 2 * i) / numCoins + (Math.random() * 0.4 - 0.2);
            const distance = 80 + Math.random() * 140;
            const destX = Math.cos(angle) * distance;
            const destY = Math.sin(angle) * distance - 40; // bias upwards
            const duration = 700 + Math.random() * 500;

            container.appendChild(coin);

            coin.animate([
                { transform: 'translate(-50%, -50%) scale(0.5) rotate(0deg)', opacity: 1 },
                { transform: `translate(calc(-50% + ${destX}px), calc(-50% + ${destY}px)) scale(1.3) rotate(${360 * (i % 2 === 0 ? 1 : -1)}deg)`, opacity: 0.9, offset: 0.6 },
                { transform: `translate(calc(-50% + ${destX}px), calc(-50% + ${destY + 60}px)) scale(0.8) rotate(720deg)`, opacity: 0 }
            ], {
                duration: duration,
                easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
                fill: 'forwards'
            });
        }

        // Cleanup
        setTimeout(() => {
            badge.style.transform = 'scale(0.8) translateY(-20px)';
            badge.style.opacity = '0';
            setTimeout(() => {
                container.remove();
            }, 300);
        }, 2200);
    };

    // Auto-detect celebration flags from URL or data attributes
    document.addEventListener('DOMContentLoaded', () => {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('celebrate_coins')) {
            const amount = parseInt(urlParams.get('celebrate_coins'), 10) || 50;
            setTimeout(() => {
                window.celebrateCoins(amount, "Vazifangiz qabul qilindi!");
            }, 600);
        }
    });
})();
