import numpy as np
from scipy.optimize import minimize
import matplotlib
from פרויקט.befor_filter_klaman import estimate_q_r_from_excel

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd  # נוודא שהמודול pandas מיובא. זוהי ספריה מעולה לעבודה עם נתונים ובמיוחד עם טבלאות(exel,cvs)
from פרויקט.classFilter_Kalman import KalmanFilter
#from פרויקט.linear_regression import linear


# הפונרציה הבאה מקבלת פרמטר אחד שהוא נתיב הקובץ שצריך לקרוא. הפונקציה מוגדרת בצורה כזו שהיא תחזיר את הקובץ בפורמט אקסל
def read_data(file_path):
    # השורה הבאה מבצעת את קריאת קובץ האקסל בנתיב שנמסר כפרמטר לפונקציה
    #:הפונקציה pd.read_excel
    # פותחת את קובץ ה-Excel בנתיב file_pathומחזירה אותו כ-DataFrame, שהוא מראה את הטבלה.
    df = pd.read_excel(file_path)  # (דוגמה לקריאת נתונים מקובץ Excel)
    return df

#הפעלת פילטר קלמן
def apply_filter_to_sensor_data(file_path, reasalQR):
    df = read_data(file_path)  # קריאת הנתונים
    # הוספת עמודת אינדקס לפי סדר השורות
    df['Index'] = df.index

    # מיון לפי עמודת האינדקס (לפי סדר השורות)
    df = df.sort_values(by='Index')

    sensors_columns = ['TGS2600', 'TGS2602', 'TGS2611', 'TGS2610', 'TGS2620', 'TGS826']  # עדכן לפי שם העמודות שלך

    # ⬇⬇⬇ נוספה רשימת תוצאות מסוננות
    filtered_data = pd.DataFrame(index=df.index)

    # אתה יכול לשנות את שמות העמודות לפי מה שיש לך בקובץ
    # measurements = df['TGS2600'].values  # מדידות מהחיישן הראשון
    for col in sensors_columns:
        # filter(col)
        measurements = df[col].values
        print(measurements)
        print(col)
        # ⬇⬇⬇ קבלת הסדרה המסוננת
        filtered_series = filter(measurements, reasalQR[col]['Q'], reasalQR[col]['R'])
        print(filtered_series)
        filtered_data[col] = filtered_series  # שמירה לטבלת התוצאות
    filtered_data['Subjek'] = df['Subjek']
    filtered_data['Time(s)'] = df['Time(s)']
    filtered_data['Number'] = df['Number']
    return filtered_data
    # save_to_data_set_filter(filtered_data, file_path)


def filter(measurements, reasalQR_Q, reasalQR_R):
    # ### שינוי: אופטימיזציה למציאת Q ו-R אופטימליים
    # res = minimize(reasalQR, [0.05, 0.5], args=(measurements,),
    #                bounds=[(1e-5, 1), (1e-5, 10)], method='L-BFGS-B')
    q_val = reasalQR_Q
    r_val = reasalQR_R
    print(f"Best parameters: Q={q_val:.4f}, R={r_val:.4f}")

    dt = 1.0 / 60
    F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
    H = np.array([1, 0, 0]).reshape(1, 3)
    Q = np.array([[reasalQR_Q, reasalQR_Q, 0], [reasalQR_Q, reasalQR_Q, 0], [0, 0, 0]])
    R = np.array([reasalQR_R]).reshape(1, 1)

    kf = KalmanFilter(F=F, H=H, Q=Q, R=R)
    predictions = []

    for z in measurements:
        if np.isnan(z):
            predictions.append(np.nan)
            continue
        pred = np.dot(H, kf.predict())[0][0]
        kf.update(np.array([[z]]))
        predictions.append(pred)

    plt.plot(range(len(measurements)), measurements, label='Measurements')
    plt.plot(range(len(predictions)), np.array(predictions), label='Kalman Filter Prediction')
    plt.legend()
    plt.show()

    return predictions  # ⬅⬅⬅ מחזיר את התחזיות לשימוש בהמשך


### שינוי: פונקציה למציאת שגיאה ממוצעת בין מדידות לסינון
# def kalman_error(params, measurements):
#     q_val, r_val = params
#     dt = 1.0 / 60
#     F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
#     H = np.array([1, 0, 0]).reshape(1, 3)
#     Q = np.array([[q_val, q_val, 0], [q_val, q_val, 0], [0, 0, 0]])
#     R = np.array([r_val]).reshape(1, 1)
#
#     kf = KalmanFilter(F=F, H=H, Q=Q, R=R)
#     predictions = []
#
#     for z in measurements:
#         if np.isnan(z):
#             continue
#         pred = np.dot(H, kf.predict())[0][0]
#         kf.update(np.array([[z]]))
#         predictions.append(pred)
#
#     measurements_clean = [z for z in measurements if not np.isnan(z)]
#     min_len = min(len(predictions), len(measurements_clean))
#     predictions = predictions[:min_len]
#     measurements_clean = measurements_clean[:min_len]
#
#     mse = np.mean((np.array(measurements_clean) - np.array(predictions)) ** 2)
#     return mse


