import ccxt
import pandas as pd

# Configuration
SYMBOL = 'BTC/USDT'  # Symbole de trading
TIMEFRAME = '1h'  # Intervalle de temps (par exemple : '1h', '15m')
SHORT_WINDOW = 7  # Moyenne mobile courte
LONG_WINDOW = 25  # Moyenne mobile longue
EXCEL_FILE = 'trading_signals_values.xlsx'  # Nom du fichier Excel

# Initialisation de l'exchange
exchange = ccxt.binance()

def fetch_data(symbol, timeframe, limit=50):
    """Récupère les données de marché."""
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open','close','high', 'low', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_signals(data):
    """Ajoute les signaux de trading aux données."""
    data['short_ma'] = data['close'].rolling(window=SHORT_WINDOW).mean()
    data['long_ma'] = data['close'].rolling(window=LONG_WINDOW).mean()
    data['signal'] = 0
    data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1  # Acheter
    data.loc[data['short_ma'] <= data['long_ma'], 'signal'] = -1  # Vendre
    data['action'] = data['signal'].diff().apply(lambda x: 'Buy' if x == 2 else 'Sell' if x == -2 else None)
    return data

def save_to_excel(data, file_name):
    """Sauvegarde les données dans un fichier Excel."""
    #actions = data[data['action'].notnull()][['timestamp', 'close', 'action']]
    actions= data
    actions.to_excel(file_name, index=False, engine='openpyxl')
    print(f"Signaux enregistrés dans {file_name}.")

def main():
    """Programme principal."""
    try:
        # Récupérer les données
        data = fetch_data(SYMBOL, TIMEFRAME)
        print(data.head())
        # Calculer les signaux
        #data = calculate_signals(data)

        # Sauvegarder les signaux dans un fichier Excel
        save_to_excel(data, EXCEL_FILE)

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()