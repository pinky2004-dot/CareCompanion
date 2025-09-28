import React, { useState } from 'react';
import './CarePlanDisplay.css';

const CarePlanDisplay = ({ data, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const formatActionPlan = (actionPlan) => {
    // Convert markdown-like formatting to HTML
    return actionPlan
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br />');
  };

  const renderMedications = () => {
    if (!data.care_plan?.medications?.length) return null;
    
    return (
      <div className="medications-section">
        <h3>💊 Your Medications</h3>
        {data.care_plan.medications.map((med, index) => (
          <div key={index} className="medication-card">
            <div className="medication-header">
              <h4>{med.name}</h4>
              <span className="dosage">{med.dosage}</span>
            </div>
            <div className="medication-details">
              <p><strong>Frequency:</strong> {med.frequency}</p>
              <p><strong>Instructions:</strong> {med.instructions}</p>
              {med.quantity && <p><strong>Quantity:</strong> {med.quantity} tablets</p>}
              {med.refills && <p><strong>Refills:</strong> {med.refills} remaining</p>}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderActionItems = () => {
    if (!data.care_plan?.action_items?.length) return null;
    
    return (
      <div className="action-items-section">
        <h3>✅ Your Action Plan</h3>
        {data.care_plan.action_items.map((item, index) => (
          <div key={index} className={`action-item ${item.priority}`}>
            <div className="action-item-header">
              <h4>{item.title}</h4>
              <span className={`priority-badge ${item.priority}`}>
                {item.priority}
              </span>
            </div>
            <p className="action-description">{item.description}</p>
            <p className="action-timeframe">
              <strong>When:</strong> {item.timeframe}
            </p>
          </div>
        ))}
      </div>
    );
  };

  const renderSimplifiedTerms = () => {
    if (!data.care_plan?.simplified_terms?.length) return null;
    
    return (
      <div className="terms-section">
        <h3>📚 Understanding Your Health</h3>
        {data.care_plan.simplified_terms.map((term, index) => (
          <div key={index} className="term-card">
            <h4>{term.term}</h4>
            <p className="term-explanation">{term.explanation}</p>
            <p className="term-importance">
              <strong>Why this matters:</strong> {term.importance}
            </p>
          </div>
        ))}
      </div>
    );
  };

  const renderLifestyleTips = () => {
    if (!data.care_plan?.lifestyle_tips?.length) return null;
    
    return (
      <div className="lifestyle-section">
        <h3>🌱 Lifestyle Tips</h3>
        <ul className="tips-list">
          {data.care_plan.lifestyle_tips.map((tip, index) => (
            <li key={index} className="tip-item">{tip}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderFollowUp = () => {
    if (!data.care_plan?.follow_up_instructions?.length) return null;
    
    return (
      <div className="followup-section">
        <h3>📅 Follow-up Instructions</h3>
        <ul className="followup-list">
          {data.care_plan.follow_up_instructions.map((instruction, index) => (
            <li key={index} className="followup-item">{instruction}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderEmergencyContacts = () => {
    if (!data.care_plan?.emergency_contacts?.length) return null;
    
    return (
      <div className="emergency-section">
        <h3>🚨 Emergency Contacts</h3>
        <ul className="contacts-list">
          {data.care_plan.emergency_contacts.map((contact, index) => (
            <li key={index} className="contact-item">{contact}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderCostSavings = () => {
    if (!data.agent_results?.resource?.result?.cost_savings?.length) return null;
    
    const costSavings = data.agent_results.resource.result.cost_savings;
    const totalSavings = data.agent_results.resource.result.total_potential_savings || 0;
    
    return (
      <div className="cost-savings-section">
        <h3>💰 Cost Savings Opportunities</h3>
        <div className="savings-summary">
          <div className="savings-total">
            <h4>Potential Annual Savings: ${totalSavings.toFixed(2)}</h4>
          </div>
        </div>
        
        {costSavings.map((saving, index) => (
          <div key={index} className="savings-card">
            <div className="savings-header">
              <h4>{saving.medication}</h4>
              <span className="savings-amount">
                Save ${saving.monthly_savings}/month
              </span>
            </div>
            
            <div className="savings-details">
              {saving.generic_available && (
                <p><strong>Generic Available:</strong> Yes - {saving.generic_name}</p>
              )}
              
              <div className="savings-tips">
                <h5>Money-Saving Tips:</h5>
                <ul>
                  {saving.savings_tips.map((tip, tipIndex) => (
                    <li key={tipIndex}>{tip}</li>
                  ))}
                </ul>
              </div>
              
              <div className="discount-programs">
                <h5>Discount Programs:</h5>
                <div className="program-tags">
                  {saving.discount_programs.map((program, programIndex) => (
                    <span key={programIndex} className="program-tag">{program}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderSupportResources = () => {
    if (!data.agent_results?.resource?.result?.support_resources?.length) return null;
    
    const resources = data.agent_results.resource.result.support_resources;
    
    return (
      <div className="support-resources-section">
        <h3>🆘 Support Resources</h3>
        <div className="resources-grid">
          {resources.map((resource, index) => (
            <div key={index} className="resource-card">
              <h4>{resource.name}</h4>
              <p className="resource-description">{resource.description}</p>
              <div className="resource-contact">
                {resource.url && (
                  <a href={resource.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                    Visit Website
                  </a>
                )}
                {resource.phone && (
                  <span className="resource-phone">{resource.phone}</span>
                )}
              </div>
              <span className="resource-type">{resource.type}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="care-plan-container">
      <div className="care-plan-header">
        <h2>Your Personalized Care Plan</h2>
        <div className="plan-meta">
          <span className="confidence-score">
            Confidence: {Math.round((data.confidence_score || 0) * 100)}%
          </span>
          <span className="processing-time">
            Processed in {data.processing_time_seconds?.toFixed(1)}s
          </span>
        </div>
        <button className="reset-button" onClick={onReset}>
          Process Another Document
        </button>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'medications' ? 'active' : ''}`}
          onClick={() => setActiveTab('medications')}
        >
          Medications
        </button>
        <button 
          className={`tab ${activeTab === 'actions' ? 'active' : ''}`}
          onClick={() => setActiveTab('actions')}
        >
          Action Plan
        </button>
        <button 
          className={`tab ${activeTab === 'education' ? 'active' : ''}`}
          onClick={() => setActiveTab('education')}
        >
          Health Education
        </button>
        <button 
          className={`tab ${activeTab === 'resources' ? 'active' : ''}`}
          onClick={() => setActiveTab('resources')}
        >
          Resources & Savings
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            {renderMedications()}
            {renderActionItems()}
            {renderLifestyleTips()}
          </div>
        )}
        
        {activeTab === 'medications' && (
          <div className="medications-tab">
            {renderMedications()}
          </div>
        )}
        
        {activeTab === 'actions' && (
          <div className="actions-tab">
            {renderActionItems()}
            {renderFollowUp()}
            {renderEmergencyContacts()}
          </div>
        )}
        
        {activeTab === 'education' && (
          <div className="education-tab">
            {renderSimplifiedTerms()}
            {renderLifestyleTips()}
          </div>
        )}
        
        {activeTab === 'resources' && (
          <div className="resources-tab">
            {renderCostSavings()}
            {renderSupportResources()}
          </div>
        )}
      </div>
    </div>
  );
};

export default CarePlanDisplay;
