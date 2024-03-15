# Login URLS
AUTH_ENDPOINT = "https://signin.tradestation.com/authorize"
TOKEN_ENDPOINT = "https://signin.tradestation.com/oauth/token"  # nosec - This isn't a hardcoded password
AUDIENCE_ENDPOINT = "https://api.tradestation.com"
REVOKE_ENDPOINT = "https://signin.tradestation.com/oauth/revoke"
# Stored credential information
client_key: str = "" # is 'client_id' may either place id here, or in credentials.jason file
client_secret: str = "" # may either place secret here, or in credentials.jason file
authorization_scope: str = "" # may either place scope here, or in credentials.jason file
call_back_domain: str = "" # may either place callback domain here, or in credentials.jason file
paper_trade: bool = False #True = simulated trading, False = live trading
access_token:str = ""
access_token_expires_at:int = 0 # track when access token will expire
access_token_expire_margin:int = 5; # Number of seconds before exporation when access token is refreshed 
refresh_token:str = ""
id_token:str = ""
scope:str = ""
# Vars for function operation, do not edit
state:str = "" # ideally this variable would be passed directly through functions, but for the moment it is simplest to keep it here
ts_state_isLoaded:bool = False # tracks if script has already looked in ts_state.jason for token information
path_to_JSON:str = "secret/"