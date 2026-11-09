"""
Izolyatsiyalangan Python kod bajarish muhiti (sandbox).

Bu paket Django'ga bog'liq emas. U ikki xil usulda ishlatiladi:

1. Django ichidan ``code_sandbox.executor.run_python`` orqali (lokal ``subprocess`` backend) —
   foydalanuvchi kodi har safar alohida, toza muhitli, resurslari cheklangan Python
   jarayonida bajariladi. Web-server jarayonining o'zida hech qachon ``exec()`` qilinmaydi.
2. Alohida konteynerda ``python -m code_sandbox.server`` HTTP xizmati sifatida —
   production uchun tavsiya etiladi (tarmoqdan uzilgan, read-only, xotira/CPU/PID limitli).
"""
