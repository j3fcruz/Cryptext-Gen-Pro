# core/qr_handler.py
"""QR code generation and scanning operations"""
import qrcode
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QBuffer as QtBuffer, QIODevice, QByteArray
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
from io import BytesIO
import cv2
from pyzbar.pyzbar import decode
from app_config.app_config import (
    QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE,
    QR_BORDER, QR_LOGO_RATIO
)


class QRHandler:
    """Handles QR code generation and scanning"""

    def generate(self, data, logo_path=None):
        """Generate QR code with optional logo"""
        if not data.strip():
            return None

        qr = qrcode.QRCode(
            version=QR_VERSION,
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{QR_ERROR_CORRECTION}"),
            box_size=QR_BOX_SIZE,
            border=QR_BORDER,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo_path:
            qr_img = self._embed_logo(qr_img, logo_path)

        return qr_img

    def _embed_logo(self, qr_img, logo_path):
        """Embed logo in center of QR code"""
        try:
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                return qr_img

            qimage = pixmap.toImage()
            buffer = QtBuffer()
            buffer.open(QIODevice.ReadWrite)
            qimage.save(buffer, "PNG")
            image_bytes = buffer.data()
            buffer.close()

            pil_logo = Image.open(BytesIO(image_bytes)).convert("RGBA")

            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * QR_LOGO_RATIO)
            pil_logo = pil_logo.resize((logo_size, logo_size), Image.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(pil_logo, pos, mask=pil_logo)
        except Exception:
            pass  # Return QR without logo on error

        return qr_img

    def to_pixmap(self, qr_img, size):
        """Convert QR image to QPixmap"""
        if not qr_img:
            return None

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        return pixmap.scaled(size, size)

    def scan_from_camera(self, camera_index=0):
        """Scan QR from camera"""
        cap = cv2.VideoCapture(camera_index)
        decoded_text = None

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                decoded_objects = decode(frame)
                for obj in decoded_objects:
                    decoded_text = obj.data.decode('utf-8')
                    x, y, w, h = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "QR Detected", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    break

                cv2.imshow("QR Scanner (Press Q to cancel)", frame)

                if decoded_text or cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        return decoded_text

    def scan_from_file(self, filename):
        """Scan QR from image file"""
        # Try OpenCV first
        image = cv2.imread(filename)
        if image is not None:
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(image)
            if data:
                return data

        # Fallback to pyzbar
        try:
            img = Image.open(filename)
            decoded_objects = decode(img)
            if decoded_objects:
                return decoded_objects[0].data.decode("utf-8")
        except Exception:
            pass

        return None