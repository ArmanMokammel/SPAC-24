from django.contrib import admin
from core.models import Token_Session, Registered_Participant, Token_Participant

# Register your models here.
@admin.register(Token_Session)
class SessionAdmin(admin.ModelAdmin):
    
    list_display = ['session_name', 'is_independent', 'is_active']

    def save_model(self, request, obj, form, change):
        print(form.data)
        if(form.data.get('is_active') == 'on' and (form.data.get('is_independent') == 'off' or obj.is_independent == False)):
                Token_Session.objects.filter(is_active=True, is_independent=False).update(is_active=False)

        super().save_model(request, obj, form, change)

admin.site.register(Registered_Participant)

@admin.register(Token_Participant)
class Token_ParticipantAdmin(admin.ModelAdmin):
     list_display = ['registered_participant', 'token_session__session_name', 'date_time']
     ordering = ['-token_session__order_of_session']