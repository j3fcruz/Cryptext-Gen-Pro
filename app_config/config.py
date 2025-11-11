# config.py

# Constant
APP_NAME = "Cryptext Gen Pro"
APP_VERSION = "1.0.0"
APP_LABEL = "Next-Gen Password Generation – Secured by Design."
APPLY_THEME = ":/assets/themes/stylesheet.qss"
LOGO_PATH = ":/assets/logo/logo.png"
WINDOW_TITLE = f"{APP_NAME}-{APP_LABEL}"
MAYA_QR = ":/assets/resources/maya_qr.bin"
ICON_PATH = ":/assets/icons/icon.png"

PAYLOAD1 = "gAAAAABodcOWwOqk8rSj5mf1-U1Cpw4A0W0xSDkXwEWg7gZcpJrYpocbG4Eezz4EOoDkrQEcneLZKHbaoI7TJLZ7ahkBGkBQBQCA14"
PAYLOAD2 ="vHflTzmA7OCBM1HKbf_3HH9yAboqhfs793OpkoNpdt-ydrb14udAdkH8g6ekZMLszfku1iYaQmdmBszepGihSzxof6W-JUvbz1F0no3R"
PAYLOAD3 ="byDSF_4SYp_w8nSj1QyVEPCGq_isFIrzqbW7hpRxlNtSrh0SJNygBK1aN_0ow3YxX8W30AJJ8tWPZ9WcBldddfl1M8xr44VEsKOQRukqU="
new_payload = f"{PAYLOAD1}{PAYLOAD2}{PAYLOAD3}" # Concatenate the three parts
payload = new_payload.encode() # Encode into bytes for consistency
ENCRYPTED_PAYLOAD = payload # For production

QR_KEY1 = "KqTen1MmkOycHJ"
QR_KEY2 = "p5HqBkcaCWZ7Be"
QR_KEY3 = "8p-ClzSf9srKm3c="
new_qr_key = f"{QR_KEY1}{QR_KEY2}{QR_KEY3}" # Concatenate the three qr key parts (1-3)
qr_key = new_qr_key.encode() # Encode into bytes
MAYA_QR_KEY = qr_key # For production

MAYA_QR_FILE = ":/assets/resources/maya_qr.bin"

    
if __name__ == "__main__":
    
    ENCRYPTED_PAYLOAD = b"gAAAAABodcOWwOqk8rSj5mf1-U1Cpw4A0W0xSDkXwEWg7gZcpJrYpocbG4Eezz4EOoDkrQEcneLZKHbaoI7TJLZ7ahkBGkBQBQCA14vHflTzmA7OCBM1HKbf_3HH9yAboqhfs793OpkoNpdt-ydrb14udAdkH8g6ekZMLszfku1iYaQmdmBszepGihSzxof6W-JUvbz1F0no3RbyDSF_4SYp_w8nSj1QyVEPCGq_isFIrzqbW7hpRxlNtSrh0SJNygBK1aN_0ow3YxX8W30AJJ8tWPZ9WcBldddfl1M8xr44VEsKOQRukqU="
    enc_payload = ENCRYPTED_PAYLOAD
    
    print(f"Encrypted Payload (bytes): {enc_payload}")
    print(f"New Payload (bytes): {payload}")

    # Verification
    if payload == enc_payload:
        print("✅ Verification passed: Concatenated payload matches ENCRYPTED_PAYLOAD")
    else:
        print("❌ Verification failed: Payloads do not match")
        
    print(f"")

    MAYA_QR_KEY = b"KqTen1MmkOycHJp5HqBkcaCWZ7Be8p-ClzSf9srKm3c=" # Securely load in real apps
    new_maya_qr_key = MAYA_QR_KEY
    
    print(f"New Maya QR Key (bytes): {new_maya_qr_key}")
    print(f"New QR Key (bytes): {qr_key}")
    
        # Verification
    if qr_key == new_maya_qr_key:
        print("✅ Verification passed: Concatenated qr key matches MAYA_QR_KEY")
    else:
        print("❌ Verification failed: QR Key do not match")
        
