import json
import pyodbc
from flask import jsonify
import os
from tensorflow.keras.models import load_model


server = r'NAYADLENOVO-1\SQLEXPRESS'  # שימי לב ל-r לפני המחרוזת כדי לא לברוח מה-backslash
database = 'data_base_AromaID'  # שם מסד הנתונים שלך

# פונקציה לפתיחת חיבור למסד נתונים PostgreSQL
def connect_db():
    conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
    )
    return conn


#
# def get_user_by_credentials(username, password):
#     """
#     מחזיר את המשתמש אם נמצא במסד, אחרת None.
#     """
#     try:
#         conn = connect_db()
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute(
#             "SELECT * FROM users WHERE username=%s AND password_hash=%s",
#             (username, password,)
#         )
#         user = cur.fetchone()
#         print(f" user:{user}")
#         return user
#     except Exception as e:
#         print(f"Error fetching user: {e}")
#         return None
#     finally:
#         cur.close()
#         conn.close()


#מחזיר את המשתמש אם נמצא במסד, אחרת None
def get_user_by_credentials(username, password):
    try:
        conn = connect_db()
        cur = conn.cursor()

        # ב-SQL Server, משתמשים ב-? כפרמטר
        cur.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password))
        row = cur.fetchone()

        if row:
            columns = [col[0] for col in cur.description]
            user = dict(zip(columns, row))
            print("user found:", user)
            return user
        else:
            print("No user found.")
            return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

#מה ההבדל בינו לקודם?
def get_user_by_id(user_id):
    """
    מחזיר את המשתמש לפי user_id אם נמצא במסד, אחרת None.
    """
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        if row:
            columns = [col[0] for col in cur.description]
            user = dict(zip(columns, row))
            return user
        else:
            return None
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None
    finally:
        cur.close()
        conn.close()



def insert_data_example(data_dict):
    """
    דוגמה לפונקציה שמכניסה נתונים עם טיפול בטרנזקציה.
    data_dict - מילון עם מפתחות תואמים לעמודות בטבלה
    """
    try:
        conn = connect_db()
        cur = conn.cursor()
        # דוגמה להוספת רשומה לטבלה כלשהי (שנה בהתאם לצורך)
        cur.execute(
            "INSERT INTO example_table (col1, col2) VALUES (?, ?)",
            (data_dict['col1'], data_dict['col2'])
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cur.close()
        conn.close()


# שמירת המודל המאומן בטבלת SQL
def save_model_and_scaler(user_id, filtered_id, model_path, training_date, metadata, scaler_path):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO Models (user_id, filtered_id, model_path, training_date, metadata, scaler_path)
            OUTPUT INSERTED.model_id
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (
            user_id, filtered_id, model_path, training_date, json.dumps(metadata), scaler_path
        ))

        new_model_id = cursor.fetchone()[0]
        conn.commit()
        print(f"המודל נוסף בהצלחה. model_id = {new_model_id}")
        return new_model_id

    except Exception as e:
        print(f"שגיאה בהוספת הרשומה: {e}")
        if conn:
            conn.rollback()
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


import os
import pickle  # או joblib אם השתמשת בו לשמירת המודל

