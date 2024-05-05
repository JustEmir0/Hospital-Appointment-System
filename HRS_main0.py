import os
import random
import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from CTkListbox import * 
from datetime import datetime

kullanici_bilgileri = {'isim': '', 'tc': ''}


def kaydet():
    with open("kullanici_bilgileri.txt", "w") as dosya:
        dosya.write(f"isim: {isim_entry.get()}\n")
        dosya.write(f"tC: {tc_entry.get()}\n")

def yükle():
    kullanici_bilgileri = {}
    dosya_adı = "kullanici_bilgileri.txt"
    if os.path.exists(dosya_adı):
        with open(dosya_adı, "r") as dosya:
            for satir in dosya:
                satir = satir.strip()
                if satir:
                    parcalar = satir.split(":")
                    if len(parcalar) == 2:
                        anahtar, deger = parcalar[0].strip(), parcalar[1].strip()
                        kullanici_bilgileri[anahtar] = deger
                    else:
                        print(f"Hatalı biçimlendirilmiş satır: {satir}")
    else:
        print(f"{dosya_adı} adlı dosya bulunamadı. Otomatik olarak oluşturulacak.")
        # Dosyayı otomatik olarak oluştur
        with open(dosya_adı, "w") as dosya:
            dosya.write("isim: \n")
            dosya.write("tC: \n")
    return kullanici_bilgileri

def giriş_yap_hasta():
    isim = isim_entry.get()
    tc = tc_entry.get()

    # İsim uzunluğu kontrolü
    if len(isim) < 5:
        messagebox.showerror('Hata', 'İsim 5 karakterden az olamaz.')
        return
    
    # TC uzunluğu ve tamamen rakam olup olmadığının kontrolü
    if len(tc) != 11 or not tc.isdigit():
        messagebox.showerror('Hata', 'TC 11 haneli ve tamamen rakamlardan oluşmalıdır.')
        return

    kullanici_bilgileri['isim'] = isim
    kullanici_bilgileri['tc'] = tc
    
    kullanici_bilgilerini_kaydet(kullanici_bilgileri)
     
    messagebox.showinfo('Başarılı', 'Giriş Başarılı Hasta Ekranına Yönlendiriliyorsunuz...')
    root.destroy()
    hasta_ekranına_giriş()

def kullanici_bilgilerini_kaydet(bilgiler):
    with open("kullanici_bilgileri.txt", "w") as dosya:
        for anahtar, deger in bilgiler.items():
            dosya.write(f"{anahtar}: {deger}\n")

def giriş_yap_doktor():
    doc_isim = doc_isim_entry.get()
    doc_sifre = sifre_entry.get()

    # Kullanıcı adı ve şifre kontrolü
    for doktor in doktorlar:
        if doktor.isim == doc_isim and doktor.sifre == doc_sifre:
            messagebox.showinfo('Başarılı','Doktor Ekranına Yönlendiriliyorsunuz...')
            root.destroy()
            doktor_ekranına_giriş()
            break
    else:
        messagebox.showerror('Hata','Geçersiz Kullanıcı Adı veya Şifre')


class Hasta:
    def __init__(self, isim, tc):
        self.isim = isim
        self.tc = tc

class Doktor:
    def __init__(self, isim, uzmanlik_alani,sifre):
        self.isim = isim
        self.uzmanlik_alani = uzmanlik_alani
        self.sifre = sifre
        self.musaitlik_durumu = True  

    def musaitlik_kontrol(self):
        return self.musaitlik_durumu

class Randevu:
    def __init__(self, tarih, doktor, hasta, sikayet):
        self.tarih = tarih
        self.doktor = doktor
        self.hasta = hasta
        self.sikayet = sikayet


