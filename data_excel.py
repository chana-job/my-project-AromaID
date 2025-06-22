import os
import pickle
import joblib
from datetime import datetime


# יצירת תיקיית data_set אם לא קיימת
DATA_SET = 'data_set'
os.makedirs(DATA_SET, exist_ok=True)


# יצירת תיקיית data_set_filter אם לא קיימת
DATA_SET_FILTER = 'data_set_filter'
os.makedirs(DATA_SET_FILTER, exist_ok=True)


# יצירת תיקיית data_set_filter אם לא קיימת
FILTER_MODELS = 'filter_models'
os.makedirs(FILTER_MODELS, exist_ok=True)


# יצירת תיקיית trained_models לשמירת המודלים המאומנים אם לא קיימת
TRAINED_MODELS = 'trained_models'
os.makedirs(TRAINED_MODELS, exist_ok=True)

SCALER_FILE = 'scaler_file'
os.makedirs(SCALER_FILE, exist_ok=True)




#  ⬇⬇⬇   שמירת הקובץ המסונן לתיקיה
def save_to_data_set_filter(filtered_data, file_path):
    #הנתיב לתיקייה שבה את רוצה לשמור את הקובץ.
    # #folder = r' C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set_filter'
    # # שומר רק את שם הקובץ בלי התיקייה המקורית.
    # filename = os.path.basename(file_path).replace('.xlsx', '_filtered.xlsx')
    # # מחבר את הנתיב לתיקייה עם שם הקובץ החדש.
    # output_path = os.path.join(DATA_SET_FILTER, filename)
    # filtered_data.to_excel(output_path, index=False)
    # print(f"Filtered data saved to: {output_path}")
    # return output_path

    # שמירת הסיומת המקורית (כבר אמורה להיות .xlsx)

    ext = os.path.splitext(file_path)[1]  # למשל ".xlsx"

    # שמירת שם הקובץ בלי הסיומת
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # יצירת חתימת זמן ייחודית
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # יצירת שם קובץ חדש עם חתימת זמן ושמירה על הסיומת המקורית
    new_filename = f"{base_name}_filtered_{timestamp}{ext}"

    # יצירת הנתיב המלא לקובץ החדש
    output_path = os.path.join(DATA_SET_FILTER, new_filename)

    # שמירת הנתונים לקובץ אקסל
    filtered_data.to_excel(output_path, index=False)

    print(f"Filtered data saved to: {output_path}")
    return output_path

# שמירת קובץ לא מאומן בתיקיית העלאות
def save_to_deta_set(file):
    filename = file.filename
    # ודא שהקובץ נגמר ב-.xlsx
    if not filename.lower().endswith('.xlsx'):
        filename += '.xlsx'  # הוספת סיומת אם חסרה

    filepath = os.path.join(DATA_SET, file.filename)
    file.save(filepath)
    return filepath


#שומר מודל פילטר בתקיב filter_models
def save_to_filter_models(model, original_filename):
    # ניקוי שם הקובץ המקורי (בלי סיומת)
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    # יצירת שם קובץ ייחודי עם תאריך וזמן
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{base_name}_{timestamp}.h5"
    model_path = os.path.join(FILTER_MODELS, model_filename)

    # שמירת המודל
    #model.save(model_path)
    #  שמירה עם pickle (במקום שמירת המודל בצורה רגילה)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"המודל נשמר בהצלחה בנתיב: {model_path}")

    return model_path


# שומר מודל מאומן בתיקיה
def save_to_trained_models(model, original_filename):
    # ניקוי שם הקובץ המקורי (בלי סיומת)
    base_name = os.path.splitext(os.path.basename(original_filename))[0]

    # יצירת שם קובץ ייחודי עם תאריך וזמן
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{base_name}_{timestamp}.h5"
    model_path = os.path.join(TRAINED_MODELS, model_filename)

    # שמירת המודל
    model.save(model_path)

    print(f"המודל נשמר בהצלחה בנתיב: {model_path}")

    return model_path


def save_scaler(scaler, original_filename):
    # ניקוי שם הקובץ המקורי (בלי סיומת)
    base_name = os.path.splitext(os.path.basename(original_filename))[0]

    # יצירת שם קובץ ייחודי עם תאריך וזמן עבור ה-scaler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scaler_filename = f"{base_name}_{timestamp}_scaler.pkl"  # הוספת _scaler.pkl לסיומת
    filepath = os.path.join(SCALER_FILE, scaler_filename)

    try:
        joblib.dump(scaler, filepath)
        print(f"Scaler נשמר בהצלחה בנתיב: {filepath}")
        return filepath
    except Exception as e:
        print(f"שגיאה בשמירת ה-scaler: {e}")
        return None
