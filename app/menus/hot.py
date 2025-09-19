import requests

from app.client.engsel import get_family
from app.client.purchase import show_multipayment, show_qris_payment, show_multipayment_v2, show_qris_payment_v2
from app.service.auth import AuthInstance
from app.menus.util import clear_screen, pause
from app.type_dict import PaymentItem

def get_package_details(api_key, tokens, family_code, variant_name, order, is_enterprise=False):
    """Get package details for a specific variant and order"""
    family_data = get_family(api_key, tokens, family_code, is_enterprise)
    if not family_data:
        return None
    
    package_variants = family_data["package_variants"]
    for variant in package_variants:
        if variant["name"] == variant_name:
            package_options = variant["package_options"]
            for option in package_options:
                if option["order"] == order:
                    # Create package detail structure similar to me-cli
                    return {
                        "package_option": {
                            "package_option_code": option["package_option_code"],
                            "name": option["name"],
                            "price": option["price"]
                        },
                        "token_confirmation": family_data.get("token_confirmation", "")
                    }
    return None

def show_hot_menu():
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    
    in_hot_menu = True
    while in_hot_menu:
        clear_screen()
        print("=======================================================")
        print("====================🔥 Paket  Hot 🔥===================")
        print("=======================================================")
        
        url = "https://me.mashu.lol/pg-hot.json"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print("Gagal mengambil data hot package.")
                pause()
                return None
        except Exception as e:
            print(f"Error mengambil data: {e}")
            pause()
            return None

        hot_packages = response.json()

        for idx, p in enumerate(hot_packages):
            print(f"{idx + 1}. {p['family_name']} - {p['variant_name']} - {p['option_name']}")
            print("-------------------------------------------------------")
        
        print("00. Kembali ke menu utama")
        print("-------------------------------------------------------")
        choice = input("Pilih paket (nomor): ")
        if choice == "00":
            in_hot_menu = False
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(hot_packages):
            selected_package = hot_packages[int(choice) - 1]
            family_code = selected_package["family_code"]
            is_enterprise = selected_package["is_enterprise"]
            variant_name = selected_package["variant_name"]
            order = selected_package["order"]
            
            # Get package details
            package_detail = get_package_details(
                api_key, tokens, family_code, variant_name, order, is_enterprise
            )
            
            if not package_detail:
                print("Gagal mengambil detail paket.")
                pause()
                continue
            
            package_option = package_detail["package_option"]
            token_confirmation = package_detail["token_confirmation"]
            
            # Show package details
            clear_screen()
            print("=======================================================")
            print(f"Family: {selected_package['family_name']}")
            print(f"Variant: {variant_name}")
            print(f"Package: {package_option['name']}")
            print(f"Harga: Rp {package_option['price']}")
            print("=======================================================")
            
            # Payment menu
            while True:
                print("Pilih Metode Pembelian:")
                print("1. E-Wallet")
                print("2. QRIS")
                print("00. Kembali ke menu sebelumnya")
                
                input_method = input("Pilih metode (nomor): ")
                if input_method == "1":
                    show_multipayment(
                        api_key,
                        tokens,
                        package_option["package_option_code"],
                        token_confirmation,
                        package_option["price"],
                        package_option["name"]
                    )
                    input("Tekan enter untuk kembali...")
                    in_hot_menu = False
                    return None
                elif input_method == "2":
                    show_qris_payment(
                        api_key,
                        tokens,
                        package_option["package_option_code"],
                        token_confirmation,
                        package_option["price"],
                        package_option["name"]
                    )
                    input("Tekan enter untuk kembali...")
                    in_hot_menu = False
                    return None
                elif input_method == "00":
                    break
                else:
                    print("Metode tidak valid. Silahkan coba lagi.")
                    pause()
                    continue
            
        else:
            print("Input tidak valid. Silahkan coba lagi.")
            pause()
            continue

def show_hot_menu2():
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    
    in_hot_menu = True
    while in_hot_menu:
        clear_screen()
        print("=======================================================")
        print("===================🔥 Paket  Hot 2 🔥==================")
        print("=======================================================")
        
        url = "https://me.mashu.lol/pg-hot2.json"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print("Gagal mengambil data hot package.")
                pause()
                return None
        except Exception as e:
            print(f"Error mengambil data: {e}")
            pause()
            return None

        hot_packages = response.json()

        for idx, p in enumerate(hot_packages):
            print(f"{idx + 1}. {p['name']}\n   Harga: {p['price']}")
        
        print("00. Kembali ke menu utama")
        print("-------------------------------------------------------")
        choice = input("Pilih paket (nomor): ")
        if choice == "00":
            in_hot_menu = False
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(hot_packages):
            selected_bundle = hot_packages[int(choice) - 1]
            packages = selected_bundle.get("packages", [])
            if len(packages) == 0:
                print("Paket tidak tersedia.")
                pause()
                continue
            
            payment_items = []
            for package in packages:
                package_detail = get_package_details(
                    api_key,
                    tokens,
                    package["family_code"],
                    package["variant_name"],
                    package["order"],
                    package["is_enterprise"],
                )
                
                # Force failed when one of the package detail is None
                if not package_detail:
                    print(f"Gagal mengambil detail paket untuk {package['family_code']}.")
                    return None
                
                payment_items.append(
                    PaymentItem(
                        item_code=package_detail["package_option"]["package_option_code"],
                        product_type="",
                        item_price=package_detail["package_option"]["price"],
                        item_name=package_detail["package_option"]["name"],
                        tax=0,
                        token_confirmation=package_detail["token_confirmation"],
                    )
                )
            
            clear_screen()
            print("=======================================================")
            print(f"Bundle: {selected_bundle['name']}")
            print(f"Harga Total: {selected_bundle['price']}")
            print(f"Detail: {selected_bundle['detail']}")
            print("=======================================================")
            print("Paket dalam bundle:")
            for idx, item in enumerate(payment_items):
                print(f"{idx + 1}. {item['item_name']} - Rp {item['item_price']}")
            print("=======================================================")
            
            in_payment_menu = True
            while in_payment_menu:
                print("Pilih Metode Pembelian:")
                print("1. E-Wallet (Bundle)")
                print("2. QRIS (Bundle)")
                print("00. Kembali ke menu sebelumnya")
                
                input_method = input("Pilih metode (nomor): ")
                if input_method == "1":
                    show_multipayment_v2(
                        api_key,
                        tokens,
                        payment_items
                    )
                    input("Tekan enter untuk kembali...")
                    in_payment_menu = False
                    in_hot_menu = False
                    return None
                elif input_method == "2":
                    show_qris_payment_v2(
                        api_key,
                        tokens,
                        payment_items
                    )
                    input("Tekan enter untuk kembali...")
                    in_payment_menu = False
                    in_hot_menu = False
                    return None
                elif input_method == "00":
                    in_payment_menu = False
                    continue
                else:
                    print("Metode tidak valid. Silahkan coba lagi.")
                    pause()
                    continue
            
        else:
            print("Input tidak valid. Silahkan coba lagi.")
            pause()
            continue