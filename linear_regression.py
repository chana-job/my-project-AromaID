import numpy as np # linear algebra # ליבוא מודול numpy עבור אלגברה לינארית
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv) # ליבוא מודול numpy עבור אלגברה לינארית
import matplotlib.pyplot as plt # ליבוא matplotlib.pyplot עבור יצירת גרפים
import seaborn as sns# ליבוא seaborn עבור גרפים סטטיסטיים יפים
import matplotlib # שוב, ליבוא matplotlib
from tensorflow.keras.models import load_model

#from פרויקט.data_sql import save_model
from filter_kalman import apply_kalman_to_row

matplotlib.use('Agg')  # או 'TkAgg', אם אתה משתמש ב-GUI, קביעת backend להצגת גרפים
import plotly.express as px  # ליבוא plotly.express ליצירת גרפים אינטרקטיביים
sns.set_style('whitegrid') # קביעת סגנון גרפים בסגנון רשת לבנה עבור seaborn

import os  # ליבוא מודול os לעבודה עם קבצים במערכת
for dirname, _, filenames in os.walk('/kaggle/input'):  # עבור כל תיקייה ותיקי קבצים בתיקיית הקלט
    for filename in filenames:
        print(os.path.join(dirname, filename))  # הצגת נתיב הקובץ
import warnings # ליבוא מודול warnings לניהול אזהרות בקוד
warnings.filterwarnings("ignore", "is_categorical_dtype")  # התעלמות מהאזהרה על סוגי נתונים קטגוריים
warnings.filterwarnings("ignore")  # התעלמות מכל שאר האזהרות

# הפונרציה הבאה מקבלת פרמטר אחד שהוא נתיב הקובץ שצריך לקרוא. הפונקציה מוגדרת בצורה כזו שהיא תחזיר את הקובץ בפורמט אקסל
def read_data(file_path):
    df = pd.read_excel(file_path)  #(דוגמה לקריאת נתונים מקובץ Excel)
    return df


