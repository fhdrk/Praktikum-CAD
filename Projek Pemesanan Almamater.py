import customtkinter as ctk
from tkinter import messagebox
import json, os
from datetime import datetime

# ==================================================
# WARNA
# ==================================================
PRIMARY_BLUE = "#001F5B"
PRIMARY_BLUE_DARK = "#001944"
WHITE = "#FFFFFF"

# ==================================================
# FILE
# ==================================================
FILE_STOK = "stok_almamater.json"
FILE_DATA = "data_pemesanan.json"

ctk.set_appearance_mode("light")

# ==================================================
# STOK
# ==================================================
def load_stok():
    if os.path.exists(FILE_STOK):
        with open(FILE_STOK, "r") as f:
            return json.load(f)
    stok_awal = {
        "XS": 9, "S": 5, "M": 5,
        "L": 0, "XL": 5, "XXL": 5, "XXXL": 5
    }
    save_stok(stok_awal)
    return stok_awal

def save_stok(stok):
    with open(FILE_STOK, "w") as f:
        json.dump(stok, f, indent=4)

stok = load_stok()

def ukuran_tersedia():
    return [u for u, s in stok.items() if s > 0]

# ==================================================
# DATA PEMESANAN
# ==================================================
def load_data():
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_DATA, "w") as f:
        json.dump(data, f, indent=4)

# ==================================================
# APP
# ==================================================
app = ctk.CTk()
app.title("Sistem Pemesanan Almamater")
app.geometry("1100x650")
app.configure(fg_color=WHITE)

# ==================================================
# SIDEBAR
# ==================================================
sidebar = ctk.CTkFrame(app, width=220, fg_color=PRIMARY_BLUE, corner_radius=0)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(
    sidebar, text="ALMAMATER\nSYSTEM",
    font=ctk.CTkFont(size=16, weight="bold"),
    text_color=WHITE
).pack(pady=30)

# ==================================================
# CONTENT
# ==================================================
content = ctk.CTkFrame(app, fg_color=WHITE)
content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

all_frames = []

def show_frame(frame):
    for f in all_frames:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ==================================================
# FRAME PESAN
# ==================================================
frame_pesan = ctk.CTkFrame(content, fg_color=WHITE)
all_frames.append(frame_pesan)

ctk.CTkLabel(
    frame_pesan, text="Form Pemesanan Almamater",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color=PRIMARY_BLUE
).pack(pady=10)

card = ctk.CTkFrame(frame_pesan, fg_color=WHITE)
card.pack(pady=10)

def input_field(label):
    ctk.CTkLabel(card, text=label, text_color=PRIMARY_BLUE)\
        .pack(anchor="w", padx=30, pady=(8, 0))
    e = ctk.CTkEntry(card, width=380)
    e.pack(padx=30, pady=6)
    return e

entry_nama = input_field("Nama")
entry_nim = input_field("NIM")
entry_fakultas = input_field("Fakultas")
entry_prodi = input_field("Prodi")

ctk.CTkLabel(card, text="Ukuran", text_color=PRIMARY_BLUE)\
    .pack(anchor="w", padx=30, pady=(8, 0))

var_ukuran = ctk.StringVar()
option_ukuran = ctk.CTkOptionMenu(
    card, variable=var_ukuran, values=ukuran_tersedia(),
    fg_color=PRIMARY_BLUE, button_color=PRIMARY_BLUE,
    button_hover_color=PRIMARY_BLUE_DARK, text_color=WHITE
)
option_ukuran.pack(padx=30, pady=6)

def refresh_ukuran():
    opsi = ukuran_tersedia()
    option_ukuran.configure(values=opsi)
    var_ukuran.set(opsi[0] if opsi else "")

