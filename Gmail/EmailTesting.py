from Gmail import AuthenticateEmail
from Gmail.DownloadEmail import getAllStegoMail

AuthenticateEmail.authenticateUser()
print(AuthenticateEmail.currentEmail)

getAllStegoMail()