def linear(file_exel_after_kalman_filter):
    #df = read_data(
       # r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut.xlsx')  # קריאת קובץ CSV לתוך DataFrame
    df = read_data(file_exel_after_kalman_filter)  # קריאת קובץ CSV לתוך DataFrame

    # df.info()   # הצגת מידע כללי על הנתונים

    # print(df.describe()) # הצגת סטטיסטיקות תיאוריות עבור הנתונים

    # print(df.head())  # הצגת 5 שורות ראשונות ב-DataFrame

    sensors = sensors = [col for col in df.columns.astype(str) if col.startswith('TGS')]
    # print(sensors)

    # gasses = {'TGS2600': 'Air contaminants', 'TGS2602': 'Air pollutants', 'TGS2611': 'Methane', # מיפוי חיישנים לגזים
    # 'TGS2610': 'LP gas', 'TGS2620': 'Alcohol and solvent vapors', 'TGS826': 'Ammonia'}

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10, 8))  # יצירת גרף עם 2 שורות ו-3 עמודות
    axes = axes.flatten()  # הפיכת מערך הגרפים לדו-ממדי

    for i, gas in enumerate(sensors):  # לולאת for עבור כל חיישן
        ax = axes[i]  # קביעת הגרף המתאים לכל חיישן
        sns.histplot(df, x=df[gas], ax=ax)  # יצירת היסטוגרמה של החיישן

        ax.axvline(x=df[gas].mean(), linestyle='dashed', color='firebrick')  # הוספת קו ממוצע בגרף

        ax.set_xlabel(gas)  # קביעת שם הציר האופקי
        ax.set_ylabel('Frequency')  # קביעת שם הציר האנכי
        ax.set_title(gas + ' histogram')  # כותרת לגרף

    fig.suptitle('Distribution Graphs of the Sensor Outputs', fontsize=16, fontweight='bold')  # כותרת עליונה לגרפים
    plt.tight_layout()  # סידור הגרפים בצורה מסודרת
    plt.show()  # הצגת הגרפים

    sns.countplot(df, x='Subjek')  # יצירת גרף ספירה של עמודת 'Subjek'

    df['Target'] = [1 if x == 'Diabetes' else 0 for x in df['Subjek']]  # יצירת עמודת 'Target' לפי ערכים ב-'Subjek'
    df.drop('Subjek', axis=1, inplace=True)  # מחיקת עמודת 'Subjek'
    print(df.head())  # הצגת 5 שורות ראשונות לאחר העדכון

    df.drop(['Time(s)', 'Number'], axis=1).corr()['Target'][0:5].plot.bar(  # חישוב קורלציה בין חיישנים ל-'Target'
        title='Simple Correlation of each Sensor Output with the Target')

    sns.heatmap(df.drop(['Time(s)', 'Number', 'Target'], axis=1).corr(),
                annot=True)  # יצירת חום-מאפ (heatmap) של הקורלציות

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10, 8))  # יצירת גרפים נוספים
    axes = axes.flatten()  # הפיכת מערך הגרפים לדו-ממדי

    for i, gas in enumerate(sensors):  # לולאת for עבור כל חיישן
        ax = axes[i]  # קביעת הגרף המתאים לכל חיישן
        sns.histplot(df, x=df[gas], ax=ax, hue=(df.Target))  # יצירת היסטוגרמה לפי ערך 'Target'

        ax.axvline(x=df[gas].mean(), linestyle='dashed', color='firebrick')  # הוספת קו ממוצע

        ax.set_xlabel(gas)  # קביעת שם הציר האופקי
        ax.set_ylabel('Frequency')  # קביעת שם הציר האנכי
        ax.set_title(gas + ' histogram')  # כותרת לגרף

    fig.suptitle('Distribution Graphs of the Sensor Outputs', fontsize=16, fontweight='bold')  # כותרת עליונה לגרפים
    plt.tight_layout()  # סידור הגרפים
    plt.show()  # הצגת הגרפים

    df.drop(['Time(s)', 'Number'], axis=1, inplace=True)  # מחיקת עמודות נוספות
    df.head()  # הצגת 5 שורות ראשונות לאחר העדכון

    from sklearn.model_selection import train_test_split  # ליבוא פונקציה לפיצול נתונים לאימון ובדיקה

    X = df.drop('Target', axis=1)  # יצירת משתנה X, ללא עמודת 'Target'
    y = df.Target  # יצירת משתנה y, רק עם עמודת 'Target'

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  # פיצול הנתונים

    from sklearn.preprocessing import StandardScaler  # ליבוא סטנדרטיזציה של נתונים

    scaler = StandardScaler()  # יצירת אובייקט scaler

    X_train = scaler.fit_transform(X_train)  # סטנדרטיזציה של נתוני האימון
    X_test = scaler.transform(X_test)  # סטנדרטיזציה של נתוני הבדיקה

    from sklearn.linear_model import LogisticRegression

    # נשתמש בלוגיסטית כי המטרה בינארית (0/1), והיא לינארית במבנה שלה
    linear_model = LogisticRegression()
    linear_model.fit(X_train, y_train)

    # הדפסת המשוואה (בהנחה ש-X זה DataFrame, אם זה numpy צריך להעביר שמות פיצ'רים ידנית)
    feature_names = X.columns if isinstance(X, pd.DataFrame) else sensors

    # פונקציה להצגת המשוואה
    def print_linear_model_equation(model, feature_names):
        terms = [f"{coef:.4f}*{name}" for coef, name in zip(model.coef_[0], feature_names)]
        equation = " + ".join(terms)
        equation = f"y = {model.intercept_[0]:.4f} + " + equation
        print("משוואת המודל הלינארית (Logistic Regression):")
        print(equation)

    print_linear_model_equation(linear_model, feature_names)

    from tensorflow.keras.models import Sequential  # ליבוא מודל Sequential מקיט TensorFlow
    from tensorflow.keras.layers import Dense, Dropout  # ליבוא שכבות Dense ו-Dropout

    model = Sequential()  # יצירת מודל Sequential
    model.add(Dense(6, activation='relu'))  # הוספת שכבת Dense עם 6 נוירונים
    # model.add(Dropout(0.5))  # הוספת Dropout להפחתת אוברפיטינג
    model.add(Dense(3, activation='relu'))  # הוספת שכבת Dense עם 3 נוירונים
    # model.add(Dropout(0.5)) # הוספת Dropout להפחתת אוברפיטינג
    model.add(Dense(1, activation='sigmoid'))  # הוספת שכבת פלט עם נוירון אחד וסיגמוד לאבחנה בינארית

    model.compile(optimizer='adam', loss='binary_crossentropy')  # קביעת אופטימיזטור ופעולת אובדן

    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), epochs=100)  # אימון המודל על הנתונים

    losses = pd.DataFrame(model.history.history).plot()  # הצגת גרף של אובדן האימון

    predictions = (model.predict(X_test) > 0.5).astype('int32')  # יצירת תחזיות מהמודל (עם סף 0.5)

    from sklearn.metrics import classification_report, confusion_matrix  # ליבוא דוחות ביצועים

    print('\033[1m' + 'Classification Report' + '\033[0m', '\n',
          classification_report(y_test, predictions))  # הצגת דוח ביצועים
    print('\033[1m' + 'Confusion Matrix' + '\033[0m', '\n', confusion_matrix(y_test, predictions))  # הצגת מטריצת בלבול
    #save_model()
    return feature_names, scaler, linear_model

    # >>> הוסיפי מפה והלאה <<<

