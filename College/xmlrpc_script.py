import xmlrpc.client as xmlrpclib
url = 'http://localhost:8069' #URL of Odoo server
db = 'training_demo'  #Database Name
user = 'admin' #User name
pwd = 'admin' #Password

# To find the Version of Odoo server
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

#Authenticate User
uid = common.authenticate(db, user, pwd, {})
print(uid)
 
#Reading Records
model = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
 
stud_records = model.execute_kw(db, uid, pwd,'clg.student','search_read',[[]],{'fields':['id','name','roll_no','department_id'],'limit':3})
print(stud_records)
for rec in stud_records:
    print("Name: %s and Roll No.: %s" %(rec['name'],rec['roll_no']))
 
#Read Specific Record
stud_record = model.execute_kw(db, uid, pwd,'clg.student','read',[[22]],{'fields':['id','name','roll_no']})
print(stud_record)
 
#Write/Update a record
stud_record = model.execute_kw(db, uid, pwd,'clg.student','write',[[1],{'height':6.2}])
stud_record = model.execute_kw(db, uid, pwd,'clg.student','read',[[1]],{'fields':['height','name']})
print(stud_record)

#Create a record
department = model.execute_kw(db, uid, pwd,'clg.department','search',[[['name','=','BCA1']]])
id = model.execute_kw(db, uid, pwd, 'clg.student', 'create', [{
    'name': "New Partner 006",'roll_no':'00000006','dob':'2020-4-6','department_id':department[0] if department else []
    }])
print("Created Record ID is: %s" % id)

