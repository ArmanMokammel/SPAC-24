
import json
import random
import string
from insb_spac24 import settings
from django.http import JsonResponse
from core.models import Registered_Participant, Token_Participant, Token_Session
from django.db.models import Count, F, Prefetch, Value
from django.db.models.functions import Coalesce
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from django.core.files.base import ContentFile
import base64
from email import encoders
from dotenv import set_key
from googleapiclient.discovery import build
from .models import Registered_Participant

class Core:

    def get_active_token_sessions():

        return Token_Session.objects.filter(is_active=True).order_by('order_of_session')

    def get_all_token_sessions():
        
        return Token_Session.objects.all().order_by('order_of_session')

    def get_all_token_sessions_with_participant_counts():
        
        return Token_Session.objects.values('session_name',sessionid=F('id')).annotate(participant_count=Coalesce(Count('token_participant'), Value(0))).order_by('order_of_session')

    def get_all_participant_universities():
        
        return Registered_Participant.objects.values('university').distinct()
    
    def get_all_reg_participants_with_sessions():

        registered_participants = Registered_Participant.objects.prefetch_related(
            Prefetch(
                'token_participant_set',  # Related name for Token_Participant
                queryset=Token_Participant.objects.only('token_session'),  # Optimize with select_related for Token_Session
                to_attr='tokens'
            )
        )
        return registered_participants
    
    def process_qr_data(request):
        try:
            # Get the POST data from the request body
            print(f"Received RAW QR Data: {request.body}")
            sessionid=request.headers.get('session-id')
            data = json.loads(request.body)

            participant = Registered_Participant.objects.get(unique_code=data.get('unqc'))
            session = Token_Session.objects.get(id=sessionid)
            if len(Token_Participant.objects.filter(registered_participant=participant,token_session=sessionid)) > 0:
                return JsonResponse({'status': 'rejected', 'session':session.session_name, 'participant': {'sl':participant.id, 'name': participant.name}})
            else:
                Token_Participant.objects.create(registered_participant=participant,token_session=session)
                return JsonResponse({'status': 'accepted', 'session':session.session_name, 'participant': {'sl':participant.id, 'name': participant.name}})
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    def update_session(sessions):
        all_sessions = Core.get_all_token_sessions()

        for session in all_sessions:
            if str(session.id) in sessions:
                session.is_active = True
            else:
                session.is_active = False
            
            session.save()
        
        return True
    
    
    def generate_unique_code(name: str, university: str) -> str:
        # Function to pick a random part of a string
        def get_random_part(s):
            if len(s) > 1:  # Ensure there are at least 2 characters to pick from
                start = random.randint(0, len(s) - 1)
                end = random.randint(start + 1, len(s))  # Ensure end > start
                return s[start:end]
            return s  # Return the whole string if it's too short
        
        # Pick random parts of the name and university
        name_part = get_random_part(name.replace(" ", "").replace(".", ""))
        university_part = get_random_part(university.replace(" ", "").replace(".", ""))
        
        # Combine the random parts
        base_string = name_part + university_part
        
        # Randomly shuffle the base string
        shuffled = ''.join(random.sample(base_string, len(base_string)))
        
        # Add random characters to make the code between 13 and 16 characters
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Combine shuffled string with random characters
        combined = shuffled + random_chars
        
        # Ensure the length is between 13 and 16 characters
        unique_code = combined[:random.randint(13, 16)]
        
        return unique_code
    
    def save_credentials(credentials):
        set_key('.env', 'GOOGLE_CLOUD_TOKEN', credentials.token)
        settings.GOOGLE_CLOUD_TOKEN = credentials.token
        if(credentials.refresh_token):
            set_key('.env', 'GOOGLE_CLOUD_REFRESH_TOKEN', credentials.refresh_token)
            settings.GOOGLE_CLOUD_REFRESH_TOKEN = credentials.refresh_token
        if(credentials.expiry):
            set_key('.env', 'GOOGLE_CLOUD_EXPIRY', credentials.expiry.isoformat())
            settings.GOOGLE_CLOUD_EXPIRY = credentials.expiry.isoformat()
    
    def get_credentials(request=None):
    
        creds = None

        if settings.GOOGLE_CLOUD_TOKEN:
            creds = Credentials.from_authorized_user_info({
                'token':settings.GOOGLE_CLOUD_TOKEN,
                'refresh_token':settings.GOOGLE_CLOUD_REFRESH_TOKEN,
                'token_uri':settings.GOOGLE_CLOUD_TOKEN_URI,
                'client_id':settings.GOOGLE_CLOUD_CLIENT_ID,
                'client_secret':settings.GOOGLE_CLOUD_CLIENT_SECRET,
                'expiry':settings.GOOGLE_CLOUD_EXPIRY
            },scopes=settings.SCOPES)
            print(creds)
        if not creds or not creds.valid:
            if request:
                user = request.user.username

                print("no creds")

            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    Core.save_credentials(creds)
                except:
                    print("NOT OK")
                    return None
            
            return creds

        return creds
    
    def send_email(request,to_email,cc_email,bcc_email):
       
        email_from = settings.EMAIL_HOST_USER 
        mail_body="Duhh"
        subject = "Hello"

        try:
            credentials = Core.get_credentials(request)
            if not credentials:
                print("NO CREDENTIALS")
                return None

            service = build(settings.GOOGLE_MAIL_API_NAME, settings.GOOGLE_MAIL_API_VERSION, credentials=credentials)
            print(settings.GOOGLE_MAIL_API_NAME, settings.GOOGLE_MAIL_API_VERSION, 'service created successfully')

            message=MIMEMultipart()

            message["From"] = "IEEE NSU SB Portal <ieeensusb.portal@gmail.com>"
            message["To"] = ','.join(to_email)
            message["Cc"] = ','.join(cc_email)
            message["Bcc"] = ','.join(bcc_email)
            message["Subject"] = subject

            # Attach the main message body
            message.attach(MIMEText(mail_body, 'html'))

            #all_participants = Registered_Participant.objects.all().order_by(-id)


            # for file in attachment:
            #     content_file = ContentFile(file.read())
            #     content_file.name = file.name

            #     # Reset the file pointer to the beginning
            #     file.seek(0)

            #     part = MIMEBase('application', 'octet-stream')
            #     part.set_payload(content_file.read())
            #     encoders.encode_base64(part)
            #     part.add_header(
            #         'Content-Disposition',
            #         f'attachment; filename={content_file.name}',
            #     )
            #     message.attach(part)

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            create_message = {"raw": encoded_message}

            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )

            print(f'Message Id: {send_message["id"]}')
            return True
        except Exception as e:
            print(e)
            print(f'Failed to create service instance for gmail')
            return None  