import psycopg2
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


    print("!!!!   Verifying Credentials   !!!!")
    #TAKING INPUT FOR VERIFICATION
    user_email_ver = input('Enter E-mail: ')
    user_pswd_ver = input('Enter Password: ')
    if user_email_ver != '' and user_pswd_ver !='':
        db_check_mail = (user_email_ver,)
        cur.execute('SELECT user_password FROM userrv WHERE user_email = %s',db_check_mail)
        db_mail_pswd = cur.fetchone()

        #TO CHECK IF THE USER ID PROVIDED IS IN THE DATA TABLE OR NOT
        if db_mail_pswd != None:

            verified = pbkdf2_sha256.verify(user_pswd_ver, db_mail_pswd[0])
            if verified == True:
                print({'Status Code':200, 'msg': 'Verified Successfully!'})
            else:
                print({'Status Code':500, 'msg': 'Incorrect Password!'})
        else:
            print({'Status Code':500, 'msg': 'Invalid User!'})
    else:
        raise Exception
    conn.commit()
except Exception as error:
    print({'Status Code':500, 'msg': 'Connection Failed!'})

finally:
    if cur is not None:
         cur.close()
    if conn is not None:
        conn.close()