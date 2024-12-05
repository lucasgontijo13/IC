import MySQLdb
from django.conf import settings

def create_database():
    try:
        # Conecta ao MySQL sem especificar um banco
        connection = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        cursor = connection.cursor()
        
        # Cria o banco de dados se ele não existir
        db_name = settings.DATABASES['default']['NAME']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Banco de dados '{db_name}' criado ou já existe.")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
    create_database()
