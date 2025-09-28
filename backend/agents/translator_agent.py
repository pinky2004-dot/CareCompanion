"""
Translator Agent - Explains medical terms using AI language models.
"""
import asyncio
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class TranslatorAgent(BaseAgent):
    """Agent responsible for translating medical jargon into plain language."""
    
    def __init__(self):
        super().__init__("Translator")
        self.medical_terms_db = self._initialize_medical_terms()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate medical terms into plain language.
        
        Args:
            input_data: Dictionary containing 'raw_text' and 'document_type'
            
        Returns:
            Dictionary containing simplified terms and explanations
        """
        raw_text = input_data.get('raw_text', '')
        document_type = input_data.get('document_type', 'unknown')
        
        if not raw_text:
            raise ValueError("No text provided for translation")
        
        logger.info(f"Translating medical terms for {document_type} document")
        
        # Extract medical terms from the text
        medical_terms = self._extract_medical_terms(raw_text)
        
        # Generate simplified explanations
        simplified_terms = await self._generate_explanations(medical_terms, document_type)
        
        # Generate overall document summary
        document_summary = await self._generate_document_summary(raw_text, document_type)
        
        return {
            "simplified_terms": simplified_terms,
            "document_summary": document_summary,
            "medical_terms_found": len(medical_terms),
            "translation_confidence": 0.92  # Mock confidence score
        }
    
    def _initialize_medical_terms(self) -> Dict[str, Dict[str, str]]:
        """Initialize database of medical terms and their explanations."""
        return {
            'lisinopril': {
                'explanation': 'A common and safe medication used to treat high blood pressure (hypertension). It works by relaxing your blood vessels, making it easier for your heart to pump blood around your body.',
                'importance': 'Essential for controlling blood pressure and preventing heart problems like heart attacks and strokes.',
                'category': 'medication'
            },
            'hypertension': {
                'explanation': 'High blood pressure - a condition where the force of blood against your artery walls is consistently too high.',
                'importance': 'Can lead to serious health problems if not controlled, including heart disease, stroke, and kidney problems.',
                'category': 'condition'
            },
            'diabetes': {
                'explanation': 'A condition where your body has trouble controlling blood sugar levels. There are two main types: Type 1 and Type 2.',
                'importance': 'Requires careful management to prevent complications like heart disease, kidney problems, and nerve damage.',
                'category': 'condition'
            },
            'metformin': {
                'explanation': 'A medication commonly used to treat Type 2 diabetes. It helps your body use insulin more effectively and reduces sugar production in the liver.',
                'importance': 'Helps control blood sugar levels and can reduce the risk of diabetes complications.',
                'category': 'medication'
            },
            'atorvastatin': {
                'explanation': 'A medication that helps lower cholesterol levels in your blood. It belongs to a group of drugs called statins.',
                'importance': 'Reduces the risk of heart disease and stroke by lowering "bad" cholesterol and increasing "good" cholesterol.',
                'category': 'medication'
            },
            'glucose': {
                'explanation': 'A type of sugar that your body uses for energy. It comes from the food you eat and is carried through your bloodstream.',
                'importance': 'Your body needs glucose for energy, but too much can cause health problems, especially for people with diabetes.',
                'category': 'lab_value'
            },
            'cholesterol': {
                'explanation': 'A waxy substance found in your blood. Your body needs some cholesterol, but too much can clog your arteries.',
                'importance': 'High cholesterol can lead to heart disease and stroke, so it\'s important to keep it at healthy levels.',
                'category': 'lab_value'
            },
            'hdl': {
                'explanation': 'High-Density Lipoprotein - often called "good" cholesterol. It helps remove other forms of cholesterol from your bloodstream.',
                'importance': 'Higher HDL levels are better and can help protect against heart disease.',
                'category': 'lab_value'
            },
            'ldl': {
                'explanation': 'Low-Density Lipoprotein - often called "bad" cholesterol. It can build up in your arteries and cause blockages.',
                'importance': 'Lower LDL levels are better. High LDL increases your risk of heart disease and stroke.',
                'category': 'lab_value'
            },
            'hemoglobin a1c': {
                'explanation': 'A blood test that shows your average blood sugar level over the past 2-3 months. It\'s also called HbA1c or A1C.',
                'importance': 'This test helps doctors see how well your diabetes is being controlled over time.',
                'category': 'lab_value'
            }
        }
    
    def _extract_medical_terms(self, text: str) -> List[str]:
        """Extract medical terms from the text."""
        text_lower = text.lower()
        found_terms = []
        
        # Check for known medical terms
        for term in self.medical_terms_db.keys():
            if term in text_lower:
                found_terms.append(term)
        
        # Also look for common medical patterns
        import re
        
        # Medication patterns (uppercase words, often with numbers)
        medication_pattern = r'\b[A-Z][A-Z\s]+\d+\s*MG?\b'
        medications = re.findall(medication_pattern, text)
        found_terms.extend([med.lower().strip() for med in medications])
        
        # Lab value patterns
        lab_pattern = r'\b(glucose|cholesterol|hdl|ldl|creatinine|bun|sodium|potassium)\b'
        lab_values = re.findall(lab_pattern, text_lower)
        found_terms.extend(lab_values)
        
        # Remove duplicates and return
        return list(set(found_terms))
    
    async def _generate_explanations(self, medical_terms: List[str], document_type: str) -> List[Dict[str, str]]:
        """Generate simplified explanations for medical terms."""
        simplified_terms = []
        
        for term in medical_terms:
            if term in self.medical_terms_db:
                term_info = self.medical_terms_db[term]
                simplified_terms.append({
                    'term': term.title(),
                    'explanation': term_info['explanation'],
                    'importance': term_info['importance'],
                    'category': term_info['category']
                })
            else:
                # Generate explanation for unknown terms (mock AI response)
                explanation = await self._generate_ai_explanation(term, document_type)
                simplified_terms.append({
                    'term': term.title(),
                    'explanation': explanation['explanation'],
                    'importance': explanation['importance'],
                    'category': explanation['category']
                })
        
        return simplified_terms
    
    async def _generate_ai_explanation(self, term: str, document_type: str) -> Dict[str, str]:
        """
        Generate AI explanation for unknown medical terms.
        
        In production, this would integrate with Gemini or another LLM.
        """
        # Simulate AI processing delay
        await asyncio.sleep(0.5)
        
        # Mock AI response based on term characteristics
        if 'mg' in term.lower() or any(char.isdigit() for char in term):
            return {
                'explanation': f'This appears to be a medication dosage. The specific medication and dosage should be discussed with your healthcare provider.',
                'importance': 'Important to take exactly as prescribed by your doctor.',
                'category': 'medication'
            }
        elif any(word in term.lower() for word in ['test', 'level', 'count', 'panel']):
            return {
                'explanation': f'This appears to be a medical test or measurement. Your doctor will explain what the results mean for your health.',
                'importance': 'Test results help your doctor monitor your health and adjust treatment if needed.',
                'category': 'lab_value'
            }
        else:
            return {
                'explanation': f'This is a medical term that should be explained by your healthcare provider. Don\'t hesitate to ask questions about any medical terms you don\'t understand.',
                'importance': 'Understanding medical terms helps you better manage your health and follow your treatment plan.',
                'category': 'general'
            }
    
    async def _generate_document_summary(self, text: str, document_type: str) -> str:
        """Generate a summary of the document in plain language."""
        # Simulate AI processing delay
        await asyncio.sleep(0.3)
        
        if document_type == 'prescription':
            return "This is a prescription for medication. It contains important information about what medication to take, how much, and when. Make sure to follow the instructions carefully and contact your pharmacy or doctor if you have questions."
        elif document_type == 'discharge_summary':
            return "This is a discharge summary from your hospital stay. It contains information about your diagnosis, treatments received, and instructions for continuing your care at home. Follow the follow-up instructions carefully."
        elif document_type == 'lab_results':
            return "These are your laboratory test results. They show various measurements of your health, like blood sugar, cholesterol, and other important values. Your doctor will explain what these results mean for your health."
        else:
            return "This is a medical document containing important health information. Review it carefully and discuss any questions with your healthcare provider."
