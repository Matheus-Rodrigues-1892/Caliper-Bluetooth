import asyncio
from bleak import BleakClient, BleakScanner

# Configurações do Caliper Shahe
DEVICE_NAME = "B-00010029"
DEVICE_ADDRESS = "00:00:00:00:27:2D"

# UUID do serviço e característica para receber medições
SERVICE_UUID = "0000ffff-0000-1000-8000-00805f9b34fb"
CHAR_UUID = "0000ff00-0000-1000-8000-00805f9b34fb"


def parse_measurement(data: bytes) -> str:
    """
    Interpreta os bytes recebidos do caliper Shahe.
    Formato : bytes[5:7] em Big Endian, dividido por 100 = mm
    """
    if len(data) < 7:
        return f"(dados incompletos: {list(data)})"
    
    raw_value = int.from_bytes(data[5:7], byteorder='big', signed=False)
    
    measurement_mm = raw_value / 100.0
    
    return f"{measurement_mm:.2f} mm"


async def main():
    print("=" * 50)
    print("       LEITOR DE CALIPER SHAHE BLE")
    print("=" * 50)
    print()
    
    # Procura o dispositivo
    print(f"Procurando caliper '{DEVICE_NAME}'...")
    
    device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=10.0)
    
    if device is None:
        # Tenta pelo endereço
        print(f"   Não encontrado pelo nome, tentando endereço {DEVICE_ADDRESS}...")
        device = await BleakScanner.find_device_by_address(DEVICE_ADDRESS, timeout=10.0)
    
    if device is None:
        print("Caliper não encontrado!")
        print("   - Verifique se o caliper está ligado")
        print("   - Tente aproximar o caliper do computador")
        return
    
    print(f"Caliper encontrado: {device.name} ({device.address})")
    print()
    
    # Conecta ao dispositivo
    print("Conectando...")
    
    async with BleakClient(device, timeout=20.0) as client:
        if not client.is_connected:
            print("Falha na conexão!")
            return
        
        print("Conectado!")
        print()
        print("=" * 50)
        print("  Aperte o botão DATA no caliper para enviar")
        print("  medições. Pressione Ctrl+C para sair.")
        print("=" * 50)
        print()
        
        # Callback para receber notificações
        def notification_handler(sender, data: bytearray):
            measurement = parse_measurement(bytes(data))
            print(f"Medição: {measurement}")
        
        # Ativa notificações na característica
        await client.start_notify(CHAR_UUID, notification_handler)
        
        # Mantém o programa rodando
        try:
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
        finally:
            # Desativa notificações antes de sair
            await client.stop_notify(CHAR_UUID)
            print("\nDesconectado!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n Finalizado")
