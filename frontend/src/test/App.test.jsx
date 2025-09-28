import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';

// Mock axios
vi.mock('axios');
import axios from 'axios';

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText('CareCompanion AI')).toBeInTheDocument();
  });

  it('renders the hero section with description', () => {
    render(<App />);
    expect(
      screen.getByText(
        'Transform complex medical documents into simple, actionable care plans'
      )
    ).toBeInTheDocument();
  });

  it('shows file upload area', () => {
    render(<App />);
    expect(screen.getByText('Upload Medical Document')).toBeInTheDocument();
  });

  it('shows analyze button as disabled when no file is selected', () => {
    render(<App />);
    const analyzeButton = screen.getByRole('button', {
      name: /analyze document/i,
    });
    expect(analyzeButton).toBeDisabled();
  });

  it('enables analyze button when file is selected', async () => {
    render(<App />);
    const fileInput = screen.getByRole('button', {
      name: /upload medical document/i,
    });

    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    fireEvent.click(fileInput);

    // Simulate file selection
    const input = document.querySelector('input[type="file"]');
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      const analyzeButton = screen.getByRole('button', {
        name: /analyze document/i,
      });
      expect(analyzeButton).not.toBeDisabled();
    });
  });

  it('shows loading state when processing', async () => {
    // Mock axios to return a pending promise
    axios.post.mockImplementation(() => new Promise(() => {}));

    render(<App />);
    const fileInput = screen.getByRole('button', {
      name: /upload medical document/i,
    });

    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    fireEvent.click(fileInput);

    const input = document.querySelector('input[type="file"]');
    fireEvent.change(input, { target: { files: [file] } });

    const analyzeButton = screen.getByRole('button', {
      name: /analyze document/i,
    });
    fireEvent.click(analyzeButton);

    await waitFor(() => {
      expect(screen.getByText('Processing your document with AI...')).toBeInTheDocument();
    });
  });

  it('shows error message when API call fails', async () => {
    const errorMessage = 'Network error';
    axios.post.mockRejectedValue(new Error(errorMessage));

    render(<App />);
    const fileInput = screen.getByRole('button', {
      name: /upload medical document/i,
    });

    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    fireEvent.click(fileInput);

    const input = document.querySelector('input[type="file"]');
    fireEvent.change(input, { target: { files: [file] } });

    const analyzeButton = screen.getByRole('button', {
      name: /analyze document/i,
    });
    fireEvent.click(analyzeButton);

    await waitFor(() => {
      expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    });
  });

  it('shows care plan when API call succeeds', async () => {
    const mockResponse = {
      data: {
        status: 'completed',
        document_type: 'prescription',
        raw_text: 'Mock prescription text',
        care_plan: {
          medications: [
            {
              name: 'Lisinopril',
              dosage: '10 MG',
              frequency: 'Once daily',
              instructions: 'Take with water',
              quantity: 30,
              refills: 12,
            },
          ],
          simplified_terms: [
            {
              term: 'Lisinopril',
              explanation: 'Blood pressure medication',
              importance: 'Controls blood pressure',
            },
          ],
          action_items: [
            {
              title: 'Take Morning Medication',
              description: 'Take one tablet every morning',
              priority: 'high',
              timeframe: 'Every morning',
            },
          ],
          lifestyle_tips: ['Monitor blood pressure'],
          follow_up_instructions: ['Schedule follow-up'],
          emergency_contacts: ['Call 911'],
        },
        processing_time_seconds: 2.5,
        confidence_score: 0.95,
      },
    };

    axios.post.mockResolvedValue(mockResponse);

    render(<App />);
    const fileInput = screen.getByRole('button', {
      name: /upload medical document/i,
    });

    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    fireEvent.click(fileInput);

    const input = document.querySelector('input[type="file"]');
    fireEvent.change(input, { target: { files: [file] } });

    const analyzeButton = screen.getByRole('button', {
      name: /analyze document/i,
    });
    fireEvent.click(analyzeButton);

    await waitFor(() => {
      expect(screen.getByText('Your Personalized Care Plan')).toBeInTheDocument();
      expect(screen.getByText('Lisinopril')).toBeInTheDocument();
    });
  });
});
