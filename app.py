
import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")


working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(os.path.join(working_dir, 'diabetes_model.sav'), 'rb'))
heart_disease_model = pickle.load(open(os.path.join(working_dir, 'heart_disease_model.sav'), 'rb'))
parkinsons_model = pickle.load(open(os.path.join(working_dir, 'parkinsons_model.sav'), 'rb'))
ckd_model = pickle.load(open(os.path.join(working_dir, 'CKD.sav'), 'rb'))

with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Chronic Kidney Disease Prediction'],
        menu_icon='hospital-fill',
        icons=['activity', 'heart', 'person', 'virus'],
        default_index=0)


if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction')
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', '0', help="Number of times the person has been pregnant.")
    with col2:
        Glucose = st.text_input('Glucose Level (mg/dL)', '120', help="Blood glucose level; normal range is < 140 mg/dL.")
    with col3:
        BloodPressure = st.text_input('Blood Pressure (mm Hg)', '70', help="The blood pressure level; normal is < 120/80 mm Hg.")
    with col1:
        SkinThickness = st.text_input('Skin Thickness (mm)', '20', help="Thickness of the skin fold; normal is around 10-20 mm.")
    with col2:
        Insulin = st.text_input('Insulin Level (μU/mL)', '80', help="Insulin level; normal range is 2.6 to 24.9 μU/mL.")
    with col3:
        BMI = st.text_input('BMI (kg/m²)', '28.0', help="Body mass index; normal range is 18.5 to 24.9 kg/m².")
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', '0.5', help="Genetic likelihood of diabetes; range is 0-1.")
    with col2:
        Age = st.text_input('Age', '40', help="Age of the person; typical onset is after 45 years.")

    
    diab_diagnosis = ''
    if st.button('Diabetes Test Result'):
        user_input = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness),
                      float(Insulin), float(BMI), float(DiabetesPedigreeFunction), float(Age)]
        diab_prediction = diabetes_model.predict([user_input])
        diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
    st.success(diab_diagnosis)


if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction')
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age', '50', help="The person's age.")
    with col2:
        sex = st.selectbox('Sex', options=['Male', 'Female'], help="Gender of the person.")
    with col3:
        cp = st.selectbox('Chest Pain Type', options=['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic'],
                          help="Type of chest pain experienced.")
    with col1:
        trestbps = st.text_input('Resting Blood Pressure (mm Hg)', '120', help="Blood pressure when resting; normal < 120/80 mm Hg.")
    with col2:
        chol = st.text_input('Cholesterol (mg/dL)', '200', help="Cholesterol level in the blood; normal < 200 mg/dL.")
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dL', options=[True, False],
                           help="Whether fasting blood sugar level exceeds 120 mg/dL.")
    with col1:
        restecg = st.selectbox('Resting ECG Results', options=['Normal', 'Abnormality', 'Hypertrophy'],
                                help="Results of an ECG at rest.")
    with col2:
        thalach = st.text_input('Max Heart Rate Achieved', '150', help="The highest heart rate achieved during a stress test.")
    with col3:
        exang = st.selectbox('Exercise-Induced Angina', options=[True, False], help="Presence of chest pain induced by exercise.")
    with col1:
        oldpeak = st.text_input('ST Depression', '1.0', help="A measure of exercise-induced changes in heart function; normal is 0.")
    with col2:
        slope = st.selectbox('Slope of Peak ST Segment', options=['Upsloping', 'Flat', 'Downsloping'],
                             help="Shape of the peak segment during a stress test.")
    with col3:
        ca = st.selectbox('Number of Major Vessels (0-3)', options=[0, 1, 2, 3],
                          help="Number of visible vessels using dye.")
    with col1:
        thal = st.selectbox('Thalassemia', options=['Normal', 'Fixed defect', 'Reversible defect'],
                            help="Type of thalassemia present.")

    
    heart_diagnosis = ''
    if st.button('Heart Disease Test Result'):
        
        sex_encoded = 1 if sex == 'Male' else 0
        cp_encoded = {
            'Typical angina': 0,
            'Atypical angina': 1,
            'Non-anginal pain': 2,
            'Asymptomatic': 3
        }[cp]
        restecg_encoded = {
            'Normal': 0,
            'Abnormality': 1,
            'Hypertrophy': 2
        }[restecg]
        slope_encoded = {
            'Upsloping': 0,
            'Flat': 1,
            'Downsloping': 2
        }[slope]
        thal_encoded = {
            'Normal': 0,
            'Fixed defect': 1,
            'Reversible defect': 2
        }[thal]

        user_input = [float(age), sex_encoded, cp_encoded, float(trestbps), float(chol), int(fbs), restecg_encoded,
                      float(thalach), int(exang), float(oldpeak), slope_encoded, int(ca), thal_encoded]
        heart_prediction = heart_disease_model.predict([user_input])
        heart_diagnosis = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
    st.success(heart_diagnosis)



