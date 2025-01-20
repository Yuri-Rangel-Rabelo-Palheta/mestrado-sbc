def evaluate_model(cbr, test_data):
    """Avalia a acurácia do sistema."""
    correct = 0
    total = len(test_data)
    for _, row in test_data.iterrows():
        new_case = row.to_dict()
        label = new_case.pop('label')
        prediction = cbr.classify(new_case)
        if prediction == label:
            correct += 1
    return correct / total
