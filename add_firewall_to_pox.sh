#!/bin/bash

# Verificar que se pasó un argumento
if [ "$#" -ne 1 ]; then
  echo "Uso: $0 archivo.py"
  exit 1
fi

SCRIPT="$1"

# Verificar que el archivo termina en .py
if [[ "$SCRIPT" != *.py ]]; then
  echo "Error: El archivo debe tener extensión .py"
  exit 2
fi

# Verificar que el archivo existe
if [ ! -f "$SCRIPT" ]; then
  echo "Error: No se encontró el archivo '$SCRIPT'"
  exit 3
fi

# Directorio destino
DEST="pox/ext"

# Crear el directorio si no existe
mkdir -p "$DEST"

# Copiar el script
cp "$SCRIPT" "$DEST/"
echo "✅ Copiado $SCRIPT a $DEST/"

# Copiar rules.json si existe junto al script
RULES_DIR=$(dirname "$SCRIPT")
RULES_SRC="$RULES_DIR/rules.json"

if [ -f "$RULES_SRC" ]; then
  cp "$RULES_SRC" "$DEST/"
  echo "✅ Copiado rules.json a $DEST/"
else
  echo "⚠️  No se encontró rules.json en $RULES_DIR"
fi
