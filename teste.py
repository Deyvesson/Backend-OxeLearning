import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("./oxelearning-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

user = auth.get_user('4JkEX0gucEVAL1IrmbrpgnDbWL72')
print(user.email)
print('Successfully fetched user data: {0}'.format(user.uid))

