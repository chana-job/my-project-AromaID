import pandas as pd
import numpy as np

# מציאת הq ו- r עבור כל עמודה בטבלה
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


if __name__ == '__main__':
    df = estimate_q_r_from_excel(r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut.xlsx')  # קריאת קובץ CSV לתוך DataFrame
    print(df)