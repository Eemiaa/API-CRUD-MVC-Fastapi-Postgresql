from configs.database import get_db

def migrate():
    """Script de migração para atualizar os documentos existentes"""
    db = next(get_db())  # Pegando a conexão com o banco


    """Script de migração para atualizar os documentos existentes"""
    llmdb = db["llmextension"]
    if ["interaction_logs"] not in llmdb.list_collection_names():
        intteraction_logs = llmdb["interaction_logs"]

        print("🛠️ Criando índice para o campo 'email'...")
        intteraction_logs.insert_one({"global_uemail": "", 
                                        "documentname": "",
                                        "documentpath": "",
                                        "language": "",
                                        "type": "",
                                        "time": "",
                                        "line": "",
                                        "text": "",
                                        "linecount": ""})

