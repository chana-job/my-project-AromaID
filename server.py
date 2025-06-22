import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from datetime import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib

import os
from befor_filter_klaman import estimate_q_r_from_excel
from data_excel import save_to_deta_set, save_to_data_set_filter, save_to_trained_models, save_to_filter_models, \
     save_scaler
from data_sql import query_test, get_user_by_credentials, save_model_and_scaler, add_excel_file, add_filtered_file, \
    get_original_file_paths, get_last_excel_file_id_by_user, get_user_by_id, user_has_existing_file, \
    load_model_by_user_id, load_model_and_scaler_path_by_user, load_trained_model, load_filter_params, save_kalman_paths_to_db, \
    load_kalman_model_path, load_kalman_models
from filter_kalman import apply_filter_to_sensor_data, apply_kalman_to_row
from linear_regression import predict_single_row, predict_single_sample
from linear_regression_from_usb import liner
from Health_checks import validate_excel

app = Flask(__name__)
app.secret_key = 'g9X2$kP!3zT#v8Ld@7sQwE1cRbY0NmFu'
app.config.update(
    SESSION_COOKIE_SECURE=False,     # שולח רק ב-HTTPS
    SESSION_COOKIE_SAMESITE='Lax', # מאפשר לשלוח cookie גם לבקשות חוצות דומיין
    SESSION_COOKIE_HTTPONLY=True    # מונע גישה ל-cookie דרך JS (המלצה)
)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173"])


# נקודת כניסה בסיסית לשרת
@app.route('/')
def index():
    return 'Smell Classifier Server is running.'


