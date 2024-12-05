import streamlit as st
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize session state to store participant details persistently
if "participants" not in st.session_state:
    st.session_state.participants = []

# Set your SendGrid API key
SENDGRID_API_KEY = "your_sendgrid_api_key_here"

# Function to send email using SendGrid
def send_email_with_sendgrid(to_email, subject, body):
    message = Mail(
        from_email="your_email@example.com",  # Your verified SendGrid sender email
        to_emails=to_email,
        subject=subject,
        html_content=body,  # Use HTML for better formatting
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        st.success(f"Email sent to {to_email}!")
    except Exception as e:
        st.error(f"Failed to send email to {to_email}. Error: {str(e)}")

# Streamlit App UI
st.title("🎅 Secret Santa - One Participant at a Time 🎁")

# Step 1: Prompt for Participant Details
st.header("Step 1: Enter Your Details")
name = st.text_input("What is your name?")
gift_preference = st.text_input("What would you like to receive as a gift?")
email = st.text_input("What is your email address?")

if st.button("Submit Your Details"):
    if not name or not gift_preference or not email:
        st.error("Please fill in all fields!")
    else:
        # Generate a random number for pairing
        participant_id = random.randint(1000, 9999)

        # Save participant details
        st.session_state.participants.append({
            "id": participant_id,
            "name": name,
            "gift_preference": gift_preference,
            "email": email,
            "paired_to": None  # Will be filled during pairing
        })

        st.success(f"Thank you, {name}! Your pairing ID is {participant_id}.")
        st.info("Please wait until all participants have signed up!")

# Step 2: Perform Pairing (Admin Functionality)
if st.session_state.participants:
    st.header("Step 2: Perform Pairing")

    if st.button("Generate Pairings"):
        participants = st.session_state.participants
        names = [p["name"] for p in participants]
        random.shuffle(names)

        # Create circular pairings
        for i, participant in enumerate(participants):
            participant["paired_to"] = names[(i + 1) % len(names)]

        st.success("Pairings have been generated!")
        st.write("Here are the pairings (for debugging purposes):")
        for participant in participants:
            st.write(f'{participant["name"]} → {participant["paired_to"]}')

# Step 3: Send Emails
if st.session_state.participants and st.button("Send Emails"):
    participants = st.session_state.participants

    for participant in participants:
        receiver_name = participant["paired_to"]
        receiver_info = next(
            p for p in participants if p["name"] == receiver_name
        )

        # Email content
        subject = "Your Secret Santa Pairing 🎁"
        body = f"""
        <p>Hello {participant['name']},</p>
        <p>You are the Secret Santa for <strong>{receiver_name}</strong>!</p>
        <p>Here is what they would like to receive: <em>{receiver_info['gift_preference']}</em></p>
        <p>Happy gifting!</p>
        """

        # Send email via SendGrid
        send_email_with_sendgrid(participant["email"], subject, body)
