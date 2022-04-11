from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd

sc = []

def Detik():
	url_detik = requests.get('https://www.detik.com/terpopuler?tag_from=wp_cb_mostPopular_more')
	soup_detik = BeautifulSoup(url_detik.text, 'lxml')
	links = soup_detik.find_all('div', class_='media__text')

	for link in links:
		text = link.text
		bt = text.replace("Berita Terpopuler", "")
		bts = bt.replace("Berita Terpopuler Sepekan", "")
		fb = bts.replace("Foto Bisnis", "")
		fh = fb.replace("Foto Health", "")
		fi = fh.replace("FotoINET", "")
		fn = fi.replace("Foto News", "")
		fo = fn.replace("Foto Oto", "")
		ft = fo.replace("Foto Travel", "")
		fs = ft.replace("Food Spot", "")
		g = fs.replace("Gerakan", "")
		gf = g.replace("Galeri Foto", "")
		i = gf.replace('Infografis', '')
		ru1 = i.replace("Round-Up", "")
		ru2 = ru1.replace("Round Up", "")
		ru3 = ru2.replace('Round-up', '')
		rug = ru3.replace("ROUND-UP", "")
		sp = rug.replace('Sudut Pandang', '')
		tk = sp.replace("Terpopuler Kemarin", "")
		tmikj = tk.replace("Tren Mie Instan Korea & Jepang", "")
		enter = tmikj.replace("\n", " ")
		wspace = enter.strip()
		space = wspace.replace("  ", "#")
		split = space.split("#")

		sc.append([split[0]])

def Kompas():
	url_kompas = requests.get('https://www.kompas.com')
	soup_kompas = BeautifulSoup(url_kompas.text, 'lxml')

	links = soup_kompas.find_all('div', class_='article__list clearfix')
	for link in links:	
		text = link.text
		enter = text.replace("\n", " ")
		wspace = enter.strip()
		space = wspace.replace("  ", "#")
		split = space.split("#")

		sc.append([split[0]])
	return sc

def Merdeka():
	url_merdeka = requests.get('https://www.merdeka.com')
	soup_merdeka = BeautifulSoup(url_merdeka.text, 'lxml')
	
	links = soup_merdeka.find_all('div', class_='mdk-link-image')

	for link in links:
		text = link.text
		wspace = text.strip()
		enter = wspace.replace("\n", " ")
		space = enter.replace("  ", "#")
		split = space.split("#")

		sc.append([split[0]])

def Tribun():
	url_tribun = requests.get('https://www.tribunnews.com/news')
	soup_tribun = BeautifulSoup(url_tribun.text, 'lxml')

	links = soup_tribun.find_all('li', class_='p1520 art-list pos_rel')

	for link in links:
		text = link.text
		apb = text.replace("Aksi Penanggulangan Bencana", "")
		akp = apb.replace("Aktivis KAMI Ditangkap", "")
		bc = akp.replace('Bursa Capres', '')
		bt = bc.replace('Buku Tematik', '')
		bv = bt.replace("Berita Viral", "")
		c2 = bv.replace("CPNS 2021", "")
		cpt = c2.replace('Calon Panglima TNI', '')
		egm = cpt.replace("Erupsi Gunung Merapi", "")
		gdpd = egm.replace("Gejolak di Partai Demokrat", "")
		hb = gdpd.replace("Hari Bhayangkara", "")
		iml = hb.replace("Imlek 2021", "")
		idatdm = iml.replace('Ibu dan Anak Tewas di Mobil', '')
		ka = idatdm.replace("Kasus Asabri", "")
		kbdp = ka.replace('Kelompok Bersenjata di Papua', '')
		kda = kbdp.replace("Konflik di Afghanistan", "")
		kdc = kda.replace("Kasus Djoko Tjandra", "")
		kj = kdc.replace("Kasus Jiwasraya", "")
		km = kj.replace("Krisis Myanmar", "")
		kmdars = km.replace("Kerumunan Massa di Acara Rizieq Shihab", "")
		kn = kmdars.replace("Kasus Nurhadi", "")
		kp = kn.replace("Kartu Prakerja", "")
		kp2 = kp.replace("Kartu PraKerja", "")
		kpk = kp2.replace("Kartu Pra Kerja", "")
		lk = kpk.replace('Lowongan Kerja', '')
		mm = lk.replace("Merapi Meletus", "")
		omk = mm.replace("OTT Menteri KKP", "")
		ps = omk.replace("Pilkada Serentak", "")
		pbkp = ps.replace("PNL Beri Keringanan Pelanggan", "")
		pbtdisj = pbkp.replace("Polemik Bupati Terpilih di Sabu Raijua", "")
		p2024 = pbtdisj.replace("Pemilu 2024", "")
		pfm = p2024.replace("Prof Firmanzah Meninggal", "")
		phkdij = pfm.replace("Pesawat Hilang Kontak di Intan Jaya", "")
		pc = phkdij.replace("Penanganan Covid", "")
		pcor = pc.replace("Penanganan Corona", "")
		pcu = pcor.replace("Prakiraan Cuaca", "")
		pdt = pcu.replace('Penembakan di Tangerang', '')
		pcuhi = pdt.replace("Prakiraan Cuaca Hari Ini", "")
		psaj = pcuhi.replace("Pesawat Sriwijaya Air Jatuh", "")
		psdr = psaj.replace("Pembunuhan Sadis di Rembang", "")
		pt2 = psdr.replace('Paralimpiade Tokyo 2020', '')
		ptt = pt2.replace("Penangkapan Terduga Teroris", "")
		pxp = ptt.replace("PON XX Papua", "")
		s21 = pxp.replace("SNMPTN 2021", "")
		spdk = s21.replace("Seleksi Kepegawaian di KPK", "")
		tu = spdk.replace("Telco Update", "")
		tl = tu.replace("Tilang Elektronik", "")
		tpudd = tl.replace("Transaksi Pakai Uang Dinar Dirham", "")
		ttd = tpudd.replace("Terduga Teroris Ditangkap", "")
		uk = ttd.replace("Ujaran Kebencian", "")
		vc = uk.replace("Virus Corona", "")
		ymkjt = vc.replace('Youtuber Muhammad Kece Jadi Tersangka', '')
			
		regex = re.compile(r'[\n\r\t]')
		s = regex.sub(" ", ymkjt)
		wsp = s.strip()
		space = wsp.replace("  ", "#")
		split = space.split("#")
		without_empty_strings = []
		for string in split:
			if (string != ""):
				without_empty_strings.append(string)
		sc.append([without_empty_strings[0]])

if __name__ == '__main__':
	Detik()
	Kompas()
	Merdeka()
	Tribun()
	df = pd.DataFrame(sc, columns=['Judul'])
	df.to_csv('data_baru.csv', index=False)