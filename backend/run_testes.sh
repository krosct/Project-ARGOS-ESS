#!/bin/bash

# Script para rodar testes do backend - Projeto Argos
# Uso: ./run_tests.sh [opção]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Projeto Argos - Test Runner ===${NC}\n"

# Verifica se está no diretório backend
if [ ! -d "tests" ]; then
    echo -e "${RED}Erro: Execute este script do diretório backend/${NC}"
    exit 1
fi

# Ativa ambiente virtual se existir
if [ -d ".venv" ]; then
    echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
    source .venv/bin/activate
fi

# Função para rodar testes unitários
run_unit_tests() {
    echo -e "${GREEN}Rodando testes unitários...${NC}"
    pytest tests/unit/ -v --tb=short
}

# Função para rodar testes com cobertura
run_coverage() {
    echo -e "${GREEN}Rodando testes com cobertura...${NC}"
    pytest tests/unit/ --cov=app --cov-report=term-missing --cov-report=html
    echo -e "\n${GREEN}Relatório HTML gerado em: htmlcov/index.html${NC}"
}

# Função para rodar testes específicos
run_specific() {
    echo -e "${GREEN}Rodando testes de $1...${NC}"
    pytest tests/unit/test_$1.py -v
}

# Função para rodar todos os testes
run_all() {
    echo -e "${GREEN}Rodando TODOS os testes...${NC}"
    pytest tests/ -v --tb=short
}

# Menu de opções
case "${1:-unit}" in
    unit)
        run_unit_tests
        ;;
    coverage|cov)
        run_coverage
        ;;
    schemas)
        run_specific "schemas"
        ;;
    models)
        run_specific "models"
        ;;
    auth)
        run_specific "auth_router"
        ;;
    check)
        run_specific "check_router"
        ;;
    history)
        run_specific "history_router"
        ;;
    all)
        run_all
        ;;
    help|--help|-h)
        echo "Uso: ./run_tests.sh [opção]"
        echo ""
        echo "Opções disponíveis:"
        echo "  unit      - Roda testes unitários (padrão)"
        echo "  coverage  - Roda testes com relatório de cobertura"
        echo "  schemas   - Roda apenas testes de schemas"
        echo "  models    - Roda apenas testes de models"
        echo "  auth      - Roda apenas testes de autenticação"
        echo "  check     - Roda apenas testes de verificação"
        echo "  history   - Roda apenas testes de histórico"
        echo "  all       - Roda todos os testes (unit + integration)"
        echo "  help      - Mostra esta mensagem"
        ;;
    *)
        echo -e "${RED}Opção inválida: $1${NC}"
        echo "Use './run_tests.sh help' para ver opções disponíveis"
        exit 1
        ;;
esac

echo -e "\n${GREEN}✓ Concluído!${NC}"