"""
MAYUGORO XL Telegram Bot - Production Version
Bot Telegram untuk layanan XL dengan interface yang user-friendly
"""

import os
import logging
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes
)

# Load environment variables dari me-cli directory
env_path = os.path.join(os.path.dirname(__file__), 'me-cli', '.env')
load_dotenv(env_path)

# Configure logging - Clean output
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

# Disable verbose logging dari library eksternal
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.ext').setLevel(logging.WARNING)
logging.getLogger('apscheduler').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MayugoroXLBot:
    """
    MAYUGORO XL Telegram Bot
    Bot untuk layanan XL dengan fitur OTP, Admin, dan Pembelian Paket
    """
    
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable not set")
        
        # Path to banner image (banner.jpg ada di direktori yang sama)
        self.banner_path = os.path.join(os.path.dirname(__file__), 'banner.jpg')
        self.banner_file_id = None  # Akan disimpan setelah upload pertama
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler untuk command /start
        Menampilkan pesan pembuka dengan credit developer
        """
        start_message = "🤖 *MAYUGORO XL BOT*\n\n" \
                       "Selamat datang di bot layanan XL!\n" \
                       "Ketik /menu untuk melihat menu utama.\n\n" \
                       "_Develop by @Mayugoro_"
        
        await update.message.reply_text(
            start_message,
            parse_mode='Markdown'
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler untuk command /menu
        Menampilkan menu utama dengan banner.jpg dan 3 inline buttons
        """
        # Create inline keyboard dengan 3 menu utama
        keyboard = [
            [InlineKeyboardButton("🔐 LOGIN OTP", callback_data='login_otp')],
            [InlineKeyboardButton("👤 ADMIN", callback_data='admin'),
             InlineKeyboardButton("🛒 BELI PAKET", callback_data='buy_package')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Caption untuk banner
        caption = """🎯 *MAYUGORO XL BOT - Menu Utama*

*Pilih layanan yang Anda butuhkan:*

🔐 **LOGIN OTP** - Masuk dengan kode OTP
👤 **ADMIN** - Panel administrator  
🛒 **BELI PAKET** - Pembelian paket XL

📱 _Silakan pilih menu di bawah ini_"""
        
        try:
            # Jika banner_file_id sudah ada, gunakan file_id untuk menghindari upload ulang
            if self.banner_file_id:
                await update.message.reply_photo(
                    photo=self.banner_file_id,
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                # Upload banner pertama kali dan simpan file_id
                if os.path.exists(self.banner_path):
                    with open(self.banner_path, 'rb') as banner_file:
                        message = await update.message.reply_photo(
                            photo=banner_file,
                            caption=caption,
                            reply_markup=reply_markup,
                            parse_mode='Markdown'
                        )
                        # Simpan file_id untuk penggunaan selanjutnya
                        self.banner_file_id = message.photo[-1].file_id
                else:
                    # Fallback jika banner tidak ada
                    await update.message.reply_text(
                        f"⚠️ Banner tidak ditemukan di: {self.banner_path}\n\n{caption}",
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
        except Exception as e:
            logger.error(f"Error sending banner: {e}")
            # Fallback ke text message
            await update.message.reply_text(
                caption,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def edit_banner_message(self, query, new_caption: str, new_keyboard: InlineKeyboardMarkup = None) -> None:
        """
        Helper function untuk edit message dengan banner yang persistent
        Mencegah error 400 "message not modified" dengan mempertahankan banner
        """
        try:
            await query.edit_message_caption(
                caption=new_caption,
                reply_markup=new_keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            # Jika edit gagal (misalnya message not modified), coba edit hanya keyboard
            if "not modified" in str(e).lower():
                try:
                    if new_keyboard:
                        await query.edit_message_reply_markup(reply_markup=new_keyboard)
                except Exception:
                    pass  # Ignore jika masih gagal
            else:
                logger.error(f"Error editing banner message: {e}")
    
    def setup_handlers(self, application: Application) -> None:
        """
        Setup semua command handlers
        """
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("menu", self.menu_command))
    
    def run(self):
        """
        Start the MAYUGORO XL Bot
        """
        try:
            # Build application
            application = Application.builder().token(self.bot_token).build()
            
            # Setup handlers
            self.setup_handlers(application)
            
            # Start bot
            print("🚀 MAYUGORO XL Bot starting...")
            
            # Run bot
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except KeyboardInterrupt:
            pass  # Silent exit
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise

def main():
    """
    Main function untuk menjalankan bot
    """
    try:
        bot = MayugoroXLBot()
        bot.run()
    except Exception as e:
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())