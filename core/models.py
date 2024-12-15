from django.db import models

# Create your models here.
class Registered_Participant(models.Model):
    university_id=models.CharField(null=False, blank=False, max_length=20)
    name=models.CharField(null=False, blank=False, max_length=150)
    university=models.CharField(null=False, blank=False, max_length=150)
    unique_code=models.CharField(null=False, blank=False, max_length=150)

    class Meta:
        verbose_name="Registered Participant"

    def __str__(self):
        return str(self.pk)

class Token_Session(models.Model):
    session_name=models.CharField(null=False, blank=False, max_length=20)
    is_active=models.BooleanField(null=False, blank=False, default=False)
    is_independent=models.BooleanField(null=False, blank=False, default=False)
    order_of_session=models.IntegerField(null=False,blank=False,default=0)

    class Meta:
        verbose_name="Token Session"

    def current_session():
        return Token_Session.objects.filter(is_active=True, is_independent=False)[0]

    def save(self, *args, **kwargs):
        if (self.pk):
            if(kwargs.get('is_active') == 'on' and (kwargs.get('is_independent') == 'off' or self.is_independent == False)):
                Token_Session.objects.filter(is_active=True, is_independent=False).update(is_active=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

class Token_Participant(models.Model):
    registered_participant=models.ForeignKey(Registered_Participant, null=False, blank=False, on_delete=models.CASCADE)
    token_session=models.ForeignKey(Token_Session, null=False, blank=False, on_delete=models.CASCADE)
    date_time=models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        verbose_name="Applied Participant Token"

    def __self__(self) -> str:
        return str(self.pk)