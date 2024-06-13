#3/9 sometimes 4
# def chooseCropInsurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
#     # Define historical data for each field
#     fields_data = {
#         'Home quarter': {'drought': 4, 'hail': 1, 'grasshoppers': 1, 'no failure': 14},
#         'Breaking': {'drought': 3, 'hail': 3, 'grasshoppers': 3, 'no failure': 11},
#         'Lyon quarter': {'drought': 0, 'hail': 4, 'grasshoppers': 0, 'no failure': 16},
#         'Down south': {'drought': 1, 'hail': 1, 'grasshoppers': 3, 'no failure': 15},
#         'Up north': {'drought': 2, 'hail': 2, 'grasshoppers': 2, 'no failure': 14},
#         'The farm': {'drought': 1, 'hail': 1, 'grasshoppers': 1, 'no failure': 17}
#     }
#     
#     # Total number of years of data
#     total_years = 20
#     
#     # Calculate probabilities for each event, p.probEvent?
#     probabilities = {}
#     for field, events in fields_data.items():
#         probabilities[field] = {event: count / total_years for event, count in events.items()}
#     
#     # Define potential insurances
#     insurances = ['comprehensive', 'hail', 'grasshopper', 'basic']
#     
#     # Calculate expected loss for each insurance type
#     expected_losses = {}
#     for insurance in insurances:
#         expected_losses[insurance] = 0
#         for field, probs in probabilities.items():
#             if insurance == 'comprehensive':
#                 payout = 0.8 * contractPrice
#                 expected_losses[insurance] += (
#                     probs['drought'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['hail'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['no failure'] * premiums[insurance]
#                 )
#             elif insurance == 'hail':
#                 payout = 0.8 * contractPrice
#                 expected_losses[insurance] += (
#                     probs['drought'] * (contractPrice + premiums[insurance]) +
#                     probs['hail'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['grasshoppers'] * (contractPrice + premiums[insurance]) +
#                     probs['no failure'] * premiums[insurance]
#                 )
#             elif insurance == 'grasshopper':
#                 payout = 0.8 * contractPrice
#                 expected_losses[insurance] += (
#                     probs['drought'] * (contractPrice + premiums[insurance]) +
#                     probs['hail'] * (contractPrice + premiums[insurance]) +
#                     probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['no failure'] * premiums[insurance]
#                 )
#             elif insurance == 'basic':
#                 payout = 0.5 * contractPrice
#                 expected_losses[insurance] += (
#                     probs['drought'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['hail'] * (contractPrice + premiums[insurance]) +
#                     probs['grasshoppers'] * (contractPrice - payout + premiums[insurance]) +
#                     probs['no failure'] * premiums[insurance]
#                 )
#     
#     # Select the insurance with the lowest expected loss
#     optimal_insurance = min(expected_losses, key=expected_losses.get)
#     
#     # Update state with the last year outcome for future use
#     new_state = {'lastYearOutcome': lastYearOutcome, 'selectedInsurance': optimal_insurance}
#     
#     return optimal_insurance, new_state

# 0/9 sometimes 1
# def calculate_probabilities(field_data):
#     probabilities = {}
#     for field, outcomes in field_data.items():
#         total = sum(outcomes.values())
#         probabilities[field] = {event: count / total for event, count in outcomes.items()}
#     return probabilities
# 
# def chooseCropInsurance(premiums, input_cost, contract_price, last_year_outcome, state):
#     field_data = {
#         'Home quarter': {'drought': 4, 'hail': 1, 'grasshoppers': 1, 'no failure': 14},
#         'Breaking': {'drought': 3, 'hail': 3, 'grasshoppers': 3, 'no failure': 11},
#         'Lyon quarter': {'drought': 0, 'hail': 4, 'grasshoppers': 0, 'no failure': 16},
#         'Down south': {'drought': 1, 'hail': 1, 'grasshoppers': 3, 'no failure': 15},
#         'Up north': {'drought': 2, 'hail': 2, 'grasshoppers': 2, 'no failure': 14},
#         'The farm': {'drought': 1, 'hail': 1, 'grasshoppers': 1, 'no failure': 17}
#     }
#     
#     # Initialize state if it's the first year
#     if state is None:
#         state = {'field_probabilities': calculate_probabilities(field_data)}
#     
#     # Retrieve the probabilities for each field
#     probabilities = state['field_probabilities']
#     
#     # Initialize expected values for each insurance type
#     ev_comprehensive = 0
#     ev_hail = 0
#     ev_grasshopper = 0
#     ev_basic = 0
#     
#     # Calculate expected values for each field and sum them up
#     for field, probs in probabilities.items():
#         ev_comprehensive += (
#             0.8 * contract_price * (probs['drought'] + probs['hail'] + probs['grasshoppers']) +
#             contract_price * probs['no failure'] - premiums['comprehensive'] - input_cost
#         )
#         ev_hail += (
#             0.8 * contract_price * probs['hail'] +
#             contract_price * (1 - probs['hail']) - premiums['hail'] - input_cost
#         )
#         ev_grasshopper += (
#             0.8 * contract_price * probs['grasshoppers'] +
#             contract_price * (1 - probs['grasshoppers']) - premiums['grasshopper'] - input_cost
#         )
#         ev_basic += (
#             0.5 * contract_price * (probs['drought'] + probs['grasshoppers']) +
#             contract_price * probs['no failure'] +
#             contract_price * probs['hail'] - premiums['basic'] - input_cost
#         )
#     
#     # Choose the insurance with the highest expected value
#     insurance_options = {
#         'comprehensive': ev_comprehensive,
#         'hail': ev_hail,
#         'grasshopper': ev_grasshopper,
#         'basic': ev_basic
#     }
#     best_insurance = max(insurance_options, key=insurance_options.get)
#     
#     return best_insurance, state

