import pandas as pd
import numpy as np


#בדיקות תקינות על הקובץ EXCEL
def validate_excel(file):
    # קריאת הקובץ
    try:
        df = pd.read_excel(file)
    except Exception as e:
        raise ValueError(f"שגיאה בטעינת הקובץ: {e}")

    # 1. בדיקה של עמודות TGS ו-LABEL
    tgs_columns = [col for col in df.columns if col.startswith("TGS")]
    if len(tgs_columns) < 2:
        raise ValueError("חייבות להיות לפחות שתי עמודות שהשם שלהן מתחיל ב-TGS")

    label_columns = [col for col in df.columns if col == "Subjek"]
    if len(label_columns) != 1:
        raise ValueError("חייבת להיות עמודה אחת ויחידה בשם Subjek")

    label_column = label_columns[0]

    # 2. בדיקה של תכנים בעמודות TGS
    tgs_data = df[tgs_columns]

    # המרה לערכים מספריים בלבד
    try:
        tgs_data_numeric = tgs_data.apply(pd.to_numeric, errors='coerce')
    except Exception:
        raise ValueError("חלק מהערכים בעמודות TGS אינם ניתנים להמרה למספרים")

    # בדיקה שיש רק ערכים חיוביים או אפס
    if not ((tgs_data_numeric >= 0) | (tgs_data_numeric.isna())).all().all():
        raise ValueError("כל הערכים בעמודות שמתחילות ב-TGS חייבים להיות חיוביים או אפס")

    # בדיקה של לפחות 70% מהערכים שהם חיוביים שונים מאפס
    positive_values = (tgs_data_numeric > 0).sum().sum()
    total_values = tgs_data_numeric.count().sum()
    if total_values == 0 or positive_values / total_values < 0.7:
        raise ValueError("פחות מ-70% מהערכים בעמודות TGS הם חיוביים שונים מאפס")

    # 3. בדיקה שיש לפחות 100 שורות מלאות (כלומר ללא ערכים חסרים)
    if df.dropna().shape[0] < 100:
        raise ValueError("יש פחות מ-100 שורות מלאות (ללא ערכים חסרים)")

    # 4. בדיקה של עמודת LABEL שהתוכן שלה רק Diabetes או Normal
    unique_labels = df[label_column].dropna().unique()
    valid_labels = {'Diabetes', 'Normal'}
    if not set(unique_labels).issubset(valid_labels):
        raise ValueError(f"עמודת LABEL יכולה להכיל רק את הערכים: {valid_labels}, אך נמצאו גם: {set(unique_labels) - valid_labels}")



