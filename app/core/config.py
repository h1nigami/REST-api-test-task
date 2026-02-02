import os

def load_env() -> None:
    try:
        with open(".env", "r") as f:
            for line in f:
               
                line = line.strip()

                
                if not line or line.startswith('#'):
                    continue

                
                key, value = line.split('=', 1)

                os.environ[key.strip()] = value.strip()

    except FileNotFoundError:
        print("Warning: .env файл не найден, скипаю загрузку переменных окружения")