#8/9 best one
# Neither include marginal likelihood?
# def chooseCropInsurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
#     import numpy as np
#     
#     if state is None:
#         # Initial probabilities (average over all fields)
#         state = {
#             'drought': 0.2,
#             'hail': 0.15,
#             'grasshoppers': 0.1,
#             'no failure': 0.55,
#             'fields': {
#                 'home': [4, 1, 1, 14],
#                 'breaking': [3, 3, 3, 11],
#                 'lyon': [0, 4, 2, 16],
#                 'down_south': [1, 1, 1, 15],
#                 'up_north': [2, 2, 3, 14],
#                 'the_farm': [1, 3, 1, 17]
#             },
#             'field_probs': {field: 1/6 for field in ['home', 'breaking', 'lyon', 'down_south', 'up_north', 'the_farm']}
#         }
#     else:
#         # Update probabilities based on last year's outcome using Bayesian inference
#         if lastYearOutcome is not None:
#             for field, counts in state['fields'].items():
#                 total = sum(counts)
#                 likelihood = counts[['drought', 'hail', 'grasshoppers', 'no failure'].index(lastYearOutcome)] / total
#                 state['field_probs'][field] *= likelihood
# 
#             total_prob = sum(state['field_probs'].values())
#             for field in state['field_probs']:
#                 state['field_probs'][field] /= total_prob
# 
#             # Update failure probabilities
#             for event in ['drought', 'hail', 'grasshoppers', 'no failure']:
#                 state[event] = sum(state['field_probs'][field] * (state['fields'][field][['drought', 'hail', 'grasshoppers', 'no failure'].index(event)] / 20) for field in state['field_probs'])
#     
#     # Calculate expected profits for each insurance
#     expected_profits = {}
#     for insurance in premiums:
#         if insurance == 'comprehensive':
#             payout = 0.8 * contractPrice
#             expected_profits[insurance] = (contractPrice * state['no failure'] + payout * (1 - state['no failure'])) - inputCost - premiums[insurance]
#         elif insurance == 'hail':
#             payout = 0.8 * contractPrice
#             expected_profits[insurance] = (contractPrice * state['no failure'] + payout * state['hail']) - inputCost - premiums[insurance]
#         elif insurance == 'grasshopper':
#             payout = 0.8 * contractPrice
#             expected_profits[insurance] = (contractPrice * state['no failure'] + payout * state['grasshoppers']) - inputCost - premiums[insurance]
#         elif insurance == 'basic':
#             payout = 0.5 * contractPrice
#             expected_profits[insurance] = (contractPrice * state['no failure'] + payout * (1 - state['hail'] - state['no failure'])) - inputCost - premiums[insurance]
#     
#     # Choose the insurance with the highest expected profit
#     best_insurance = max(expected_profits, key=expected_profits.get)
#     
#     return best_insurance, state
def chooseCropInsurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
    import numpy as np
    
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
            'drought': 0.092, #0.2
            'hail': 0.117, #0.15
            'grasshoppers': 0.092, #0.1
            'no failure': 0.742 #0.55
        }
    else:
        # Update probabilities based on last year's outcome using Bayesian inference
        if lastYearOutcome is not None:
            for field, counts in state['fields'].items():
                total = sum(counts)
                likelihood = counts[['drought', 'hail', 'grasshoppers', 'no failure'].index(lastYearOutcome)] / total
                state['field_probs'][field] *= likelihood

            total_prob = sum(state['field_probs'].values())
            for field in state['field_probs']:
                state['field_probs'][field] /= total_prob

            # Update failure probabilities
            event_probs = {event: 0 for event in ['drought', 'hail', 'grasshoppers', 'no failure']}
            for field, prob in state['field_probs'].items():
                counts = state['fields'][field]
                for i, event in enumerate(['drought', 'hail', 'grasshoppers', 'no failure']):
                    event_probs[event] += (counts[i] / 20) * prob
            
            state['event_probs'] = event_probs
    
    # Calculate expected profits for each insurance
    expected_profits = {}
    for insurance in premiums:
        if insurance == 'comprehensive':
            payout = 0.8 * contractPrice
            expected_profits[insurance] = (contractPrice * state['event_probs']['no failure'] +
                                           payout * (1 - state['event_probs']['no failure'])) - inputCost - premiums[insurance]
        elif insurance == 'hail':
            payout = 0.8 * contractPrice
            expected_profits[insurance] = (contractPrice * state['event_probs']['no failure'] +
                                           payout * state['event_probs']['hail']) - inputCost - premiums[insurance]
        elif insurance == 'grasshopper':
            payout = 0.8 * contractPrice
            expected_profits[insurance] = (contractPrice * state['event_probs']['no failure'] +
                                           payout * state['event_probs']['grasshoppers']) - inputCost - premiums[insurance]
        elif insurance == 'basic':
            payout = 0.5 * contractPrice
            expected_profits[insurance] = (contractPrice * state['event_probs']['no failure'] +
                                           payout * (1 - state['event_probs']['hail'] - state['event_probs']['no failure'])) - inputCost - premiums[insurance]
    
    # Choose the insurance with the highest expected profit
    best_insurance = max(expected_profits, key=expected_profits.get)
    
    return best_insurance, state
