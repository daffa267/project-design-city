from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

class PetaKota:
    #Deklarasi variabel awal yang nantinya akan digunakan
    def __init__(self) -> None:
        self.skala = 10
        self.jumlah_jalan = 0
        self.lebar = 150 * self.skala
        self.tinggi = 150 * self.skala
        self.padding = self.skala
        self.panjang_jalan = 20 * self.skala
        self.lebar_jalan = 20
        self.persimpangan = []
        self.jarak_bangunan = 10
        #Deklarasi Bangunan dan Dekor
        self.bangunan = [
            Image.open("build/sedang1.png").resize((50,30)),
            Image.open("build/sedang2-x.png").resize((50,30)), 
            Image.open("build/besar1-x.png").resize((100,50)), 
            Image.open("build/besar2-x.png").resize((100,50)),
            Image.open("build/rumah1.png").resize((20,10)),
            Image.open("build/rumah2.png").resize((20,10)),
            Image.open("build/kecil1.png").resize((20,20)),
            Image.open("build/kecil2.png").resize((20,20)),
        ]
        self.bangunan_vertikal = [
            Image.open("build/sedang2-y.jpg").resize((30,50)), 
            Image.open("build/besar1-y.jpg").resize((50,100)),
            Image.open("build/rumah1.png").resize((10,20)),
            Image.open("build/besar2-y.jpg").resize((50,100)),
            Image.open("build/kecil1.png").resize((20,20))
        ]
        self.lingkungan = [
            Image.open("decor/Pohon1.jpg").resize((20,20)),
            Image.open("decor/pohon2.png").resize((20,20)),
            Image.open("decor/pohon3.png").resize((20,20)), 
            Image.open("decor/pohon4.png").resize((20,20)), 
            Image.open("decor/pohon5.png").resize((20,20)), 
            Image.open("decor/batu.jpg").resize((20,20))
        ]
        self.gambar_peta = Image.new("RGBA", (self.lebar, self.tinggi), "gray")
        self.gambar_peta_draw = ImageDraw.Draw(self.gambar_peta)

    #Fungsi limit ini untuk membatasi posisi x dan y agar tidak keluar dari map  
    def batas_x(self, x) : return 0 if x <= 0 else (x if x < self.lebar else self.lebar)
    def batas_y(self, y) : return 0 if y <= 0 else (y if y < self.tinggi else self.tinggi)

    #Fungsi untuk membuat jalan , dimulai dari titik 0,0
    #Menggunakan metode rekursif
    def buat_jalan(self, pos, arah):
        self.jumlah_jalan += 1
        if self.jumlah_jalan > 150 and (pos[0]<= 0 or pos[0] >= self.lebar or pos[1] <= 0 or pos[1] >= self.tinggi):
            return
        self.persimpangan.append(pos)
        langkah = random.choice([1, 1])

        #Next vertice berarti titik selanjutnya atau x2, y2
        #Titik selanjutnya itu menggunakan library random untuk mencari x dan y terdekat
        simpul_berikutnya = (pos[0] + self.lebar_jalan if arah == "y" else pos[0] + self.panjang_jalan * langkah, 
                       pos[1] + self.lebar_jalan if arah == "x" else pos[1] + self.panjang_jalan * langkah)
        if simpul_berikutnya not in self.persimpangan:
            self.persimpangan.append(simpul_berikutnya)
        valid = [pos[0] <= 0 and arah == "y", pos[1] <= 0 and arah == "x", 
                 simpul_berikutnya[1] >= self.tinggi and arah == "x", pos[0] >= self.tinggi and arah == "x"]
        simpul_berikutnya = (self.batas_x(simpul_berikutnya[0]), self.batas_y(simpul_berikutnya[1]))
        x_sorted, y_sorted = sort([pos[0], simpul_berikutnya[0]]), sort([pos[1], simpul_berikutnya[1]])
        if x_sorted[1] >= self.lebar or x_sorted[1] <= 0:
            self.persimpangan.append((self.batas_x(x_sorted[1]), pos[1]))
        if y_sorted[1] >= self.tinggi or y_sorted[1] <= 0:
            self.persimpangan.append((pos[0] + 10, self.batas_y(y_sorted[1])))
        
        if not sum(valid):
            #Fungsi untk menggambar jalan
            self.gambar_peta_draw.rectangle(((x_sorted[0], y_sorted[0]), (x_sorted[1], y_sorted[1])), "black")
            if arah == "y":
                for y in range(y_sorted[0] + 10, y_sorted[1] - 10, 20):
                    self.gambar_peta_draw.line(((x_sorted[0] + 10, y), (x_sorted[0] + 10, y + 10)), "white", 1)
            else:
                for x in range(x_sorted[0] + 20, x_sorted[1] - 10, 20):
                    self.gambar_peta_draw.line(((x, y_sorted[0] + 10), (x + 10, y_sorted[0] + 10)), "white", 1)
        
        next_x = self.lebar if simpul_berikutnya[0] <= 0 else (simpul_berikutnya[0] - (20 if arah == "y" else 0) if simpul_berikutnya[0] < self.lebar else 0)
        next_y = self.tinggi if simpul_berikutnya[1] <= 0 else (simpul_berikutnya[1] - (20 if arah == 'x' else 0) if simpul_berikutnya[1] < self.tinggi else 0)

        print((next_x, next_y), " : terakhir - ", self.simpul_terakhir, self.simpul_terakhir2)
        self.simpul_terakhir = (next_x, next_y)
        self.simpul_terakhir2 = pos
        self.buat_jalan((next_x, next_y), random.choice(["x", 'y']))

    #Fungsi untuk membuat map baru, yang mana akan dieksekusi ketika tombol generate map ditekan
    def buat_peta(self):
        self.persimpangan = [(0, 0), (0, self.tinggi), (self.lebar, 0), (self.lebar, self.tinggi)]
        self.jumlah_jalan = 0
        self.simpul_terakhir = (random.randrange(0, self.lebar, self.panjang_jalan), random.choice([0, self.tinggi]))
        self.simpul_terakhir2 = (random.randrange(0, self.lebar, self.panjang_jalan), random.choice([0, self.tinggi]))
        self.gambar_peta = Image.new("RGBA", (self.lebar, self.tinggi), (100, 100, 100))
        self.gambar_peta_draw = ImageDraw.Draw(self.gambar_peta)
        self.buat_jalan(self.simpul_terakhir, "y")
        #Save map
        #self.gambar_peta.save("map1.png")
        self.mapping()
        #Save map2
        #self.gambar_peta.save("map2.png")
        return self.gambar_peta

    #Panggil fungsi generate building ketika jalan sudah berada di batas bawah map
    def generate_building(self, area):
        x = area[0][0]
        #titik paling atas area
        #Fungsi ini untuk mengembalikan asset / gambar bangunan yang muat dengan area yang sekarang ingin digenerate
        #BangunanX berarti menyamping gambarnya
        def get_building_x(x):
            return [building for building in self.bangunan if building.size[0] + x < area[1][0] - self.padding]
        #Fungsi ini untuk mengembalikan asset / gambar bangunan yang muat dengan area yang sekarang ingin digenerate
        #BangunanY berarti vertical atau keatas
        def get_building_y(x, y):
            return [env for env in self.lingkungan if env.size[0] + x < area[1][0] - self.padding and env.size[1] + y < area[1][1] - 50]
        
        while x < area[1][0]:
            #Kandidat bangunan yang muat utk diletakkan
            candidates = get_building_x(x)
            #Jika ternyata ada atau memungkinkan untuk memasukkan bangunan
            if len(candidates):
                #Ambil salah satu bangunan yang muat utuk diamsukkan ke area, menggunakan library random / diacak
                build = random.choice(candidates)
                #Untuk rectangel ini kita isi arenya dengan warna abu-abu supaya berkesan ada jalan setapak
                self.gambar_peta_draw.rectangle(((x, area[0][1]), (x + build.size[0] + 20, area[0][1] + build.size[1])), "green")
                #Kita paste atau tempelkan gambar bangunan kedalam area yang sekrang
                self.gambar_peta.paste(build, (x, area[0][1]))
                #Tambahkan nilai x karena disini penempatan bangunan nya dari kiri ke kanan area
                x += build.size[0] + self.jarak_bangunan
            else:
                break

        x = area[0][0]
        y = area[0][1] + 50 + self.padding

        #Ini kusus untuk ditengah atau dekorasi / pepohonan
        while y < area[1][1] - 50:
            max_height = 50
            while x < area[1][0]:
                candidates = get_building_y(x, y)
                if len(candidates):
                    build = random.choice(candidates)
                    self.gambar_peta_draw.rectangle(((x, y), (x + build.size[0] + 20, y + build.size[1])), "green")
                    self.gambar_peta.paste(build, (x, random.randint(y, y + (max_height - build.size[1]))))
                    max_height = max(build.size[1], max_height)
                    x += build.size[0] + self.padding
                else:
                    break
            y += max_height + self.padding

        x = area[0][0]
        #Sama saja , tapi untuk titik paling bawah area
        if abs(area[1][1] - area[0][1]) < 120:
            return
        while x < area[1][0]:
            candidates = get_building_x(x)
            if len(candidates):
                build = random.choice(candidates)
                self.gambar_peta_draw.rectangle(((x, area[1][1] - build.size[1]), (x + build.size[0] + 20, area[1][1] - build.size[1] + build.size[1])), "green")
                self.gambar_peta.paste(build, (x, area[1][1] - build.size[1]))
                x += build.size[0] + self.jarak_bangunan
            else:
                break

    #Fungsi mapping dipanggil untuk memetakan area yang sekirannya bisa dimasukkan bangunan 
    #Biasanya berupa area kotak 
    #Utk algoritmanya dia cari sebuah titik kemudian cari titik tetangga terdekatnya
    def mapping(self):
        debug_text = ["" for _ in range(len(self.persimpangan))]
        #Mencari titik yang akan dijadikan titik orign area
        for idx, point in enumerate(self.persimpangan):
            if point[1] > self.tinggi:
                continue
            nearest_x, nearest_y = 0, 0
            #Perulangan untuk mencari titik tetangga terdekat
            for neighbor in self.persimpangan:
                if point != neighbor and point[0] > 0 and point[1] > 0:
                    nearest_x = neighbor[0] if neighbor[0] > nearest_x and neighbor[0] < point[0] and point[1] == neighbor[1] else nearest_x
                    nearest_y = neighbor[1] if neighbor[1] > nearest_y and neighbor[1] < point[1] else nearest_y
            
            if idx < len(debug_text) and debug_text[idx] != "":
                debug_text[idx] = ""
            if point[1] == 1500:
                print(point, ": ", nearest_x, nearest_y)
            if point[0] - nearest_x >= 30 and point[1] - nearest_y >= 30:
                if (point[0], nearest_y) not in self.persimpangan:
                    debug_text.append("aha")
                    self.persimpangan.append((point[0], nearest_y - 20))
                if point[1] < self.lebar - 20:
                    self.gambar_peta_draw.rectangle(((nearest_x + 1, nearest_y + 1), (point[0] - 1, point[1] - 1)), "gray")
                self.gambar_peta_draw.rectangle(((nearest_x + 10, nearest_y + 10), (point[0] - 10, point[1] - 10)), "green")
                self.generate_building(((nearest_x + 10, nearest_y + 10), (point[0] - 10, point[1] - 10)))

