import numpy as np
from sklearn.ensemble import IsolationForest
import logging

# Configuração de log para output profissional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UEFIAnomalyDetector:
    """
    Detector de anomalias estruturais em módulos UEFI utilizando Isolation Forest.
    Foca na identificação de ofuscação e injeção de código através de metadados PE/COFF.
    """
    def __init__(self, contamination=0.05):
        self.contamination = contamination
        # Isolation Forest é ideal pois não requer um dataset balanceado com malwares reais
        self.model = IsolationForest(
            n_estimators=100, 
            contamination=self.contamination, 
            random_state=42
        )
        self.is_trained = False

    def train_baseline(self, normal_features):
        """Treina o modelo com a estrutura matemática de binários conhecidos e seguros."""
        logging.info("Iniciando treinamento com a estrutura de binários conhecidos (Golden Image)...")
        self.model.fit(normal_features)
        self.is_trained = True
        logging.info("Treinamento concluído com sucesso.")

    def analyze_module(self, module_features):
        """Avalia um novo módulo e retorna a predição (-1 para anomalia, 1 para normal)."""
        if not self.is_trained:
            raise ValueError("O modelo precisa ser treinado antes da análise.")
            
        prediction = self.model.predict(module_features)
        anomaly_score = self.model.decision_function(module_features)
        
        return prediction[0], anomaly_score[0]

if __name__ == "__main__":
    print("===================================================")
    print("🛡️ Detector de Anomalias Estruturais em Binários UEFI - PoC")
    print("===================================================\n")

    # Features: [Entropia_Secao_Text, Tamanho_Relativo_Cabecalho, Num_Funcoes_Exportadas]
    
    # 1. Base de Conhecimento (Golden Image)
    # Simulando a extração de 100 módulos UEFI íntegros
    # Entropia média ~4.5, Cabeçalho ~1024 bytes, Funções ~10
    np.random.seed(42)
    normal_data = np.random.normal(loc=[4.5, 1024, 10], scale=[0.5, 50, 2], size=(100, 3))
    
    # 2. Inicializando e Treinando o Detector
    detector = UEFIAnomalyDetector(contamination=0.05)
    detector.train_baseline(normal_data)
    
    # 3. Cenários de Teste
    print("\n--- Iniciando Auditoria de Módulos ---")
    
    # Teste A: Módulo Íntegro
    clean_module = np.array([[4.6, 1010, 11]]) 
    pred_clean, score_clean = detector.analyze_module(clean_module)
    
    # Teste B: Módulo Comprometido (Entropia altíssima indicando código ofuscado/injetado)
    infected_module = np.array([[7.9, 1500, 1]]) 
    pred_infected, score_infected = detector.analyze_module(infected_module)
    
    # 4. Resultados
    print("\n[Resultado Teste A - Módulo Íntegro]")
    if pred_clean == 1:
         print(f"✅ Status: SEGURO (Score: {score_clean:.3f})")
    
    print("\n[Resultado Teste B - Módulo Suspeito]")
    if pred_infected == -1:
         print(f"⚠️ Status: ANOMALIA DETECTADA (Score: {score_infected:.3f})")
         print("   -> Motivo: Desvio estrutural significativo (Possível ofuscação ou injeção).")