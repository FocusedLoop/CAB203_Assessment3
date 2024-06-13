def chooseCropInsurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
    import probability
    if state is None:
        # Initial probabilities (average over all fields)
        state = {
            'fields': {
                'home': [4, 1, 1, 14],
                'breaking': [3, 3, 3, 11],
                'lyon': [0, 4, 2, 16],
                'down_south': [1, 1, 1, 17],
                'up_north': [2, 2, 3, 14],
                'the_farm': [1, 3, 1, 17]
            },
            'field_probs': {field: 1/6 for field in ['home', 'breaking', 'lyon', 'down_south', 'up_north', 'the_farm']}
        }
        # Initial event probabilities
        state['event_probs'] = {
            'drought': 0.092, 
            'hail': 0.117, 
            'grasshoppers': 0.092, 
            'no failure': 0.742 
        }
    else:
        # Update probabilities based on last year's outcome using Bayesian inference
        if lastYearOutcome is not None:
            # Update the field probabilities
            event_indices = ['drought', 'hail', 'grasshoppers', 'no failure']
            for field, counts in state['fields'].items():
                total = sum(counts)
                likelihood = counts[event_indices.index(lastYearOutcome)] / total
                state['field_probs'][field] *= likelihood

            # Normalize to get posterior probabilities
            total_prob = sum(state['field_probs'].values())
            state['field_probs'] = {field: prob / total_prob for field, prob in state['field_probs'].items()}

            # Update failure probabilities based on posterior field probabilities
            event_probs = {event: 0 for event in event_indices}
            for field, prob in state['field_probs'].items():
                counts = state['fields'][field]
                for i, event in enumerate(event_indices):
                    event_probs[event] += (counts[i] / sum(counts)) * prob

            state['event_probs'] = event_probs

    # Define the utility functions for each insurance
    utility_functions = {}
    for insurance in premiums:
        if insurance == 'comprehensive':
            utility_functions[insurance] = {
                'drought': 0.8 * contractPrice - inputCost - premiums[insurance],
                'hail': 0.8 * contractPrice - inputCost - premiums[insurance],
                'grasshoppers': 0.8 * contractPrice - inputCost - premiums[insurance],
                'no failure': contractPrice - inputCost - premiums[insurance]
            }
        elif insurance == 'hail':
            utility_functions[insurance] = {
                'drought': -inputCost - premiums[insurance],
                'hail': 0.8 * contractPrice - inputCost - premiums[insurance],
                'grasshoppers': -inputCost - premiums[insurance],
                'no failure': contractPrice - inputCost - premiums[insurance]
            }
        elif insurance == 'grasshopper':
            utility_functions[insurance] = {
                'drought': -inputCost - premiums[insurance],
                'hail': -inputCost - premiums[insurance],
                'grasshoppers': 0.8 * contractPrice - inputCost - premiums[insurance],
                'no failure': contractPrice - inputCost - premiums[insurance]
            }
        elif insurance == 'basic':
            utility_functions[insurance] = {
                'drought': 0.5 * contractPrice - inputCost - premiums[insurance],
                'hail': 0.5 * contractPrice - inputCost - premiums[insurance],
                'grasshoppers': 0.5 * contractPrice - inputCost - premiums[insurance],
                'no failure': contractPrice - inputCost - premiums[insurance]
            }

    # Use the decide function to find the best insurance option
    P = state['event_probs']
    print(probability.decide(P, utility_functions))
    best_insurance, _ = probability.decide(P, utility_functions)
    
    return best_insurance, state
