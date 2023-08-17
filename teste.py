from models.firebase import initialize_firebase

#iniciando conexão com o firebase
firebase = initialize_firebase()
db = firebase.database()


a = db.order_by_child("sourceID").equal_to('src_Zdd8jxt9mgyenpQygblcz').get()
#print(a[0].key())
try:
  print(a[0].key())
  db.child(a[0].key()).remove()
  print('ok')
except:
  print('NOK')
