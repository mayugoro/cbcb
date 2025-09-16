from dotenv import load_dotenv

load_dotenv() 

import sys
from app.menus.util import clear_screen, pause
from app.client.engsel import *
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family

def show_popular_packages_menu():
    """Show menu for popular normal packages"""
    packages = [
        ("Special For You", "6fda76ee-e789-4897-89fb-9114da47b805"),
        ("Akrab 2Kb", "340be7a9-9ab8-d23e5-3059-70b81ec984e"),
        ("Bonus Flex Rp.0", "1b42d4f6-a76e-4986-aa5c-e2979da952f4"),
        ("Kuota Bersama Rp 0", "434a1449-1d18-43f8-b059-10b3d5e3f5c3"),
        ("Addon Hotrod/Xcs 8gb", "74eb925a-4a05-4ede-b04b-edd90786419b"),
        ("Xcs Flex Ori", "4a1acab0-da54-462c-84b1-25fd0efa9318"),
        ("EduCoference Ori", "5d63dddd-4f90-4f4c-8438-2f005c20151f"),
        ("Mastif Bundling Setahun", "6bcc96f4-f196-4e8f-969f-e45a121d21bd"),
        ("Paket XL Point", "784be350-9364-4f03-8efa-e7cf31e8baa2"),
        ("Paket Bonus MyRewards", "07461ed8-8a81-4d89-a8f2-4dd0271efdde"),
        ("Addon XCP 2GB", "580c1f94-7dc4-416e-96f6-8faf26567516"),
        ("Addon XCP 15GB", "45c3a622-8c06-4bb1-8e56-bba1f3434600"),
        ("Bebas Puas", "d0a349a7-0b3a-4552-bc1d-3fd9ac0a17ee"),
        ("XCP OLD 10GB", "364d5764-77d3-41b8-9c22-575b555bf9df"),
        ("XCP VIP", "23b71540-8785-4abe-816d-e9b4efa48f95"),
        ("Akrab 2Kb New", "4889cc43-55c9-47dd-8f7e-d3ac9fae6022"),
        ("XCP GIFT", "0895946e-d277-4218-914c-b663c09debf7"),
        ("Addon XCP 1GB", "8080ddcf-18c5-4d6d-86a4-89eb8ca5f2d1"),
        ("Pilkada Damai Kuota", "e3b2c02e-0e2f-4275-a6de-84fb9efab992"),
        ("Bonus Akrab Rp 0", "a677d649-3c5a-46c2-a043-cb69ac841208"),
        ("XC FLEX LENGKAP", "3a6a256f-1524-4dc3-a989-35584f31c265"),
        ("Unli Turbo Xcs/Hotrod", "08a3b1e6-8e78-4e45-a540-b40f06871cfe"),
        ("Addon XCP 6GB", "5412b964-474e-42d3-9c86-f5692da627db"),
        ("Family Hide Addon Prepaid", "31c9605f-1a3a-4410-ae45-362650bb507d"),
        ("SLOT AKRAB 20rb", "86d86765-65a6-4ece-8056-ab2b220429e4"),
        ("Akrab Full Versi", "f4fd69c7-12a4-4047-a1f2-f4072a7c543e"),
        ("Akrab Big", "6e469cb2-443d-402f-ba77-681b032ead6a"),
        ("Booster Akrab", "5452eed8-91f3-4e9c-b7bb-0985759d5440"),
        ("Addon Akrab", "c5dbcb2d-31cc-462c-afe8-b3a767c6d404"),
        ("XCS 8GB & 14GB", "3e6d45f1-f314-4acd-a75b-be40c0726198"),
        ("New Comer XCS 2GB & 4GB", "6bc5a34d-7901-4bf9-8629-5bd7de28c89f"),
        ("XC FLEX LENGKAP V2", "3c71892a-852c-4a0f-8cb5-9cf731e26508"),
        ("Paket Harian Rp 0", "96d99f87-8963-40e4-a522-8bea86504fee"),
        ("Paket Youtube Bonus", "1fe292a5-5fef-430e-917b-e0eaeeb89f93"),
        ("Pengguna Baru 100mb", "ccb162e6-b7cf-4162-8e3f-662e67cbb4cb")
    ]
    
    while True:
        clear_screen()
        print("--------------------------")
        print("Paket Populer (Normal)")
        print("--------------------------")
        for i, (name, code) in enumerate(packages, 1):
            print(f"{i:2}. {name}")
        print("99. Kembali ke menu utama")
        print("--------------------------")
        
        choice = input(f"Pilih paket (1-{len(packages)} atau 99): ")
        if choice == "99":
            break
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(packages):
                name, family_code = packages[choice_idx]
                print(f"Loading {name}...")
                get_packages_by_family(family_code)
            else:
                print("Pilihan tidak valid!")
                pause()
        except ValueError:
            print("Masukkan angka yang valid!")
            pause()

