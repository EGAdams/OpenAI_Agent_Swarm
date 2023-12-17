import sys
sys.path.append('/home/adamsl/linuxBash/thanksgiving_week_temp/OpenAI_Agent_Swarm/pydantic-settings')
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    OPENAI_API_KEY: str  

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
