import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CARAS = 20
DADOS = 3

def calcular_frecuencias():
    """Calcula las frecuencias usando programación dinámica."""
    dp = [0] * (CARAS * DADOS + 1)
    
    for i in range(1, CARAS + 1):
        dp[i] = 1
        
    for _ in range(DADOS - 1):
        nuevo_dp = [0] * (CARAS * DADOS + 1)
        for suma_actual in range(len(dp)):
            if dp[suma_actual] == 0:
                continue
            for cara in range(1, CARAS + 1):
                nueva_suma = suma_actual + cara
                if nueva_suma <= CARAS * DADOS:
                    nuevo_dp[nueva_suma] += dp[suma_actual]
        dp = nuevo_dp
    
    return {i: dp[i] for i in range(DADOS, CARAS * DADOS + 1) if dp[i] > 0}

frecuencias = calcular_frecuencias()

df = pd.DataFrame({
    'Suma (X)': frecuencias.keys(),
    'Frecuencia': frecuencias.values()
})

df['Probabilidad'] = df['Frecuencia'] / (CARAS**DADOS)
df['Frec. Acumulada'] = df['Frecuencia'].cumsum()
df['Prob. Acumulada'] = df['Probabilidad'].cumsum()

assert sum(frecuencias.values()) == CARAS**DADOS, "Error en el cálculo"
assert df['Suma (X)'].min() == DADOS, "Mínimo incorrecto"
assert df['Suma (X)'].max() == CARAS * DADOS, "Máximo incorrecto"

plt.figure(figsize=(15, 7))
sns.set_style("whitegrid")
ax = sns.barplot(data=df, x='Suma (X)', y='Frecuencia', color='steelblue')

plt.title(f'Distribución de la Suma de {DADOS} Dados de {CARAS} Caras\n', fontsize=14)
plt.xlabel('\nSuma de los dados', fontsize=12)
plt.ylabel('Frecuencia\n', fontsize=12)
plt.axvline(x=31.5 - 3, color='red', linestyle='--', label='Media (31.5)')  # Ajuste de posición

stats_text = f'''
Media: 31.5
Varianza: 104.25
Rango: 3-60
Total combinaciones: {CARAS**DADOS:,}
'''
plt.text(0.75, 0.95, stats_text, 
         transform=ax.transAxes,
         verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.9))

plt.xticks(ticks=range(0, len(df), 5), 
           labels=df['Suma (X)'][::5],
           rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Mostrar tabla completa
print("\nTabla Completa de Distribución:")
pd.set_option('display.max_rows', None)
print(df)
pd.reset_option('display.max_rows')