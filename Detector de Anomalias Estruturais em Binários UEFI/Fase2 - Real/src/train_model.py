import os
import numpy as np
from sklearn.ensemble import IsolationForest
import logging

# Importa a função do nosso extrator real
from feature_extractor import extract_uefi_features

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class UEFITrainer:
    def __init__(self):
        # Isolation Forest focado em contaminação baixa (anomalias raras)
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

    def load_dataset_from_directory(self, directory_path):
        """Varre um diretório, extrai features de todos os .efi e converte em matriz numpy."""
        features_list = []
        file_names = []
        
        if not os.path.exists(directory_path):
            logging.warning(f"Diretório não encontrado: {directory_path}")
            return np.array([]), []

        for filename in os.listdir(directory_path):
            if filename.lower().endswith(".efi"):
                filepath = os.path.join(directory_path, filename)
                feats = extract_uefi_features(filepath)
                
                if feats:
                    # Converte o dicionário em um vetor numérico
                    feature_vector = [
                        feats.get('text_entropy', 0.0),
                        feats.get('header_size', 0),
                        feats.get('num_sections', 0),
                        feats.get('has_exports', 0)
                    ]
                    features_list.append(feature_vector)
                    file_names.append(filename)
                    
        return np.array(features_list), file_names

    def train(self, X_train):
        logging.info(f"Treinando o modelo com {len(X_train)} módulos legítimos...")
        self.model.fit(X_train)
        logging.info("Modelo treinado com sucesso!")

    def evaluate(self, X_test, test_filenames):
        logging.info(f"Avaliando {len(X_test)} módulos suspeitos...\n")
        predictions = self.model.predict(X_test)
        scores = self.model.decision_function(X_test)
        
        for i, pred in enumerate(predictions):
            status = "✅ SEGURO" if pred == 1 else "⚠️ ANOMALIA ESTRUTURAL (Possível Rootkit/Ofuscação)"
            print(f"Arquivo: {test_filenames[i]}")
            print(f"Status:  {status} | Score: {scores[i]:.3f}\n")


# ==========================================================
# NOVA FUNÇÃO PARA INTEGRAÇÃO COM A FASE 3
# ==========================================================
def predict():
    """Treina o modelo e retorna o gabarito real e as predições para análise estatística."""
    LEGITIMATE_DIR = "../data/legitimate_efi/"
    INFECTED_DIR = "../data/infected_efi/"
    
    trainer = UEFITrainer()
    
    # 1. Carrega e Treina
    X_train, _ = trainer.load_dataset_from_directory(LEGITIMATE_DIR)
    if len(X_train) == 0:
        raise ValueError("Sem dados legítimos para treinar.")
    trainer.train(X_train)
    
    # 2. Prepara listas de avaliação
    y_true = []
    y_pred = []
    
    # 3. Testa a IA com os arquivos Legítimos (Esperamos que retorne 1)
    X_legit, _ = trainer.load_dataset_from_directory(LEGITIMATE_DIR)
    if len(X_legit) > 0:
        pred_legit = trainer.model.predict(X_legit)
        y_true.extend([1] * len(X_legit)) # Gabarito: 1 (Seguro)
        y_pred.extend(pred_legit)
        
    # 4. Testa a IA com os arquivos Infectados (Esperamos que retorne -1)
    X_infect, _ = trainer.load_dataset_from_directory(INFECTED_DIR)
    if len(X_infect) > 0:
        pred_infect = trainer.model.predict(X_infect)
        y_true.extend([-1] * len(X_infect)) # Gabarito: -1 (Anomalia)
        y_pred.extend(pred_infect)
        
    return y_true, y_pred


if __name__ == "__main__":
    # Mantemos o comportamento original se a pessoa rodar só a Fase 2
    print("===================================================")
    print("🧠 Treinamento de IA com Binários UEFI")
    print("===================================================\n")
    
    trainer = UEFITrainer()
    X_train, train_files = trainer.load_dataset_from_directory("../data/legitimate_efi/")
    if len(X_train) > 0:
        trainer.train(X_train)
        X_test, test_files = trainer.load_dataset_from_directory("../data/infected_efi/")
        if len(X_test) > 0:
            trainer.evaluate(X_test, test_files)