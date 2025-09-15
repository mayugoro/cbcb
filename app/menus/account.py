from app.client.engsel import get_otp, submit_otp
from app.menus.util import clear_screen, pause
from app.service.auth import AuthInstance

def normalize_phone_number(phone_number: str) -> str:
    """
    Normalize phone number to 628 format
    Converts various formats to standard 628XXXXXXXXX format
    """
    # Remove all non-digit characters
    phone_number = ''.join(filter(str.isdigit, phone_number))
    
    # Handle different starting patterns
    if phone_number.startswith('628'):
        # Already in correct format
        return phone_number
    elif phone_number.startswith('08'):
        # Convert 08XXXXXXXXX to 628XXXXXXXXX
        return '628' + phone_number[2:]
    elif phone_number.startswith('8'):
        # Convert 8XXXXXXXXX to 628XXXXXXXXX
        return '628' + phone_number[1:]
    elif phone_number.startswith('628'):
        # Already correct
        return phone_number
    elif phone_number.startswith('62'):
        # Handle 62XXXXXXXXX (missing 8)
        if len(phone_number) >= 3 and phone_number[2] == '8':
            return phone_number
        else:
            return '628' + phone_number[2:]
    else:
        # Default: assume it's local number, add 628
        return '628' + phone_number

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate if phone number is valid after normalization
    """
    normalized = normalize_phone_number(phone_number)
    
    # Check if starts with 628
    if not normalized.startswith('628'):
        return False
    
    # Check length (628 + 8-11 digits = 11-14 total)
    if len(normalized) < 11 or len(normalized) > 14:
        return False
    
    # Check if all characters are digits
    if not normalized.isdigit():
        return False
    
    return True

def show_login_menu():
    clear_screen()
    print("--------------------------")
    print("Login ke MyXL")
    print("--------------------------")
    print("1. Request OTP")
    print("2. Submit OTP")
    print("99. Tutup aplikasi")
    print("--------------------------")
    
def login_prompt(api_key: str):
    clear_screen()
    print("--------------------------")
    print("Login ke MyXL")
    print("--------------------------")
    print("Masukan nomor XL Prabayar:")
    print("Format yang didukung:")
    print("  • 6281234567890")
    print("  • 081234567890") 
    print("  • 81234567890")
    print("--------------------------")
    phone_number = input("Nomor: ")

    # Normalize phone number
    normalized_number = normalize_phone_number(phone_number)
    
    # Validate normalized number
    if not validate_phone_number(phone_number):
        print(f"❌ Nomor tidak valid: {phone_number}")
        print(f"📱 Format yang dinormalisasi: {normalized_number}")
        print("💡 Pastikan nomor XL yang valid (8-11 digit setelah 628)")
        print("\nContoh format yang benar:")
        print("  • 085946492065 → 6285946492065")
        print("  • 6285946492065 → 6285946492065")
        pause()
        return None

    # Show conversion if different
    if phone_number != normalized_number:
        print(f"📱 Nomor dikonversi: {phone_number} → {normalized_number}")

    try:
        print(f"🔄 Mengirim OTP ke nomor: {normalized_number}")
        subscriber_id = get_otp(normalized_number)
        if not subscriber_id:
            print("❌ Gagal mengirim OTP. Periksa nomor dan coba lagi.")
            pause()
            return None
            
        print("✅ OTP Berhasil dikirim ke nomor Anda.")
        
        otp = input("Masukkan OTP yang telah dikirim: ")
        if not otp.isdigit() or len(otp) != 6:
            print("❌ OTP tidak valid. Pastikan OTP terdiri dari 6 digit angka.")
            pause()
            return None
        
        tokens = submit_otp(api_key, normalized_number, otp)
        if not tokens:
            print("❌ Gagal login. Periksa OTP dan coba lagi.")
            pause()
            return None
        
        print("✅ Berhasil login!")
        
        return normalized_number, tokens["refresh_token"]
    except Exception as e:
        print(f"❌ Error during login: {str(e)}")
        print("💡 Coba lagi dengan nomor yang berbeda atau periksa koneksi internet.")
        pause()
        return None, None

def show_account_menu():
    clear_screen()
    AuthInstance.load_tokens()
    users = AuthInstance.refresh_tokens
    active_user = AuthInstance.get_active_user()
    
    # print(f"users: {users}")
    
    in_account_menu = True
    add_user = False
    while in_account_menu:
        clear_screen()
        print("--------------------------")
        if AuthInstance.get_active_user() is None or add_user:
            number, refresh_token = login_prompt(AuthInstance.api_key)
            if not refresh_token:
                print("Gagal menambah akun. Silahkan coba lagi.")
                pause()
                continue
            
            AuthInstance.add_refresh_token(int(number), refresh_token)
            AuthInstance.load_tokens()
            users = AuthInstance.refresh_tokens
            active_user = AuthInstance.get_active_user()
            
            
            if add_user:
                add_user = False
            continue
        
        print("Akun Tersimpan:")
        if not users or len(users) == 0:
            print("Tidak ada akun tersimpan.")

        for idx, user in enumerate(users):
            is_active = active_user and user["number"] == active_user["number"]
            active_marker = " (Aktif)" if is_active else ""
            print(f"{idx + 1}. {user['number']}{active_marker}")
        
        print("Command:")
        print("0: Tambah Akun")
        print("00: Kembali ke menu utama")
        print("99: Hapus Akun aktif")
        print("Masukan nomor akun untuk berganti.")
        input_str = input("Pilihan:")
        if input_str == "00":
            in_account_menu = False
            return active_user["number"] if active_user else None
        elif input_str == "0":
            add_user = True
            continue
        elif input_str == "99":
            if not active_user:
                print("Tidak ada akun aktif untuk dihapus.")
                pause()
                continue
            confirm = input(f"Yakin ingin menghapus akun {active_user['number']}? (y/n): ")
            if confirm.lower() == 'y':
                AuthInstance.remove_refresh_token(active_user["number"])
                # AuthInstance.load_tokens()
                users = AuthInstance.refresh_tokens
                active_user = AuthInstance.get_active_user()
                print("Akun berhasil dihapus.")
                pause()
            else:
                print("Penghapusan akun dibatalkan.")
                pause()
            continue
        elif input_str.isdigit() and 1 <= int(input_str) <= len(users):
            selected_user = users[int(input_str) - 1]
            return selected_user['number']
        else:
            print("Input tidak valid. Silahkan coba lagi.")
            pause()
            continue