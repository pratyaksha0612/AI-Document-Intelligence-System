def calculate_average_confidence(data):
    """
    Calculate average OCR confidence score
    """

    confidences = []

    for conf in data["conf"]:

        try:
            conf = float(conf)

            if conf > 0:
                confidences.append(conf)

        except:
            pass

    if len(confidences) == 0:
        return 0

    return round(sum(confidences) / len(confidences), 2)