# def predict_single_row(input_row, feature_names, scaler, model):
#         """
#         input_row: dict או list של ערכים לפי סדר העמודות
#         feature_names: שמות הפיצ'רים
#         scaler: האובייקט של StandardScaler שאומן קודם
#         model: המודל המאומן (Keras)
#         """
#
#         if isinstance(input_row, dict):
#             row_df = pd.DataFrame([input_row])[feature_names]
#         elif isinstance(input_row, list) or isinstance(input_row, np.ndarray):
#             row_df = pd.DataFrame([input_row], columns=feature_names)
#         else:
#             raise ValueError("Input must be a dict or list/array")
#
#         # סטנדרטיזציה
#         row_scaled = scaler.transform(row_df)
#
#         # תחזית
#         prediction = model.predict(row_scaled)[0][0]
#
#         # תוצאה בינארית
#         result = int(prediction > 0.5)
#         print(f"\n❯ סיכוי לסוכרת: {prediction:.2%} → {'חולה' if result == 1 else 'בריא'}")
#         return result, prediction
#


# מבחינת פילטר קלמן1 -
def predict_single_row(sensor_values, kalman_model, sensors, model):

    print(sensor_values)
    print('11')
    print(type(model))

    # המרה ל-DataFrame עם העמודות בסדר הנכון, בהתאם לסוג הקלט
    if isinstance(sensor_values, dict):
        print('12')
        # במקרה שמקבלים dict, יוצרים DataFrame וממיינים לפי feature_names
        row_df = pd.DataFrame([sensor_values])[sensors]
    elif isinstance(sensor_values, list) or isinstance(sensor_values, np.ndarray):
        # במקרה של list או numpy array, יוצרים DataFrame עם כותרות מהfeature_names
        row_df = pd.DataFrame([sensor_values], columns=sensors)
    else:
        print('14')
        # אם הקלט לא מוכר, מיידעים על שגיאה
        raise ValueError("Input must be a dict or list/array")
    print(row_df)
    print('15')
    if row_df.isnull().values.any():
        raise ValueError("שורת הקלט מכילה ערכים חסרים (NaN)")
    # סטנדרטיזציה של השורה לפי המודל (scale לפי האימון)
    try:
        row_scaled = apply_kalman_to_row(sensor_values, kalman_model, sensors)
        print('77777')
        print(row_scaled)
    except Exception as e:
        print(f"שגיאה בסקיילר: {e}")
        raise
    print('16')
    print(row_scaled)
    print(type(row_scaled))
    row_scaled_df = pd.DataFrame([row_scaled], columns= sensors)
    # תחזית המודל, מחזיר מערך דו-ממדי, לוקחים את הערך הראשון
    prediction = model.predict(row_scaled_df)[0][0]
    print('17')
    # המרת הסיכוי לתוצאה בינארית לפי סף 0.5
    result = int(prediction > 0.5)
    print('18')
    print(model)
    # החזרת התוצאה הבינארית והסיכוי הרציף
    return result, prediction, row_scaled


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

