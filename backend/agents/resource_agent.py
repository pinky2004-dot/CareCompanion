"""
Resource Agent - Finds cost-saving resources and support information.
"""
import asyncio
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class ResourceAgent(BaseAgent):
    """Agent responsible for finding cost-saving resources and support information."""
    
    def __init__(self):
        super().__init__("Resource")
        self.cost_savings_db = self._initialize_cost_savings_db()
        self.support_resources = self._initialize_support_resources()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find cost-saving resources and support information.
        
        Args:
            input_data: Dictionary containing 'simplified_terms' and 'document_type'
            
        Returns:
            Dictionary containing cost savings and resource information
        """
        simplified_terms = input_data.get('simplified_terms', [])
        document_type = input_data.get('document_type', 'unknown')
        
        logger.info(f"Finding resources for {document_type} document")
        
        # Extract medications from simplified terms
        medications = self._extract_medications(simplified_terms)
        
        # Find cost savings for medications
        cost_savings = await self._find_medication_cost_savings(medications)
        
        # Find general support resources
        support_resources = await self._find_support_resources(document_type, medications)
        
        # Generate insurance and financial assistance info
        financial_assistance = await self._generate_financial_assistance_info(medications)
        
        return {
            "cost_savings": cost_savings,
            "support_resources": support_resources,
            "financial_assistance": financial_assistance,
            "medications_analyzed": len(medications),
            "total_potential_savings": self._calculate_total_savings(cost_savings)
        }
    
    def _initialize_cost_savings_db(self) -> Dict[str, Dict[str, Any]]:
        """Initialize database of medication cost savings."""
        return {
            'lisinopril': {
                'generic_available': True,
                'generic_name': 'Lisinopril',
                'brand_names': ['Prinivil', 'Zestril'],
                'average_generic_cost': 15.00,
                'average_brand_cost': 45.00,
                'monthly_savings': 30.00,
                'annual_savings': 360.00,
                'discount_programs': [
                    'GoodRx',
                    'SingleCare',
                    'RxSaver'
                ],
                'manufacturer_coupons': True,
                'patient_assistance': True
            },
            'metformin': {
                'generic_available': True,
                'generic_name': 'Metformin',
                'brand_names': ['Glucophage'],
                'average_generic_cost': 8.00,
                'average_brand_cost': 25.00,
                'monthly_savings': 17.00,
                'annual_savings': 204.00,
                'discount_programs': [
                    'GoodRx',
                    'SingleCare',
                    'RxSaver'
                ],
                'manufacturer_coupons': False,
                'patient_assistance': True
            },
            'atorvastatin': {
                'generic_available': True,
                'generic_name': 'Atorvastatin',
                'brand_names': ['Lipitor'],
                'average_generic_cost': 20.00,
                'average_brand_cost': 80.00,
                'monthly_savings': 60.00,
                'annual_savings': 720.00,
                'discount_programs': [
                    'GoodRx',
                    'SingleCare',
                    'RxSaver'
                ],
                'manufacturer_coupons': True,
                'patient_assistance': True
            }
        }
    
    def _initialize_support_resources(self) -> Dict[str, List[Dict[str, str]]]:
        """Initialize support resources database."""
        return {
            'general': [
                {
                    'name': 'Medicare.gov',
                    'description': 'Official Medicare website with information about coverage and benefits',
                    'url': 'https://www.medicare.gov',
                    'phone': '1-800-MEDICARE',
                    'type': 'government'
                },
                {
                    'name': 'Healthcare.gov',
                    'description': 'Health insurance marketplace and coverage information',
                    'url': 'https://www.healthcare.gov',
                    'phone': '1-800-318-2596',
                    'type': 'government'
                },
                {
                    'name': 'Patient Advocate Foundation',
                    'description': 'Free case management and financial assistance for patients',
                    'url': 'https://www.patientadvocate.org',
                    'phone': '1-800-532-5274',
                    'type': 'nonprofit'
                }
            ],
            'diabetes': [
                {
                    'name': 'American Diabetes Association',
                    'description': 'Resources, education, and support for diabetes management',
                    'url': 'https://www.diabetes.org',
                    'phone': '1-800-DIABETES',
                    'type': 'nonprofit'
                },
                {
                    'name': 'Diabetes Self-Management Education',
                    'description': 'Classes and resources for diabetes self-care',
                    'url': 'https://www.diabeteseducator.org',
                    'phone': '1-800-338-3633',
                    'type': 'education'
                }
            ],
            'hypertension': [
                {
                    'name': 'American Heart Association',
                    'description': 'Resources for heart health and blood pressure management',
                    'url': 'https://www.heart.org',
                    'phone': '1-800-AHA-USA1',
                    'type': 'nonprofit'
                },
                {
                    'name': 'Blood Pressure Monitoring',
                    'description': 'Free blood pressure monitoring at many pharmacies',
                    'url': 'https://www.heart.org/en/health-topics/high-blood-pressure',
                    'phone': '1-800-AHA-USA1',
                    'type': 'service'
                }
            ]
        }
    
    def _extract_medications(self, simplified_terms: List[Dict[str, str]]) -> List[str]:
        """Extract medication names from simplified terms."""
        medications = []
        for term in simplified_terms:
            if term.get('category') == 'medication':
                medications.append(term['term'].lower())
        return medications
    
    async def _find_medication_cost_savings(self, medications: List[str]) -> List[Dict[str, Any]]:
        """Find cost savings for medications."""
        cost_savings = []
        
        for medication in medications:
            if medication in self.cost_savings_db:
                med_info = self.cost_savings_db[medication]
                
                # Simulate API call delay
                await asyncio.sleep(0.2)
                
                cost_savings.append({
                    'medication': medication.title(),
                    'generic_available': med_info['generic_available'],
                    'generic_name': med_info['generic_name'],
                    'brand_names': med_info['brand_names'],
                    'monthly_savings': med_info['monthly_savings'],
                    'annual_savings': med_info['annual_savings'],
                    'discount_programs': med_info['discount_programs'],
                    'manufacturer_coupons': med_info['manufacturer_coupons'],
                    'patient_assistance': med_info['patient_assistance'],
                    'savings_tips': self._generate_savings_tips(med_info)
                })
        
        return cost_savings
    
    def _generate_savings_tips(self, med_info: Dict[str, Any]) -> List[str]:
        """Generate cost-saving tips for medications."""
        tips = []
        
        if med_info['generic_available']:
            tips.append(f"Ask your doctor about generic {med_info['generic_name']} to save ${med_info['monthly_savings']:.2f} per month")
        
        if med_info['discount_programs']:
            tips.append(f"Use discount programs like {', '.join(med_info['discount_programs'])} for additional savings")
        
        if med_info['manufacturer_coupons']:
            tips.append("Check for manufacturer coupons on the drug company's website")
        
        if med_info['patient_assistance']:
            tips.append("Ask your doctor about patient assistance programs if you're having trouble affording this medication")
        
        tips.append("Consider using a 90-day supply to reduce co-pays and pharmacy visits")
        tips.append("Compare prices at different pharmacies - costs can vary significantly")
        
        return tips
    
    async def _find_support_resources(self, document_type: str, medications: List[str]) -> List[Dict[str, str]]:
        """Find relevant support resources."""
        resources = []
        
        # Add general resources
        resources.extend(self.support_resources['general'])
        
        # Add condition-specific resources based on medications
        if any(med in ['metformin', 'glucose', 'diabetes'] for med in medications):
            resources.extend(self.support_resources['diabetes'])
        
        if any(med in ['lisinopril', 'atorvastatin', 'hypertension'] for med in medications):
            resources.extend(self.support_resources['hypertension'])
        
        # Simulate API call delay
        await asyncio.sleep(0.3)
        
        return resources
    
    async def _generate_financial_assistance_info(self, medications: List[str]) -> Dict[str, Any]:
        """Generate financial assistance information."""
        # Simulate API call delay
        await asyncio.sleep(0.2)
        
        return {
            'medicare_part_d': {
                'description': 'Prescription drug coverage for Medicare beneficiaries',
                'website': 'https://www.medicare.gov/drug-coverage-part-d',
                'phone': '1-800-MEDICARE',
                'eligibility': 'Medicare beneficiaries'
            },
            'medicaid': {
                'description': 'Health coverage for low-income individuals and families',
                'website': 'https://www.medicaid.gov',
                'phone': '1-800-318-2596',
                'eligibility': 'Low-income individuals and families'
            },
            'patient_assistance_programs': {
                'description': 'Drug company programs that provide free or low-cost medications',
                'website': 'https://www.needymeds.org',
                'phone': '1-800-503-6897',
                'eligibility': 'Varies by program and income'
            },
            'pharmacy_discount_programs': {
                'description': 'Programs that offer discounted prescription medications',
                'examples': ['GoodRx', 'SingleCare', 'RxSaver', 'Blink Health'],
                'eligibility': 'Available to everyone'
            }
        }
    
    def _calculate_total_savings(self, cost_savings: List[Dict[str, Any]]) -> float:
        """Calculate total potential annual savings."""
        total = 0.0
        for savings in cost_savings:
            total += savings.get('annual_savings', 0.0)
        return total