def show_enterprise_packages_menu():
    """Show menu for enterprise packages"""
    packages = [
        ("Biz Starter Unli", "20342db0-e03e-4dfd-b2d0-cd315d7ddc36"),
        ("Biz Data+", "53de8ac3-521d-43f5-98ce-749ad0481709"),
        ("EduCoference Rp 10", "fcf982c8-523b-4748-9258-5fca2c0b703d"),
        ("Xtra Combo Flex - SP", "3e6d45f1-f314-4acd-a75b-be40c0726198")
    ]
    
    while True:
        clear_screen()
        print("--------------------------")
        print("Paket Enterprise")
        print("--------------------------")
        for i, (name, code) in enumerate(packages, 1):
            print(f"{i}. {name}")
        print("99. Kembali ke menu utama")
        print("--------------------------")
        
        choice = input(f"Pilih paket (1-{len(packages)} atau 99): ")
        if choice == "99":
            break
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(packages):
                name, family_code = packages[choice_idx]
                print(f"Loading {name}...")
                get_packages_by_family(family_code, is_enterprise=True)
            else:
                print("Pilihan tidak valid!")
                pause()
        except ValueError:
            print("Masukkan angka yang valid!")
            pause()

def show_main_menu(number, balance, balance_expired_at):
    clear_screen()
    phone_number = number
    remaining_balance = balance
    expired_at = balance_expired_at
    expired_at_dt = datetime.fromtimestamp(expired_at).strftime("%Y-%m-%d %H:%M:%S")
    
    print()
    print("    QQQQ      QQQ   QQQQ  QQ   Q  QQQQQQQ QQQQ  QQ")
    print("  QQQQQQQQ    QQQQ  QQQQ  QQQQQQ  QQQ     QQQQ  QQ")
    print(" QQQQQQQQQQ   QQQQ QQQQQ   QQQQ   QQQQQQ  QQ QQ QQ")
    print("QQQQQQQQQQQQ  QQ QQQQ QQ    QQ    QQQ     QQ  QQQQ")
    print("QQQQQQQQQQQQ  QQ QQQQ QQ    QQ    QQQ     QQ   QQQ")
    print(" QQQQQQQQQQ   QQ QQQ  QQ    QQ    QQQQQQQ QQ   QQQ")
    print("     QQ")
    print("--------------------------")
    print("Informasi Akun")
    print(f"Nomor: {phone_number}")
    print(f"Pulsa: Rp {remaining_balance}")
    print(f"Masa aktif: {expired_at_dt}")
    print("--------------------------")
    print("PAKET TERSEDIA:")
    
    # All packages in main menu
    packages = [
        ("Addon Akrab", "c5dbcb2d-31cc-462c-afe8-b3a767c6d404"),
        ("Addon Hotrod/Xcs 8gb", "74eb925a-4a05-4ede-b04b-edd90786419b"),
        ("Addon XCP 1GB", "8080ddcf-18c5-4d6d-86a4-89eb8ca5f2d1"),
        ("Addon XCP 2GB", "580c1f94-7dc4-416e-96f6-8faf26567516"),
        ("Addon XCP 6GB", "5412b964-474e-42d3-9c86-f5692da627db"),
        ("Addon XCP 15GB", "45c3a622-8c06-4bb1-8e56-bba1f3434600"),
        ("Akrab 2Kb", "340be7a9-9ab8-d23e5-3059-70b81ec984e"),
        ("Akrab 2Kb New", "4889cc43-55c9-47dd-8f7e-d3ac9fae6022"),
        ("Akrab Big", "6e469cb2-443d-402f-ba77-681b032ead6a"),
        ("Akrab Full Versi", "f4fd69c7-12a4-4047-a1f2-f4072a7c543e"),
        ("Bebas Puas", "d0a349a7-0b3a-4552-bc1d-3fd9ac0a17ee"),
        ("Beli Paket XUT", "08a3b1e6-8e78-4e45-a540-b40f06871cfe"),
        ("Biz Data+", "53de8ac3-521d-43f5-98ce-749ad0481709"),
        ("Biz Starter Unli", "20342db0-e03e-4dfd-b2d0-cd315d7ddc36"),
        ("Bonus Akrab Rp 0", "a677d649-3c5a-46c2-a043-cb69ac841208"),
        ("Bonus Flex Rp.0", "1b42d4f6-a76e-4986-aa5c-e2979da952f4"),
        ("Booster Akrab", "5452eed8-91f3-4e9c-b7bb-0985759d5440"),
        ("EduCoference Ori", "5d63dddd-4f90-4f4c-8438-2f005c20151f"),
        ("EduCoference Rp 10", "fcf982c8-523b-4748-9258-5fca2c0b703d"),
        ("Family Hide Addon Prepaid", "31c9605f-1a3a-4410-ae45-362650bb507d"),
        ("Kuota Bersama Rp 0", "434a1449-1d18-43f8-b059-10b3d5e3f5c3"),
        ("Mastif Bundling Setahun", "6bcc96f4-f196-4e8f-969f-e45a121d21bd"),
        ("New Comer XCS 2GB & 4GB", "6bc5a34d-7901-4bf9-8629-5bd7de28c89f"),
        ("Paket Bonus MyRewards", "07461ed8-8a81-4d89-a8f2-4dd0271efdde"),
        ("Paket Harian Rp 0", "96d99f87-8963-40e4-a522-8bea86504fee"),
        ("Paket XL Point", "784be350-9364-4f03-8efa-e7cf31e8baa2"),
        ("Paket Youtube Bonus", "1fe292a5-5fef-430e-917b-e0eaeeb89f93"),
        ("Pengguna Baru 100mb", "ccb162e6-b7cf-4162-8e3f-662e67cbb4cb"),
        ("Pilkada Damai Kuota", "e3b2c02e-0e2f-4275-a6de-84fb9efab992"),
        ("SLOT AKRAB 20rb", "86d86765-65a6-4ece-8056-ab2b220429e4"),
        ("Spesial For You", "6fda76ee-e789-4897-89fb-9114da47b805"),
        ("Unli Turbo Xcs/Hotrod", "08a3b1e6-8e78-4e45-a540-b40f06871cfe"),
        ("XC FLEX LENGKAP", "3a6a256f-1524-4dc3-a989-35584f31c265"),
        ("XC FLEX LENGKAP V2", "3c71892a-852c-4a0f-8cb5-9cf731e26508"),
        ("XCP GIFT", "0895946e-d277-4218-914c-b663c09debf7"),
        ("XCP OLD 10GB", "364d5764-77d3-41b8-9c22-575b555bf9df"),
        ("XCP VIP", "23b71540-8785-4abe-816d-e9b4efa48f95"),
        ("XCS 8GB & 14GB", "3e6d45f1-f314-4acd-a75b-be40c0726198"),
        ("Xcs Flex Ori", "4a1acab0-da54-462c-84b1-25fd0efa9318")
    ]
    
    for i, (name, code) in enumerate(packages, 1):
        print(f"{i:2}. {name}")
    
    print("--------------------------")
    print("MENU LAINNYA:")
    print("90. Login/Ganti akun")
    print("91. Lihat Paket Saya")
    print("92. Beli Paket Berdasarkan Family Code")
    print("93. Beli Paket Berdasarkan Family Code (Enterprise)")
    print("94. Bookmark Paket")
    print("99. Tutup aplikasi")
    print("--------------------------")
    
    return packages