default_parkinsons_values = [
    150,  # MDVP:Fo(Hz)
    200,  # MDVP:Fhi(Hz)
    90,   # MDVP:Flo(Hz)
    0.1,  # MDVP:Jitter(%)
    0.03, # MDVP:Jitter(Abs)
    0.05, # MDVP:RAP
    0.05, # MDVP:PPQ
    0.05, # Jitter:DDP
    0.1,  # MDVP:Shimmer
    0.5,  # MDVP:Shimmer(dB)
    0.5,  # Shimmer:APQ3
    0.5,  # Shimmer:APQ5
    0.5,  # MDVP:APQ
    0.5,  # Shimmer:DDA
    0.1,  # NHR
    30,   # HNR
    0.9,  # RPDE
    0.5,  # DFA
    0.5,  # spread1
    0.5,  # spread2
    0.5,  # D2
    0.5   # PPE
]


if selected == "Parkinsons Prediction":

    
    st.title("Parkinson's Disease Prediction")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)', value=default_parkinsons_values[0], 
                           help="Fundamental frequency of vocal fold vibration (normal range: 130 - 160 Hz)")

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)', value=default_parkinsons_values[1], 
                            help="Maximum fundamental frequency (normal range: 180 - 210 Hz)")
    
    with col3:
        flo = st.text_input('MDVP:Flo(Hz)', value=default_parkinsons_values[2], 
                            help="Minimum fundamental frequency (normal range: 90 - 120 Hz)")
    
    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)', value=default_parkinsons_values[3], 
                                        help="Variation in pitch (normal range: <0.2%)")
    
    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)', value=default_parkinsons_values[4], 
                                    help="Absolute Jitter (normal range: <0.01)")

    with col1:
        RAP = st.text_input('MDVP:RAP', value=default_parkinsons_values[5], 
                            help="Relative Average Perturbation (normal range: <0.2)")
    
    with col2:
        PPQ = st.text_input('MDVP:PPQ', value=default_parkinsons_values[6], 
                            help="Pitch Period Perturbation Quotient (normal range: <0.1)")
    
    with col3:
        DDP = st.text_input('Jitter:DDP', value=default_parkinsons_values[7], 
                            help="Difference of differences of periods (normal range: <0.01)")
    
    with col4:
        Shimmer = st.text_input('MDVP:Shimmer', value=default_parkinsons_values[8], 
                                help="Variation in amplitude (normal range: <0.5)")
    
    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)', value=default_parkinsons_values[9], 
                                    help="Shimmer in decibels (normal range: <0.5)")

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3', value=default_parkinsons_values[10], 
                              help="Amplitude perturbation quotient 3 (normal range: <0.5)")
    
    with col2:
        APQ5 = st.text_input('Shimmer:APQ5', value=default_parkinsons_values[11], 
                              help="Amplitude perturbation quotient 5 (normal range: <0.5)")
    
    with col3:
        APQ = st.text_input('MDVP:APQ', value=default_parkinsons_values[12], 
                             help="Average Amplitude Perturbation Quotient (normal range: <0.5)")
    
    with col4:
        DDA = st.text_input('Shimmer:DDA', value=default_parkinsons_values[13], 
                            help="Difference of Amplitudes (normal range: <0.5)")
    
    with col5:
        NHR = st.text_input('NHR', value=default_parkinsons_values[14], 
                            help="Noise-to-harmonics ratio (normal range: <0.1)")

    with col1:
        HNR = st.text_input('HNR', value=default_parkinsons_values[15], 
                            help="Harmonics-to-noise ratio (normal range: >15 dB)")
    
    with col2:
        RPDE = st.text_input('RPDE', value=default_parkinsons_values[16], 
                             help="Recurrence Period Density Entropy (normal range: >0.5)")
    
    with col3:
        DFA = st.text_input('DFA', value=default_parkinsons_values[17], 
                            help="Detrended Fluctuation Analysis (normal range: >0.5)")
    
    with col4:
        spread1 = st.text_input('spread1', value=default_parkinsons_values[18], 
                                help="Spread measure 1 (normal range: <0.5)")
    
    with col5:
        spread2 = st.text_input('spread2', value=default_parkinsons_values[19], 
                                help="Spread measure 2 (normal range: <0.5)")

    with col1:
        D2 = st.text_input('D2', value=default_parkinsons_values[20], 
                           help="D2 measure (normal range: <2)")
    
    with col2:
        PPE = st.text_input('PPE', value=default_parkinsons_values[21], 
                            help="Pitch period entropy (normal range: >0.5)")


    parkinsons_diagnosis = ''

     
    if st.button("Parkinson's Test Result"):
        
        user_input = [
            fo, fhi, flo, Jitter_percent, Jitter_Abs,
            RAP, PPQ, DDP, Shimmer, Shimmer_dB, 
            APQ3, APQ5, APQ, DDA, NHR, HNR, 
            RPDE, DFA, spread1, spread2, D2, PPE
        ]

        user_input = [float(x) for x in user_input]  

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has Parkinson's disease"
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"

    st.success(parkinsons_diagnosis)

    
    
