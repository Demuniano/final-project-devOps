#!/bin/bash

# Script para ejecutar pruebas del proyecto Store API

echo "🧪 Ejecutando pruebas de Store API..."
echo "=================================="

# Verificar que pytest esté instalado
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest no está instalado. Instalando..."
    pip install pytest pytest-asyncio httpx pytest-cov
fi

# Ejecutar pruebas con diferentes opciones
case "${1:-all}" in
    "unit")
        echo "🔬 Ejecutando pruebas unitarias..."
        pytest tests/test_clients.py tests/test_products.py tests/test_sales.py -v
        ;;
    "integration")
        echo "🔗 Ejecutando pruebas de integración..."
        pytest tests/test_integration.py -v
        ;;
    "coverage")
        echo "📊 Ejecutando pruebas con reporte de cobertura..."
        pytest --cov=app --cov-report=term-missing --cov-report=html:htmlcov
        echo "📈 Reporte HTML generado en: htmlcov/index.html"
        ;;
    "fast")
        echo "⚡ Ejecutando pruebas rápidas (sin cobertura)..."
        pytest -x --disable-warnings
        ;;
    "all"|*)
        echo "🎯 Ejecutando todas las pruebas..."
        pytest
        ;;
esac

echo ""
echo "✅ Pruebas completadas!"
echo ""
echo "💡 Uso del script:"
echo "  ./run_tests.sh          # Todas las pruebas"
echo "  ./run_tests.sh unit     # Solo pruebas unitarias"
echo "  ./run_tests.sh integration  # Solo integración"
echo "  ./run_tests.sh coverage # Con reporte de cobertura"
echo "  ./run_tests.sh fast     # Pruebas rápidas"
