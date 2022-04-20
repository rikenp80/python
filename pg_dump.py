import psycopg2 # for database operations
import datetime
import subprocess

# -------------------
# Database connection
# -------------------
t_host = "reimagine-dev-canada.cluster-c514w15qevsg.ca-central-1.rds.amazonaws.com"
t_port = "5432"
t_dbname = "config"
t_name_user = "reimagineUser"
t_password = "ZNUBob1MQepRJjgNUN3T"
t_dumpfile = "C:\\Users\\rpatel3\\Documents\\dumps\\config2.dump"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
cur = db_conn.cursor()

command = 'psql -U reimagineUser -h reimagine-dev-canada.cluster-c514w15qevsg.ca-central-1.rds.amazonaws.com -d config -c "update """Branch""" set creator_id=2 where id=1;"'

proc = subprocess.Popen(command, shell=True, env={
            'PGPASSWORD': t_password
            })
proc.wait()




dump_success = 1
print ('Backing up %s database ' % (t_dbname))
command = f'pg_dump -h {t_host} ' \
            f'-U "{t_name_user}" ' \
            f'-s {t_dbname} > "{t_dumpfile}"'
#try:
proc = subprocess.Popen(command, shell=True, env={'PGPASSWORD': t_password})
proc.wait()
print (command)


except Exception as e:
    dump_success = 0
    print('Exception happened during dump %s' %(e))


 if dump_success:
    print('db dump successfull')
 print(' restoring to a new database database')

 """database to restore dump must be created with 
the same user as of previous db (in my case user is 'postgres'). 
i have #created a db called ReplicaDB. no need of tables inside. 
restore process will #create tables with data.
"""

backup_file = '/home/Downloads/BlogTemplate/BlogTemplate/backup.dmp' 
"""give absolute path of your dump file. This script will create the backup.dmp in the same directory from which u are running the script """



if not dump_success:
    print('dump unsucessfull. retsore not possible')
 else:
    try:
        process = subprocess.Popen(
                        ['pg_restore',
                         '--no-owner',
                         '--dbname=postgresql://{}:{}@{}:{}/{}'.format('postgres',#db user
                                                                       'sarath1996', #db password
                                                                       'localhost',  #db host
                                                                       '5432', 'ReplicaDB'), #db port ,#db name
                         '-v',
                         backup_file],
                        stdout=subprocess.PIPE
                    )
        output = process.communicate()[0]

     except Exception as e:
           print('Exception during restore %e' %(e) )






def GetProcesses():
    s = "SELECT * FROM pg_stat_activity;"

    # Get data and return it to main below
    db_cursor.execute(s)
    return db_cursor.fetchall()
    # ... to list_of_backups
    db_cursor.close()
    

v_processes = GetProcesses()

print (v_processes)
