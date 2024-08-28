from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.constants import INTENT
from rasa.nlu.classifiers.classifier import IntentClassifier
from transformers import AlbertTokenizer, AlbertForSequenceClassification
import torch

@DefaultV1Recipe.register([GraphComponent], is_trainable=True)
class AlbertIntentClassifier(IntentClassifier, GraphComponent):
    def __init__(self, model_name: str, model_storage: ModelStorage, resource: Resource):
        self.model_name = model_name
        self.model_storage = model_storage
        self.resource = resource
        self.tokenizer = AlbertTokenizer.from_pretrained(self.model_name)
        self.model = AlbertForSequenceClassification.from_pretrained(self.model_name)

    @classmethod
    def required_components(cls):
        return []

    def train(self, training_data: TrainingData):
        # Train ALBERT on the intent data
        # This is simplified; typically you'd need to fine-tune ALBERT on your specific dataset
        pass

    def process(self, messages: [Message]):
        for message in messages:
            inputs = self.tokenizer(message.get("text"), return_tensors="pt", truncation=True, padding=True)
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_intent = torch.argmax(logits, dim=1).item()
            message.set(INTENT, {"name": str(predicted_intent), "confidence": torch.max(logits).item()})

    def persist(self, model_dir: str):
        self.tokenizer.save_pretrained(model_dir)
        self.model.save_pretrained(model_dir)

    @classmethod
    def load(cls, model_dir: str):
        tokenizer = AlbertTokenizer.from_pretrained(model_dir)
        model = AlbertForSequenceClassification.from_pretrained(model_dir)
        return cls(tokenizer, model)
