import psycopg2, uuid, re
from passlib.hash import pbkdf2_sha256
conn = None
cur = None
try:
    conn = psycopg2.connect(
                host = 'localhost', 
                database = 'User_N',
                user = 'postgres',
                password = 'nameitasyoulike',
                port = 5432
                )

    cur = conn.cursor()
    
    cur.execute('''SELECT user_email FROM userrv''')
    users_list_fetch = cur.fetchall()
    users_list = [item for t in users_list_fetch for item in t]

    #TO INSERT DATA INTO USERS TABLE
    no_of_users = int(input('Enter No. Of Users: '))
    if no_of_users == 0:
        print({'Status Code':500, 'msg': 'Requested Range Unsatisfiable!'})
    else:
        for i in range(no_of_users):
            user_uid = uuid.uuid4()
            j =0
            while j == 0:
                user_mail = input('Enter Your Mail ID: ')
                j += 1
                if user_mail in users_list:
                    print({'Status Code':500, 'msg': 'Already in Database. Add another Email ID'})
                    j -= 1
                elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', user_mail):
                    print({'Status Code':500, 'msg': 'Enter Valid eMail!'})
                    j -= 1

            k = 0
            while k == 0:
                user_pswd = input('Enter Password: ')
                k = 1
                if re.search('[\s]',user_pswd) or user_pswd == '' :
                    print({'Status Code':500, 'msg': 'Try another way!'})
                    k -= 1
            insert_script = ''' INSERT INTO userrv (user_id, user_email, user_password) VALUES(%s, %s, %s)'''
            insert_values = (str(user_uid), user_mail, pbkdf2_sha256.hash(user_pswd))
            cur.execute(insert_script, insert_values)
            print({'Status Code':200, 'msg': 'Succesfully Done'})
    conn.commit()
except Exception as error:
    print({'Status Code':500, 'msg': 'Something Happened. Try again later.'})

finally:
    if cur is not None:
         cur.close()
    if conn is not None:
        conn.close()