import os
from nlp_case.server.app.models.parsers.tokenParser import *
from nlp_case.server.app.models.NER_Disease_net import SentenceDiseaseRecognizer
import torch
from torch.utils.data import TensorDataset
import numpy as np
from torch.utils.data import DataLoader
import json

MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../data/sentence_level_em_pos.model"
MODEL_DESCRIPTON_PATH =  os.path.dirname(os.path.abspath(__file__)) + "/../../../data/model_data.json"

def copy_data_to_device(data, device):
    if torch.is_tensor(data):
        return data.to(device)
    elif isinstance(data, (list, tuple)):
        return [copy_data_to_device(elem, device) for elem in data]
    raise ValueError('Недопустимый тип данных {}'.format(type(data)))

def predict_with_model(model, dataset, device=None, batch_size=32, num_workers=0, return_labels=False):
    """
    :param model: torch.nn.Module - обученная модель
    :param dataset: torch.utils.data.Dataset - данные для применения модели
    :param device: cuda/cpu - устройство, на котором выполнять вычисления
    :param batch_size: количество примеров, обрабатываемых моделью за одну итерацию
    :return: numpy.array размерности len(dataset) x *
    """
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    results_by_batch = []

    device = torch.device(device)
    model.to(device)
    model.eval()

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    labels = []
    with torch.no_grad():
        import tqdm
        for batch_x, batch_y in tqdm.tqdm(dataloader, total=len(dataset)/batch_size):
            batch_x = copy_data_to_device(batch_x, device)

            if return_labels:
                labels.append(batch_y.numpy())

            batch_pred = model(batch_x)
            results_by_batch.append(batch_pred.detach().cpu().numpy())

    if return_labels:
        return np.concatenate(results_by_batch, 0), np.concatenate(labels, 0)
    else:
        return np.concatenate(results_by_batch, 0)

class NERDiseaseRecognizer:
    def __init__(self):
        with open(MODEL_DESCRIPTON_PATH) as json_file:
            data = json.load(json_file)
        self.char2id = data['char_vocab']
        self.id2label = data['unique_tags']
        self.max_sent_len = data['max_sent_length']
        self.max_token_len = data['max_token_length']
        model = torch.load(MODEL_PATH)
        self.model = model
        

    def __call__(self, sentences):
        tokenized_corpus = tokenize_corpus(sentences, min_token_size=1)

        inputs = torch.zeros((len(sentences), self.max_sent_len, self.max_token_len + 2), dtype=torch.long)

        for sent_i, sentence in enumerate(tokenized_corpus):
            for token_i, token in enumerate(sentence):
                for char_i, char in enumerate(token):
                    inputs[sent_i, token_i, char_i + 1] = self.char2id.get(char, 0)

        dataset = TensorDataset(inputs, torch.zeros(len(sentences)))
        predicted_probs = predict_with_model(self.model, dataset)  # SentenceN x TagsN x MaxSentLen
        predicted_classes = predicted_probs.argmax(1)

        result = []
        for sent_i, sent in enumerate(tokenized_corpus):
            result.append([self.id2label[cls] for cls in predicted_classes[sent_i, :len(sent)]])
        return result

    def find_all_Disease_entities(self, sentences):
        tokenized_corpus = tokenize_corpus(sentences, min_token_size=1)
        inputs = torch.zeros((len(sentences), self.max_sent_len, self.max_token_len + 2), dtype=torch.long)

        for sent_i, sentence in enumerate(tokenized_corpus):
            for token_i, token in enumerate(sentence):
                for char_i, char in enumerate(token):
                    inputs[sent_i, token_i, char_i + 1] = self.char2id.get(char, 0)
        
        dataset = TensorDataset(inputs, torch.zeros(len(sentences)))
        predicted_probs = predict_with_model(self.model, dataset)
        predicted_classes = predicted_probs.argmax(1)

        result = []
        tags = []
        for sent_i, sent in enumerate(tokenized_corpus): 
            tags.append([self.id2label[cls] for cls in predicted_classes[sent_i, :len(sent)]])
        
        i = 0
        for sent_tokens, sent_tags in zip(tokenized_corpus, tags):
            for tok, tag in zip(sent_tokens, sent_tags):
                if (tag == '<NE>'):
                    result.append((tok, i))
                if (tag == '<PNE>'): 
                    if len(result) > 0 and result[-1][1] == i - 1:
                        result[-1] = (result[-1][0] +' '+ tok, i)
                    else:
                        result.append((tok,i))
                i +=1
        return list(map(lambda e: e[0], result))



