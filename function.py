import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix, accuracy_score
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

# file = 'data/data.csv'
# dataset = pd.read_csv(file)

f_stem = StemmerFactory()
stemmer = f_stem.create_stemmer()
f_stop = StopWordRemoverFactory()
getStop = f_stop.get_stop_words()

# hapus kata pada library sastrawi(getstop) supaya ciri clickbaitnya bisa terdeteksi
unwanted_num = {'akankah', 'akhirnya', 'apa', 'apakah', 'bagaimana', 'bagaimanakah', 'begini', 'benarkah', 'berapa', 'berapakah', 'disebut', 'ini', 'kapan','kenapa', 'ketika', 'kok', 'mengapa', 'ungkap', 'wah', 'sebut', 'dimana'}
getStop = [ele for ele in getStop if ele not in unwanted_num]

dictionary = ArrayDictionary(getStop)
stopword = StopWordRemover(dictionary)
vectorizer = TfidfVectorizer()

# proses text preprocessing
def preproLatih(data):
	data = data.lower() # case folding
	data = re.sub(r'([0-9]+)', '', data) # cleaning
	data = re.sub(r'([^a-zA-Z0-9\s]+)', '', data) # cleaning
	data = stopword.remove(data) # stopword removal
	data = stemmer.stem(data) # stemming
	
	return data

def preproUji(data):
	vectorizer_pickle = pickle.load(open('vector_klasifikasi.pkl', 'rb'))
	data = data.lower()
	data = re.sub(r'([0-9]+)', '', data)
	data = re.sub(r'([^a-zA-Z0-9\s]+)', '', data)
	data = stopword.remove(data)
	data = stemmer.stem(data)
	
	# count vectorizer
	data = vectorizer_pickle.transform([data])
	
	return data

# pake kernel linier
# hasil trainnya di simpen pake pickle
def klasifikasiLatih(data):
	label = []
	for i in range(len(data)) :
		if data.loc[i, "Keterangan"] =='Clickbait':
			label.append(1)
		else:
			label.append(0)

	data['label']=label
	data.drop(['Keterangan'], axis=1, inplace=True)
	data.drop_duplicates(subset=['Judul'])

	data_baru = data.copy()

	# fb1 = data_baru[data_baru['label']==0].sample(800,replace=True)
	# fb2 = data_baru[data_baru['label']==1].sample(800,replace=True)
	# data_baru = pd.concat([fb1,fb2])

	hasil_prepro = []
	for index, row in data_baru.iterrows():
		hasil_prepro.append(preproLatih(row["Judul"]))
		
	data_baru["Judul"] = hasil_prepro
	# penggunaan wordcloud u/ mengetahui kata yang sering muncul pada data clickbait
	train_s1 = data_baru[data_baru['label']==1]
	all_text_s1 = ' '.join(word for word in train_s1['Judul'])
	wordcloud = WordCloud(width=2000, height=1000, colormap='Blues', background_color='white', mode='RGBA').generate(all_text_s1)
	plt.figure(figsize=(7,4))
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.margins(x=0, y=0)
	plt.title("Wordcloud")
	plt.savefig('static/images/wordcloud_plot.png')

	# Split the dataset by using the function train_test_split(). you need to pass 3 parameters features, target, and test_set size.
	# Additionally, you can use random_state to select records randomly.
	X_train, X_test, y_train, y_test = train_test_split(data_baru['Judul'], data_baru['label'], test_size=0.2, stratify=data_baru['label'], random_state=30)
	# proses tfidf
	X_train = vectorizer.fit_transform(X_train)
	X_test = vectorizer.transform(X_test)
	pickle.dump(vectorizer, open('vector_klasifikasi.pkl', 'wb'))

	clf = SVC(kernel="linear")
	clf.fit(X_train,y_train)

	pickle.dump(clf, open('model_svm_liniear.pkl', 'wb'))

	return 'static/images/wordcloud_plot.png'

def kLinier(data):
	label = []
	for i in range(len(data)) :
		if data.loc[i, "Keterangan"] =='Clickbait':
			label.append(1)
		else:
			label.append(0)

	data['label']=label
	data.drop(['Keterangan'], axis=1, inplace=True)
	data.drop_duplicates(subset=['Judul'])

	data_baru = data.copy()

	# fb1 = data_baru[data_baru['label']==0].sample(800,replace=True)
	# fb2 = data_baru[data_baru['label']==1].sample(800,replace=True)
	# data_baru = pd.concat([fb1,fb2])

	hasil_prepro = []
	for index, row in data_baru.iterrows():
		hasil_prepro.append(preproLatih(row["Judul"]))
		
	data_baru["Judul"] = hasil_prepro

	# Split the dataset by using the function train_test_split(). you need to pass 3 parameters features, target, and test_set size.
	# Additionally, you can use random_state to select records randomly.
	X_train, X_test, y_train, y_test = train_test_split(data_baru['Judul'], data_baru['label'], test_size=0.2, stratify=data_baru['label'], random_state=30)

	X_train = vectorizer.fit_transform(X_train)
	X_test = vectorizer.transform(X_test)

	liniersclass = SVC(kernel="linear")
	liniersclass.fit(X_train,y_train)
	
	hasil = liniersclass.predict(X_test)

	# predict = clf.predict(X_test)
	tn, fp, fn, tp = confusion_matrix(y_test, hasil).ravel()
	# f1_score
	f1s = f1_score(y_test, hasil)
	percent_f1s = "{:.2%}".format(f1s)
	# print("f1 score hasil prediksi adalah: ", f1s)

	asc = accuracy_score(y_test, hasil)
	percent_asc = "{:.2%}".format(asc)
	# print("accuracy score hasil prediksi adalah: ", asc)

	pcs = precision_score(y_test, hasil)
	percent_pcs = "{:.2%}".format(pcs)
	# print("precision score hasil prediksi adalah: ", pcs)

	rcs = recall_score(y_test, hasil)
	percent_rcs = "{:.2%}".format(rcs)
	# print("recall score hasil prediksi adalah: ", rcs)

	return tn, fp, fn, tp, percent_f1s, percent_asc, percent_pcs, percent_rcs

# if __name__ == '__main__':
# 	klasifikasiLatih(dataset)