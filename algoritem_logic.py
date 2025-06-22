import numpy as np
from scipy.optimize import minimize
import matplotlib

from befor_filter_klaman import estimate_q_r_from_excel

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd  # נוודא שהמודול pandas מיובא. זוהי ספריה מעולה לעבודה עם נתונים ובמיוחד עם טבלאות(exel,cvs)
from classFilter_Kalman import KalmanFilter
from linear_regression import linear



def estimate_q_r_from_excel(file_path, sheet_name=0, num_rows_for_estimate=100):
    # טוען את הנתונים
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    results = {}
    sensors_columns = ['TGS2600', 'TGS2602', 'TGS2611', 'TGS2610', 'TGS2620', 'TGS826']  # עדכן לפי שם העמודות שלך

    # אתה יכול לשנות את שמות העמודות לפי מה שיש לך בקובץ
    # measurements = df['TGS2600'].values  # מדידות מהחיישן הראשון
    for column in sensors_columns:
        data = df[column].dropna().values  # הסר NaNs
        if len(data) < 2:
            continue  # לא ניתן לחשב נגזרת

        # ניקח את הקטע הראשוני רק אם רוצים להגביל
        if num_rows_for_estimate and len(data) > num_rows_for_estimate:
            data = data[:num_rows_for_estimate]

        # אומדן לרעש המדידה - שונות המדידות
        r_est = np.var(data)

        # אומדן לרעש תהליך - שונות השינוי בין מדידות עוקבות (כמו נגזרת)
        diffs = np.diff(data)
        q_est = np.var(diffs)

        results[column] = {
            'Q': round(float(q_est), 6),
            'R': round(float(r_est), 6)
        }

    return results

sensors_columns = ['TGS2600', 'TGS2602', 'TGS2611', 'TGS2610', 'TGS2620', 'TGS826']


def estimate_q_r_from_excel(file_path, sheet_name=0, num_rows_for_estimate=100, sensors_columns=None):
    # טוען את הנתונים מקובץ Excel לגיליון המבוקש
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # מילון שישמור את התוצאות עבור כל חיישן
    results = {}

    # עובר על כל אחד מהחיישנים בקובץ
    for column in sensors_columns:
        # מוציא את המדידות מהעמודה, ומסיר ערכים חסרים (NaN)
        data = df[column].dropna().values

        # אם יש פחות משתי מדידות, לא ניתן לחשב את השונות של ההפרשים (נגזרת)
        if len(data) < 2:
            continue

        # אם מצוין מספר שורות להערכת הפרמטרים, נחתוך את המידע רק לשורות הראשונות
        if num_rows_for_estimate and len(data) > num_rows_for_estimate:
            data = data[:num_rows_for_estimate]

        # אומדן ל-R (רעש מדידה): שונות המדידות עצמן
        r_est = np.var(data)

        # אומדן ל-Q (רעש תהליך): שונות השינויים בין מדידות עוקבות
        # למעשה, זה כמו להסתכל על נגזרת המדידות ולחשב את השונות שלה
        diffs = np.diff(data)
        q_est = np.var(diffs)

        # שומר את התוצאות עבור כל חיישן, מעוגל ל-6 ספרות אחרי הנקודה
        results[column] = {
            'Q': round(float(q_est), 6),
            'R': round(float(r_est), 6)
        }

    # מחזיר מילון עם ערכי Q ו-R לכל חיישן
    return results