@app.route('/auth/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        # שליפת פרטי המשתמש מה-DB לפי user_id
        user = get_user_by_id(user_id=user_id)
        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



#כניסה - שם משתמש וסיסמא
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("data received:", data)
        username = data.get('username')
        password = data.get('password')
        print("username:", username, "password:", password)

        user = get_user_by_credentials(username, password)
        print("user:", user)

        if user:
            #שמירה של המשתמש עבור זמן השימוש שלו באתר
            session['user_id'] = user['user_id']
            print("session")
            print(session['user_id'])
            return jsonify({'success': True, 'user': dict(user)})
        else:
            return jsonify({'success': False, 'message': 'שם משתמש או סיסמה שגויים'}), 401
    except Exception as e:
        print("ERROR:", e)
        return jsonify({'success': False, 'message': str(e)}), 500


# 🔧 API  ואיתחול מערכת עם קובץ לאימון מודל - מקבל קובץ אקסל עם הנתונים לאימון ושומר אותו
@app.route('/datasets/upload', methods=['POST'])
def save_to_file():
    # קבלת הקובץ מהבקשה
    file = request.files.get('file')
    if not file:
        return 'Missing file', 400 # שגיאה אם לא התקבל קובץ

    user_id = session.get('user_id')
    print(user_id)
    if not user_id:
        return 'Unauthorized', 401
    # 💡 בדיקה אם למשתמש כבר יש קובץ
    if user_has_existing_file(user_id):
        return 'User already has an uploaded file', 409
    # שמירת הקובץ בתיקיה data_set
    filepath = save_to_deta_set(file)
    # בדיקות תקינות על הקובץ אקסל
    filea = request.files['file']
    validate_excel(filea)
    try:
       # שמירת הנתונים בטבלתSQL
       file_orginal_id = add_excel_file(user_id, filepath)
    # בדיקה אם הקובץ אכן נשמר בSQL נכון( צריך להוסיף אותה)
    except Exception as e:
        print('שגיאה בהוספת קובץ:', e)
        return 'Error saving file info', 500

    return {"message": "File saved successfully", "file_id": file_orginal_id}, 200


#איתחול מערכת
@app.route('/models/train/<datasetId>', methods=['POST'])
def System_initialization(datasetId):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return 'Unauthorized', 401
        print(user_id)
        # שליפת הנתונים מטבלת SQL
        filepath = get_original_file_paths(user_id)
        print('a')
        #מציאת  Q ו R לכל עמודה
        resaltQR = estimate_q_r_from_excel(filepath[0])
        print('b')
        # אם זה רשימה עם פריט אחד:
        if isinstance(filepath, list):
            filepath = filepath[0]

        #הפעלת פילטר קלמן על הנתונים
        filtered_data, kalman_models, sensors_columns = apply_filter_to_sensor_data(filepath, resaltQR)
        print('c')
        #שמירת הקובץ המסונן בתיקיה
        data_set_filter_path = save_to_data_set_filter(filtered_data, filepath)
        print('d')
        #מציאת האידי של הקובץ המקורי - כפי שהוא שמור בטבלאות
        file_orginal_id = get_last_excel_file_id_by_user(user_id)
        print(file_orginal_id)
        #שמירת הקובץ המסונן עם ערכי Q R בטבלת SQL
        filtered_id = add_filtered_file(file_orginal_id, data_set_filter_path, resaltQR)
        print('e')
        # שמירת מודל קלמן עבור המשתמש בתיקיה
        model_file_path = save_to_filter_models(kalman_models, filepath)
        print('f')
        # שמירת הנתיב למודל קלמן
        save_kalman_paths_to_db(user_id, filtered_id, kalman_models, model_file_path)
        print('g')
        #הפעלת אימון מודל על הקובץ המסונן
        training_date = datetime.now()

        model, scaler = liner(data_set_filter_path)

        # שמירת המודל המאומן בתקיה
        model_path = save_to_trained_models(model, filepath)
        scaler_path = save_scaler(scaler,filepath)
        print('h')
        #שמירת המודל המאומן בקובץ SQL
        user_id = session.get('user_id')
        metadata = {}
        # user_id       - מזהה המשתמש מתוך session['user_id']
        # filtered_id   - מזהה הקובץ המסונן שחזר מ-add_filtered_file
        # model_path    - נתיב לקובץ המודל ששמרת בדיסק (str)
        # training_date - תאריך ושעה של האימון, לרוב datetime.now()
        # metadata      - מילון עם מידע נוסף (אפשר גם {} אם אין מידע)
        if isinstance(filepath, list):
            filepath = filepath[0]
        new_model_id = save_model_and_scaler(user_id, filtered_id, model_path, training_date, metadata, scaler_path)
        print('good')
        return jsonify({"status": "success", "message": "Model trained successfully"})
    except Exception as e:
        # במקרה של שגיאה תחזיר JSON עם הודעת שגיאה וסטטוס 500
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    print("Method received:", request.method)

    try:
        user_id = session.get('user_id')
        # אם אין למשתמש קובץ מודל מאומן – מחזיר שגיאה 405 ("לא קיים מודל מאומן").
        if not user_has_existing_file(user_id):
            return 'There is no trained model file for this user.', 405

        data = request.get_json()
        print(data)
        # בודק אם לא התקבלו ערכים או שחסרים ערכי חיישנים – מחזיר שגיאה 400.
        if not data or 'sensorValues' not in data:
            return jsonify({'error': 'Missing sensor values'}), 400
        print('1')
        # שולף את רשימת הערכים של החיישנים מה־JSON
        sensor_values = data['sensorValues']
        print(sensor_values)
        sensors = ['TGS2600', 'TGS2602', 'TGS2611', 'TGS2610',  # רשימת חיישנים
                   'TGS2620', 'TGS826']
        print('2')
        #שליפת הניתוב למודל המאומן של המשתמש
        model_path, filtered_id, scaler_path = load_model_and_scaler_path_by_user(user_id)
        if not model_path or not scaler_path:
            return jsonify({'error': 'Model or scaler paths not found for user.'}), 404
        print('3. Model and scaler paths retrieved.')
        print('3')
        #טעינת המודל המאומן של המשתמש
        print(model_path)
        model = load_trained_model(model_path)
        model.summary()
        print('4')
        # טעינת ה-scaler המאומן
        scaler = joblib.load(scaler_path)
        print('5. Scaler loaded.')

        #טוען את פרמטרי הסינון
        #RQ = load_filter_params(filtered_id)
        print('5')
        # טוען את הנתיב למודל קלמן
        kalman_model_path = load_kalman_model_path(user_id, filtered_id)
        #טוען את קלמן מודל
        kalman_model = load_kalman_models(kalman_model_path)
        # סינון קלמן על הנתונים
        row_scaled = apply_kalman_to_row(sensor_values, kalman_model, sensors)
        print('5.5')
        values_array = np.array(list(row_scaled.values()))
        # קריאה לפונקציית החיזוי
        #result, probability, row_scaled = predict_single_row(sensor_values, kalman_model, sensors, model)
        result_prediction, confidence_score = predict_single_sample(model,sensor_values, scaler)
        print(f"Prediction Result: {result_prediction}")
        print(f"Confidence Score: {confidence_score}")
        print(row_scaled)
        print('6')
        return jsonify(
            {
                "originalValues": sensor_values,#רשימת ערכים לא מסוננים
                "filteredValues":  list(row_scaled.values()),#רשימת ערכים מסוננים
                "prediction": int(result_prediction),#תוצאה
                "confidence": float(confidence_score/100),#רמת ביטחון
                "smellName": "תות "
            })
    except Exception as e:
        print(f"שגיאה בפונקציית /predict: {e}")
        return jsonify({'error': 'Server error'}), 500



# # 🚀 הפעלת השרת במצב דיבאג
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
