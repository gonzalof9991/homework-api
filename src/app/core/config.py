def get_url_database() -> str:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    db = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
