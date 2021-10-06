
def compare_models(models, data, keywords):
    for model in models:
        model_pred = []
        for text in data:
            tags = model.predict_tags(text)
            model_pred.append(tags)
        get_model_report(keywords, model_pred, model.name)

def get_model_report(true_y, pred_y, model_name=""):
    """
    Печатает оценку качества модели по поиску ключевых слов

    Входные параметры
    - true_y: список списков тэгов к текстам 
    - pred_y: список списков тэгов сгенерированных к текстам

    подсчитывает:
    полноту(recall) (доля правильно предсазанных тэгов)
    точность(precision) (доля правильно предсказанных тэгов от общего количества предсказанных тэгов)

    """
    trueKW_count = 0
    predictedKW_count = 0
    tp = 0
    for true_tags, pred_tags in zip(true_y, pred_y):
        tkw, pkw, correct_keywords_count = count_correct_keywords(true_tags, pred_tags)
        trueKW_count += tkw
        predictedKW_count += pkw
        tp += correct_keywords_count
    recall = tp / trueKW_count
    precision = tp / predictedKW_count
    print("-"*10)
    print(model_name + " Report")
    print("True keywords: Total %d Mean %f"%(trueKW_count, trueKW_count / len(true_y)))
    print("Extracted keywords: Total %d Mean %f"%(predictedKW_count, predictedKW_count / len(pred_y)))
    print("Correct keywords: Total %d Mean %f"%(tp, tp / len(pred_y)))
    print("Recall: %f Precision: %f"%(recall,precision))
    f1 = (recall * precision) / (recall + precision)
    print("F1: %f"%f1)
    print("-"*10)


def count_correct_keywords(true_tags, pred_tags):
    correct_keywords_count = 0
    for tag in pred_tags:
        if tag in true_tags:
            correct_keywords_count+=1
    return len(true_tags), len(pred_tags), correct_keywords_count