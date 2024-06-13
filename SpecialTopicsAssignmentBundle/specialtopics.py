import probability
def chooseCropInsurance(premiums, inputCost, contractPrice, lastYearOutcome, state):
    # Check if this is the first interation of the state (is this the first year?)
    # State stores all probability data
    if state is None:
        # Set the number of failure types for each field
        state = {
            'fields': {
                'home': [4, 1, 1, 14],
                'breaking': [3, 3, 3, 11],
                'lyon': [0, 4, 2, 16],
                'down_south': [1, 1, 1, 17],
                'up_north': [2, 2, 3, 14],
                'the_farm': [1, 3, 1, 17]
            },
            # For the field that is charlies set all fields to equal probabilities as its unknown
            'field_probs': {field: 1/6 for field in ['home', 'breaking', 'lyon', 'down_south', 'up_north', 'the_farm']}
        }
        # Set the event probabilities for each failure type, creates a new key
        # This is calculated by number of failure event divide by the number of fields times the number of years
        total_years = 20
        number_fields = len(state['fields'])
        state['event_probs'] = {
            'drought': (sum(field[0] for field in state['fields'].values())) / (number_fields*total_years), 
            'hail': (sum(field[1] for field in state['fields'].values())) / (number_fields*total_years),
            'grasshoppers': (sum(field[2] for field in state['fields'].values())) / (number_fields*total_years),
            'no failure': (sum(field[3] for field in state['fields'].values())) / (number_fields*total_years)
        }
    else:
        # Updatating failure type probability based on field belief with Bayesian inference
        if lastYearOutcome is not None:
            # Set the prior from the belief of which field is charlie's from the previous year
            fields_prior = state['field_probs']
            # Set the likelihood from the failure probabilities of the previous year
            # Create a dictionary of all the failure types probabilities for each field
            likelihoods = {
                field: {event: counts[event_index] / sum(counts) for event_index, event in enumerate(['drought', 'hail', 'grasshoppers', 'no failure'])}
                for field, counts in state['fields'].items()
            }
            # Update field probabilities using posterior
            # In probability.posterior calculate the marginal likelihood using the prior, likelihood and the previous years probabilities
            updated_field_probabilities = probability.posterior(fields_prior, likelihoods, {lastYearOutcome})
            state['field_probs'] = updated_field_probabilities
            # Update failure probabilities for each failure type likelihood
            total_probabilities = {event: 0 for event in ['drought', 'hail', 'grasshoppers', 'no failure']}
            for field, probabiltiy in updated_field_probabilities.items():
                for event in total_probabilities.keys():
                    total_probabilities[event] += probabiltiy * likelihoods[field][event]
            state['event_probs'] = total_probabilities
    
    # Insurance calculation
    # For each insurance type calculate the potential profits
    insurance_utility = {}
    for insurance in premiums:
        insurance_utility[insurance] = {}
        for event, prob in state['event_probs'].items():
            # Comprehensive profit calculation
            if insurance == 'comprehensive':
                # Payout calculation
                payout = 0.8 * contractPrice
                insurance_utility[insurance][event] = (contractPrice * state['event_probs']['no failure'] + payout * (1 - state['event_probs']['no failure'])) - inputCost - premiums[insurance]
            # Hail profit calculation
            elif insurance == 'hail':
                payout = 0.8 * contractPrice
                insurance_utility[insurance][event] = (contractPrice * state['event_probs']['no failure'] + payout * state['event_probs']['hail']) - inputCost - premiums[insurance]
            # Grasshopper profit calculation
            elif insurance == 'grasshopper':
                payout = 0.8 * contractPrice
                insurance_utility[insurance][event] = (contractPrice * state['event_probs']['no failure'] + payout * state['event_probs']['grasshoppers']) - inputCost - premiums[insurance]
            # Basic profit calculation
            elif insurance == 'basic':
                payout = 0.5 * contractPrice
                insurance_utility[insurance][event] = (contractPrice * state['event_probs']['no failure'] + payout * (1 - state['event_probs']['hail'] - state['event_probs']['no failure'])) - inputCost - premiums[insurance]
    
    # Decide which insurance provides the most profit for that year
    event_probabilities = state['event_probs']
    best_insurance, best_insurance_profit = probability.decide(event_probabilities, insurance_utility)
    
    # Return the best insurance with the current probability data
    return best_insurance, state