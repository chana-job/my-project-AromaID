import numpy as np # linear algebra # ליבוא מודול numpy עבור אלגברה לינארית
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv) # ליבוא מודול numpy עבור אלגברה לינארית
import matplotlib # ליבוא מודול matplotlib עבור יצירת גרפים וויזואליזציות
import matplotlib.pyplot as plt # ליבוא matplotlib.pyplot עבור יצירת גרפים
import seaborn as sns# ליבוא seaborn עבור גרפים סטטיסטיים יפים
import matplotlib # שוב, ליבוא matplotlib

from linear_regression import predict_single_row

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



def liner(file):
    df = pd.read_excel(file)  # קריאת קובץ CSV לתוך DataFrame

    df.info()  # הצגת מידע כללי על הנתונים

    print(df.describe())  # הצגת סטטיסטיקות תיאוריות עבור הנתונים

    print(df.head())  # הצגת 5 שורות ראשונות ב-DataFrame

    sensors = ['TGS2600', 'TGS2602', 'TGS2611', 'TGS2610',  # רשימת חיישנים
               'TGS2620', 'TGS826']
    gasses = {'TGS2600': 'Air contaminants', 'TGS2602': 'Air pollutants', 'TGS2611': 'Methane',  # מיפוי חיישנים לגזים
              'TGS2610': 'LP gas', 'TGS2620': 'Alcohol and solvent vapors', 'TGS826': 'Ammonia'}

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10, 8))  # יצירת גרף עם 2 שורות ו-3 עמודות
    axes = axes.flatten()  # הפיכת מערך הגרפים לדו-ממדי

    for i, gas in enumerate(sensors):  # לולאת for עבור כל חיישן
        ax = axes[i]  # קביעת הגרף המתאים לכל חיישן
        sns.histplot(df, x=df[gas], ax=ax)  # יצירת היסטוגרמה של החיישן

        ax.axvline(x=df[gas].mean(), linestyle='dashed', color='firebrick')  # הוספת קו ממוצע בגרף

        ax.set_xlabel(gas)  # קביעת שם הציר האופקי
        ax.set_ylabel('Frequency')  # קביעת שם הציר האנכי
        ax.set_title(gasses[gas] + ' histogram')  # כותרת לגרף

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
        ax.set_title(gasses[gas] + ' histogram')  # כותרת לגרף

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
    
    return model, scaler


if __name__ == '__main__':
    a = liner(r'C:\Users\school.DESKTOP-7E8R3ME\Desktop\פרויקט חני\פרויקט\data_set\frut_filtered.xlsx')
    print("model")
    print(a)
    # sample_input = {
    #     'TGS2600': 123.5,
    #     'TGS2602': 234.6,
    #     'TGS2610': 111.2,
    #     'TGS2611': 954.4,
    #     'TGS2620': 400.7,
    #     'TGS826': 76.9
    # }
    #
    # predict_single_row(sample_input, feature_names, scaler, linear_model)








