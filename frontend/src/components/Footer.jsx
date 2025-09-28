import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>CareCompanion AI</h4>
          <p>Making healthcare information accessible and understandable for everyone.</p>
        </div>
        
        <div className="footer-section">
          <h4>Important Notice</h4>
          <p>
            This tool is for informational purposes only and should not replace 
            professional medical advice. Always consult with your healthcare provider.
          </p>
        </div>
        
        <div className="footer-section">
          <h4>Privacy & Security</h4>
          <p>
            Your documents are processed securely and are not stored permanently. 
            We prioritize your privacy and data protection.
          </p>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; 2024 CareCompanion AI. Built for Hack for Health Hackathon.</p>
      </div>
    </footer>
  );
};

export default Footer;
