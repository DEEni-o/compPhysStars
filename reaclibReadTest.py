import numpy as np


def parse_reaclib1_file(filename):
    """
    Parses a Reaclib1 file and extracts the reaction details and coefficients.
    """
    reactions = []
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Skip the header (chapter number)
        i = 1  # Start reading from the second line

        while i < len(lines):
            # First line of the set entry
            line1 = lines[i].strip()
            if not line1:  # Skip empty lines
                i += 1
                continue

            # Extract reactants and products
            reactants = [line1[5:10].strip(), line1[10:15].strip(), line1[15:20].strip()]
            products = [line1[20:25].strip(), line1[25:30].strip(), line1[30:35].strip()]

            # Extract set label, rate type, reverse flag, and Q value
            set_label = line1[43:47].strip() if len(line1) >= 47 else ''
            rate_type = line1[47] if len(line1) >= 48 else ''
            reverse_flag = line1[48] if len(line1) >= 49 else ''
            q_value = float(line1[52:64]) if len(line1) >= 64 else 0.0

            # Second line of the set entry (first four coefficients)
            line2 = lines[i + 1].strip() if i + 1 < len(lines) else ''
            # Split line2 into coefficients using 'e+' or 'e-' as delimiters
            coeffs_line2 = []
            if line2:
                # Use a regular expression to split the line into valid scientific notation strings
                import re
                parts = re.findall(r'[-+]?\d*\.\d+[eE][-+]?\d+', line2)
                coeffs_line2 = [float(part) for part in parts]

            # Third line of the set entry (last three coefficients)
            line3 = lines[i + 2].strip() if i + 2 < len(lines) else ''
            # Split line3 into coefficients using 'e+' or 'e-' as delimiters
            coeffs_line3 = []
            if line3:
                # Use a regular expression to split the line into valid scientific notation strings
                import re
                parts = re.findall(r'[-+]?\d*\.\d+[eE][-+]?\d+', line3)
                coeffs_line3 = [float(part) for part in parts]

            # Combine all coefficients
            coefficients = coeffs_line2 + coeffs_line3
            if len(coefficients) < 7:
                coefficients.extend([0.0] * (7 - len(coefficients)))  # Pad with zeros if necessary

            # Store the reaction details and coefficients
            reaction = {
                'reactants': reactants,
                'products': products,
                'set_label': set_label,
                'rate_type': rate_type,
                'reverse_flag': reverse_flag,
                'q_value': q_value,
                'coefficients': coefficients
            }
            reactions.append(reaction)

            # Move to the next set entry
            i += 3

    return reactions


def calculate_reaction_rate(T9, coefficients):
    """
    Calculates the reaction rate at a given temperature T9 (in 10^9 K).
    """
    a0, a1, a2, a3, a4, a5, a6 = coefficients
    log_rate = a0 + a1 / T9 + a2 / T9 ** (1 / 3) + a3 * T9 ** (1 / 3) + a4 * T9 + a5 * T9 ** (5 / 3) + a6 * np.log(T9)
    return np.exp(log_rate)


def main():
    # Example usage
    filename = 'models/rates/he3-p-he4-bet'  # Replace with your Reaclib1 file path
    T9 = 5  # Temperature in 10^9 K

    reactions = parse_reaclib1_file(filename)

    for reaction in reactions:
        reactants = reaction['reactants']
        products = reaction['products']
        coefficients = reaction['coefficients']

        # Calculate the reaction rate
        rate = calculate_reaction_rate(T9, coefficients)

        # Print the reaction details and rate
        print(f"Reaction: {' + '.join(reactants)} -> {' + '.join(products)}")
        print(f"Set Label: {reaction['set_label']}")
        print(f"Rate Type: {reaction['rate_type']}")
        print(f"Reverse Flag: {reaction['reverse_flag']}")
        print(f"Q Value: {reaction['q_value']}")
        print(f"Reaction Rate at T9 = {T9}: {rate}")
        print()


if __name__ == "__main__":
    main()