show_menu = True
def main():
    
    while True:
        active_user = AuthInstance.get_active_user()

        # Logged in
        if active_user is not None:
            balance = get_balance(AuthInstance.api_key, active_user["tokens"]["id_token"])
            if balance is not None:
                balance_remaining = balance.get("remaining")
                balance_expired_at = balance.get("expired_at")
            else:
                # Default values when balance fetch fails
                balance_remaining = "Unknown"
                balance_expired_at = "Unknown"

            packages = show_main_menu(active_user["number"], balance_remaining, balance_expired_at)

            choice = input("Pilih menu: ")
            
            # Handle package selection (1-35)
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(packages):
                    name, family_code = packages[choice_num - 1]
                    print(f"Loading {name}...")
                    get_packages_by_family(family_code)
                    continue
            except ValueError:
                pass
            
            # Handle other menu options
            if choice == "90":
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print("No user selected or failed to load user.")
                continue
            elif choice == "91":
                fetch_my_packages()
                continue
            elif choice == "92":
                print("\n📋 Contoh family code yang valid:")
                print("   • c5dbcb2d-31cc-462c-afe8-b3a767c6d404 (Addon Akrab)")
                print("   • d0a349a7-0b3a-4552-bc1d-3fd9ac0a17ee (Bebas Puas)")
                print("   • 6e469cb2-443d-402f-ba77-681b032ead6a (Akrab Big)")
                print("💡 Tip: Gunakan menu utama (1-39) untuk paket yang sudah tersedia\n")
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                get_packages_by_family(family_code)
            elif choice == "93":
                print("\n📋 Contoh family code yang valid:")
                print("   • c5dbcb2d-31cc-462c-afe8-b3a767c6d404 (Addon Akrab)")
                print("   • d0a349a7-0b3a-4552-bc1d-3fd9ac0a17ee (Bebas Puas)")
                print("   • 6e469cb2-443d-402f-ba77-681b032ead6a (Akrab Big)")
                print("💡 Tip: Gunakan menu utama (1-39) untuk paket yang sudah tersedia\n")
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                get_packages_by_family(family_code, is_enterprise=True)
            elif choice == "94":
                show_bookmark_menu()
            elif choice == "99":
                print("Exiting the application.")
                sys.exit(0)
            elif choice == "9":
                # Playground
                pass
                # data = get_package(
                #     AuthInstance.api_key,
                #     active_user["tokens"],
                #     "U0NfX8A08oQLUQuLplGhfT_FXQokJ9GFF9kAKRiV5trm6BfbRoxrsizKkWIVNxM0az6lroT92FYXnWmTXRXZOl1Meg",
                #     ""
                #     ""
                #     )
                # print(json.dumps(data, indent=2))
                # pause()
            else:
                print("Invalid choice. Please try again.")
                pause()
        else:
            # Not logged in
            selected_user_number = show_account_menu()
            if selected_user_number:
                AuthInstance.set_active_user(selected_user_number)
            else:
                print("No user selected or failed to load user.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the application.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