def hasta_ekranına_giriş():

    app_pai = CTk()
    app_pai.geometry('750x750')
    app_pai.title('Hastane Randevu Sistemi (Hasta Ekranı)')

    frame = CTkFrame(master=app_pai, width=690 , height=710 , corner_radius=30,)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER )

    label_giriş = CTkLabel(master=frame,text="Hasta Ekranına Hoşgeldiniz",font=('Arial',20))
    label_giriş.place(x=220, y=10)

    label_sikayet = CTkLabel(master=frame,text="Şikayetiniz",font=('Arial',16))
    label_sikayet.place(x=390, y=165)
    entry_sikayet = CTkEntry(master=frame,width=180,height=200)
    entry_sikayet.place(x=485,y=80)

    label_doktorlar = CTkLabel(master=frame,text="Doktor Seçiniz",font=('Arial',16))
    label_doktorlar.place(x=17, y=80)
    sec_doktorlar = CTkComboBox(master=frame , values=doktor_kişiler, width=230)
    sec_doktorlar.place(x=17, y=115)

    label_randevu_tarihi = CTkLabel(master=frame, text="Randevu Tarihi (GG-AA-YYYY)",font=('Arial',16))
    label_randevu_tarihi.place(x=17,y=160)
    entry_randevu_tarihi = CTkEntry(master=frame,width=230, height=26)
    entry_randevu_tarihi.place(x=17, y=190)

    label_randevular = CTkLabel(master=frame,text="--- Randevu Ekranı ---",font=('Arial',20))
    label_randevular.place(x=225, y=300)
    listbox_randevular = CTkListbox(master=frame, width=640, height=270)
    listbox_randevular.place(x=10, y=330)


    def randevu_al():
        isim = kullanici_bilgileri.get('isim')
        tc = kullanici_bilgileri.get('tc')
        doktor = sec_doktorlar.get()  
        randevu_tarih = entry_randevu_tarihi.get()
        sikayet = entry_sikayet.get()  

        try:
            randevu_tarih = datetime.strptime(randevu_tarih, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen GG-AA-YYYY formatında girin.")
            return

        # Kullanıcının daha önce aldığı randevuları kontrol et
        if doktor in randevular and any(randevu.hasta == isim for randevu in randevular[doktor]):
            messagebox.showerror("Hata", "Bu doktordan daha önce randevu aldınız. Başka bir doktor seçin.")
            return

        # Yeni randevuyu oluştur ve randevular sözlüğüne ekle
        randevu = Randevu(randevu_tarih, doktor, isim, sikayet)  
        if doktor in randevular:
            randevular[doktor].append(randevu)
        else:
            randevular[doktor] = [randevu]
        
        listbox_randevular.insert(tk.END, f"Doktor: Dr.{doktor}, Tarih: {randevu_tarih.strftime('%d-%m-%Y')}, Şikayet: {sikayet}")  
        messagebox.showinfo("Başarılı", "Randevu başarıyla alındı.")



    btn_rdv_al = CTkButton(master=frame,text='Randevu Al',font=('Arial',16),width=230,height=23,command=randevu_al)
    btn_rdv_al.place(x=17, y=240)

    def tüm_rdv_iptal_et():
        # Clear the listbox
        listbox_randevular.delete(0, tk.END)
        
        # Clear the appointments dictionary
        randevular.clear()
        messagebox.showinfo("Başarılı","Bütün Randevularınız İptal Edildi")

    btn_rdv_dzl = CTkButton(master=frame,text="Bütün Randevuları İptal Et",font=('Arial',16),width=250,height=27,command=tüm_rdv_iptal_et)
    btn_rdv_dzl.place(x=40, y=635)

    def randevu_iptal():#something is not right 
        selected_index = listbox_randevular.curselection()
        if selected_index == listbox_randevular.curselection():
            listbox_randevular.delete(selected_index)
            # Randevuyu sözlükten sil
            for doktor, randevu_listesi in randevular.items():
                for i, randevu in enumerate(randevu_listesi):
                    if i == selected_index:
                        randevu_listesi.pop(i)
                        break


    btn_rdv_ipt = CTkButton(master=frame,text="Seçili Randevuyu İptal Et",font=('Arial',16),width=250,height=27,command=randevu_iptal)
    btn_rdv_ipt.place(x=400, y=635)

    app_pai.mainloop()


from datetime import datetime, timedelta

# Rastgele hastaların ve şikayetlerin listesi
hastalar = ["Ahmet Yılmaz", "Ayşe Kaya", "Mehmet Demir", "Fatma Şahin", "Mustafa Aydın", "Zeynep Aksoy"]
sikayetler = ["Baş ağrısı", "Mide bulantısı", "Yorgunluk", "Sırt ağrısı", "İshal", "Öksürük", "Kusma", "Ateş"]

# Rastgele hasta, şikayet ve tarih oluşturma
def random_hasta_sikayet_ve_tarih_olustur():
    hasta = random.choice(hastalar)
    sikayet = random.choice(sikayetler)
    # Rastgele bir tarih oluşturmak için, bugünün tarihine rastgele bir gün ekleyebiliriz
    rastgele_tarih = datetime.now() + timedelta(days=random.randint(1, 30))
    return hasta, sikayet, rastgele_tarih.strftime("%d-%m-%Y")  # Tarihi belirli bir formata dönüştürüyoruz

def doktor_ekranına_giriş():
    app_doc = CTk()
    app_doc.geometry('600x600')
    app_doc.title('Hastane Randevu Sistemi (Doktor Ekranı)')

    frame = CTkFrame(master=app_doc, width=580, height=580, corner_radius=30)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label_giriş = CTkLabel(master=frame, text="--- Doktor Ekranına Hoşgeldiniz ---", font=('Arial', 20))
    label_giriş.place(x=140, y=10)

    label_randevular = CTkLabel(master=frame, text="--- Hastalarınız ---", font=('Arial', 20))
    label_randevular.place(x=200, y=175)
    listbox_randevular = CTkListbox(master=frame, width=530, height=270)
    listbox_randevular.place(x=10, y=200)

    # Rastgele hasta sayısı belirleme
    hasta_sayısı = random.randint(1, 10)  # 1 ile 10 arasında rastgele hasta sayısı seçelim

    # Rastgele hastaları, şikayetleri ve tarihleri listbox'a ekleme
    for _ in range(hasta_sayısı):
        hasta, sikayet, tarih = random_hasta_sikayet_ve_tarih_olustur()
        listbox_randevular.insert(tk.END, f"Hasta: {hasta}, Şikayet: {sikayet}, Tarih: {tarih}")


    def randevu_iptal_doc():
        # Seçili randevuyu bul
        selected_index = listbox_randevular.curselection()
        listbox_randevular.delete(selected_index)
        messagebox.showinfo('Başarılı',"Randevu İptal Edildi. Hastaya En Yakın Zamanda Haber Verilecek")


    btn_rdv_ipt = CTkButton(master=frame, text="Randevuyu İptal Et", font=('Arial', 16), width=200, height=23,command=randevu_iptal_doc)
    btn_rdv_ipt.place(x=180, y=510)

    app_doc.mainloop()




#Veriler
randevular = {}
doktorlar = [
    Doktor("Fırat Güneri", "Kardiyoloji", "1234"),
    Doktor("Sıla Kaya", "Dahiliye", "1414"),
    Doktor("Bayram Çelik", "Göz Hastalıkları", "3435"),
    Doktor("Senem Akın", "Ortopedi", "4007"),
    Doktor("Mirza Koç", "Kulak Burun Boğaz", "7890")]
doktor_kişiler = [f"{doktor.isim} - {doktor.uzmanlik_alani}" for doktor in doktorlar]



#-----Logın Page-----#
root = CTk()
root.geometry('450x400')
root.title('Logın Page')

tabwiev = CTkTabview(master=root,height=330)
tabwiev.place(x=75,y=20)

tabwiev.add("Hasta")
tabwiev.add("Doktor")

label_isim = CTkLabel(master=tabwiev.tab("Hasta"),text="İsim Soyisim",font=('Arial',16))
label_isim.place(x=85, y=30)
isim_entry = CTkEntry(master=tabwiev.tab("Hasta"),width=140, height=23)
isim_entry.place(x=65, y=65)

label_tc = CTkLabel(master=tabwiev.tab("Hasta"),text="TC Kimlik No",font=('Arial',16))
label_tc.place(x=85, y=100)
tc_entry = CTkEntry(master=tabwiev.tab("Hasta"),width=140, height=20)
tc_entry.place(x=65, y=135)


doc_label_isim = CTkLabel(master=tabwiev.tab("Doktor"),text="İsim Soyisim",font=('Arial',16))
doc_label_isim.place(x=75, y=30)
doc_isim_entry = CTkEntry(master=tabwiev.tab("Doktor"),width=140, height=23)
doc_isim_entry.place(x=65, y=65)

label_sifre = CTkLabel(master=tabwiev.tab("Doktor"),text="Şifre",font=('Arial',16))
label_sifre.place(x=75, y=100)
sifre_entry = CTkEntry(master=tabwiev.tab("Doktor"),width=140, height=20)
sifre_entry.place(x=65, y=135)

btn_giriş_yap_doc = CTkButton(master=tabwiev.tab("Doktor"),text='Giriş Yap',font=('Arial',16),width=140, height=23,command=giriş_yap_doktor)
btn_giriş_yap_doc.place(x=65, y=185,)


btn_giriş_yap_patient = CTkButton(master=tabwiev.tab("Hasta"),text='Giriş Yap',font=('Arial',16),width=140, height=23,command=giriş_yap_hasta)
btn_giriş_yap_patient.place(x=65, y=185,)

root.mainloop()