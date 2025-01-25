import json
import psycopg2
from config import rds_host, db_username, db_password, db_name

def lambda_handler(event, context):
    cpf = event['cpf']
    
    # Conexão com o banco de dados
    connection = psycopg2.connect(
        host=rds_host,
        user=db_username,
        password=db_password,
        dbname=db_name
    )
    
    try:
        with connection.cursor() as cursor:
            # Ajuste a consulta SQL para buscar os períodos da tabela demonstrativos_pagamento
            sql = """
                SELECT dp.ano, dp.mes
                FROM demonstrativos_pagamento dp
                JOIN ex_funcionarios ef ON dp.ex_funcionario_id = ef.id
                WHERE ef.cpf = %s
            """
            cursor.execute(sql, (cpf,))
            result = cursor.fetchall()
        
        # Agrupar meses por ano
        grouped_result = {}
        for row in result:
            ano, mes = row
            if ano not in grouped_result:
                grouped_result[ano] = []
            grouped_result[ano].append(mes)
        
        # Formatar a resposta
        response_data = [{"ano": ano, "meses": meses} for ano, meses in grouped_result.items()]
        response = {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
    finally:
        connection.close()
    
    return response