def pesan():
    nama = entry_nama.get().strip()
    nim = entry_nim.get().strip()
    fakultas = entry_fakultas.get().strip()
    prodi = entry_prodi.get().strip()
    ukuran = var_ukuran.get()

    if not all([nama, nim, fakultas, prodi, ukuran]):
        messagebox.showerror("Error", "Semua data wajib diisi!")
        return
    if not nim.isdigit():
        messagebox.showerror("Error", "NIM harus angka!")
        return
    if any(c.isdigit() for c in nama):
        messagebox.showerror("Error", "Nama tidak boleh mengandung angka!")
        return

    stok[ukuran] -= 1
    save_stok(stok)

    data = load_data()
    data.append({
        "nama": nama,
        "nim": nim,
        "fakultas": fakultas,
        "prodi": prodi,
        "ukuran": ukuran,
        "waktu": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    save_data(data)

    messagebox.showinfo("Berhasil", "Pemesanan berhasil!")
    entry_nama.delete(0, "end")
    entry_nim.delete(0, "end")
    entry_fakultas.delete(0, "end")
    entry_prodi.delete(0, "end")
    refresh_ukuran()

ctk.CTkButton(
    card, text="SUBMIT PEMESANAN",
    height=45, fg_color=PRIMARY_BLUE,
    hover_color=PRIMARY_BLUE_DARK,
    text_color=WHITE,
    font=ctk.CTkFont(size=14, weight="bold"),
    command=pesan
).pack(pady=25)

# ==================================================
# FRAME LIHAT DATA
# ==================================================
frame_lihat = ctk.CTkFrame(content, fg_color=WHITE)
all_frames.append(frame_lihat)

textbox_lihat = ctk.CTkTextbox(frame_lihat, font=("Consolas", 12))
textbox_lihat.pack(fill="both", expand=True)

def load_all_data():
    textbox_lihat.configure(state="normal")
    textbox_lihat.delete("1.0", "end")
    data = load_data()

    if not data:
        textbox_lihat.insert("1.0", "Belum ada pemesanan.")
    else:
        for i, d in enumerate(data, 1):
            textbox_lihat.insert(
                "end",
                f"=== PEMESANAN {i} ===\n"
                f"Nama     : {d['nama']}\n"
                f"NIM      : {d['nim']}\n"
                f"Fakultas : {d['fakultas']}\n"
                f"Prodi    : {d['prodi']}\n"
                f"Ukuran   : {d['ukuran']}\n"
                f"Waktu    : {d['waktu']}\n"
                f"--------------------------\n"
            )
    textbox_lihat.configure(state="disabled")

# ==================================================
# FRAME CARI DATA
# ==================================================
frame_cari = ctk.CTkFrame(content, fg_color=WHITE)
all_frames.append(frame_cari)

ctk.CTkLabel(
    frame_cari, text="Cari Data Pemesanan",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color=PRIMARY_BLUE
).pack(pady=10)

entry_cari = ctk.CTkEntry(
    frame_cari,
    width=300,
    placeholder_text="Masukkan Nama atau NIM"
)
entry_cari.pack(pady=(5, 8))

ctk.CTkButton(
    frame_cari,
    text="Cari",
    width=120,
    fg_color=PRIMARY_BLUE,
    hover_color=PRIMARY_BLUE_DARK,
    text_color=WHITE,
    command=lambda: proses_cari()
).pack(pady=(0, 10))

textbox_cari = ctk.CTkTextbox(frame_cari, font=("Consolas", 12))
textbox_cari.pack(fill="both", expand=True, pady=10)

def reset_cari():
    entry_cari.delete(0, "end")
    textbox_cari.configure(state="normal")
    textbox_cari.delete("1.0", "end")
    textbox_cari.configure(state="disabled")

def proses_cari():
    keyword = entry_cari.get().strip().lower()
    textbox_cari.configure(state="normal")
    textbox_cari.delete("1.0", "end")

    if not keyword:
        textbox_cari.insert("1.0", "Masukkan Nama atau NIM.")
        textbox_cari.configure(state="disabled")
        return

    data = load_data()
    ditemukan = False
    for d in data:
        if keyword in d["nama"].lower() or keyword in d["nim"]:
            textbox_cari.insert(
                "end",
                f"Nama     : {d['nama']}\n"
                f"NIM      : {d['nim']}\n"
                f"Fakultas : {d['fakultas']}\n"
                f"Prodi    : {d['prodi']}\n"
                f"Ukuran   : {d['ukuran']}\n"
                f"Waktu    : {d['waktu']}\n"
                f"--------------------------\n"
            )
            ditemukan = True

    if not ditemukan:
        textbox_cari.insert("1.0", "Data tidak ditemukan.")

    textbox_cari.configure(state="disabled")

# ==================================================
# FRAME CEK STOK
# ==================================================
frame_stok = ctk.CTkFrame(content, fg_color=WHITE)
all_frames.append(frame_stok)

textbox_stok = ctk.CTkTextbox(frame_stok, font=("Consolas", 13))
textbox_stok.pack(fill="both", expand=True)

def load_stok_view():
    textbox_stok.configure(state="normal")
    textbox_stok.delete("1.0", "end")
    textbox_stok.insert("1.0", "=== STOK ALMAMATER ===\n\n")
    for u, j in stok.items():
        textbox_stok.insert("end", f"{u:<6} : {'HABIS' if j == 0 else f'{j} pcs'}\n")
    textbox_stok.configure(state="disabled")

# ==================================================
# SIDEBAR BUTTON
# ==================================================
def sidebar_btn(text, cmd):
    ctk.CTkButton(
        sidebar, text=text, height=42, anchor="w",
        fg_color=PRIMARY_BLUE, hover_color=PRIMARY_BLUE_DARK,
        text_color=WHITE, command=cmd
    ).pack(fill="x", padx=20, pady=6)

sidebar_btn("🧾 Pesan Almamater", lambda: show_frame(frame_pesan))
sidebar_btn("📋 Lihat Data", lambda: (load_all_data(), show_frame(frame_lihat)))
sidebar_btn("🔍 Cari Data", lambda: (reset_cari(), show_frame(frame_cari)))
sidebar_btn("📦 Cek Stok", lambda: (load_stok_view(), show_frame(frame_stok)))
sidebar_btn("🚪 Keluar", app.destroy)

# ==================================================
# START
# ==================================================
refresh_ukuran()
show_frame(frame_pesan)
app.mainloop()
