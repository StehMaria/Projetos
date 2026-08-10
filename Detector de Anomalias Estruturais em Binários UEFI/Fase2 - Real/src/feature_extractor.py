import pefile
import math
import os
import json

def calculate_shannon_entropy(data):
    """Calcula a entropia de Shannon real baseada nos bytes da seção."""
    if not data:
        return 0.0
    
    entropy = 0
    length = len(data)
    
    # Conta a frequência de cada byte (0 a 255)
    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1
        
    # Aplica a fórmula matemática H(X)
    for count in byte_counts:
        if count > 0:
            p_x = float(count) / length
            entropy -= p_x * math.log(p_x, 2)
            
    return entropy

def extract_uefi_features(file_path):
    """Abre um arquivo .efi real e extrai metadados da estrutura PE/COFF."""
    try:
        # Carrega o binário UEFI (que utiliza o formato PE)
        pe = pefile.PE(file_path)
        features = {}

        # 1. Buscar a Entropia da seção de código (.text)
        features['text_entropy'] = 0.0
        for section in pe.sections:
            if b'.text' in section.Name:
                features['text_entropy'] = calculate_shannon_entropy(section.get_data())
                break
        
        # 2. Metadados estruturais do cabeçalho
        features['header_size'] = pe.OPTIONAL_HEADER.SizeOfHeaders
        features['num_sections'] = pe.FILE_HEADER.NumberOfSections
        
        # 3. Identificar se possui tabela de exportação (comum em drivers UEFI)
        features['has_exports'] = 1 if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0

        return features
    except Exception as e:
        print(f"Erro ao processar o binário {file_path}: {e}")
        return None

if __name__ == "__main__":
    print("===================================================")
    print("🛡️ Extrator de Caracteristicas em Binários UEFI")
    print("===================================================\n")
    
    # Exemplo prático: Para testar, coloque um arquivo .efi real nesta pasta
    sample_efi = "../data/legitimate_efi/DxeCore.efi"
    
    if os.path.exists(sample_efi):
        print(f"Analisando binário real: {sample_efi}")
        real_features = extract_uefi_features(sample_efi)
        
        print("\n[Metadados Extraídos com Sucesso]")
        print(json.dumps(real_features, indent=4))
    else:
        print(f"⚠️ Arquivo de teste não encontrado em: {sample_efi}")
        print("💡 DICA: Compile o EDK II e copie um arquivo .efi real para a pasta 'data/legitimate_efi/' para testar a extração.")