from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def autenticar_google():
    print("Iniciando fluxo de autenticação...")
    
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": "262006177488-3425ks60hkk80fssi9vpohv88g6q1iqd.apps.googleusercontent.com",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )
    
    
    credentials = flow.run_local_server(port=8080, prompt='consent')
    
    print("\n[SUCESSO] Você foi autenticado!")
    print("Token gerado com sucesso. Agora você pode rodar o seu script principal.")

if __name__ == "__main__":
    autenticar_google()
