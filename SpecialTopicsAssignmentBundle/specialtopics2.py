import numpy as np
import csv

def blendWheat(filename):
    # Read the CSV file
    bins = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bins.append({
                'weight': float(row['Weight']),
                'protein': float(row['Protein']),
                'moisture': float(row['Moisture'])
            })
    
    # Extract data from bins
    weights = np.array([bin['weight'] for bin in bins])
    proteins = np.array([bin['protein'] for bin in bins])
    moistures = np.array([bin['moisture'] for bin in bins])
    
    # Initialize blend
    blend_weights = np.zeros(len(bins))
    
    # Helper function to calculate weighted average
    def weighted_average(weights, values):
        return np.sum(weights * values) / np.sum(weights)
    
    # Iterate to adjust blend weights
    total_weight = 0
    step_size = 0.01
    max_iterations = 10000  # Safety limit for the number of iterations
    
    for _ in range(max_iterations):
        # Calculate current protein and moisture percentages
        if total_weight > 0:
            current_protein = weighted_average(blend_weights, proteins)
            current_moisture = weighted_average(blend_weights, moistures)
        else:
            current_protein = 0
            current_moisture = 0
        
        # Check if the blend meets the requirements
        if total_weight > 0 and current_protein >= 14 and current_moisture <= 12.5:
            break
        
        # Find the bin that contributes the best improvement towards meeting constraints
        best_bin = -1
        best_value = float('-inf')
        
        for i in range(len(bins)):
            if blend_weights[i] + step_size <= weights[i]:
                new_blend_weights = blend_weights.copy()
                new_blend_weights[i] += step_size
                new_total_weight = total_weight + step_size
                new_protein = weighted_average(new_blend_weights, proteins)
                new_moisture = weighted_average(new_blend_weights, moistures)
                
                if new_protein >= 14 and new_moisture <= 12.5:
                    blend_weights = new_blend_weights
                    total_weight = new_total_weight
                    break
                
                # Evaluate this bin based on the improvements it provides
                value = (new_protein - current_protein) / (new_moisture - current_moisture + 0.01)
                if value > best_value:
                    best_value = value
                    best_bin = i
        
        # If no bin provided an improvement, stop
        if best_bin == -1:
            break
        
        # Update the blend with the best bin found
        blend_weights[best_bin] += step_size
        total_weight += step_size
    
    # Round the results to 2 decimal places
    blend_weights = np.round(blend_weights, 2)
    total_weight = np.round(total_weight, 2)
    
    # Create the result dictionary
    blend_dict = {f'Bin_{i+1}': blend_weights[i] for i in range(len(bins))}
    
    return blend_dict, total_weight

# Example usage:
# blend, total_weight = blendWheat('bins1.csv')
# print(blend, total_weight)
