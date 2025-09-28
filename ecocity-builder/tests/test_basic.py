"""
Testes básicos para as funcionalidades iniciais
"""

import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from models.base import Recurso

class TestRecurso:
    """Testes para a classe Recurso"""
    
    def test_criacao_recurso(self):
        """Testa a criação de recursos com valores padrão"""
        recurso = Recurso()
        assert recurso.dinheiro == 1000
        assert recurso.emissao_carbono == 50
        assert recurso.satisfacao_populacional == 70
    
    def test_recursos_suficientes(self):
        """Testa verificação de recursos suficientes"""
        recurso = Recurso(dinheiro=500)
        
        assert recurso.verificar_recursos_suficientes(400) == True
        assert recurso.verificar_recursos_suficientes(600) == False
    
    def test_string_representation(self):
        """Testa a representação em string dos recursos"""
        recurso = Recurso(dinheiro=1234.56, emissao_carbono=45.5, satisfacao=85)
        string_repr = str(recurso)
        
        assert "💰 $1234.56" in string_repr
        assert "🌍 45.5CO₂" in string_repr  
        assert "😊 85%" in string_repr

def test_exemplo_integracao():
    """Teste de integração básico"""
    recurso = Recurso(dinheiro=1000, emissao_carbono=50, satisfacao=70)
    
    # Simular construção
    recurso.dinheiro -= 300
    recurso.emissao_carbono -= 5
    
    assert recurso.dinheiro == 700
    assert recurso.emissao_carbono == 45

def test_recurso_completo():
    """Teste completo da classe Recurso"""
    # Teste criação
    recurso = Recurso(dinheiro=2000, emissao_carbono=40, satisfacao=85)
    
    assert recurso.dinheiro == 2000
    assert recurso.emissao_carbono == 40
    assert recurso.satisfacao_populacional == 85
    
    # Teste verificação de recursos
    assert recurso.verificar_recursos_suficientes(1000) == True
    assert recurso.verificar_recursos_suficientes(2500) == False
    
    # Teste string representation
    string_repr = str(recurso)
    assert "💰 $2000.00" in string_repr
    assert "🌍 40.0CO₂" in string_repr
    assert "😊 85%" in string_repr
    
    # Teste método atualizar (deveria fazer nada por enquanto)
    recurso.atualizar()
    assert recurso.dinheiro == 2000  # Não mudou