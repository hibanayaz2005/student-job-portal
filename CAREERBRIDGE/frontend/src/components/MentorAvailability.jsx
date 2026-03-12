import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MentorAvailability = () => {
  console.log('MentorAvailability component rendering...');
  
  const [mentors, setMentors] = useState([]);
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingData, setBookingData] = useState({
    topic: '',
    session_type: 'video',
    session_date: ''
  });

  useEffect(() => {
    fetchMentors();
  }, []);

  const fetchMentors = async () => {
    try {
      setLoading(true);
      console.log('Fetching mentors from API...');
      const response = await axios.get('http://127.0.0.1:8000/api/mentorship/mentors/');
      console.log('Mentors API response:', response.data);
      setMentors(response.data.mentors);
      if (response.data.mentors.length === 0) {
        console.log('No mentors found in API response');
      }
    } catch (error) {
      console.error('Error fetching mentors:', error);
      if (error.response) {
        console.error('Error response:', error.response.data);
        console.error('Error status:', error.response.status);
      }
      alert('Failed to load mentors. Please check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const fetchMentorAvailability = async (mentorId) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://127.0.0.1:8000/api/mentorship/mentors/${mentorId}/availability/`);
      setAvailability(response.data.availability);
    } catch (error) {
      console.error('Error fetching availability:', error);
      alert('Failed to load mentor availability. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleMentorSelect = (mentor) => {
    setSelectedMentor(mentor);
    fetchMentorAvailability(mentor.id);
  };

  const handleSlotSelect = (slot, date) => {
    setSelectedSlot({ ...slot, date });
    setShowBookingModal(true);
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedSlot || !bookingData.topic) {
      alert('Please fill in all required fields.');
      return;
    }

    try {
      const sessionDateTime = new Date(`${selectedSlot.date}T${selectedSlot.start_time}:00`);
      
      const bookingPayload = {
        mentor_id: selectedMentor.id,
        availability_id: selectedSlot.id,
        topic: bookingData.topic,
        session_type: bookingData.session_type,
        session_date: sessionDateTime.toISOString()
      };

      const response = await axios.post(
        'http://127.0.0.1:8000/api/mentorship/book-session/',
        bookingPayload,
        {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          }
        }
      );

      alert('Session booked successfully! The mentor will confirm your booking.');
      setShowBookingModal(false);
      setBookingData({ topic: '', session_type: 'video', session_date: '' });
      setSelectedSlot(null);
      
      // Refresh availability
      fetchMentorAvailability(selectedMentor.id);
      
    } catch (error) {
      console.error('Error booking session:', error);
      alert(error.response?.data?.error || 'Failed to book session. Please try again.');
    }
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const getAvailabilityStatus = (mentor) => {
    if (mentor.today_available) {
      return {
        status: 'Available Today',
        color: '#10b981',
        type: 'available',
        slots: mentor.today_slots
      };
    } else {
      // Check if mentor has any slots this week (even if not today)
      const currentHour = new Date().getHours();
      const isBusinessHours = currentHour >= 9 && currentHour <= 18;
      
      if (isBusinessHours) {
        return {
          status: 'Busy',
          color: '#ef4444',
          type: 'busy',
          slots: []
        };
      } else {
        return {
          status: 'Next Available Tomorrow',
          color: '#f59e0b',
          type: 'next_slot',
          slots: []
        };
      }
    }
  };

  const handleQuickBook = (mentor, event) => {
    event.stopPropagation(); // Prevent card selection
    handleMentorSelect(mentor);
    
    // If mentor is available today, show booking modal directly
    if (mentor.today_available && mentor.today_slots.length > 0) {
      const firstSlot = mentor.today_slots[0];
      const today = new Date().toISOString().split('T')[0];
      setSelectedSlot({ 
        ...firstSlot, 
        date: today,
        id: `today-${firstSlot.start_time}` // Temporary ID for demonstration
      });
      setShowBookingModal(true);
    } else {
      // Show availability schedule
      alert(`${mentor.name} is not available today. Please check their weekly schedule.`);
    }
  };

  return (
    <section className="section-pad" id="mentorship" style={{ background: 'var(--surface)', border: '5px solid red' }}>
      <div className="container">
        <div className="section-label">Mentorship</div>
        <h2 className="section-title" style={{ color: 'red' }}>Learn from Industry Experts (UPDATED VERSION)</h2>
        <p className="section-sub">Connect with verified mentors for personalized guidance and career advice</p>
        
        {/* Debug Info */}
        <div style={{ 
          background: 'white', 
          border: '1px solid var(--border)', 
          borderRadius: '8px', 
          padding: '15px', 
          marginBottom: '20px',
          fontSize: '12px',
          color: 'var(--muted)'
        }}>
          <strong>Debug Info:</strong><br/>
          Mentors loaded: {mentors.length}<br/>
          Loading: {loading ? 'Yes' : 'No'}<br/>
          Selected Mentor: {selectedMentor ? selectedMentor.name : 'None'}<br/>
          API Endpoint: http://127.0.0.1:8000/api/mentorship/mentors/
        </div>
        
        <div className="mentorship-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '30px', marginTop: '40px' }}>
          {/* Mentors List */}
          <div>
            <h3 style={{ marginBottom: '20px', fontSize: '20px', fontWeight: '700' }}>Available Mentors</h3>
            {loading && mentors.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)' }}>
                Loading mentors...
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                {mentors.map(mentor => {
                  const availability = getAvailabilityStatus(mentor);
                  return (
                    <div
                      key={mentor.id}
                      className="mentor-card"
                      onClick={() => handleMentorSelect(mentor)}
                      style={{
                        background: 'white',
                        border: selectedMentor?.id === mentor.id ? '2px solid var(--accent)' : '1px solid var(--border)',
                        borderRadius: '12px',
                        padding: '20px',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                        <div>
                          <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px' }}>
                            {mentor.name}
                          </h4>
                          <p style={{ fontSize: '13px', color: 'var(--muted)', marginBottom: '8px' }}>
                            {mentor.designation} {mentor.company && `@ ${mentor.company}`}
                          </p>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ 
                            fontSize: '12px', 
                            fontWeight: '600', 
                            color: availability.color,
                            marginBottom: '4px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                            justifyContent: 'flex-end'
                          }}>
                            {availability.type === 'available' && (
                              <>
                                <span style={{ 
                                  width: '8px', 
                                  height: '8px', 
                                  borderRadius: '50%', 
                                  background: availability.color 
                                }}></span>
                                {availability.status}
                              </>
                            )}
                            {availability.type === 'busy' && (
                              <>
                                <span style={{ 
                                  width: '8px', 
                                  height: '8px', 
                                  borderRadius: '50%', 
                                  background: availability.color 
                                }}></span>
                                {availability.status}
                              </>
                            )}
                            {availability.type === 'next_slot' && (
                              <>
                                <span style={{ 
                                  width: '8px', 
                                  height: '8px', 
                                  borderRadius: '50%', 
                                  background: availability.color 
                                }}></span>
                                {availability.status}
                              </>
                            )}
                          </div>
                          <div style={{ fontSize: '14px', fontWeight: '700', color: 'var(--accent)' }}>
                            ₹{mentor.hourly_rate}/hr
                          </div>
                        </div>
                      </div>
                      
                      <div style={{ marginBottom: '12px' }}>
                        <div style={{ fontSize: '12px', color: 'var(--muted)', marginBottom: '4px' }}>
                          Expertise: {mentor.expertise.join(', ')}
                        </div>
                        <div style={{ display: 'flex', gap: '8px', fontSize: '12px' }}>
                          <span style={{ color: 'var(--muted)' }}>⭐ {mentor.rating}</span>
                          <span style={{ color: 'var(--muted)' }}>•</span>
                          <span style={{ color: 'var(--muted)' }}>{mentor.sessions_completed} sessions</span>
                          <span style={{ color: 'var(--muted)' }}>•</span>
                          <span style={{ color: 'var(--muted)' }}>{mentor.years_experience} years exp.</span>
                        </div>
                      </div>
                      
                      {availability.slots.length > 0 && (
                        <div style={{ fontSize: '11px', color: availability.color, marginBottom: '12px' }}>
                          Today: {availability.slots.map(slot => `${slot.start_time}-${slot.end_time}`).join(', ')}
                        </div>
                      )}
                      
                      <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                        <button
                          onClick={(e) => handleQuickBook(mentor, e)}
                          style={{
                            flex: 1,
                            padding: '8px 12px',
                            background: availability.type === 'available' ? 'var(--accent)' : 'var(--muted)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: '600',
                            cursor: 'pointer',
                            transition: 'background 0.3s ease'
                          }}
                          onMouseOver={(e) => {
                            if (availability.type === 'available') {
                              e.target.style.background = 'var(--accent-dark)';
                            }
                          }}
                          onMouseOut={(e) => {
                            if (availability.type === 'available') {
                              e.target.style.background = 'var(--accent)';
                            }
                          }}
                        >
                          {availability.type === 'available' ? 'Book Session' : 
                           availability.type === 'busy' ? 'View Schedule' : 'View Schedule'}
                        </button>
                        <button
                          onClick={() => handleMentorSelect(mentor)}
                          style={{
                            padding: '8px 12px',
                            background: 'transparent',
                            color: 'var(--accent)',
                            border: '1px solid var(--accent)',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: '600',
                            cursor: 'pointer'
                          }}
                        >
                          View Profile
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Availability Details */}
          <div>
            {selectedMentor ? (
              <div>
                <h3 style={{ marginBottom: '20px', fontSize: '20px', fontWeight: '700' }}>
                  {selectedMentor.name}'s Schedule
                </h3>
                
                {loading ? (
                  <div style={{ textAlign: 'center', padding: '40px', color: 'var(--muted)' }}>
                    Loading availability...
                  </div>
                ) : availability.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    {availability.map(day => (
                      <div key={day.date} style={{ 
                        background: 'white', 
                        border: '1px solid var(--border)', 
                        borderRadius: '12px', 
                        padding: '20px' 
                      }}>
                        <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px' }}>
                          {day.day_name} ({day.date})
                        </h4>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: '10px' }}>
                          {day.slots.map(slot => (
                            <button
                              key={slot.id}
                              onClick={() => handleSlotSelect(slot, day.date)}
                              style={{
                                padding: '10px',
                                background: 'var(--accent)',
                                color: 'white',
                                border: 'none',
                                borderRadius: '8px',
                                fontSize: '13px',
                                fontWeight: '600',
                                cursor: 'pointer',
                                transition: 'background 0.3s ease'
                              }}
                              onMouseOver={(e) => e.target.style.background = 'var(--accent-dark)'}
                              onMouseOut={(e) => e.target.style.background = 'var(--accent)'}
                            >
                              {slot.start_time} - {slot.end_time}
                            </button>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '40px', 
                    background: 'white', 
                    border: '1px solid var(--border)', 
                    borderRadius: '12px',
                    color: 'var(--muted)'
                  }}>
                    No available time slots for the next 7 days
                  </div>
                )}
              </div>
            ) : (
              <div style={{ 
                textAlign: 'center', 
                padding: '60px 20px', 
                background: 'white', 
                border: '1px solid var(--border)', 
                borderRadius: '12px',
                color: 'var(--muted)'
              }}>
                <h4 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>
                  Select a Mentor
                </h4>
                <p>Choose a mentor from the list to view their availability and book a session.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Booking Modal */}
      {showBookingModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'white',
            padding: '30px',
            borderRadius: '16px',
            width: '100%',
            maxWidth: '500px',
            margin: '20px'
          }}>
            <h3 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '20px' }}>
              Book Session with {selectedMentor?.name}
            </h3>
            
            <form onSubmit={handleBookingSubmit}>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
                  Session Topic *
                </label>
                <input
                  type="text"
                  value={bookingData.topic}
                  onChange={(e) => setBookingData({...bookingData, topic: e.target.value})}
                  required
                  placeholder="e.g., Career guidance, Resume review, Interview prep"
                  style={{ width: '100%', padding: '12px', border: '1px solid var(--border)', borderRadius: '8px' }}
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
                  Session Type
                </label>
                <select
                  value={bookingData.session_type}
                  onChange={(e) => setBookingData({...bookingData, session_type: e.target.value})}
                  style={{ width: '100%', padding: '12px', border: '1px solid var(--border)', borderRadius: '8px' }}
                >
                  <option value="video">Video Call</option>
                  <option value="audio">Audio Call</option>
                  <option value="text">Text Chat</option>
                </select>
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '14px' }}>
                  Selected Time Slot
                </label>
                <div style={{ padding: '12px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px' }}>
                  <div style={{ fontWeight: '600' }}>
                    {selectedSlot?.date} • {selectedSlot?.start_time} - {selectedSlot?.end_time}
                  </div>
                  <div style={{ fontSize: '13px', color: 'var(--muted)', marginTop: '4px' }}>
                    Session fee: ₹{selectedMentor?.hourly_rate}/hour
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => setShowBookingModal(false)}
                  style={{
                    padding: '12px 24px',
                    background: 'transparent',
                    color: 'var(--muted)',
                    border: '1px solid var(--border)',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  style={{
                    padding: '12px 24px',
                    background: 'var(--accent)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  Book Session
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </section>
  );
};

export default MentorAvailability;