# Fungsi untuk memperbarui peta dan memperlihatkannya pada label
def perbarui_peta():
    peta_baru = peta_saya.buat_peta()
    peta_baru = peta_baru.crop((viewport_x, viewport_y, viewport_x + viewport_lebar, viewport_y + viewport_tinggi))
    peta_baru = peta_baru.resize((LEBAR_AWAL, TINGGI_AWAL))
    peta_baru = ImageTk.PhotoImage(peta_baru)
    label_peta.config(image=peta_baru)
    label_peta.image = peta_baru

# Fungsi untuk memperbarui tampilan peta
def perbarui():
    peta_baru = peta_saya.gambar_peta.crop((viewport_x, viewport_y, viewport_x + viewport_lebar, viewport_y + viewport_tinggi))
    peta_baru = peta_baru.resize((LEBAR_AWAL, TINGGI_AWAL))
    peta_baru = ImageTk.PhotoImage(peta_baru)
    label_peta.config(image=peta_baru)
    label_peta.image = peta_baru

# Fungsi untuk memperbesar tampilan peta
def zoom_in():
    global faktor_zoom, viewport_lebar, viewport_tinggi, viewport_x, viewport_y
    faktor_zoom = min(4.0, faktor_zoom + 0.1)
    viewport_lebar = int(LEBAR_AWAL / faktor_zoom)
    viewport_tinggi = int(TINGGI_AWAL / faktor_zoom)
    viewport_x = max(0, min(viewport_x, peta_saya.lebar - viewport_lebar))
    viewport_y = max(0, min(viewport_y, peta_saya.tinggi - viewport_tinggi))
    perbarui()

