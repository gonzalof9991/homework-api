def get_url_database() -> str:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST")
    db = os.environ.get("POSTGRES_DB")
    port = os.environ.get("POSTGRES_PORT")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
