def select_insurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
    # Define historical data for each field
    fields_data = {
        'Home quarter': {'drought': 4, 'hail': 1, 'grasshoppers': 1, 'no failure': 14},
        'Breaking': {'drought': 3, 'hail': 3, 'grasshoppers': 3, 'no failure': 11},
        'Lyon quarter': {'drought': 0, 'hail': 4, 'grasshoppers': 0, 'no failure': 16},
        'Down south': {'drought': 1, 'hail': 1, 'grasshoppers': 3, 'no failure': 15},
        'Up north': {'drought': 2, 'hail': 2, 'grasshoppers': 2, 'no failure': 14},
        'The farm': {'drought': 1, 'hail': 1, 'grasshoppers': 1, 'no failure': 17}
    }
    
    # Total number of years of data
    total_years = 20
    
    # Calculate probabilities for each event
    probabilities = {}
    for field, events in fields_data.items():
        probabilities[field] = {event: count / total_years for event, count in events.items()}
    
    # Define potential insurances
    insurances = ['comprehensive', 'hail', 'grasshopper', 'basic']
    
    # Calculate expected loss for each insurance type
    expected_losses = {}
    for insurance in insurances:
        expected_losses[insurance] = 0
        for field, probs in probabilities.items():
            if insurance == 'comprehensive':
                payout = 0.8 * contractPrice
                expected_losses[insurance] += (
                    probs['drought'] * (contractPrice - payout + premiums[insurance]) +
                    probs['hail'] * (contractPrice - payout + premiums[insurance]) +
                    probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
                    probs['no failure'] * premiums[insurance]
                )
            elif insurance == 'hail':
                payout = 0.8 * contractPrice
                expected_losses[insurance] += (
                    probs['drought'] * (contractPrice + premiums[insurance]) +
                    probs['hail'] * (contractPrice - payout + premiums[insurance]) +
                    probs['grasshoppers'] * (contractPrice + premiums[insurance]) +
                    probs['no failure'] * premiums[insurance]
                )
            elif insurance == 'grasshopper':
                payout = 0.8 * contractPrice
                expected_losses[insurance] += (
                    probs['drought'] * (contractPrice + premiums[insurance]) +
                    probs['hail'] * (contractPrice + premiums[insurance]) +
                    probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
                    probs['no failure'] * premiums[insurance]
                )
            elif insurance == 'basic':
                payout = 0.5 * contractPrice
                expected_losses[insurance] += (
                    probs['drought'] * (contractPrice - payout + premiums[insurance]) +
                    probs['hail'] * (contractPrice + premiums[insurance]) +
                    probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
                    probs['no failure'] * premiums[insurance]
                )
    
    # Select the insurance with the lowest expected loss
    optimal_insurance = min(expected_losses, key=expected_losses.get)
    
    # Update state with the last year outcome for future use
    new_state = {'lastYearOutcome': lastYearOutcome, 'selectedInsurance': optimal_insurance}
    
    return optimal_insurance, new_state

