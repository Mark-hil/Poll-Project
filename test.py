from django.contrib.auth.models import User
admins = User.objects.filter(is_staff=True, is_superuser=True)
for admin in admins:
    print(admin.username, admin.email)
