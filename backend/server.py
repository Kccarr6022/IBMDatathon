from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import tensorflow

# init app
basedir = os.path.abspath(os.path.dirname(__file__))  # base directory
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db and ma
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database classes
class SYMPTOMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100))
    symptom_value = db.Column(db.String(100))

    def __init__(self, id, symptom, value):
        self.id = id
        self.symptom = symptom
        self.symptom_value = value

class CLIENTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    symptoms_table = db.Column(db.Integer)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class CLIENTSYMPTOMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100))

    def __init__(self, id, symptom):
        self.id = id
        self.symptom = symptom


# Database schemas
class SymptomSchema(ma.Schema):
    class Meta: # symptom number, symptom, symptom value
        fields = ('id', 'symptom', 'symptom_value')

class ClientSchema(ma.Schema):
    class Meta: # client id, name
        fields = ('id', 'name')

class ClientSymptomSchema(ma.Schema):
    class Meta: # client id, symptom
        fields = ('id', 'symptom')


# Init schema
symptom_schema = SymptomSchema()
symptoms_schema = SymptomSchema(many=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

client_symptom_schema = ClientSymptomSchema()
client_symptoms_schema = ClientSymptomSchema(many=True)

# Data
"""
0,itching,1
1,skin_rash,3
2,nodal_skin_eruptions,4
3,continuous_sneezing,4
4,shivering,5
5,chills,3
6,joint_pain,3
7,stomach_pain,5
8,acidity,3
9,ulcers_on_tongue,4
10,muscle_wasting,3
11,vomiting,5
12,burning_micturition,6
13,spotting_urination,6
14,fatigue,4
15,weight_gain,3
16,anxiety,4
17,cold_hands_and_feets,5
18,mood_swings,3
19,weight_loss,3
20,restlessness,5
21,lethargy,2
22,patches_in_throat,6
23,irregular_sugar_level,5
24,cough,4
25,high_fever,7
26,sunken_eyes,3
27,breathlessness,4
28,sweating,3
29,dehydration,4
30,indigestion,5
31,headache,3
32,yellowish_skin,3
33,dark_urine,4
34,nausea,5
35,loss_of_appetite,4
36,pain_behind_the_eyes,4
37,back_pain,3
38,constipation,4
39,abdominal_pain,4
40,diarrhoea,6
41,mild_fever,5
42,yellow_urine,4
43,yellowing_of_eyes,4
44,acute_liver_failure,6
45,fluid_overload,6
46,swelling_of_stomach,7
47,swelled_lymph_nodes,6
48,malaise,6
49,blurred_and_distorted_vision,5
50,phlegm,5
51,throat_irritation,4
52,redness_of_eyes,5
53,sinus_pressure,4
54,runny_nose,5
55,congestion,5
56,chest_pain,7
57,weakness_in_limbs,7
58,fast_heart_rate,5
59,pain_during_bowel_movements,5
60,pain_in_anal_region,6
61,bloody_stool,5
62,irritation_in_anus,6
63,neck_pain,5
64,dizziness,4
65,cramps,4
66,bruising,4
67,obesity,4
68,swollen_legs,5
69,swollen_blood_vessels,5
70,puffy_face_and_eyes,5
71,enlarged_thyroid,6
72,brittle_nails,5
73,swollen_extremeties,5
74,excessive_hunger,4
75,extra_marital_contacts,5
76,drying_and_tingling_lips,4
77,slurred_speech,4
78,knee_pain,3
79,hip_joint_pain,2
80,muscle_weakness,2
81,stiff_neck,4
82,swelling_joints,5
83,movement_stiffness,5
84,spinning_movements,6
85,loss_of_balance,4
86,unsteadiness,4
87,weakness_of_one_body_side,4
88,loss_of_smell,3
89,bladder_discomfort,4
90,foul_smell_ofurine,5
91,continuous_feel_of_urine,6
92,passage_of_gases,5
93,internal_itching,4
94,toxic_look_(typhos),5
95,depression,3
96,irritability,2
97,muscle_pain,2
98,altered_sensorium,2
99,red_spots_over_body,3
100,belly_pain,4
101,abnormal_menstruation,6
102,dischromic_patches,6
103,watering_from_eyes,4
104,increased_appetite,5
105,polyuria,4
106,family_history,5
107,mucoid_sputum,4
108,rusty_sputum,4
109,lack_of_concentration,3
110,visual_disturbances,3
111,receiving_blood_transfusion,5
112,receiving_unsterile_injections,2
113,coma,7
114,stomach_bleeding,6
115,distention_of_abdomen,4
116,history_of_alcohol_consumption,5
118,blood_in_sputum,5
119,prominent_veins_on_calf,6
120,palpitations,4
121,painful_walking,2
122,pus_filled_pimples,2
123,blackheads,2
124,scurring,2
125,skin_peeling,3
126,silver_like_dusting,2
127,small_dents_in_nails,2
128,inflammatory_nails,2
129,blister,4
130,red_sore_around_nose,2
131,yellow_crust_ooze,3
132,prognosis,5


symptom = SYMPTOMS(17, "Cold Hands and Feet", "cold_hands_and_feets")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(18, "Mood Swings", "mood_swings")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(19, "Weight Loss", "weight_loss")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(20, "Restlessness", "restlessness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(21, "Lethargy", "lethargy")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(22, "Patches in Throat", "patches_in_throat")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(23, "Irregular Sugar Level", "irregular_sugar_level")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(24, "Cough", "cough")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(25, "High Fever", "high_fever")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(26, "Sunken Eyes", "sunken_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(27, "Breathlessness", "breathlessness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(28, "Sweating", "sweating")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(29, "Dehydration", "dehydration")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(30, "Indigestion", "indigestion")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(31, "Headache", "headache")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(32, "Yellowish Skin", "yellowish_skin")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(33, "Dark Urine", "dark_urine")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(34, "Nausea", "nausea")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(35, "Loss of Appetite", "loss_of_appetite")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(36, "Pain behind the Eyes", "pain_behind_the_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(37, "Back Pain", "back_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(38, "Constipation", "constipation")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(39, "Abdominal Pain", "abdominal_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(40, "Diarrhoea", "diarrhoea")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(41, "Mild Fever", "mild_fever")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(42, "Yellow Urine", "yellow_urine")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(43, "Yellowing of Eyes", "yellowing_of_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(44, "Acute Liver Failure", "acute_liver_failure")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(45, "Fluid Overload", "fluid_overload")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(46, "Swelling of Stomach", "swelling_of_stomach")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(47, "Swelled Lymph Nodes", "swelled_lymph_nodes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(48, "Malaise", "malaise")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(49, "Blurred and Distorted Vision", "blurred_and_distorted_vision")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(50, "Phlegm", "phlegm")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(51, "Throat Irritation", "throat_irritation")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(52, "Redness of Eyes", "redness_of_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(53, "Sinus Pressure", "sinus_pressure")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(54, "Runny Nose", "runny_nose")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(55, "Congestion", "congestion")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(56, "Chest Pain", "chest_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(57, "Weakness in Limbs", "weakness_in_limbs")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(58, "Fast Heart Rate", "fast_heart_rate")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(59, "Pain during Bowel Movements", "pain_during_bowel_movements")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(60, "Pain in Anal Region", "pain_in_anal_region")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(61, "Bloody Stool", "bloody_stool")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(62, "Irritation in Anus", "irritation_in_anus")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(63, "Neck Pain", "neck_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(64, "Dizziness", "dizziness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(65, "Cramps", "cramps")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(66, "Bruising", "bruising")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(67, "Obesity", "obesity")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(68, "Swollen Legs", "swollen_legs")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(69, "Swollen Blood Vessels", "swollen_blood_vessels")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(70, "Puffy Face and Eyes", "puffy_face_and_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(71, "Enlarged Thyroid", "enlarged_thyroid")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(72, "Brittle Nails", "brittle_nails")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(73, "Swollen Extremeties", "swollen_extremeties")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(74, "Excessive Hunger", "excessive_hunger")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(75, "Extra Marital Contacts", "extra_marital_contacts")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(76, "Drying and Tingling Lips", "drying_and_tingling_lips")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(77, "Slurred Speech", "slurred_speech")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(78, "Knee Pain", "knee_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(79, "Hip Joint Pain", "hip_joint_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(80, "Muscle Weakness", "muscle_weakness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(81, "Stiff Neck", "stiff_neck")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(82, "Swelling Joints", "swelling_joints")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(83, "Movement Stiffness", "movement_stiffness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(84, "Spinning Movements", "spinning_movements")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(85, "Loss of Balance", "loss_of_balance")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(86, "Unsteadiness", "unsteadiness")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(87, "Weakness of One Body Side", "weakness_of_one_body_side")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(88, "Loss of Smell", "loss_of_smell")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(89, "Bladder Discomfort", "bladder_discomfort")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(90, "Foul Smell of Urine", "foul_smell_of_urine")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(91, "Continuous Feel of Urine", "continuous_feel_of_urine")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(92, "Passage of Gases", "passage_of_gases")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(93, "Internal Itching", "internal_itching")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(94, "Toxic Look (Typhos)", "toxic_look_(typhos)")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(95, "Depression", "depression")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(96, "Irritability", "irritability")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(97, "Muscle Pain", "muscle_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(98, "Altered Sensorium", "altered_sensorium")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(99, "Red Spots Over Body", "red_spots_over_body")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(100, "Belly Pain", "belly_pain")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(101, "Abnormal Menstruation", "abnormal_menstruation")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(102, "Dischromic Patches", "dischromic_patches")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(103, "Watering from Eyes", "watering_from_eyes")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(104, "Increased Appetite", "increased_appetite")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(105, "Polyuria", "polyuria")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(106, "Family History", "family_history")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(107, "Mucoid Sputum", "mucoid_sputum")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(108, "Rusty Sputum", "rusty_sputum")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(109, "Lack of Concentration", "lack_of_concentration")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(110, "Visual Disturbances", "visual_disturbances")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(111, "Receiving Blood Transfusion", "receiving_blood_transfusion")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(112, "Receiving Unsterile Injections", "receiving_unsterile_injections")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(113, "Coma", "coma")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(114, "Stomach Bleeding", "stomach_bleeding")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(115, "Distention of Abdomen", "distention_of_abdomen")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(116, "History of Alcohol Consumption", "history_of_alcohol_consumption")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(117, "Fluid Overload", "fluid_overload")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(118, "Blood in Sputum", "blood_in_sputum")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(119, "Prominent Veins on Calf", "prominent_veins_on_calf")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(120, "Palpitations", "palpitations")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(121, "Painful Walking", "painful_walking")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(122, "Pus Filled Pimples", "pus_filled_pimples")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(123, "Blackheads", "blackheads")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(124, "Scurring", "scurring")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(125, "Skin Peeling", "skin_peeling")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(126, "Silver Like Dusting", "silver_like_dusting")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(127, "Small Dents in Nails", "small_dents_in_nails")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(128, "Inflammatory Nails", "inflammatory_nails")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(129, "Blister", "blister")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(130, "Red Sore Around Nose", "red_sore_around_nose")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(131, "Yellow Crust Ooze", "yellow_crust_ooze")
db.session.add(symptom)
db.session.commit()

symptom = SYMPTOMS(132, "Prognosis", "prognosis")
db.session.add(symptom)
db.session.commit()

"""


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/test')
def test():
    #import data from SQL
    symptoms = SYMPTOMS.query.order_by(SYMPTOMS.symptom).all() 
    #sort data alphabetically
    symptoms.sort(key=lambda x: x.symptom)

    return render_template('test.html', data = symptoms)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)