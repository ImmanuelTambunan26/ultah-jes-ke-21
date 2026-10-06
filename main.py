import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# Filter resample fleksibel untuk semua versi Pillow
RESAMPLE = getattr(Image, 'Resampling', Image).LANCZOS

class BirthdayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Special 21st Birthday for Jes (Tata-chan) ✨")
        
        # Pengaturan jendela aplikasi
        self.w, self.h = 1000, 650
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        pos_x = (screen_w - self.w) // 2
        pos_y = (screen_h - self.h) // 2
        self.root.geometry(f"{self.w}x{self.h}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#0c0e17")

        # Canvas Utama
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg="#0c0e17", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Konten 5 Babak: Ucapan & Rangkaian Doa Terbaik buat Tata
        self.slides = [
            {
                "img": os.path.join("asset", "foto1.png"),
                "chapter": "CHAPTER 01 • SPARKLE AT 21",
                "title": "Selamat Ulang Tahun, Tata! ✨",
                "text": (
                    "Tanjoubi omedetou, Tata-chan! 🥳🎂\n\n"
                    "Selamat bertambah usia yang ke-21 ya sayang. "
                    "Bersyukur banget Tuhan menghadirkan kamu ke dunia ini untuk membawa tawa, "
                    "warna baru, dan sukacita besar bagi keluarga dan orang-orang di sekitarmu.\n\n"
                    "Terima kasih sudah tumbuh jadi sosok yang luar biasa sampai hari ini!"
                )
            },
            {
                "img": os.path.join("asset", "foto2.png"),
                "chapter": "CHAPTER 02 • DOA UNTUK LANGKAHMU",
                "title": "Hati yang Selalu Bersandar pada Tuhan 🙏",
                "text": (
                    "Doaku yang paling tulus buat langkah Tata ke depan:\n\n"
                    "• Selalu andalkan Tuhan dan tetap takut akan Tuhan di setiap rencana hidupmu.\n"
                    "• Tumbuh jadi pribadi yang makin dewasa, bijaksana, dan tangguh menghadapi dunia.\n"
                    "• Dikelilingi selalu oleh orang-orang baik yang tulus sayang sama kamu.\n\n"
                    "Tetap jadi anak baik yang hatinya tulus ya has, apa pun situasinya."
                )
            },
            {
                "img": os.path.join("asset", "foto3.png"),
                "chapter": "CHAPTER 03 • MASA DEPAN & KULIAH",
                "title": "Lancar Kuliah & Wisuda Bareng! 🎓",
                "text": (
                    "Semangat terus buat setiap perjuangan dan tugas kuliahmu!\n\n"
                    "Doaku biar setiap proses akademikmu dimudahkan: lancar di darat, laut, udara, "
                    "dan dijauhkan dari rasa jenuh yang bikin down.\n\n"
                    "Semoga Tuhan buka jalan selebar-lebarnya buat cita-citamu, dan semoga nanti "
                    "kita bisa sama-sama pakai toga wisuda ya sayang!"
                )
            },
            {
                "img": os.path.join("asset", "foto4.png"),
                "chapter": "CHAPTER 04 • KITA & PROSES BERSAMA",
                "title": "Saling Menjaga & Tumbuh Berdua 🤍",
                "text": (
                    "Di umur baru ini, semoga hatimu selalu dipenuhi rasa tenang dan bahagia.\n\n"
                    "Semoga kita berdua bisa terus saling mengerti, saling dukung di tengah kesibukan masing-masing, "
                    "dan terus berproses jadi versi terbaik bersama-sama.\n\n"
                    "Kalau harimu lagi berat, jangan dipendam sendiri ya has. Cerita ke aku, aku selalu ada di sini."
                )
            },
            {
                "img": os.path.join("asset", "foto5.png"),
                "chapter": "CHAPTER 05 • DARI HATI TERDALAM",
                "title": "Daisuki da yo, Tata-chan! 🌷",
                "text": (
                    "Sekali lagi, Happy 21st Birthday, Tata tersayang! 🎉✨\n\n"
                    "Semoga berkat, kesehatan, dan sukacita dari Tuhan Yesus selalu melimpah ruah "
                    "dalam setiap detak kehidupanmu.\n\n"
                    "Aku sayang banget sama kamu. Bahagia terus ya Tataku!\n"
                    "God bless you always and forever. ❤️"
                )
            }
        ]
        
        self.current_slide = 0
        self.is_typing = False
        self.full_text = ""
        self.typed_index = 0
        self.photo_cache = None

        # Sistem Partikel Melayang di Background
        self.particles = []
        for _ in range(35):
            self.particles.append({
                "x": random.randint(0, self.w),
                "y": random.randint(0, self.h),
                "speed": random.uniform(1.0, 2.5),
                "size": random.randint(12, 22),
                "symbol": random.choice(["♥", "♡", "✨", "✦", "🌸"]),
                "color": random.choice(["#ff4d6d", "#ff758f", "#ffb3c1", "#c77dff", "#f72585", "#ffd166"])
            })

        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<space>", self.on_click)

        self.animate_particles()
        self.render_slide(0)

    def animate_particles(self):
        """Membuat efek partikel hati & bintang melayang ke atas"""
        self.canvas.delete("particle")
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < -20:
                p["y"] = self.h + 20
                p["x"] = random.randint(0, self.w)
            
            self.canvas.create_text(
                p["x"], p["y"],
                text=p["symbol"],
                font=("Arial", p["size"]),
                fill=p["color"],
                tags="particle"
            )
        self.canvas.tag_lower("particle")
        self.root.after(35, self.animate_particles)

    def load_photo(self, filename):
        """Memuat foto dengan frame Polaroid otomatis"""
        target_w, target_h = 360, 480
        if os.path.exists(filename):
            try:
                img = Image.open(filename)
                w_orig, h_orig = img.size
                ratio = min(target_w / w_orig, target_h / h_orig)
                new_w = int(w_orig * ratio)
                new_h = int(h_orig * ratio)
                img = img.resize((new_w, new_h), RESAMPLE)
                return ImageTk.PhotoImage(img)
            except Exception:
                pass
        return None

    def render_slide(self, index):
        self.current_slide = index
        self.canvas.delete("ui_content")
        slide = self.slides[index]

        # 1. Bingkai Foto Kiri
        frame_x1, frame_y1 = 60, 65
        frame_x2, frame_y2 = 450, 565
        
        # Bayangan frame
        self.canvas.create_rectangle(frame_x1 + 6, frame_y1 + 6, frame_x2 + 6, frame_y2 + 6, fill="#05060a", outline="", tags="ui_content")
        # Kartu foto putih polaroid
        self.canvas.create_rectangle(frame_x1, frame_y1, frame_x2, frame_y2, fill="#ffffff", outline="#ff758f", width=2, tags="ui_content")

        # Load dan letakkan foto
        self.photo_cache = self.load_photo(slide["img"])
        if self.photo_cache:
            self.canvas.create_image(
                (frame_x1 + frame_x2) // 2,
                (frame_y1 + frame_y2 - 25) // 2,
                image=self.photo_cache,
                tags="ui_content"
            )
            self.canvas.create_text(
                (frame_x1 + frame_x2) // 2,
                frame_y2 - 22,
                text="♥ Jes • 21st Birthday ♥",
                font=("Courier", 11, "bold"),
                fill="#333333",
                tags="ui_content"
            )
        else:
            self.canvas.create_text(
                (frame_x1 + frame_x2) // 2,
                (frame_y1 + frame_y2) // 2,
                text=f"[{slide['img']}]\nSimpan foto di folder ini",
                font=("Courier", 12),
                fill="#888888",
                justify="center",
                tags="ui_content"
            )

        # 2. Kotak Teks Sisi Kanan
        text_x1, text_y1 = 485, 65
        text_x2, text_y2 = 940, 565
        # Kartu pesan semi-transparan elegan
        self.canvas.create_rectangle(text_x1, text_y1, text_x2, text_y2, fill="#16192b", outline="#2b314e", width=1, tags="ui_content")

        # Tag Babak
        self.canvas.create_text(
            text_x1 + 30, text_y1 + 35,
            text=slide["chapter"],
            font=("Courier", 10, "bold"),
            fill="#ff758f",
            anchor="w",
            tags="ui_content"
        )

        # Judul Babak
        self.canvas.create_text(
            text_x1 + 30, text_y1 + 68,
            text=slide["title"],
            font=("Georgia", 16, "bold"),
            fill="#ffffff",
            anchor="w",
            tags="ui_content"
        )

        # Garis Pembatas Aksen
        self.canvas.create_line(text_x1 + 30, text_y1 + 95, text_x2 - 30, text_y1 + 95, fill="#ff4d6d", width=2, tags="ui_content")

        # Teks Pesan (Animasi Ketik)
        self.text_display_id = self.canvas.create_text(
            text_x1 + 30, text_y1 + 120,
            text="",
            font=("Georgia", 11),
            fill="#e2e8f0",
            anchor="nw",
            width=395,
            tags="ui_content"
        )

        # Bar Navigasi Bawah
        progress_str = "● " * (index + 1) + "○ " * (len(self.slides) - index - 1)
        self.canvas.create_text(
            text_x1 + 30, text_y2 - 30,
            text=f"Babak {index + 1} dari 5  [{progress_str.strip()}]",
            font=("Courier", 10),
            fill="#8b949e",
            anchor="w",
            tags="ui_content"
        )

        self.canvas.create_text(
            text_x2 - 30, text_y2 - 30,
            text="[ Klik untuk Lanjut ▶ ]",
            font=("Courier", 10, "bold"),
            fill="#ffd166",
            anchor="e",
            tags="ui_content"
        )

        # Mulai animasi ketik
        self.full_text = slide["text"]
        self.typed_index = 0
        self.is_typing = True
        self.typewriter_tick()

    def typewriter_tick(self):
        if not self.is_typing:
            return
        if self.typed_index <= len(self.full_text):
            current_str = self.full_text[:self.typed_index]
            self.canvas.itemconfig(self.text_display_id, text=current_str)
            self.typed_index += 1
            self.root.after(16, self.typewriter_tick)
        else:
            self.is_typing = False

    def on_click(self, event=None):
        # Jika teks masih mengetik, klik akan langsung menyelesaikan teks
        if self.is_typing:
            self.is_typing = False
            self.canvas.itemconfig(self.text_display_id, text=self.full_text)
            return

        # Jika teks sudah selesai, klik akan pindah ke babak selanjutnya
        if self.current_slide < len(self.slides) - 1:
            self.render_slide(self.current_slide + 1)
        else:
            # Babak akhir: Ledakan partikel cinta
            for p in self.particles:
                p["speed"] = random.uniform(3.5, 6.0)
                p["color"] = random.choice(["#ff0054", "#ff5400", "#ffbd00", "#ffffff"])

if __name__ == "__main__":
    root = tk.Tk()
    app = BirthdayApp(root)
    root.mainloop()