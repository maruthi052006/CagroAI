import os
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class LocalIntentClassifier:
    """
    100% Offline, Zero External LLM Intent Classifier.
    Combines rule-based keyword/regex heuristics with a local scikit-learn
    TF-IDF + Logistic Regression model trained exclusively on project-internal data.
    """

    KEYWORD_RULES = {
        "CROP": [
            (r"\b(stage|growth|grow|vegetative|flowering|maturity|progress|cycle)\b", "GROWTH_STATUS"),
            (r"\b(biomass|weight|matter|canopy|vegetation volume)\b", "BIOMASS_INFO"),
            (r"\b(confidence|accuracy|sure|reliable|calibration)\b", "CONFIDENCE_QUERY"),
        ],
        "WEATHER": [
            (r"\b(flood|waterlog|excess rain|heavy rain|rain risk)\b", "RAIN_RISK"),
            (r"\b(forecast|precipitation|7-day|outlook|rain.*week|weekly rain)\b", "FORECAST_QUERY"),
            (r"\b(temperature|thermal|heat|hot|cold|frost|degree|celsius)\b", "TEMPERATURE_QUERY"),
        ],
        "PEST": [
            (r"\b(why.*risk|reason|cause|humidity trigger|explain pest)\b", "PEST_RISK_REASON"),
            (r"\b(history|past|outbreak|attack|previous|historical)\b", "PEST_RISK_HISTORY"),
            (r"\b(level|score|threat|danger|pathogen|fungus|disease risk)\b", "PEST_RISK_LEVEL"),
        ],
        "YIELD": [
            (r"\b(uncertainty|range|p10|p90|bounds|worst case|best case|monte carlo)\b", "UNCERTAINTY_RANGE"),
            (r"\b(compare|comparison|benchmark|district|average|norm)\b", "COMPARISON_QUERY"),
            (r"\b(estimate|expected|produce|harvest|yield|production|kg/ha)\b", "YIELD_ESTIMATE"),
        ],
        "EXAI": [
            (r"\b(why|reason|reasoning|explain decision|trace|step by step|how did you)\b", "WHY_QUESTION"),
            (r"\b(trust|reliable|certainty|score breakdown)\b", "TRUST_QUESTION"),
            (r"\b(conflict|disagree|dispute|contradict|opposing)\b", "CONFLICT_QUESTION"),
            (r"\b(recommend|recommendation|advice|advise|action|what should i do)\b", "RECOMMENDATION_QUESTION"),
            (r"\b(health|gauge|index|farm health|vitality|status)\b", "FARM_HEALTH_QUESTION"),
            (r"\b(help|capabilities|what can you|who are you|hello|hi)\b", "GENERAL_HELP"),
        ]
    }

    def __init__(self):
        self.models = {}
        self.vocabularies = {}
        self._train_local_models()

    def _train_local_models(self):
        data_path = os.path.join(os.path.dirname(__file__), "training_data", "intents.json")
        if not os.path.exists(data_path):
            return

        with open(data_path, "r", encoding="utf-8") as f:
            intents_data = json.load(f)

        for persona, examples in intents_data.items():
            texts = [ex["text"] for ex in examples]
            labels = [ex["intent"] for ex in examples]

            # Build domain vocabulary for persona
            tokens = set()
            for t in texts:
                for word in re.findall(r"\w+", t.lower()):
                    if len(word) > 2:
                        tokens.add(word)
            self.vocabularies[persona] = tokens

            if len(set(labels)) > 1:
                clf = Pipeline([
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                    ("clf", LogisticRegression(C=1.0, max_iter=200))
                ])
                clf.fit(texts, labels)
                self.models[persona] = clf

    def classify(self, persona: str, text: str) -> tuple[str, float]:
        """
        Classifies user query within the context of the active persona.
        Returns: (intent_name, confidence)
        """
        persona = persona.upper()
        clean_text = text.lower().strip()

        # 1. Check direct deterministic rules
        rules = self.KEYWORD_RULES.get(persona, [])
        for pattern, intent in rules:
            if re.search(pattern, clean_text):
                return intent, 0.95

        # 2. Check domain relevance: if query contains zero words in persona vocabulary, reject as CLARIFICATION
        persona_vocab = self.vocabularies.get(persona, set())
        query_words = set(re.findall(r"\w+", clean_text))
        if not (query_words & persona_vocab):
            return "CLARIFICATION", 0.05

        # 3. Check local ML model
        if persona in self.models:
            clf = self.models[persona]
            probas = clf.predict_proba([clean_text])[0]
            classes = clf.classes_
            max_idx = probas.argmax()
            confidence = float(probas[max_idx])
            best_intent = str(classes[max_idx])

            if confidence >= 0.40:
                return best_intent, round(confidence, 2)

        # 4. Fallback to CLARIFICATION if below threshold
        return "CLARIFICATION", 0.10

classifier = LocalIntentClassifier()
