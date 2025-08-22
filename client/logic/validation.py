import pymssql

def validar_pre_clockin(user_code):
    try:
        conn = pymssql.connect(server='GUNDMAIN', user='mie', password='mie', database='GunderlinLive')
        cursor = conn.cursor()
        cursor.execute("SELECT UserPK FROM [User] WHERE Code = %s", (user_code,))
        row = cursor.fetchone()
        if not row: return False
        user_pk = row[0]
        cursor.execute("""
            SELECT COUNT(*) FROM WorkOrderCollection
            WHERE EmployeeFK = %s AND TimeOn IS NOT NULL AND TimeOff IS NULL
        """, (user_pk,))
        result = cursor.fetchone()
        return result[0] > 0
    except: return False


def validar_post_clockin(user_code, wo_number):
    try:
        conn = pymssql.connect(server='GUNDMAIN', user='mie', password='mie', database='GunderlinLive')
        cursor = conn.cursor()
        cursor.execute("SELECT UserPK FROM [User] WHERE Code = %s", (user_code,))
        row = cursor.fetchone()
        if not row: return False
        user_pk = row[0]
        cursor.execute("""
            SELECT COUNT(*) FROM WorkOrderCollection
            WHERE WorkOrderNumber = %s AND EmployeeFK = %s
              AND TimeOn IS NOT NULL AND TimeOff IS NULL
        """, (wo_number, user_pk))
        result = cursor.fetchone()
        return result[0] > 0
    except: return False


def validar_pre_clockout(user_code, wo):
    try:
        conn = pymssql.connect(server='GUNDMAIN', user='mie', password='mie', database='GunderlinLive')
        cursor = conn.cursor()
        cursor.execute("SELECT UserPK FROM [User] WHERE Code = %s", (user_code,))
        row = cursor.fetchone()
        if not row: return False
        user_pk = row[0]
        cursor.execute("""
            SELECT COUNT(*) FROM WorkOrderCollection
            WHERE WorkOrderNumber = %s AND EmployeeFK = %s
              AND TimeOn IS NOT NULL AND TimeOff IS NULL
        """, (wo, user_pk))
        result = cursor.fetchone()
        return result[0] > 0
    except: return False


def validar_post_clockout(user_code, wo):
    try:
        conn = pymssql.connect(server='GUNDMAIN', user='mie', password='mie', database='GunderlinLive')
        cursor = conn.cursor()
        cursor.execute("SELECT UserPK FROM [User] WHERE Code = %s", (user_code,))
        row = cursor.fetchone()
        if not row: return False
        user_pk = row[0]
        cursor.execute("""
            SELECT COUNT(*) FROM WorkOrderCollection
            WHERE WorkOrderNumber = %s AND EmployeeFK = %s
              AND TimeOn IS NOT NULL AND TimeOff IS NOT NULL
        """, (wo, user_pk))
        result = cursor.fetchone()
        return result[0] > 0
    except: return False
