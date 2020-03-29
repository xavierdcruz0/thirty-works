"""

Usage: $ python manage.py shell < createusers.py

"""


from django.contrib.auth.models import User
import pandas as pd
import os
from django.db.utils import IntegrityError


EVENTBRITE_EXCEL_PATH = os.path.join(os.path.expanduser('~'), '3030DryRun2.xlsx')

def id_generator(size):
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def email(subject, message, recipient_list):
    from django.conf import settings
    from django.core.mail import send_mail
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )

EMAIL_SUBJECT = "Your new 30works account is ready"
EMAIL_MESSAGE = """

Dear User,

You're receiving this message because I wanted to say hello and see how you're doing.

Not really. This email was automatically generated by a program.

Just to let you know that your 30works account is set up:

        Username: {}
        Password: {}

You can now log in at https://www.thirty.works/login/ with these credentials. 

After logging in for the first time we advise changing your password to something memorable for security, which you can do by visiting https://www.thirty.works/profile/ and hitting "Change Password".

Your username can also be changed there.

Good luck and we look forward to receiving your works this month.

Best wishes,

The Unfeeling Email Robot 🤖

"""

# read the CSV file
# df = pd.read_csv(USER_DATA_PATH)
# read the Excel file
df = pd.read_excel(EVENTBRITE_EXCEL_PATH)

for i, row in df.iterrows():
    username = row['First Name'] + '_' + row['Surname']
    email_address = row['Email Address']
    password = id_generator(10)
    try:
        user = User.objects.create_user(username=username, password=password, email=email_address)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        print('Created User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))

        email_message = "{}".format(EMAIL_MESSAGE)
        email_message = email_message.format(username, password)
        email(EMAIL_SUBJECT, email_message, [email_address])

    except IntegrityError as ie:
        print(ie)
        print('Couldnt create User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))