def load_model_by_user_id(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # נשלוף את הנתיב למודל האחרון שאומן על ידי המשתמש
        query = """
            SELECT TOP 1 model_id, model_path
            FROM Models
            WHERE user_id = ?
            ORDER BY training_date DESC
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if not result:
            print("❌ לא נמצא מודל עבור המשתמש")
            return None, None

        model_id, model_path = result

        if not os.path.exists(model_path):
            print(f"❌ קובץ המודל לא נמצא בנתיב: {model_path}")
            return None, None

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        return model, model_id

    except Exception as e:
        print("שגיאה בטעינת המודל:", e)
        return None, None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# def save_model():
#     data = request.get_json()  # קבלת נתוני JSON מהבקשה
#     user_id = data['user_id']  # מזהה המשתמש
#     filtered_id = data['filtered_id']  # מזהה הקלט המסונן
#     model_path = data['model_path']  # נתיב למודל המאומן
#     metadata = data.get('metadata', {})  # מטא-דאטה אופציונלי
#
#     model_id = save_model_record(user_id, filtered_id, model_path, metadata)  # שמירת המידע במסד נתונים (כנראה)
#     return jsonify({"model_id": model_id, "message": "Model record saved successfully"})


def save_kalman_paths_to_db(user_id, filtered_id, kalman_models_dict, model_file_path):
    """
    שומר רשומות של מודלי קלמן עבור כל חיישן בטבלת KalmanStates.

    :param connection: אובייקט חיבור למסד (מחובר כבר)
    :param user_id: מזהה המשתמש (int)
    :param filtered_id: מזהה הקובץ המסונן (int)
    :param kalman_models_dict: מילון עם שם חיישן כ־key (לא חייב את האובייקט עצמו)
    :param model_file_path: נתיב הקובץ הפיזי שבו שמורים המודלים (str)
    """

    conn = connect_db()
    cursor = conn.cursor()

    try:
        print("8888")
        for sensor_name in kalman_models_dict.keys():
            cursor.execute("""
                INSERT INTO KalmanStates (user_id, filtered_id, sensor_name, kalman_state_path)
                VALUES (?, ?, ?, ?)
            """, (user_id, filtered_id, sensor_name, model_file_path))
        print("0000")
        conn.commit()
        print("99999")
        print("✔ נתיבי מודלים נשמרו בהצלחה לטבלת KalmanStates.")
        return True

    except Exception as e:
        connection.rollback()
        print("❌ שגיאה בשמירה לטבלה KalmanStates:", str(e))
        return False

    finally:
        conn.close()


def query_test():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 * FROM Users;")  # ב-SQL Server זה TOP, לא LIMIT
        row = cursor.fetchone()
        if row:
            # הפיכת השורה למילון (אם רוצים גישה לפי שם עמודה)
            columns = [column[0] for column in cursor.description]
            result = dict(zip(columns, row))
            print(result)
            return result
        return None
    except Exception as e:
        print(f"Error in query_test: {e}")
        return "error"
    finally:
        cursor.close()
        conn.close()

#בדיקה אם קובץ אקסל קיים עבור המשתמש
def user_has_existing_file(user_id):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM ExcelFiles WHERE user_id = ?", (user_id,))
        count = cur.fetchone()[0]
        return count > 0
    finally:
        cur.close()
        conn.close()


import pickle
import os
import psycopg2  # או pyodbc תלוי במה שאת משתמשת


#לטעון את המודל המאומן
def load_trained_model(model_id):
    try:
        conn = connect_db()  # פונקציה שלך שמחזירה connection
        cur = conn.cursor()

        # שליפת הנתיב או שם הקובץ של הסקלר מהמודל (נניח שהוא בטבלת Models)
        cur.execute("""
            SELECT model_path FROM Models WHERE model_id = %s
        """, (model_id,))
        result = cur.fetchone()
        if not result:
            print("לא נמצא סקלר עבור המודל")
            return None

        scaler_path = result[0]
        if not os.path.exists(scaler_path):
            print("קובץ הסקלר לא קיים בנתיב:", scaler_path)
            return None

        # # כאן את יכולה לטעון את הסקלר אם שמרת אותו בתוך תיקיית המודל או נתיב נפרד
        # # למשל, אם הסקלר נשמר בקובץ נפרד:
        # scaler_path = model_path.replace('model.h5', 'scaler.pkl')  # דוגמה להחלפה בשם הקובץ

        try:
            model = load_model(model_path)
            return model
        except Exception as e:
            print(f"שגיאה בטעינת המודל: {e}")
            return None
        # טעינת הסקלר מקובץ
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        return scaler

    except Exception as e:
        print("שגיאה בטעינת הסקלר:", e)
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


#הוספת הניתוב של קובץ אקסל רגיל לטבלה
def add_excel_file(user_id, original_file_path):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ExcelFiles (user_id, original_file_path)
            OUTPUT INSERTED.file_id
            VALUES (?, ?)
        """, (user_id, original_file_path))

        new_file_id = cur.fetchone()[0]
        conn.commit()
        print(f"הקובץ נוסף בהצלחה עם מזהה: {new_file_id}")
        return new_file_id
    except Exception as e:
        print("שגיאה בהוספת קובץ:", e)
        return None
    finally:
        cur.close()
        conn.close()


    # שומר קובץ מסונן בטבלת FilteredFiles ומחזיר את filtered_id שנוצר
    # :param file_id: מספר מזהה של הקובץ המקורי (מתוך טבלת ExcelFiles)
    # :param filtered_file_path: נתיב לקובץ המסונן שנשמר בדיסק (str)
    # :param filter_params: מילון עם פרמטרים של הפילטר קלמן (dict), לדוגמה: {"Q":0.1, "R":0.3}
    # :return: filtered_id (int) אם הצליח, אחרת None
