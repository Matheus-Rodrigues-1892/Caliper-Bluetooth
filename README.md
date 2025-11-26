# Caliper Bluetooth - Leitor de Paquímetro Shahe BLE

Este projeto permite a leitura de medições de um paquímetro digital Shahe via Bluetooth Low Energy (BLE).

## Requisitos

- Módulo `bleak` para comunicação Bluetooth Low Energy
- 5114L Built-in Wireless Depth caliper

## 🔧 Instalação

### 1. Instalar o módulo bleak

```bash
pip install bleak
```

Ou, se você tiver múltiplas versões do Python instaladas:

```bash
python -m pip install bleak
```

## Arquivos do Projeto

### `caliper_reader.py`

**Descrição:** Script principal para leitura de medições do paquímetro Shahe.

**Funcionalidades:**
- Procura automaticamente o dispositivo pelo nome ou endereço MAC
- Conecta ao paquímetro via Bluetooth
- Recebe medições em tempo real quando você pressiona o botão do paquímetro
- Exibe as medições em milímetros (mm)

**Como usar:**

```bash
python caliper_reader.py
```

**Configuração:** Se seu paquímetro tiver um nome ou endereço diferente, edite as variáveis no início do arquivo:

```python
DEVICE_NAME = "B-00010029"       # Nome do seu dispositivo
DEVICE_ADDRESS = "00:00:00:00:27:2D"  # Endereço MAC do seu dispositivo
```

**Saída esperada:**

```
==================================================
       LEITOR DE CALIPER SHAHE BLE
==================================================

Procurando caliper 'B-00010029'...
Caliper encontrado: B-00010029 (00:00:00:00:27:2D)

Conectando...
Conectado!

==================================================
 Pressione o botão para enviar novas medições
==================================================

Medição: 25.40 mm
Medição: 30.15 mm
```

Para encerrar, pressione `Ctrl+C`.

---

### `test_blue.py`

**Descrição:** Script de diagnóstico para descobrir dispositivos Bluetooth disponíveis e seus serviços.

**Funcionalidades:**
- Escaneia todos os dispositivos Bluetooth Low Energy próximos
- Lista informações detalhadas de cada dispositivo:
  - Nome e endereço MAC
  - Serviços disponíveis
  - Características (UUIDs)
  - Descritores

**Como usar:**

```bash
python test_blue.py
```

**Quando usar:** Use este script para:
- Descobrir o nome e endereço do seu paquímetro
- Identificar os UUIDs de serviço e característica corretos
- Depurar problemas de conexão


