import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

def comparar_modelos_calibracao(matriz_dados):
    """
    Recebe uma matriz (N, 4) e compara um meta-modelo linear vs. quadrático
    para calibração.

    Formato da Matriz :
    - Coluna 0: y_true 
    - Coluna 1: prob_alta 
    - Coluna 2: prob_ui 
    - Coluna 3: prob_uti 
    """
    
    y_true = matriz_dados[:, 0]
    X_meta = matriz_dados[:, 2:4].astype(float) 
    

    labels = sorted(np.unique(y_true))
    
    print(f"Total de {len(y_true)} amostras recebidas.")
    print(f"Classes únicas encontradas: {labels}\n")

    pipe_linear = Pipeline([
        ('scaler', StandardScaler()),
        ('meta_model', LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42))
    ])


    pipe_quadratico = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('scaler', StandardScaler()),
        ('meta_model', LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42))
    ])


    scoring_metric = 'f1_weighted'
    cv_folds = 5

    print(f"Avaliando Modelo Padrão (Linear) com Validação Cruzada ({cv_folds} folds)...")
    scores_linear = cross_val_score(pipe_linear, X_meta, y_true, cv=cv_folds, scoring=scoring_metric)
    print(f"  Scores (F1 Ponderado): {np.round(scores_linear, 4)}")
    print(f"  Média F1: {scores_linear.mean():.4f} (+/- {scores_linear.std():.4f})\n")

    print(f"Avaliando Modelo Quadrático (Grau 2) com Validação Cruzada ({cv_folds} folds)...")
    scores_quad = cross_val_score(pipe_quadratico, X_meta, y_true, cv=cv_folds, scoring=scoring_metric)
    print(f"  Scores (F1 Ponderado): {np.round(scores_quad, 4)}")
    print(f"  Média F1: {scores_quad.mean():.4f} (+/- {scores_quad.std():.4f})\n")


    print("--- Conclusão da Comparação ---")
    
    melhor_pipeline = None
    nome_melhor_modelo = ""
    
    if scores_quad.mean() > scores_linear.mean():
        diferenca = scores_quad.mean() - scores_linear.mean()
        print(f"O Modelo Quadrático (Grau 2) teve performance superior (+{diferenca:.4f}).")
        melhor_pipeline = pipe_quadratico
        nome_melhor_modelo = "Quadrático (Grau 2)"
    else:
        diferenca = scores_linear.mean() - scores_quad.mean()
        print(f"O Modelo Padrão (Linear) teve performance superior ou igual (+{diferenca:.4f}).")
        melhor_pipeline = pipe_linear
        nome_melhor_modelo = "Linear Padrão"

    

    X_train, X_test, y_train, y_test = train_test_split(X_meta, y_true, test_size=0.3, stratify=y_true, random_state=42)
    
    melhor_pipeline.fit(X_train, y_train)
    y_pred = melhor_pipeline.predict(X_test)
    
    print(f"\nRelatório de Classificação (em {len(y_test)} amostras de teste):")
    print(classification_report(y_test, y_pred, labels=labels))
    
    print("Matriz de Confusão (Teste):")
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, 
                         index=[f'Real: {l}' for l in labels], 
                         columns=[f'Prev: {l}' for l in labels])
    print(cm_df)
    

    return melhor_pipeline




