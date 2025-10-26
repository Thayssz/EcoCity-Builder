# [file name]: src/core/salvamento.py
# [file content begin]
import json
import os
from datetime import datetime

class GerenciadorSalvamento:
    def __init__(self, pasta_saves="saves"):
        self.pasta_saves = pasta_saves
        self.criar_pasta_saves()
    
    def criar_pasta_saves(self):
        """Cria a pasta de saves se não existir"""
        if not os.path.exists(self.pasta_saves):
            os.makedirs(self.pasta_saves)
    
    def salvar_jogo(self, cidade, nome_arquivo=None):
        """Salva o estado atual do jogo"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{cidade.nome}_{timestamp}.json"
        
        caminho_save = os.path.join(self.pasta_saves, nome_arquivo)
        
        dados_save = {
            'cidade': {
                'nome': cidade.nome,
                'dificuldade': cidade.dificuldade,
                'populacao': cidade.populacao,
                'tempo_jogo': cidade.tempo_jogo,
                'construcoes': [construcao.get_beneficios() for construcao in cidade.construcoes],
                'tecnologias_desbloqueadas': cidade.tecnologias_desbloqueadas
            },
            'recursos': cidade.recursos.to_dict(),
            'metadata': {
                'data_salvamento': datetime.now().isoformat(),
                'versao_jogo': '1.0'
            }
        }
        
        try:
            with open(caminho_save, 'w', encoding='utf-8') as f:
                json.dump(dados_save, f, indent=2, ensure_ascii=False)
            return True, f"Jogo salvo em {nome_arquivo}"
        except Exception as e:
            return False, f"Erro ao salvar: {e}"
    
    def listar_saves(self):
        """Lista todos os saves disponíveis"""
        saves = []
        if os.path.exists(self.pasta_saves):
            for arquivo in os.listdir(self.pasta_saves):
                if arquivo.endswith('.json'):
                    caminho = os.path.join(self.pasta_saves, arquivo)
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            dados = json.load(f)
                        
                        saves.append({
                            'arquivo': arquivo,
                            'cidade': dados['cidade']['nome'],
                            'dificuldade': dados['cidade']['dificuldade'],
                            'populacao': dados['cidade']['populacao'],
                            'data_salvamento': dados['metadata']['data_salvamento'],
                            'tempo_jogo': dados['cidade']['tempo_jogo']
                        })
                    except:
                        continue
        
        # Ordenar por data mais recente
        saves.sort(key=lambda x: x['data_salvamento'], reverse=True)
        return saves
    
    def carregar_jogo(self, nome_arquivo):
        """Carrega um jogo salvo"""
        caminho_save = os.path.join(self.pasta_saves, nome_arquivo)
        
        try:
            with open(caminho_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Criar cidade
            from models.cidade import Cidade
            cidade = Cidade(
                dados['cidade']['nome'],
                dados['cidade']['dificuldade']
            )
            
            # Restaurar estado
            cidade.populacao = dados['cidade']['populacao']
            cidade.tempo_jogo = dados['cidade']['tempo_jogo']
            cidade.tecnologias_desbloqueadas = dados['cidade']['tecnologias_desbloqueadas']
            
            # Restaurar recursos
            cidade.recursos = Recurso.from_dict(dados['recursos'])
            
            # Restaurar construções (simplificado por enquanto)
            cidade.construcoes = []  # Será reconstruído durante o jogo
            
            return True, cidade, "Jogo carregado com sucesso!"
            
        except Exception as e:
            return False, None, f"Erro ao carregar: {e}"
    
    def deletar_save(self, nome_arquivo):
        """Deleta um save"""
        caminho_save = os.path.join(self.pasta_saves, nome_arquivo)
        try:
            os.remove(caminho_save)
            return True, "Save deletado com sucesso"
        except Exception as e:
            return False, f"Erro ao deletar: {e}"
# [file content end]