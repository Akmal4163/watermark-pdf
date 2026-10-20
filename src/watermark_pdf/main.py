import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter, Transformation


def terapkan_watermark(file_input, file_watermark, file_output):
  reader = PdfReader(file_input)
  watermark = PdfReader(file_watermark)
  hal_watermark = watermark.pages[0]

  writer = PdfWriter()

  # Ambil ukuran lebar dan tinggi dari dokumen asli dan watermark
  lebar_asli = float(reader.pages[0].mediabox.width)
  tinggi_asli = float(reader.pages[0].mediabox.height)

  lebar_wm = float(hal_watermark.mediabox.width)
  tinggi_wm = float(hal_watermark.mediabox.height)

  # Hitung titik tengah
  koordinat_x = (lebar_asli - lebar_wm) / 2
  koordinat_y = (tinggi_asli - tinggi_wm) / 2

  # Buat transformasi untuk menggeser posisi watermark ke tengah
  op_transformasi = (
      Transformation().translate(koordinat_x, koordinat_y)
  )

  for halaman in reader.pages:
    halaman.merge_transformed_page(hal_watermark, op_transformasi)
    writer.add_page(halaman)

  with open(file_output, "wb") as f_out:
    writer.write(f_out)

def pilih_folder_sumber():
  folder = filedialog.askdirectory()
  if folder:
    entry_sumber.delete(0, tk.END)
    entry_sumber.insert(0, folder)


def pilih_file_wm():
  file_pdf = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
  if file_pdf:
    entry_wm.delete(0, tk.END)
    entry_wm.insert(0, file_pdf)


def pilih_folder_tujuan():
  folder = filedialog.askdirectory()
  if folder:
    entry_tujuan.delete(0, tk.END)
    entry_tujuan.insert(0, folder)


def mulai_proses():
  folder_sumber = entry_sumber.get()
  file_wm = entry_wm.get()
  folder_tujuan = entry_tujuan.get()

  os.makedirs(folder_tujuan, exist_ok=True)
  jumlah = 0

  for nama_file in os.listdir(folder_sumber):
    if nama_file.lower().endswith(".pdf"):
      jalur_input = os.path.join(folder_sumber, nama_file)
      jalur_output = os.path.join(folder_tujuan, nama_file)
      terapkan_watermark(jalur_input, file_wm, jalur_output)
      jumlah += 1

  messagebox.showinfo("Informasi", f"Proses selesai sebanyak {jumlah} file.")


root = tk.Tk()
root.title("Aplikasi Watermark PDF")
root.geometry("450x400")

tk.Label(root, text="Folder PDF Sumber:").pack(anchor="w", padx=10, pady=2)
entry_sumber = tk.Entry(root, width=50)
entry_sumber.pack(padx=10)
tk.Button(root, text="Pilih Folder Sumber", command=pilih_folder_sumber).pack(
    padx=10, pady=2
)

tk.Label(root, text="File Watermark (PDF):").pack(anchor="w", padx=10, pady=2)
entry_wm = tk.Entry(root, width=50)
entry_wm.pack(padx=10)
tk.Button(root, text="Pilih File Watermark", command=pilih_file_wm).pack(
    padx=10, pady=2
)

tk.Label(root, text="Folder Hasil Output:").pack(anchor="w", padx=10, pady=2)
entry_tujuan = tk.Entry(root, width=50)
entry_tujuan.pack(padx=10)
tk.Button(root, text="Pilih Folder Tujuan", command=pilih_folder_tujuan).pack(
    padx=10, pady=2
)

tk.Button(
    root, text="Proses Watermark", command=mulai_proses, bg="green", fg="white"
).pack(pady=10)

root.mainloop()