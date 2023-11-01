from flask import Flask, render_template, request

app = Flask(__name__)

import pickle
import os

# Memuat model dari file pickle
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def combine_certainty_factors(cf1, cf2):
    # Menggabungkan faktor kepastian secara kombinatif
    combined_cf = cf1 + (cf2 * (1 - cf1))
    return combined_cf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html')

@app.route('/informasi')
def informasi():
    return render_template('info-penyakit/all.html')

@app.route('/informasi/<string:name>')
def detail_informasi(name):
    return render_template('info-penyakit/' + name + '.html')

@app.route('/pencegahan')
def pencegahan():
    return render_template('pencegahan.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Mendapatkan nilai checkbox dari request

    kulit_menggumpal_value = request.form.get('kulit_menggumpal', '0')
    kulit_menggumpal = int(kulit_menggumpal_value) if kulit_menggumpal_value else 0

    kulit_memerah_value = request.form.get('kulit_memerah', '0')
    kulit_memerah = int(kulit_memerah_value) if kulit_memerah_value else 0

    luka_melingkar_value = request.form.get('luka_melingkar', '0')
    luka_melingkar = int(luka_melingkar_value) if luka_melingkar_value else 0

    kulit_berkerak_value = request.form.get('kulit_berkerak', '0')
    kulit_berkerak = int(kulit_berkerak_value) if kulit_berkerak_value else 0

    bintik_pasir_hitam = request.form.get('bintik_pasir_hitam', '0')
    bintik_pasir_hitam = int(bintik_pasir_hitam) if bintik_pasir_hitam else 0 

    bintik_pasir_abu = request.form.get('bintik_pasir_abu', '0')
    bintik_pasir_abu = int(bintik_pasir_abu) if bintik_pasir_abu else 0 

    kutu = request.form.get('kutu', '0')
    kutu = int(kutu) if kutu else 0 

    bulu_rontok = request.form.get('bulu_rontok', '0')
    bulu_rontok = int(bulu_rontok) if bulu_rontok else 0 

    telinga_berkerak = request.form.get('telinga_berkerak', '0')
    telinga_berkerak = int(telinga_berkerak) if telinga_berkerak else 0 

    kebotakan = request.form.get('kebotakan', '0')
    kebotakan = int(kebotakan) if kebotakan else 0 

    bulu_berminyak = request.form.get('bulu_berminyak', '0')
    bulu_berminyak = int(bulu_berminyak) if bulu_berminyak else 0 

    bercak_pd_ekor = request.form.get('bercak_pd_ekor', '0')
    bercak_pd_ekor = int(bercak_pd_ekor) if bercak_pd_ekor else 0 

    menggaruk = request.form.get('menggaruk', '0')
    menggaruk = int(menggaruk) if menggaruk else 0 

    aroma = request.form.get('aroma', '0')
    aroma = int(aroma) if aroma else 0 


    # Menentukan faktor kepastian untuk setiap atribut
    certainty_factors = {
        'kulit_menggumpal': 0.8,
        'kulit_memerah': 0.6,
        'luka_melingkar': 0.7,
        'kulit_berkerak': 0.9,
        'bintik_pasir_hitam': 0.5,
        'bintik_pasir_abu': 0.4,
        'kutu': 0.6,
        'bulu_rontok': 0.7,
        'telinga_berkerak': 0.8,
        'kebotakan': 0.3,
        'ekor_berminyak': 0.6,
        'bercak_pd_ekor': 0.4,
        'menggaruk': 0.5,
        'aroma': 0.2
    }
    
    # Membuat input pengguna berdasarkan nilai checkbox
    user_input = {
        'kulit_menggumpal': kulit_menggumpal,
        'kulit_memerah': kulit_memerah,
        'luka_melingkar': luka_melingkar,
        'kulit_berkerak': kulit_berkerak,
        'bintik_pasir_hitam': bintik_pasir_hitam,
        'bintik_pasir_abu': bintik_pasir_abu,
        'kutu': kutu,
        'bulu_rontok': bulu_rontok,
        'telinga_berkerak': telinga_berkerak,
        'kebotakan': kebotakan,
        'ekor_berminyak': bulu_berminyak,
        'bercak_pd_ekor': bercak_pd_ekor,
        'menggaruk': menggaruk,
        'aroma': aroma
    }
    if request.form.get('kulit_menggumpal_ya'):
        user_input['kulit_menggumpal'] = 1

    if request.form.get('kulit_menggumpal_tidak'):
        user_input['kulit_menggumpal'] = 0

    if request.form.get('kulit_memerah_ya'):
        user_input['kulit_memerah'] = 1

    if request.form.get('kulit_memerah_tidak'):
        user_input['kulit_memerah'] = 0

    if request.form.get('luka_melingkar_ya'):
        user_input['luka_melingkar'] = 1

    if request.form.get('luka_melingkar_tidak'):
        user_input['luka_melingkar'] = 0

    if request.form.get('kulit_berkerak_ya'):
        user_input['kulit_berkerak'] = 1

    if request.form.get('kulit_berkerak_tidak'):
        user_input['kulit_berkerak'] = 0

    if request.form.get('bintik_pasir_hitam_ya'):
        user_input['bintik_pasir_hitam'] = 1

    if request.form.get('bintik_pasir_hitam_tidak'):
        user_input['bintik_pasir_hitam'] = 0

    if request.form.get('bintik_pasir_abu_ya'):
        user_input['bintik_pasir_abu'] = 1

    if request.form.get('bintik_pasir_abu_tidak'):
        user_input['bintik_pasir_abu'] = 0

    if request.form.get('kutu_ya'):
        user_input['kutu'] = 1

    if request.form.get('kutu_tidak'):
        user_input['kutu'] = 0 

    if request.form.get('bulu_rontok_ya'):
        user_input['bulu_rontok'] = 1

    if request.form.get('bulu_rontok_tidak'):
        user_input['bulu_rontok'] = 0 

    if request.form.get('telinga_berkerak_ya'):
        user_input['telinga_berkerak'] = 1

    if request.form.get('telinga_berkerak_tidak'):
        user_input['telinga_berkerak'] = 0

    if request.form.get('kebotakan_ya'):
        user_input['kebotakan'] = 1

    if request.form.get('kebotakan_tidak'):
        user_input['kebotakan'] = 0

    if request.form.get('ekor_berminyak_ya'):
        user_input['ekor_berminyak'] = 1

    if request.form.get('ekor_berminyak_tidak'):
        user_input['ekor_berminyak'] = 0

    if request.form.get('bercak_pd_ekor_ya'):
        user_input['bercak_pd_ekor'] = 1

    if request.form.get('bercak_pd_ekor_tidak'):
        user_input['bercak_pd_ekor'] = 0

    if request.form.get('menggaruk_ya'):
        user_input['menggaruk'] = 1

    if request.form.get('menggaruk_tidak'):
        user_input['menggaruk'] = 0

    if request.form.get('aroma_ya'):
        user_input['aroma'] = 

    if request.form.get('aroma_tidak'):
        user_input['aroma'] = 0

    # Melakukan prediksi menggunakan model C4.5
    prediction = model.predict([list(user_input.values())])
    
    # Menghitung bobot hasil prediksi menggunakan faktor kepastian
    instance_prediction = {**user_input, 'hasil': prediction[0]}
    weight = sum([val * certainty_factors[attr] for attr, val in instance_prediction.items() if attr != 'hasil'])
    

    #Kirim hasil prediksi dan bobotnya ke halaman HTML
    disease_name = prediction[0]
    disease_name = disease_name.replace(' ', '-').lower()

    # cf combine
    combined_cf = 0
    for objs in user_input.items():
        if (objs[1] == 1): 
            combined_cf = combine_certainty_factors(combined_cf, certainty_factors[objs[0]])


    if disease_name + '.html' in os.listdir('templates/info-penyakit') and 0.6 <= weight <= 3.7:
        return render_template('info-penyakit/' + disease_name + '.html', weight=weight, combined_cf=combined_cf, prediction_page=True)
    else:
        return render_template('info-penyakit/' + 'notfound.html')


    
if __name__ == '__main__':
    app.run(debug=True)