#עובד ללא scaler
# def predict_single_sample(model, sample_data):
#     """
#     מבצעת חיזוי על דגימה בודדת באמצעות מודל מאומן.
#
#     Args:
#         model: המודל המאומן (לדוגמה, מודל TensorFlow Keras שהוחזר מהפונקציה liner).
#         sample_data: מערך חד-ממדי של נתונים עבור דגימה אחת. יש לוודא שהנתונים
#                      במערך זה הם לפי סדר החיישנים ששימשו לאימון המודל.
#
#     Returns:
#         tuple: זוג ערכים הכולל:
#                - prediction (int): תוצאת החיזוי (0 או 1).
#                - confidence (float): אחוז הביטחון של החיזוי.
#     """
#     # ודא שהקלט הוא מערך numpy
#     sample_data = np.array(sample_data).reshape(1, -1)
#
#     # יש לבצע סקאלינג לנתונים באותו אופן שבו נתוני האימון עברו סקאלינג.
#     # מכיוון שהסקיילר נוצר בתוך הפונקציה liner ואינו מוחזר, נצטרך
#     # ליצור סקיילר חדש ולהתאים אותו מחדש על נתוני אימון כלשהם אם רוצים דיוק מוחלט.
#     # לשם הפשטות בדוגמה זו, נניח שהסקיילר שומש רק לשינוי קנה מידה
#     # ונוכל להשתמש באובייקט חדש שיעבור fit_transform על נתוני האימון
#     # במידה וזה היה זמין. במקרה הנוכחי, נבצע סקאלינג עם scaler חדש,
#     # אך חשוב לציין שבסביבת פרויקט אמיתית, יש לשמור ולטעון את ה-scaler
#     # ששימש לאימון המודל.
#
#     # יצירת סקיילר חדש (לצורך הדגמה בלבד! ביישום אמיתי, השתמש בסקיילר המאומן)
#     scaler_for_prediction = StandardScaler()
#     # נניח ש-X_train הוגדר מראש או שנספק לו נתוני דמה
#     # לצורך הדגמה, ניצור נתוני דמה של X_train
#     # במידה ואת המודל שקיבלנו, קיבלנו מחוץ לסקופ של הפונקציה הזאת
#     # כלומר, המודל אומן כבר על ידי הפונקציה liner שהיא בפני עצמה
#     # פונקציה עצמאית, אז אנחנו לא יכולים לגשת ל X_train שלה.
#     # לכן, לצורך הדוגמה, נפעיל את הסקיילר על הנתונים הגולמיים, וזה לא הדרך המומלצת.
#     # הדרך המומלצת היא לשמור את ה-scaler ביחד עם המודל.
#
#     # בגלל מגבלות הקוד שסופק, נצטרך להניח שה-sample_data כבר עבר סקאלינג או
#     # לבצע סקאלינג בדרך אחרת (לדוגמה, אם יש לנו את נתוני האימון בנפרד).
#     # אם אין לך גישה לסקיילר המקורי, לא ניתן לשחזר את הטרנספורמציה המדויקת.
#     # הפתרון הטוב ביותר הוא להחזיר את ה-scaler מהפונקציה liner יחד עם המודל.
#
#     # נבצע סקאלינג לדוגמה עם סקיילר חדש. שימו לב: זה עשוי להוביל לאי דיוק
#     # אם ה-scaler המקורי השתנה משמעותית.
#     # דרך טובה יותר תהיה להעביר את ה-scaler המאומן כארגומנט נוסף לפונקציה הזו.
#
#     # נניח שהסקיילר אומן על 6 תכונות (מספר החיישנים)
#     # לצורך הדוגמה, נדמה התאמה של סקיילר לנתונים כלשהם
#     # ביישום אמיתי, תצטרך לשמור את ה-scaler שאומן בתוך liner
#     # ולטעון אותו כאן, או להעבירו כארגומנט.
#
#     # יצירת DataFrame פיקטיבי להתאמת הסקיילר - רק אם אין גישה לסקיילר המקורי
#     # זהו פתרון חלקי בלבד. הפתרון הנכון הוא לשמר את ה-scaler המקורי.
#     dummy_data_for_scaler_fit = np.random.rand(10, sample_data.shape[1])
#     scaler_for_prediction.fit(dummy_data_for_scaler_fit)
#
#     scaled_sample = scaler_for_prediction.transform(sample_data)
#
#     # ביצוע חיזוי
#     prediction_probability = model.predict(scaled_sample)[0][0]
#
#     # קביעת תוצאת החיזוי (0 או 1)
#     prediction = 1 if prediction_probability > 0.5 else 0
#
#     # חישוב אחוז הביטחון
#     # אם החיזוי הוא 1, הביטחון הוא ההסתברות עצמה.
#     # אם החיזוי הוא 0, הביטחון הוא 1 פחות ההסתברות.
#     confidence = prediction_probability if prediction == 1 else (1 - prediction_probability)
#     confidence_percent = confidence * 100
#     print(prediction)
#     print(confidence_percent)
#
#     return prediction, confidence_percent