# Fungsi untuk memperkecil tampilan peta
def zoom_out():
    global faktor_zoom, viewport_lebar, viewport_tinggi, viewport_x, viewport_y
    faktor_zoom = max(0.1, faktor_zoom - 0.1)
    viewport_lebar = int(LEBAR_AWAL / faktor_zoom)
    viewport_tinggi = int(TINGGI_AWAL / faktor_zoom)
    viewport_x = max(0, min(viewport_x, peta_saya.lebar - viewport_lebar))
    viewport_y = max(0, min(viewport_y, peta_saya.tinggi - viewport_tinggi))
    perbarui()

# Fungsi untuk menangani peristiwa scroll mouse
def gulir(event):
    global viewport_x, viewport_y
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()

# Fungsi untuk menangani peristiwa tekanan tombol pada keyboard
def pada_tekanan_tombol(event):
    global viewport_x, viewport_y
    ukuran_langkah = 50
    if event.keysym == "w":
        viewport_y = max(0, viewport_y - ukuran_langkah)
    elif event.keysym == "s":
        viewport_y = min(peta_saya.tinggi - viewport_tinggi, viewport_y + ukuran_langkah)
    elif event.keysym == "a":
        viewport_x = max(0, viewport_x - ukuran_langkah)
    elif event.keysym == "d":
        viewport_x = min(peta_saya.lebar - viewport_lebar, viewport_x + ukuran_langkah)
    perbarui()

