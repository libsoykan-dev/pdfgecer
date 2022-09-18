    # Z-Kitaplardan PDF dosyası oluşturmaya yarayan program
    # Copyright (C) 2022 libsoykan-dev

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pynput.mouse import Controller, Button, Controller

from fpdf import FPDF

import time

from PIL import ImageGrab

import re

import os

import PySimpleGUI as gka

import sys

pdfsay = 0

syfliste = []

pdf = FPDF()

mouse = Controller()

duzen = [[gka.Text("Sayfa Sayısı", 12), gka.Input(s=12, key='sayfasayisi'), gka.Text("Bekleme Süresi", 12), gka.Input(s=12, key='beklemesuresi')],
         [gka.Button('Sayfa Alanı ve İleri Butonu Belirle', key='sayfaalan'), gka.FileSaveAs('PDF Kayıt Yeri Belirle', key='dosya'), gka.Button('Oluştur', key='olustur')],
         [gka.Text("Ekran Alıntısı İlerleme: ", 20), gka.ProgressBar(100, orientation='h', size=(21, 10), border_width=4, key='ilerleme')],
         [gka.Text("PDF Oluşturucu İlerleme: ", 20), gka.ProgressBar(100, orientation='h', size=(21, 10), border_width=4, key='ilerlemepdf')]]

gka.Popup('Unutmayın! Siz öğrencilere eğitim için her türlü desteği sunmak devletin görevidir. Vergi rekortmenlerinin vergi borçlarını affedip halkını sefalete ve sizleri zorluklara mahkum eden devletin yerine getirmediği görev yüzünden böyle bir yola başvurmanız sizin suçunuz değildir.\n\nTotaliter rejimlerin en büyük korkusu eğitimdir. Bu demektir ki böyle bir ülke ancak ve ancak eğitimle kurtulabilir. Bunu yapacak olan sizlersiniz.', keep_on_top=True)

window = gka.Window('PDFGeçer v2.189_build2022 (C) 2022 libsoykan-dev', duzen)

event, values = window.read()

def kapat_kontrol():
    
    if event == gka.WIN_CLOSED:

        print("Çıkış")
        
        sys.exit()


while True:

    kapat_kontrol()

    pdfdosya = values['dosya']

    syf = int(values['sayfasayisi'])

    sure = int(values['beklemesuresi'])

    if event == 'sayfaalan':

        gka.Popup('Fare işaretçisini sayfanın sol üst köşesine getirdikten sonra ENTER basın.', keep_on_top=True)

        solx = int(mouse.position[0]) * 1.25081433225

        soly = int(mouse.position[1]) * 1.25081433225

        gka.Popup('Fare işaretçisini sayfanın sağ alt köşesine getirdikten sonra ENTER basın.', keep_on_top=True)

        sagx = int(mouse.position[0]) * 1.25081433225

        sagy = int(mouse.position[1]) * 1.25081433225

        gka.Popup('Fare işaretçisini sonraki sayfa okuna getirdikten sonra ENTER basın.', keep_on_top=True)

        tikx = int(mouse.position[0])

        tiky = int(mouse.position[1])

    if event == 'olustur':

        for dongu in range(0, (syf)):

            kapat_kontrol()

            pic = ImageGrab.grab(bbox=(solx, soly, sagx, sagy))

            pic.save(str(dongu) + ".png")

            syfliste.append(str(dongu) + ".png")

            mouse.position = (tikx, tiky)

            mouse.press(Button.left)
    
            mouse.release(Button.left)

            window['ilerleme'].update_bar(int((dongu / syf) * 100))

            time.sleep(sure)

        print("PDF dönüştürme...")

        for pdfsyf in syfliste:

            pdfsay += 1

            pdf.add_page()

            pdf.image(pdfsyf,0,0,210,297)

            window['ilerlemepdf'].update_bar(int((pdfsay / syf) * 100))

        pdf.output(pdfdosya, "F")

        test = os.listdir()

        for item in test:

            if item.endswith(".png"):

                os.remove(item)