from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    Application
)
from .student_api import StudentAPI
import logging
from os import getenv
from datetime import datetime

# States untuk conversation
LOGIN, PRESENCE = range(2)

# Simpan instance StudentAPI
student_api = StudentAPI(getenv('BASE_URL', 'https://student.amikompurwokerto.ac.id'))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start."""
    await update.message.reply_text(
        "✦ AbsenKuy Bot\n"
        "────\n"
        "⟢ Tentang:\n"
        "    » Bot presensi otomatis untuk mahasiswa AMIKOM\n"
        "    » Akses cepat dan mudah melalui Telegram\n"
        "────\n"
        "⟢ Perintah:\n"
        "    » /login - Masuk ke portal mahasiswa\n"
        "    » /help - Melihat semua perintah",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help."""
    help_text = (
        "✦ Bantuan AbsenKuy\n"
        "────\n"
        "⟢ Umum:\n"
        "    » /start - Memulai bot\n"
        "    » /help - Menampilkan bantuan\n"
        "────\n"
        "⟢ Akademik:\n"
        "    » /login - Login ke portal\n"
        "    » /logout - Logout dari portal\n"
        "    » /absenbang - Melakukan presensi\n"
        "────\n"
        "⟢ Informasi:\n"
        "    » Butuh bantuan? Hubungi admin\n"
        "    » Bot version 1.0"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /login."""
    if student_api.is_logged_in():
        await update.message.reply_text(
            "✦ Sudah Login\n"
            "────\n"
            "⟢ Status:\n"
            "    » Anda sudah login ke portal\n"
            "────\n"
            "⟢ Opsi:\n"
            "    » /absenbang - Melakukan presensi\n"
            "    » /logout - Keluar dari portal",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "✦ Login Portal\n"
        "────\n"
        "⟢ Instruksi:\n"
        "    » Masukkan NIM dan password\n"
        "    » Format: `NIM password`\n"
        "    » Contoh: `22SA1234 rahasia123`\n"
        "────\n"
        "⟢ Opsi:\n"
        "    » /cancel - Membatalkan login",
        parse_mode='Markdown'
    )
    return LOGIN

async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk memproses kredensial login."""
    try:
        credentials = update.message.text.split()
        if len(credentials) != 2:
            await update.message.reply_text(
                "✦ Format Salah\n"
                "────\n"
                "⟢ Error:\n"
                "    » Format tidak sesuai\n"
                "────\n"
                "⟢ Contoh:\n"
                "    » `NIM password`\n"
                "    » `22SA1234 rahasia123`",
                parse_mode='Markdown'
            )
            return LOGIN
        
        username, password = credentials
        if student_api.login(username, password):
            # Ambil informasi profil
            profile = student_api.get_profile()
            if profile:
                context.user_data['profile'] = profile
                profile_text = (
                    f"✦ Login Berhasil\n"
                    f"────\n"
                    f"⟢ Mahasiswa:\n"
                    f"    » Nama: {profile['nama']}\n"
                    f"    » NIM: {profile['nim']}\n"
                    f"    » Kontak: {profile['no_hp']}\n"
                    f"    » Email: {profile['email']}\n"
                    f"────\n"
                    f"⟢ Akademik:\n"
                    f"    » Fakultas: {profile['fakultas']}\n"
                    f"    » Program: {profile['prodi']}\n"
                    f"    » Angkatan: {profile['angkatan']}\n"
                    f"    » Pembimbing: {profile['pembimbing']}\n"
                    f"────\n"
                    f"⟢ Prestasi:\n"
                    f"    » IPK: {profile['ipk']}\n"
                    f"    » Total SKS: {profile['total_sks']}\n"
                    f"    » Semester ini: {profile['sks_sekarang']} SKS\n"
                    f"────\n"
                    f"Gunakan /absenbang untuk melakukan presensi"
                )
                await update.message.reply_text(profile_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "✦ Login Berhasil\n"
                    "────\n"
                    "⟢ Status:\n"
                    "    » Berhasil masuk ke portal\n"
                    "────\n"
                    "⟢ Selanjutnya:\n"
                    "    » Gunakan /absenbang untuk presensi",
                    parse_mode='Markdown'
                )
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "✦ Login Gagal\n"
                "────\n"
                "⟢ Error:\n"
                "    » NIM atau password salah\n"
                "────\n"
                "⟢ Solusi:\n"
                "    » Periksa kembali kredensial Anda\n"
                "    » Pastikan NIM dan password benar\n"
                "    » Gunakan format \"NIM password\"\n"
                "────\n"
                "Kirim /cancel untuk membatalkan",
                parse_mode='Markdown'
            )
            return LOGIN
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        await update.message.reply_text(
            "✦ Terjadi Kesalahan\n"
            "────\n"
            "⟢ Error:\n"
            "    » Gagal melakukan login\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Silakan coba lagi\n"
            "    » Hubungi admin jika masalah berlanjut",
            parse_mode='Markdown'
        )
        return LOGIN

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk membatalkan conversation."""
    await update.message.reply_text(
        "✦ Operasi Dibatalkan\n"
        "────\n"
        "⟢ Status:\n"
        "    » Operasi telah dibatalkan\n"
        "────\n"
        "⟢ Opsi:\n"
        "    » /help - Melihat daftar perintah",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /logout."""
    if not student_api.is_logged_in():
        await update.message.reply_text(
            "✦ Belum Login\n"
            "────\n"
            "⟢ Status:\n"
            "    » Anda belum login\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Gunakan /login terlebih dahulu",
            parse_mode='Markdown'
        )
        return
    
    student_api.logout()
    await update.message.reply_text(
        "✦ Logout Berhasil\n"
        "────\n"
        "⟢ Status:\n"
        "    » Berhasil keluar dari portal\n"
        "────\n"
        "⟢ Opsi:\n"
        "    » /login - Masuk kembali ke portal\n"
        "    » /help - Melihat semua perintah",
        parse_mode='Markdown'
    )

