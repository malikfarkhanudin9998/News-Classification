from flask import (Flask, render_template, request, Response, redirect)
from function import (klasifikasiLatih, preproUji, kLinier)
import pickle
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
# from werkzeug.utils import secure_filename
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import io

app = Flask(__name__)
# baca data untuk ditampilin saja
data_latih = 'data/data_copy.csv' #data_copy = data hasil revisi
data_uji = 'data/dataujiv2.csv'

# baca data untuk proses training dan proses klasifikasi
def baca_latih():
	dataset_latih = pd.read_csv('data/data_copy.csv')
	return dataset_latih

def baca_uji():
	dataset_uji = pd.read_csv('data/dataujiv2.csv')
	return dataset_uji

# show dashboard
@app.route('/')
def index():
	return render_template('index.html')

# show data latih
@app.route('/data')
def show_data():
	kosong = []
	with open(data_latih) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		next(csv_reader, None)
		for row in csv_reader:
			kosong.append(row)
	csv_file.close()
	
	return render_template('data.html', data=kosong)

# show klasifikasi
@app.route('/klasifikasi', methods=['GET', 'POST'])
def show_klasifikasi():
	if request.method == 'POST':
		# file = pd.read_csv('data/data.csv')
		dataset_latih = baca_latih()
		tes = klasifikasiLatih(dataset_latih)

		return render_template('klasifikasi.html', url=tes)
	
	return render_template('klasifikasi.html')

# show cek klasifikasi, u/ mengklasifikasikan data baru pada form
@app.route('/cek_judul', methods=['GET', 'POST'])
def show_cek_judul():
	# model = pickle.load(open('clf.pkl', 'rb'))
	if request.method == 'POST':
		# return 'berul' + request.form['judul']
		# judul = request.form['email']
		judul = request.form['judul']

		if 'judul' not in request.form:
			return redirect(request.url)

		klasifikasi = proses_predict(preproUji(judul))
		if klasifikasi == 1:
			hasil_klasifikasi = 'Clickbait'
		else:
			hasil_klasifikasi = 'Non Clickbait'
		return render_template('cek_judul.html',judul=judul, hasil_klasifikasi=hasil_klasifikasi)
	
	return render_template('cek_judul.html')

# show klasifikasi data uji
@app.route('/klasifikasi_uji', methods=['GET', 'POST'])
def show_klasifikasi_uji():
	data = []
	with open(data_uji) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		next(csv_reader, None)
		for row in csv_reader:
			data.append(row)
	csv_file.close()
	
	return render_template('klasifikasi_uji.html', data=data)

# predict data uji
@app.route('/predict', methods=['GET', 'POST'])
def predict():
	# model = pickle.load(open('model_svm_liniear.pkl', 'rb'))
	dataset_uji = baca_uji()
	if request.method == 'POST':
		hasil_predict = []
		hasil_predict_2 = []
		label = []
		for index, row in dataset_uji.iterrows():
			hasil_predict.append(preproUji(row['Judul']))

		dataset_uji['Hasil'] = hasil_predict

		for index, row in dataset_uji.iterrows():
			hasil_predict_2.append(proses_predict(row['Hasil']))

		dataset_uji['Hasil'] = hasil_predict_2

		for i in range(len(dataset_uji)) :
			if dataset_uji.loc[i, "Hasil"] ==[1]:
				label.append('Clickbait')
			else:
				label.append('Non Clickbait')

		dataset_uji['Hasil']=label
		gdata = dataset_uji['Hasil'].value_counts()
		mylabels = ["Non clickbait", "Clickbait"]
		mycolors = ["cyan", "beige"]
		myexplode = [0, 0.1]
		wp = { 'linewidth' : 1, 'edgecolor' : "black" }
		# def func(pct, allvalues):
		# 	absolute = int(pct / 100.*np.sum(allvalues))
		# 	return "{:.1f}%\n{:d} Data".format(pct, absolute)

		plt.subplots(figsize =(7, 4))
		plt.pie(gdata, labels=mylabels, startangle = 90, autopct='%.1f%%',colors = mycolors,explode = myexplode, shadow = True, wedgeprops = wp)
		plt.legend(title = "Hasil Klasifikasi:")
		plt.title("Klasifikasi Data Uji")
		plt.savefig('static/images/new_plot.png')

		asw = dataset_uji.values.tolist()
		return render_template('hasil_klasifikasi.html',judul=asw, url='static/images/new_plot.png')
	
	return render_template('klasifikasi.html')

# proses predict pake pickle
def proses_predict(data):
	model = pickle.load(open('model_svm_liniear.pkl', 'rb'))
	data = model.predict(data)
	
	return data

# show akurasi
@app.route('/akurasi', methods=['GET', 'POST'])
def show_akurasi():
	if request.method == 'POST':
		file = baca_latih()
		tn, fp, fn, tp, percent_f1s, percent_asc, percent_pcs, percent_rcs = kLinier(file)
		
		return render_template('akurasi.html',tn=tn,fp=fp,fn=fn,tp=tp, f1s=percent_f1s, asc=percent_asc, pcs=percent_pcs,rcs=percent_rcs)
	
	return render_template('akurasi.html')

@app.errorhandler(401)
def page_not_found(e):
	return render_template('401.html'), 401

if __name__ == '__main__':
	app.run(debug=True)