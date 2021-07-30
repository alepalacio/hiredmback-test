from django.db import models
from django.db.models.deletion import CASCADE
from users.models import User

# Create your models here.

def _upload_path(instance, filename):
    return instance.get_upload_path(filename)

#PERFIL DE USUARIO

class Developer(models.Model):

    AREAS = (
        ("Full Stack", "Full Stack"),
        ("Backend", "Backend"),
        ("Frontend", "Frontend"),
        ("UX/UI", "UX/UI"),
    )

    LANGUAGES = (
        ("Python", "Python"),
        ("JavaScript", "JavaScript"),
        ("Java", "Java"),
        ("C/C++", "C/C++"),
        ("C#", "C#"),
        ("GO", "GO"),
        ("Other language", "Other language"),
    )

    id = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name="user_id")
    email = models.OneToOneField(User, on_delete=CASCADE, related_name="user_email", verbose_name="User email", default="")
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=50, default="")
    bio = models.TextField("Biography", null=True, blank=True)
    education = models.CharField("Education degree", max_length=200, default="")
    dev_area = models.CharField("Main development area", max_length=50, choices=AREAS, default="")
    main_language = models.CharField("Main development language", max_length=50, choices=LANGUAGES, default="")
    experience = models.TextField(default="")
    website = models.URLField(null=True, blank=True, default="")
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_upload_path(self, filename):
        return "./" + str(self.user_id.id) + "/" + filename

#LOGROS DE USUARIO
class Achievement(models.Model):
    typeoptions = (
        ("Certifications", "Certifications"),
        ("Languages", "Languages"),
        ("Conferences", "Conferences"),
        ("Repositories", "Repositories"),
        ("Experience", "Experience"),
        ("Others", "Others"),
    )
    user_id = models.ForeignKey(
        Developer, on_delete=CASCADE, default="", related_name="achievements"
    )
    title = models.CharField(max_length=40)
    origin = models.CharField(max_length=60, default="")
    description = models.CharField(max_length=100, default="")
    start_date = models.DateField()
    finish_date = models.DateField(null=True, blank=True, default=None)
    feats_type = models.CharField(choices=typeoptions, max_length=40)
    is_verified = models.BooleanField(default=False)
    verification = models.ImageField(blank=True, upload_to=_upload_path)

    def __str__(self):
        return self.title

    def get_upload_path(self, filename):
        return "./" + str(self.user_id.id) + "/" + filename
