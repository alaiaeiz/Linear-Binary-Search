import pandas as pd
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def linear_search(data, kolom, keyword):
    hasil = []
    for i in range(len(data)):
        if keyword.lower() in str(data[kolom][i]).lower():
            hasil.append(data.iloc[i])
    return hasil

def binary_search(data, kolom, keyword):
    hasil = []
    
    if kolom == "Tahun Terbit":
        data[kolom] = pd.to_numeric(data[kolom], errors="coerce")
        data = data.dropna(subset=[kolom])
        data[kolom] = data[kolom].astype(int)
        try:
            keyword = int(keyword)
        except ValueError:
            print("Masukkan tahun yang valid!")
            return []

    data_sorted = data.sort_values(by=kolom).reset_index(drop=True)
    low, high = 0, len(data_sorted) - 1

    while low <= high:
        mid = (low + high) // 2
        nilai = data_sorted[kolom][mid]

        if kolom == "Tahun Terbit":
            if keyword == nilai:
                hasil.append(data_sorted.iloc[mid])
                kiri, kanan = mid - 1, mid + 1
                while kiri >= 0 and data_sorted[kolom][kiri] == keyword:
                    hasil.append(data_sorted.iloc[kiri])
                    kiri -= 1
                while kanan < len(data_sorted) and data_sorted[kolom][kanan] == keyword:
                    hasil.append(data_sorted.iloc[kanan])
                    kanan += 1
                break
            elif keyword < nilai:
                high = mid - 1
            else:
                low = mid + 1
        else:
            nilai_str = str(nilai)
            if keyword.lower() in nilai_str.lower():
                hasil.append(data_sorted.iloc[mid])
                kiri, kanan = mid - 1, mid + 1
                while kiri >= 0 and keyword.lower() in str(data_sorted[kolom][kiri]).lower():
                    hasil.append(data_sorted.iloc[kiri])
                    kiri -= 1
                while kanan < len(data_sorted) and keyword.lower() in str(data_sorted[kolom][kanan]).lower():
                    hasil.append(data_sorted.iloc[kanan])
                    kanan += 1
                break
            elif keyword.lower() < nilai_str.lower():
                high = mid - 1
            else:
                low = mid + 1
    return hasil

def main():
    try:
        url = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv"
        data = pd.read_csv(url, header=0)
        data.columns = data.columns.str.strip()
        print("Kolom tersedia:", data.columns.tolist())
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca data: {e}")
        return

    while True:
        clear()
        print("=== MENU PENCARIAN JURNAL ===")
        print("1. Linear Search")
        print("2. Binary Search")
        print("3. Keluar")
        metode = input("Pilih metode pencarian (1/2/3): ")

        if metode == "3":
            print("Terima kasih telah menggunakan program pencarian jurnal ini.")
            break
        elif metode not in ["1", "2"]:
            input("Pilihan tidak valid.")
            continue

        clear()
        print("=== PILIH PENCARIAN BERDASARKAN ===")
        print("1. Judul Paper")
        print("2. Tahun Terbit")
        print("3. Nama Penulis")
        kolom_pilihan = input("Pilih kolom pencarian (1/2/3): ")

        kolom_map = {
            "1": "Judul Paper",
            "2": "Tahun Terbit",
            "3": "Nama Penulis"
        }

        if kolom_pilihan not in kolom_map:
            input("Pilihan kolom tidak valid.")
            continue

        kolom = kolom_map[kolom_pilihan]
        keyword = input(f"Masukkan keyword untuk {kolom}: ")

        clear()
        print(f"=== HASIL PENCARIAN ({kolom} = '{keyword}') ===")

        if metode == "1":
            hasil = linear_search(data, kolom, keyword)
        else:
            if kolom != "Tahun Terbit":
                print("Binary search hanya tersedia untuk pencarian berdasarkan Tahun Terbit.")
                input("\nTekan Enter untuk kembali ke menu utama...")
                continue
            hasil = binary_search(data, kolom, keyword)

        if hasil:
            for i, h in enumerate(hasil, 1):
                print(f"{i:<3} {h.get('Judul Paper', ''):<50} | {str(h.get('Tahun Terbit', '')):^10} | {h.get('Nama Penulis', ''):<30}")
        else:
            print("Tidak ditemukan hasil yang cocok.")

        input("\nTekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    main()
