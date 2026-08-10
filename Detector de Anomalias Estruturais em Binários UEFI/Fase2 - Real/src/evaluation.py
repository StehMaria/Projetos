import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import logging

# IMPORTAÇÃO REAL DA FASE 2
from train_model import predict

logging.basicConfig(level=logging.INFO, format='%(message)s')

def generate_evaluation_report(y_true, y_pred):
    """
    Compara o gabarito real (y_true) com as predições da IA (y_pred)
    e gera um relatório estatístico de performance.
    """
    logging.info("\n📊 Relatório de Validação do Modelo (Isolation Forest)\n")
    
    # Convertendo 1 e -1 para binário (0 e 1) onde a Anomalia (-1) é a classe Positiva (1) detectada
    y_true_binary = [1 if y == -1 else 0 for y in y_true]
    y_pred_binary = [1 if y == -1 else 0 for y in y_pred]

    acc = accuracy_score(y_true_binary, y_pred_binary)
    prec = precision_score(y_true_binary, y_pred_binary, zero_division=0)
    rec = recall_score(y_true_binary, y_pred_binary, zero_division=0)
    f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
    cm = confusion_matrix(y_true_binary, y_pred_binary)

    print(f"✅ Acurácia Global: {acc:.2%}")
    print(f"🎯 Precisão:        {prec:.2%} (Das anomalias apontadas, quantas eram reais?)")
    print(f"🔍 Recall:          {rec:.2%} (De todas as anomalias reais, quantas a IA achou?)")
    print(f"⚖️ F1-Score:        {f1:.2%} (Balanço harmônico)\n")
    
    print("⬛ Matriz de Confusão:")
    # Tratamento caso a matriz retorne apenas 1 dimensão (ex: só testou arquivos legítimos)
    if cm.size == 4:
        print(f"   Verdadeiros Negativos (Módulos Seguros validados):      {cm[0][0]}")
        print(f"   Falsos Positivos      (Alarme Falso):                   {cm[0][1]}")
        print(f"   Falsos Negativos      (Rootkit passou batido):         {cm[1][0]}")
        print(f"   Verdadeiros Positivos (Rootkits pegos com sucesso):    {cm[1][1]}\n")
    else:
        print(f"   (Matriz incompleta - adicione arquivos infectados para visualização total: {cm})")

if __name__ == "__main__":
    print("===================================================")
    print("🛡️ Avaliação Estatística de Detecção de Rootkits")
    print("===================================================")
    print("Iniciando bateria de testes com dados extraídos da Fase 2...\n")
    
    try:
        # Extrai os dados reais da Fase 2 (Isso vai ler os .efi, treinar a IA e classificar tudo)
        gabarito_real, resposta_da_ia = predict()
        
        # Chama a função geradora de métricas
        generate_evaluation_report(gabarito_real, resposta_da_ia)
        
    except ValueError as ve:
        print(f"❌ Erro de Validação: {ve}")
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")