# Inisialisasi GUI
root = tk.Tk()
root.title("IKN CITY")
frame = ttk.Frame(root, padding=10)
frame.grid()

# Membuat gambar peta awal
peta_saya = PetaKota()
gambar_peta = peta_saya.buat_peta()
gambar_peta = gambar_peta.crop((0, 0, 500, 400)).resize((500, 400))
gambar_peta = ImageTk.PhotoImage(gambar_peta)
label_peta = ttk.Label(frame, image=gambar_peta)
label_peta.grid(column=0, row=0, columnspan=4)


# Menambahkan tombol untuk memperbarui peta
tombol_generate = ttk.Button(frame, text="Redesign", command=perbarui_peta)
tombol_generate.grid(column=1, row=1, sticky="e", padx=15, pady=10)

# Menambahkan event handler untuk scroll mouse dan tekanan tombol
label_peta.bind("<MouseWheel>", gulir)
root.bind("<KeyPress>", pada_tekanan_tombol)

# Inisialisasi variabel untuk zoom dan viewport
LEBAR_AWAL, TINGGI_AWAL = 500, 400
faktor_zoom = 1.0
viewport_lebar, viewport_tinggi = LEBAR_AWAL, TINGGI_AWAL
viewport_x, viewport_y = 0, 0
# Menjalankan loop utama aplikasi
root.mainloop()
