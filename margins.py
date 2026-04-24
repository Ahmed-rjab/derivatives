import pandas as pd



def simulate_margin(prices, initial_margin, maintenance_margin, contract_size, position='long'):

    balance = initial_margin
    records = []
    direction = 1 if position == 'long' else -1

    for i in range(len(prices)):
        if i == 0:
            records.append({
                'Day': i , 'Price':prices[i], 'Balance': balance,'Variation Margin call': 0
            })
        continue

    current_price = prices[i]
    prior_price = prices[i-1]
    price_change = current_price - prior_price
    daily_pnl = price_change * contract_size * direction
    balance += daily_pnl
    variation_margin_call = 0

    if balance < maintenance_margin:
        variation_margin_call = initial_margin - balance 
        balance += variation_margin_call

    records.append({
        'Day':i,
        'Price': current_price,
        'Balance': balance,
        'Variation Margin call': variation_margin_call

    })

    return pd.DataFrame(records)




daily_settlement_prices = [1800, 1795, 1780, 1785, 1760]

df_margin = simulate_margin(
    prices=daily_settlement_prices,
    initial_margin=6000, 
    maintenance_margin=4500, 
    contract_size=100, 
    position='long'
)


print(df_margin)