default_ckd_values = [1, 120, 15, 0, 0, 0, 0, 14, 1.02, 45, 5.5, 0]

if selected == "Chronic Kidney Disease Prediction":
    
    st.title("Chronic Kidney Disease Prediction")
    col1, col2, col3 = st.columns(3)

    with col1:
        pus_cell = st.text_input('pus_cell (1 for normal, 0 for abnormal)', value=str(default_ckd_values[0]), help="Normal: 1; Indicates presence of pus cells in urine.")
    with col2:
        blood_glucose_random = st.text_input('blood_glucose_random', value=str(default_ckd_values[1]), help="Normal range: < 200 mg/dL; Random blood glucose level.")
    with col3:
        blood_urea = st.text_input('blood_urea', value=str(default_ckd_values[2]), help="Normal range: 7-20 mg/dL; Indicates kidney function.")

    with col1:
        pedal_edema = st.text_input('pedal_edema (1 for yes, 0 for no)', value=str(default_ckd_values[3]), help="Normal: 0; Indicates swelling in the legs.")
    with col2:
        anemia = st.text_input('anemia (1 for yes, 0 for no)', value=str(default_ckd_values[4]), help="Normal: 0; Indicates presence of anemia.")
    with col3:
        diabetesmellitus = st.text_input('diabetesmellitus (1 for yes, 0 for no)', value=str(default_ckd_values[5]), help="Normal: 0; Indicates presence of diabetes.")

    with col1:
        hypertension = st.text_input('hypertension (1 for yes, 0 for no)', value=str(default_ckd_values[6]), help="Normal: 0; Indicates presence of high blood pressure.")
    with col2:
        hemoglobin = st.text_input('hemoglobin', value=str(default_ckd_values[7]), help="Normal range: 13.5-17.5 g/dL; Measures oxygen-carrying capacity.")
    with col3:
        specific_gravity = st.text_input('specific_gravity', value=str(default_ckd_values[8]), help="Normal range: 1.005 - 1.030; Indicates concentration of urine.")

    with col1:
        packed_cell_volume = st.text_input('packed_cell_volume', value=str(default_ckd_values[9]), help="Normal range: 40%-54%; Indicates the volume of red blood cells.")
    with col2:
        red_blood_cell_count = st.text_input('red_blood_cell_count', value=str(default_ckd_values[10]), help="Normal range: 4.5-6.0 million cells/mcL; Counts red blood cells in blood.")
    with col3:
        appetite = st.text_input('appetite (1 for poor, 0 for good)', value=str(default_ckd_values[11]), help="Normal: 0; Indicates presence of poor appetite.")

    
    CKD_diagnosis = ''

      
    if st.button("CKD's Test Result"):
        user_input = [float(pus_cell), float(blood_glucose_random), float(blood_urea),
                      float(pedal_edema), float(anemia), float(diabetesmellitus), float(hypertension), 
                      float(hemoglobin), float(specific_gravity), float(packed_cell_volume), 
                      float(red_blood_cell_count), float(appetite)]

        ckd_prediction = ckd_model.predict([user_input])

        if ckd_prediction[0] == 1:
            CKD_diagnosis = "The person has Chronic Kidney disease"
        else:
            CKD_diagnosis = "The person does not have Chronic Kidney disease"

    st.success(CKD_diagnosis)
