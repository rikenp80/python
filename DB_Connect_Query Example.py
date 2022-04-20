import psycopg2

conn = psycopg2.connect(host="reimagine-dev-canada.cluster-c514w15qevsg.ca-central-1.rds.amazonaws.com", database="orders", user="reimagineUser", password="")
cur=conn.cursor()

sql='select count(*) from "Branch"'

cur.execute(sql)
results = cur.fetchone()

cur.close()

print (results)