def add_filtered_file(file_id, filtered_file_path, filter_params):
    try:
        conn = connect_db()  # יצירת חיבור למסד הנתונים
        print('1')
        cursor = conn.cursor()
        print('2')

        insert_query = """
            INSERT INTO FilteredFiles (file_id, filtered_file_path, filter_params, created_at)
            OUTPUT INSERTED.filtered_id
            VALUES (?, ?, ?, GETDATE())
        """
        print('3')

        cursor.execute(insert_query, (
            file_id,
            filtered_file_path,
            json.dumps(filter_params),  # המרת dict ל־JSON
        ))
        print('4')

        result = cursor.fetchone()
        print("INSERT result:", result)  # הוסף את זה
        print('5')

        if result:
            filtered_id = result[0]
        else:
            print("⚠️ לא התקבל filtered_id אחרי INSERT.")
            filtered_id = None

        #filtered_id = cursor.fetchone()[0]  # שליפת ה-id של השורה החדשה
        print('6')
        conn.commit()
        return filtered_id

    except Exception as e:
        print(f"שגיאה בהוספת הקובץ המסונן: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#מחזיר את מספר הקובץ המקורי השמור בטבלה
def get_last_excel_file_id_by_user(user_id):
    """
    מחזירה את ה־file_id האחרון שהוזן עבור משתמש מסוים מתוך טבלת ExcelFiles
    :param user_id: מזהה המשתמש
    :return: file_id האחרון או None אם לא נמצא
    """
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT TOP 1 file_id
            FROM ExcelFiles
            WHERE user_id = ?
            ORDER BY file_id DESC
        """, (user_id,))

        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print("שגיאה בשליפת הקובץ האחרון:", e)
        return None
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

#שליפת הקובץ הלא מסונן מטבלת SQL לפי הuser_id
def get_original_file_paths(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        if user_id is not None:
            query = "SELECT original_file_path FROM ExcelFiles WHERE user_id = ?"
            cursor.execute(query, (user_id,))
        else:
            query = "SELECT original_file_path FROM ExcelFiles"
            cursor.execute(query)

        rows = cursor.fetchall()
        return [row[0] for row in rows]  # כי אין dict ב־pyodbc כברירת מחדל

    except Exception as e:
        print(f"שגיאה בשליפת הנתיבים: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

# זוהי פונקציה ששולף את הניתוב למודל המאומן
def load_model_and_scaler_path_by_user(user_id: int):
    """
    טוענת את נתיב המודל האחרון שנשמר עבור משתמש לפי user_id.

    :param user_id: מזהה המשתמש
    :return: מחרוזת עם נתיב המודל או None אם לא נמצא
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT TOP 1 model_path, filtered_id, scaler_path
            FROM Models
            WHERE user_id = ?
            ORDER BY training_date DESC
        """

        cursor.execute(query, user_id)
        row = cursor.fetchone()

        if row:
            model_path, filtered_id, scaler_path = row[0], row[1], row[2]
            return model_path, filtered_id, scaler_path
        else:
            print("לא נמצא מודל עבור המשתמש.")
            return None

    except Exception as e:
        print(f"שגיאה בשליפת הנתיב: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#זוהי פונקציה שטוענת את המודל המאומן לפי ניתוב
def load_trained_model(model_path: str):

    try:
        if not os.path.exists(model_path):
            print(f"שגיאה: הקובץ '{model_path}' לא נמצא.")
            return None
        model = load_model(model_path)
        print("המודל נטען בהצלחה.")
        return model
    except Exception as e:
        print(f"שגיאה בטעינת המודל: {e}")
        return None

# טוען את הנתיב למודל קלמן 
def load_kalman_model_path(user_id, filtered_id):
    """
    שולף את נתיב קובץ מודלי קלמן ששמור בטבלת KalmanStates לפי user_id ו־filtered_id.

    :param user_id: מזהה המשתמש
    :param filtered_id: מזהה הקובץ המסונן
    :return: נתיב הקובץ כ־string או None אם לא נמצא
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT TOP 1 kalman_state_path
            FROM KalmanStates
            WHERE user_id = ? AND filtered_id = ?
        """

        cursor.execute(query, (user_id, filtered_id))
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            print("⚠️ לא נמצא נתיב מודל קלמן במסד הנתונים.")
            return None

    except Exception as e:
        print(f"שגיאה בשליפת נתיב מודל קלמן: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
# טוען את קלמן מודל
def load_kalman_models(model_path):
    with open(model_path, 'rb') as f:
        kalman_models = pickle.load(f)
    return kalman_models



# טוען את פרמטרי הסינון (filter_params) עבור קובץ מסונן מסוים.
def load_filter_params(filtered_id: int):
    """
    טוען את פרמטרי הסינון (filter_params) עבור קובץ מסונן מסוים.

    :param filtered_id: מזהה הקובץ המסונן
    :return: מילון Python עם הפרמטרים או None אם לא נמצא
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT filter_params
            FROM FilteredFiles
            WHERE filtered_id = ?
        """

        cursor.execute(query, filtered_id)
        row = cursor.fetchone()

        if row and row[0]:
            return json.loads(row[0])
        else:
            print("לא נמצאו פרמטרים עבור filtered_id =", filtered_id)
            return None

    except Exception as e:
        print(f"שגיאה בטעינת הפרמטרים: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    query_test()