async def absenbang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /absenbang."""
    if not student_api.is_logged_in():
        await update.message.reply_text(
            "✦ Belum Login\n"
            "────\n"
            "⟢ Status:\n"
            "    » Anda belum login\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Gunakan /login terlebih dahulu",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    # Mendapatkan daftar presensi dengan tahun ajaran dan semester yang sesuai
    presence_list = student_api.get_presence_list("2024/2025", "2")  # Tahun ajaran 2024/2025, semester genap (2)
    if not presence_list:
        await update.message.reply_text(
            "✦ Tidak Ada Mata Kuliah\n"
            "────\n"
            "⟢ Penyebab:\n"
            "    » Bukan waktu presensi\n"
            "    » Sesi login telah berakhir\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Coba login kembali dengan /login\n"
            "    » Cek jadwal presensi di portal",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    # Simpan daftar mata kuliah ke context untuk digunakan nanti
    context.user_data['makul_list'] = presence_list
    
    # Format dan tampilkan daftar mata kuliah
    profile = context.user_data.get('profile')
    
    message = "✦ Daftar Presensi\n────\n"
    
    # Tambahkan informasi profil jika tersedia
    if profile:
        message += (
            f"⟢ Mahasiswa:\n"
            f"    » {profile['nama']} ({profile['nim']})\n"
            f"    » {profile['prodi']}\n"
            f"    » IPK: {profile['ipk']} | Total: {profile['total_sks']} SKS\n"
            f"────\n"
        )
    
    message += "⟢ Mata Kuliah:\n"
    
    for idx, makul in enumerate(presence_list, 1):
        message += f"    » {idx}. {makul['nama_makul']} ({makul['kode']})\n"
    
    message += "────\n"
    message += "Kirim nomor mata kuliah untuk presensi atau /cancel untuk batal"
    
    await update.message.reply_text(message, parse_mode='Markdown')
    return PRESENCE

async def handle_presence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk memproses pilihan presensi."""
    try:
        choice = int(update.message.text)
        makul_list = context.user_data.get('makul_list', [])
        
        if not makul_list:
            await update.message.reply_text(
                "✦ Terjadi Kesalahan\n"
                "────\n"
                "⟢ Error:\n"
                "    » Data mata kuliah tidak ditemukan\n"
                "────\n"
                "⟢ Solusi:\n"
                "    » Silakan coba /absenbang lagi",
                parse_mode='Markdown'
            )
            return ConversationHandler.END
            
        if choice < 1 or choice > len(makul_list):
            await update.message.reply_text(
                "✦ Nomor Tidak Valid\n"
                "────\n"
                "⟢ Error:\n"
                "    » Nomor mata kuliah tidak valid\n"
                "────\n"
                "⟢ Solusi:\n"
                "    » Pilih nomor sesuai daftar mata kuliah",
                parse_mode='Markdown'
            )
            return PRESENCE
            
        selected_makul = makul_list[choice - 1]
        if student_api.do_presence("2024/2025", "2", selected_makul['id']):  # Tahun ajaran 2024/2025, semester genap (2)
            await update.message.reply_text(
                f"✦ Presensi Berhasil\n"
                f"────\n"
                f"⟢ Detail:\n"
                f"    » Mata Kuliah: {selected_makul['nama_makul']}\n"
                f"    » Kode: {selected_makul['kode']}\n"
                f"    » Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"────\n"
                f"Presensi telah tercatat di sistem",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "✦ Presensi Gagal\n"
                "────\n"
                "⟢ Error:\n"
                "    » Gagal melakukan presensi\n"
                "────\n"
                "⟢ Solusi:\n"
                "    » Silakan coba lagi\n"
                "    » Hubungi admin jika masalah berlanjut",
                parse_mode='Markdown'
            )
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "✦ Format Salah\n"
            "────\n"
            "⟢ Error:\n"
            "    » Input bukan angka\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Silakan kirim nomor mata kuliah (angka)",
            parse_mode='Markdown'
        )
        return PRESENCE
    except Exception as e:
        logging.error(f"Presence error: {str(e)}")
        await update.message.reply_text(
            "✦ Terjadi Kesalahan\n"
            "────\n"
            "⟢ Error:\n"
            "    » Gagal memproses presensi\n"
            "────\n"
            "⟢ Solusi:\n"
            "    » Silakan coba lagi\n"
            "    » Hubungi admin jika masalah berlanjut",
            parse_mode='Markdown'
        )
        return PRESENCE

def register_handlers(application: Application):
    """Mendaftarkan semua handlers ke aplikasi bot."""
    # Basic handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("logout", logout))
    
    # Login conversation handler
    login_handler = ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(login_handler)
    
    # Presence conversation handler
    presence_handler = ConversationHandler(
        entry_points=[CommandHandler("absenbang", absenbang)],
        states={
            PRESENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_presence)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(presence_handler) 