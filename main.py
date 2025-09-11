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
        ("XCP VIP", "23b71540-8785-4abe-816d-e9b4efa48f95")
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
        
        choice = input("Pilih paket (1-15 atau 99): ")
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
        ("EduCoference Rp 0", "fcf982c8-523b-4748-9258-5fca2c0b703d")
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
        
        choice = input("Pilih paket (1-2 atau 99): ")
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
    
    print("--------------------------")
    print("Informasi Akun")
    print(f"Nomor: {phone_number}")
    print(f"Pulsa: Rp {remaining_balance}")
    print(f"Masa aktif: {expired_at_dt}")
    print("--------------------------")
    print("Menu:")
    print("1. Login/Ganti akun")
    print("2. Lihat Paket Saya")
    print("3. Beli Paket XUT")
    print("4. Paket Populer (Normal)")
    print("5. Paket Enterprise")
    print("6. Beli Paket Berdasarkan Family Code")
    print("7. Beli Paket Berdasarkan Family Code (Enterprise)")
    print("00. Bookmark Paket")
    print("99. Tutup aplikasi")
    print("--------------------------")

show_menu = True
def main():
    
    while True:
        active_user = AuthInstance.get_active_user()

        # Logged in
        if active_user is not None:
            balance = get_balance(AuthInstance.api_key, active_user["tokens"]["id_token"])
            balance_remaining = balance.get("remaining")
            balance_expired_at = balance.get("expired_at")

            show_main_menu(active_user["number"], balance_remaining, balance_expired_at)

            choice = input("Pilih menu: ")
            if choice == "1":
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print("No user selected or failed to load user.")
                continue
            elif choice == "2":
                fetch_my_packages()
                continue
            elif choice == "3":
                # XUT 
                get_packages_by_family("08a3b1e6-8e78-4e45-a540-b40f06871cfe")
            elif choice == "4":
                show_popular_packages_menu()
            elif choice == "5":
                show_enterprise_packages_menu()
            elif choice == "6":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                get_packages_by_family(family_code)
            elif choice == "7":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                get_packages_by_family(family_code, is_enterprise=True)
            elif choice == "00":
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
        