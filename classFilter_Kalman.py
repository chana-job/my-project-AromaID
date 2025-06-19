#היא ספריית מתמטיקה לפייתון. אנחנו משתמשים בה כדי לחשב מטריצות, וקטורים, מכפלות מטריצות, ועוד.
import numpy as np


#המחלקה הזאת מייצגת מימוש של מסנן קלמן –
# אלגוריתם מתמטית שמטרתו לעקוב אחרי מצב מערכת שמתפתחת בזמן למרות רעשים במדידות או במודל עצמו.
class KalmanFilter(object):
    #שם מיוחד לפונקציית אתחול של אובייקט. __init__
    #פייתון מפעיל אותה כשקוראים למחלקה (כמו kf = KalmanFilter(...)).
    #מצביע לאדם עצמו. self,
    # דרכו אפשר לשמור ערכים באובייקט, למשל: self.F = F.
    def __init__(self, F=None, B=None, H=None, Q=None, R=None, P=None, x0=None):
        if (F is None or H is None):
            raise ValueError("Set proper system dynamics.")

        #self.n: מספר העמודות במטריצת המעבר F(מציג את גודל המצב).
        self.n = F.shape[1]
        #self.m: מספר העמודות במטריצת המדידה H(מציג את מספר המדידות)
        self.m = H.shape[1]

        self.F = F
        self.H = H
        # זהו תנאי מקוצר ,
        # אם המשתנה בי לא הוגדר אז סלף בי יקבל את הערך אפס,
        # אם בי הוא לא none סלף בי יהיה שווה לבי
        self.B = 0 if B is None else B

        #יוצר מצטריצה בגודל Q עלQ או R על R וכו' עם אלכסון אחדות
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

    #🔹 זו פונקציה שמחשבת מה לדעתנו יהיה המצב הבא, לפי המצב הנוכחי והמודל שלנו.
    def predict(self, u=0):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        I = np.eye(self.n)
        self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P),
                        (I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R), K.T)