def start_filter_kalman(file_path):
    output_path = apply_filter_to_sensor_data(file_path)
    linear(r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut_filtered.xlsx')


def filter(measurements, reasalQR_Q, reasalQR_R):

    # הגדרת פרק הזמן בין מדידות – לדוגמה 1/60 שניות
    dt = 1.0 / 60

    # מטריצת המעבר (Transition matrix) – מגדירה איך המצב משתנה עם הזמן
    F = np.array([
        [1, dt, 0],  # מיקום מושפע ממהירות
        [0, 1, dt],  # מהירות מושפעת מתאוצה
        [0, 0, 1]  # תאוצה קבועה
    ])

    # מטריצת התצפית – רק המיקום נמדד בפועל
    H = np.array([1, 0, 0]).reshape(1, 3)

    # רעש תהליך – מייצג חוסר ודאות בשינוי מצב (מעריך שינוי במצב האמיתי)
    Q = np.array([
        [reasalQR_Q, reasalQR_Q, 0],
        [reasalQR_Q, reasalQR_Q, 0],
        [0, 0, 0]
    ])

    # רעש מדידה – חוסר ודאות במדידות עצמן (למשל רעש חיישן)
    R = np.array([reasalQR_R]).reshape(1, 1)

    # יצירת אובייקט של פילטר קלמן עם המטריצות שהגדרנו
    kf = KalmanFilter(F=F, H=H, Q=Q, R=R)

    # רשימת התחזיות שנחזיר בסוף
    predictions = []

    # לולאה על כל המדידות
    for z in measurements:
        if np.isnan(z):
            # אם אין מדידה – שמור NaN ואל תעדכן את הפילטר
            predictions.append(np.nan)
            continue

        # חיזוי הערך הבא לפי מצב הפילטר (לפני עדכון עם המדידה)
        pred = np.dot(H, kf.predict())[0][0]

        # עדכון הפילטר עם המדידה הנוכחית
        kf.update(np.array([[z]]))

        # שמירה של התחזית שחושבה
        predictions.append(pred)

    # החזרת התחזיות – אפשר להשתמש בהן בהמשך (למשל למידול או אחסון)
    return predictions

#פילטר קלמן עבור שורה אחת-מדידה בזמן אמת
# input_row – שורת הנתונים החדשים, כ־dict או רשימה (list/np.ndarray) של ערכי חיישנים.
# reasalQR – מילון המכיל ערכי Q ו-R עבור כל חיישן, למשל:
# {
#   'TGS2600': {'Q': 0.01, 'R': 0.1},
#   'TGS2602': {'Q': 0.02, 'R': 0.15},
#   ...
# }
# feature_names – רשימת שמות העמודות/חיישנים, לפי סדר הנתונים בשורה.
def apply_kalman_to_row(input_row, reasalQR, feature_names):
    """
    מקבלת שורת נתונים של מדידות חיישנים,
    מפעילה עליה פילטר קלמן נפרד לכל חיישן,
    ומחזירה dict עם הערכים המסוננים.

    :param input_row: dict או list של ערכים
    :param reasalQR: dict עם Q ו-R לכל חיישן, לדוגמה:
                     {'TGS2600': {'Q': 0.01, 'R': 0.1}, ...}
    :param feature_names: רשימת שמות החיישנים לפי סדר
    :return: dict עם ערכים מסוננים לכל חיישן
    """
    # אם קיבלנו DataFrame, נחלץ ממנו את השורה הראשונה כ- dict
    print("כעיחל")
    print(input_row)
    if isinstance(input_row, pd.DataFrame):
        input_row = input_row.iloc[0].to_dict()
    # אם קיבלנו רשימה או מערך, נהפוך ל-dict לפי שמות העמודות
    elif isinstance(input_row, list) or isinstance(input_row, np.ndarray):
        input_row = dict(zip(feature_names, input_row))
        print(feature_names)
    print(input_row)
    filtered_row = {}

    for feature in feature_names:
        val = input_row.get(feature, np.nan)
        if np.isnan(val):
            filtered_row[feature] = np.nan
            continue

        Q = reasalQR[feature]['Q']
        R = reasalQR[feature]['R']

        # כאן יוצרים פילטר קלמן קטן לכל חיישן
        dt = 1.0 / 60
        F = np.array([[1, dt, 0],
                      [0, 1, dt],
                      [0, 0, 1]])
        H = np.array([1, 0, 0]).reshape(1, 3)
        Q_mat = np.array([[Q, Q, 0],
                          [Q, Q, 0],
                          [0, 0, 0]])
        R_mat = np.array([R]).reshape(1, 1)

        kf = KalmanFilter(F=F, H=H, Q=Q_mat, R=R_mat)

        # מניחים התחלת מצב אפס, עם העדכון הראשון
        kf.update(np.array([[val]]))
        filtered_val = np.dot(H, kf.predict())[0][0]

        filtered_row[feature] = filtered_val

    return filtered_row


if __name__ == '__main__':
    file_path = r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut.xlsx'
    df = estimate_q_r_from_excel(
        r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut.xlsx')  # קריאת קובץ CSV לתוך DataFrame
    # example(file_path)
    apply_filter_to_sensor_data(file_path, df)

