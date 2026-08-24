"""
SatQuery AI — Captioning Engine

Image Captioning Model using BLIP.
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
        logger.info("Loading BLIP Captioning Model (this may take a moment)...")
        from transformers import BlipProcessor, BlipForConditionalGeneration
        # Base model for captioning
        model_id = "Salesforce/blip-image-captioning-base"
        _processor = BlipProcessor.from_pretrained(model_id)
        _model = BlipForConditionalGeneration.from_pretrained(model_id)
        logger.info("BLIP Captioning Model loaded.")

class CaptionEngine(BaseAnalyzer):
    """
    BLIP-based Caption Engine.
    """

    @property
    def name(self) -> str:
        return "Image Captioning"

    @property
    def module_id(self) -> str:
        return "models.captioning.caption_engine"

    async def analyze(self, **kwargs) -> Any:
        image_path = kwargs.get("image_path")

        if not image_path:
            return self.make_skipped("No image provided for captioning.")

        try:
            _load_model()
            
            raw_image = Image.open(image_path).convert('RGB')
            
            # The prompt can be unconditional or conditional. We'll do unconditional captioning.
            text = "a satellite image of"
            
            t0 = time.time()
            inputs = _processor(raw_image, text, return_tensors="pt")
            out = _model.generate(**inputs, max_new_tokens=50)
            caption = _processor.decode(out[0], skip_special_tokens=True)
            inference_time = round((time.time() - t0) * 1000, 1)

            evidence = [
                EvidenceItem(
                    source=self.module_id,
                    verdict="supporting",
                    detail=f"Caption: '{caption}'",
                    data={"caption": caption}
                )
            ]

            return self.make_success(
                task=self.name,
                result={"caption": caption},
                confidence=0.8,
                evidence=evidence,
                metadata={"inference_time_ms": inference_time}
            )

        except Exception as e:
            logger.error(f"Caption Inference failed: {e}")
            return self.make_skipped(f"Caption Inference failed: {str(e)}")