#מחזיר כל פעם את אותה תוצאה
# def predict_single_row(filtered_row, feature_names, model):
#     """
#     מבצעת חיזוי על שורת נתונים שכבר עברה סינון (פילטר קלמן).
#
#     :param filtered_row: dict עם ערכי חיישנים מסוננים (key = sensor name, value = filtered value)
#     :param feature_names: רשימת שמות החיישנים לפי סדר
#     :param QR: פרמטרי Q ו-R (לא בשימוש כאן אבל נשאר למקרה שתרצה)
#     :param model: המודל המאומן (למשל sklearn, keras וכו')
#     :return: tuple (תוצאה בינארית, סיכוי החיזוי, הערכים המסוננים)
#     """
#     print("נתוני קלט מסוננים:", filtered_row)
#
#     # המרה ל-DataFrame לפי סדר העמודות (feature_names)
#     row_df = pd.DataFrame([filtered_row])[feature_names]
#
#     if row_df.isnull().values.any():
#         raise ValueError("שורת הקלט מכילה ערכים חסרים (NaN)")
#
#     # כאן כבר לא מבצעים סינון נוסף, כי הנתונים כבר מסוננים
#     print(row_df)
#     # תחזית המודל, מחזיר מערך דו-ממדי, לוקחים את הערך הראשון
#     prediction = model.predict(row_df)[0][0]
#
#     # המרת הסיכוי לתוצאה בינארית לפי סף 0.5
#     result = int(prediction > 0.5)
#
#     return result, prediction, filtered_row

#קוד חדש עם scaler
# ודא ש-numpy מיובא (import numpy as np)
# וודא ש-StandardScaler לא מיובא בתוך הפונקציה הזו,
# ואובייקט ה-scaler יגיע כארגומנט

def predict_single_sample(model, sample_data, scaler):  # <--- הוספת scaler כארגומנט
    """
    מבצעת חיזוי על דגימה בודדת באמצעות מודל מאומן ו-scaler.

    Args:
        model: המודל המאומן (TensorFlow Keras).
        sample_data: מערך חד-ממדי של נתונים (לאחר סינון קלמן).
        scaler: אובייקט ה-StandardScaler המאומן.

    Returns:
        tuple: זוג ערכים הכולל:
               - prediction (int): תוצאת החיזוי (0 או 1).
               - confidence (float): אחוז הביטחון של החיזוי.
    """
    # ודא שהקלט הוא מערך numpy דו-ממדי עבור המודל (1 דגימה, N פיצ'רים)
    sample_data = np.array(sample_data).reshape(1, -1)

    # בצע סקאלינג לנתונים באמצעות ה-scaler שקיבלת
    scaled_sample = scaler.transform(sample_data)  # <--- זה התיקון הקריטי

    # ביצוע חיזוי
    prediction_probability = model.predict(scaled_sample)[0][0]

    # קביעת תוצאת החיזוי (0 או 1)
    prediction = 1 if prediction_probability > 0.5 else 0

    # חישוב אחוז הביטחון
    confidence = prediction_probability if prediction == 1 else (1 - prediction_probability)
    confidence_percent = confidence * 100

    print(f"predict_single_sample - Prediction: {prediction}, Confidence: {confidence_percent:.2f}%")

    return prediction, confidence_percent

if __name__ == '__main__':
    feature_names, scaler, linear_model= linear(r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut.xlsx')
    sample_input = {
        'TGS2600': 123.5,
        'TGS2602': 234.6,
        'TGS2610': 111.2,
        'TGS2611': 954.4,
        'TGS2620': 400.7,
        'TGS826': 76.9
    }

    predict_single_row(sample_input, feature_names, scaler, linear_model)




