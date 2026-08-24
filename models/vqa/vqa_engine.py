"""
SatQuery AI — VQA Engine

Vision-Language Model for Visual Question Answering using BLIP.
Conforms to the BaseAnalyzer interface.
"""

import time
import logging
from typing import Any
from PIL import Image

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import EvidenceItem

logger = logging.getLogger(__name__)

# Lazy loaded globals
_processor = None
_model = None

def _load_model():
    global _processor, _model
    if _model is None:
        logger.info("Loading BLIP VQA Model (this may take a moment)...")
        from transformers import BlipProcessor, BlipForQuestionAnswering
        # Using the base model which is smaller and runs okay on CPU
        model_id = "Salesforce/blip-vqa-base"
        _processor = BlipProcessor.from_pretrained(model_id)
        _model = BlipForQuestionAnswering.from_pretrained(model_id)
        logger.info("BLIP VQA Model loaded.")

class VQAEngine(BaseAnalyzer):
    """
    BLIP-based VQA Engine.
    """

    @property
    def name(self) -> str:
        return "Visual Question Answering"

    @property
    def module_id(self) -> str:
        return "models.vqa.vqa_engine"

    async def analyze(self, **kwargs) -> Any:
        image_path = kwargs.get("image_path")
        question = kwargs.get("question", "What is in this image?")

        if not image_path:
            return self.make_skipped("No image provided for VQA.")

        try:
            # Ensure model is loaded (blocks async thread slightly, but ok for this demo)
            _load_model()
            
            raw_image = Image.open(image_path).convert('RGB')
            
            t0 = time.time()
            inputs = _processor(raw_image, question, return_tensors="pt")
            out = _model.generate(**inputs)
            answer = _processor.decode(out[0], skip_special_tokens=True)
            inference_time = round((time.time() - t0) * 1000, 1)
            
            # Formulate the response
            # BLIP sometimes gives very short answers (e.g. "yes", "no", "water"). 
            # We'll consider it a supporting verdict if it provides an answer.
            verdict = "supporting" if answer else "neutral"

            evidence = [
                EvidenceItem(
                    source=self.module_id,
                    verdict=verdict,
                    detail=f"VQA Model answered: '{answer}' in {inference_time}ms.",
                    data={"question": question, "answer": answer}
                )
            ]

            return self.make_success(
                task=self.name,
                result={"answer": answer, "question": question},
                confidence=0.8,
                evidence=evidence,
                metadata={"inference_time_ms": inference_time}
            )

        except Exception as e:
            logger.error(f"VQA Inference failed: {e}")
            return self.make_skipped(f"VQA Inference failed: {str(e)}")
