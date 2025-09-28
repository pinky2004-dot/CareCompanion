"""
Planner Agent - Generates personalized daily care plans and checklists.
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from agents.base_agent import BaseAgent
from models import MedicationInfo, ActionItem, CarePlan
from utils.logger import logger


class PlannerAgent(BaseAgent):
    """Agent responsible for generating personalized care plans and daily checklists."""
    
    def __init__(self):
        super().__init__("Planner")
        self.lifestyle_tips_db = self._initialize_lifestyle_tips()
        self.emergency_contacts_db = self._initialize_emergency_contacts()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized care plan and daily checklist.
        
        Args:
            input_data: Dictionary containing all previous agent outputs
            
        Returns:
            Dictionary containing complete care plan
        """
        raw_text = input_data.get('raw_text', '')
        document_type = input_data.get('document_type', 'unknown')
        simplified_terms = input_data.get('simplified_terms', [])
        cost_savings = input_data.get('cost_savings', [])
        
        logger.info(f"Generating care plan for {document_type} document")
        
        # Extract medications from the document
        medications = await self._extract_medications(raw_text, simplified_terms)
        
        # Generate action items based on document type and content
        action_items = await self._generate_action_items(raw_text, document_type, medications)
        
        # Generate lifestyle tips based on conditions and medications
        lifestyle_tips = await self._generate_lifestyle_tips(medications, simplified_terms)
        
        # Generate follow-up instructions
        follow_up_instructions = await self._generate_follow_up_instructions(document_type, medications)
        
        # Generate emergency contacts
        emergency_contacts = await self._generate_emergency_contacts(document_type, raw_text)
        
        # Create the complete care plan
        care_plan = CarePlan(
            medications=medications,
            simplified_terms=simplified_terms,
            action_items=action_items,
            lifestyle_tips=lifestyle_tips,
            follow_up_instructions=follow_up_instructions,
            emergency_contacts=emergency_contacts
        )
        
        return {
            "care_plan": care_plan,
            "daily_checklist": self._generate_daily_checklist(medications, action_items),
            "weekly_schedule": self._generate_weekly_schedule(medications, action_items),
            "priority_levels": self._assign_priority_levels(action_items),
            "completion_tracking": self._generate_completion_tracking(action_items)
        }
    
    def _initialize_lifestyle_tips(self) -> Dict[str, List[str]]:
        """Initialize database of lifestyle tips by condition."""
        return {
            'hypertension': [
                'Monitor your blood pressure at home once a week and keep a log',
                'Maintain a low-sodium diet (less than 2,300mg per day)',
                'Engage in regular physical activity (30 minutes most days)',
                'Limit alcohol consumption to moderate levels',
                'Manage stress through relaxation techniques like deep breathing',
                'Maintain a healthy weight',
                'Get 7-9 hours of quality sleep each night',
                'Limit caffeine intake if it affects your blood pressure'
            ],
            'diabetes': [
                'Check your blood sugar levels as recommended by your doctor',
                'Follow a consistent meal schedule with balanced portions',
                'Choose complex carbohydrates over simple sugars',
                'Stay physically active - even a 10-minute walk helps',
                'Keep your feet clean and dry, check for cuts or sores daily',
                'Stay hydrated by drinking plenty of water',
                'Plan ahead for meals and snacks',
                'Work with a diabetes educator or nutritionist'
            ],
            'high_cholesterol': [
                'Choose lean proteins like fish, chicken, and beans',
                'Increase fiber intake with fruits, vegetables, and whole grains',
                'Limit saturated and trans fats',
                'Include heart-healthy fats like olive oil and nuts',
                'Exercise regularly to help raise HDL (good) cholesterol',
                'Maintain a healthy weight',
                'Limit processed foods and fast food',
                'Consider working with a nutritionist'
            ],
            'general': [
                'Take medications at the same time each day',
                'Keep a medication list with you at all times',
                'Use a pill organizer to stay organized',
                'Set reminders on your phone for medications',
                'Keep all medical appointments',
                'Ask questions if you don\'t understand something',
                'Keep emergency contact information handy',
                'Maintain a positive attitude about your health'
            ]
        }
    
    def _initialize_emergency_contacts(self) -> Dict[str, List[str]]:
        """Initialize emergency contacts database."""
        return {
            'general': [
                'Emergency Services: 911',
                'Poison Control: 1-800-222-1222',
                'National Suicide Prevention Lifeline: 988'
            ],
            'medical': [
                'Your Primary Care Doctor',
                'Your Pharmacy',
                'Local Emergency Room',
                'Urgent Care Center'
            ]
        }
    
    async def _extract_medications(self, raw_text: str, simplified_terms: List[Dict[str, str]]) -> List[MedicationInfo]:
        """Extract medication information from the document."""
        medications = []
        
        # Extract medications from simplified terms
        for term in simplified_terms:
            if term.get('category') == 'medication':
                medication_name = term['term']
                
                # Try to extract dosage and frequency from raw text
                dosage, frequency, instructions = self._extract_medication_details(raw_text, medication_name)
                
                medication = MedicationInfo(
                    name=medication_name,
                    dosage=dosage,
                    frequency=frequency,
                    instructions=instructions,
                    quantity=self._extract_quantity(raw_text, medication_name),
                    refills=self._extract_refills(raw_text, medication_name)
                )
                medications.append(medication)
        
        return medications
    
    def _extract_medication_details(self, text: str, medication_name: str) -> tuple:
        """Extract dosage, frequency, and instructions for a medication."""
        text_lower = text.lower()
        med_lower = medication_name.lower()
        
        # Look for dosage patterns
        dosage = "As prescribed"
        frequency = "As directed"
        instructions = "Take as directed by your doctor"
        
        # Find lines containing the medication
        lines = text.split('\n')
        for line in lines:
            if med_lower in line.lower():
                line_lower = line.lower()
                
                # Extract dosage (look for numbers with mg, etc.)
                import re
                dosage_match = re.search(r'(\d+\s*mg)', line_lower)
                if dosage_match:
                    dosage = dosage_match.group(1).upper()
                
                # Extract frequency
                if 'daily' in line_lower or 'every day' in line_lower:
                    frequency = "Once daily"
                elif 'twice' in line_lower or '2 times' in line_lower:
                    frequency = "Twice daily"
                elif 'three times' in line_lower or '3 times' in line_lower:
                    frequency = "Three times daily"
                
                # Extract instructions
                if 'mouth' in line_lower:
                    instructions = "Take by mouth"
                if 'food' in line_lower:
                    instructions += " with food"
                if 'water' in line_lower:
                    instructions += " with water"
        
        return dosage, frequency, instructions
    
    def _extract_quantity(self, text: str, medication_name: str) -> int:
        """Extract quantity for a medication."""
        import re
        text_lower = text.lower()
        med_lower = medication_name.lower()
        
        # Look for quantity patterns
        lines = text.split('\n')
        for line in lines:
            if med_lower in line.lower() and 'qty' in line.lower():
                qty_match = re.search(r'qty:\s*(\d+)', line.lower())
                if qty_match:
                    return int(qty_match.group(1))
        
        return 30  # Default quantity
    
    def _extract_refills(self, text: str, medication_name: str) -> int:
        """Extract number of refills for a medication."""
        import re
        text_lower = text.lower()
        med_lower = medication_name.lower()
        
        # Look for refill patterns
        lines = text.split('\n')
        for line in lines:
            if med_lower in line.lower() and 'refill' in line.lower():
                refill_match = re.search(r'refill[s]?:\s*(\d+)', line.lower())
                if refill_match:
                    return int(refill_match.group(1))
        
        return 0  # Default no refills
    
    async def _generate_action_items(self, raw_text: str, document_type: str, medications: List[MedicationInfo]) -> List[ActionItem]:
        """Generate action items based on the document content."""
        action_items = []
        
        # Medication-related action items
        for medication in medications:
            action_items.append(ActionItem(
                title=f"Take {medication.name}",
                description=f"Take {medication.dosage} of {medication.name} {medication.frequency.lower()}",
                priority="high",
                timeframe=medication.frequency,
                completed=False
            ))
        
        # Document-specific action items
        if document_type == 'prescription':
            action_items.extend([
                ActionItem(
                    title="Pick up prescription",
                    description="Go to the pharmacy to pick up your prescription",
                    priority="high",
                    timeframe="As soon as possible",
                    completed=False
                ),
                ActionItem(
                    title="Set up medication reminders",
                    description="Set up phone reminders for your medication schedule",
                    priority="medium",
                    timeframe="Today",
                    completed=False
                )
            ])
        
        elif document_type == 'discharge_summary':
            action_items.extend([
                ActionItem(
                    title="Schedule follow-up appointment",
                    description="Call your doctor to schedule the recommended follow-up appointment",
                    priority="high",
                    timeframe="Within 1 week",
                    completed=False
                ),
                ActionItem(
                    title="Review discharge instructions",
                    description="Read through all discharge instructions carefully",
                    priority="high",
                    timeframe="Today",
                    completed=False
                )
            ])
        
        elif document_type == 'lab_results':
            action_items.extend([
                ActionItem(
                    title="Discuss results with doctor",
                    description="Schedule an appointment to discuss your lab results",
                    priority="high",
                    timeframe="Within 2 weeks",
                    completed=False
                ),
                ActionItem(
                    title="Implement lifestyle changes",
                    description="Start any recommended lifestyle changes based on your results",
                    priority="medium",
                    timeframe="This week",
                    completed=False
                )
            ])
        
        # Add general action items
        action_items.extend([
            ActionItem(
                title="Keep medical records organized",
                description="File this document with your other medical records",
                priority="low",
                timeframe="This week",
                completed=False
            ),
            ActionItem(
                title="Update emergency contacts",
                description="Make sure your emergency contacts have your current medical information",
                priority="medium",
                timeframe="This month",
                completed=False
            )
        ])
        
        return action_items
    
    async def _generate_lifestyle_tips(self, medications: List[MedicationInfo], simplified_terms: List[Dict[str, str]]) -> List[str]:
        """Generate lifestyle tips based on conditions and medications."""
        tips = []
        
        # Get tips based on conditions
        conditions = [term['term'].lower() for term in simplified_terms if term.get('category') == 'condition']
        
        for condition in conditions:
            if condition in self.lifestyle_tips_db:
                tips.extend(self.lifestyle_tips_db[condition])
        
        # Add general tips
        tips.extend(self.lifestyle_tips_db['general'])
        
        # Add medication-specific tips
        for medication in medications:
            if 'blood pressure' in medication.name.lower() or 'lisinopril' in medication.name.lower():
                tips.extend(self.lifestyle_tips_db['hypertension'])
            elif 'diabetes' in medication.name.lower() or 'metformin' in medication.name.lower():
                tips.extend(self.lifestyle_tips_db['diabetes'])
            elif 'cholesterol' in medication.name.lower() or 'atorvastatin' in medication.name.lower():
                tips.extend(self.lifestyle_tips_db['high_cholesterol'])
        
        # Remove duplicates and return
        return list(set(tips))
    
    async def _generate_follow_up_instructions(self, document_type: str, medications: List[MedicationInfo]) -> List[str]:
        """Generate follow-up instructions."""
        instructions = []
        
        if document_type == 'prescription':
            instructions.extend([
                "Take your medication exactly as prescribed",
                "Contact your doctor if you experience any side effects",
                "Schedule a follow-up appointment in 4-6 weeks",
                "Keep track of how you feel while taking the medication"
            ])
        
        elif document_type == 'discharge_summary':
            instructions.extend([
                "Follow all discharge instructions carefully",
                "Take all prescribed medications as directed",
                "Attend all scheduled follow-up appointments",
                "Contact your doctor if you have any concerns or questions",
                "Keep a record of your symptoms and any changes"
            ])
        
        elif document_type == 'lab_results':
            instructions.extend([
                "Discuss these results with your doctor",
                "Follow any recommendations for lifestyle changes",
                "Schedule follow-up tests as recommended",
                "Monitor your health and report any changes"
            ])
        
        # Add medication-specific instructions
        for medication in medications:
            if 'blood pressure' in medication.name.lower():
                instructions.append("Monitor your blood pressure regularly and keep a log")
            elif 'diabetes' in medication.name.lower():
                instructions.append("Check your blood sugar levels as recommended by your doctor")
        
        return instructions
    
    async def _generate_emergency_contacts(self, document_type: str, raw_text: str) -> List[str]:
        """Generate emergency contacts."""
        contacts = []
        
        # Add general emergency contacts
        contacts.extend(self.emergency_contacts_db['general'])
        
        # Try to extract specific contacts from the document
        import re
        
        # Look for phone numbers
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_numbers = re.findall(phone_pattern, raw_text)
        
        for phone in phone_numbers:
            contacts.append(f"Phone: {phone}")
        
        # Look for doctor names
        doctor_pattern = r'Dr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+'
        doctors = re.findall(doctor_pattern, raw_text)
        
        for doctor in doctors:
            contacts.append(f"{doctor} - Your Doctor")
        
        # Add medical emergency contacts
        contacts.extend(self.emergency_contacts_db['medical'])
        
        return contacts
    
    def _generate_daily_checklist(self, medications: List[MedicationInfo], action_items: List[ActionItem]) -> Dict[str, Any]:
        """Generate a daily checklist."""
        daily_tasks = []
        
        # Add medication tasks
        for medication in medications:
            daily_tasks.append({
                'task': f"Take {medication.name} ({medication.dosage})",
                'time': "Morning" if "daily" in medication.frequency.lower() else "As directed",
                'priority': 'high',
                'completed': False
            })
        
        # Add high-priority action items
        for item in action_items:
            if item.priority == 'high':
                daily_tasks.append({
                    'task': item.title,
                    'time': item.timeframe,
                    'priority': item.priority,
                    'completed': item.completed
                })
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tasks': daily_tasks,
            'total_tasks': len(daily_tasks),
            'completed_tasks': sum(1 for task in daily_tasks if task['completed'])
        }
    
    def _generate_weekly_schedule(self, medications: List[MedicationInfo], action_items: List[ActionItem]) -> Dict[str, Any]:
        """Generate a weekly schedule."""
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_schedule = {}
        
        for day in week_days:
            daily_tasks = []
            
            # Add medication tasks for each day
            for medication in medications:
                daily_tasks.append({
                    'task': f"Take {medication.name}",
                    'time': "Morning",
                    'type': 'medication'
                })
            
            # Add other tasks
            for item in action_items:
                if item.priority in ['high', 'medium']:
                    daily_tasks.append({
                        'task': item.title,
                        'time': item.timeframe,
                        'type': 'action'
                    })
            
            weekly_schedule[day] = daily_tasks
        
        return weekly_schedule
    
    def _assign_priority_levels(self, action_items: List[ActionItem]) -> Dict[str, int]:
        """Assign priority levels to action items."""
        priority_counts = {'high': 0, 'medium': 0, 'low': 0}
        
        for item in action_items:
            priority_counts[item.priority] += 1
        
        return priority_counts
    
    def _generate_completion_tracking(self, action_items: List[ActionItem]) -> Dict[str, Any]:
        """Generate completion tracking information."""
        total_items = len(action_items)
        completed_items = sum(1 for item in action_items if item.completed)
        completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0
        
        return {
            'total_items': total_items,
            'completed_items': completed_items,
            'completion_percentage': round(completion_percentage, 1),
            'remaining_items': total_items - completed_items
        }
