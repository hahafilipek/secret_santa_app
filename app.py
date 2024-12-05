import streamlit as st
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize session state to store participant details persistently
if "participants" not in st.session_state:
    st.session_state.participants = []

# Set your SendGrid API key
SENDGRID_API_KEY = "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"

# Function to send email using SendGrid
def send_email_with_sendgrid(to_email, subject, body):
    message = Mail(
        from_email="husf00@vse.cz",  # Your verified SendGrid sender email
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

# Add a GIF at the top
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://media1.tenor.com/m/tVrkM5XhW-EAAAAd/flick-esfand.gif" alt="Secret Santa Gif" width="400">
    </div>
    """,
    unsafe_allow_html=True,
)

# Add a Czech flag with fires under it
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/2560px-Flag_of_the_Czech_Republic.svg.png" 
        alt="Czech Flag with Fire" width="400">
        <p style="color: red; font-size: 20px; font-weight: bold;">🔥🔥🔥</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("🎅 Secret Santa for the best board 🎁")

# Step 1: Prompt for Participant Details
st.header("Step 1: Enter Your Details")
name = st.text_input("What is your name?")
gift_preference = st.text_input("Give a hint what would you like to receive as a gift:)")
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
        st.info("wait for others to join, do not perform pairings")

# Step 2: Perform Pairing (Admin Functionality)
if st.session_state.participants:
    st.header("Step 2: Perform Pairing")

    if st.button("Generate Pairings"):
        participants = st.session_state.participants
        names = [p["name"] for p in participants]
        random.shuffle(names)

       # Generate pairings ensuring no one is paired with themselves
def generate_pairings(participants):
    names = [p["name"] for p in participants]
    shuffle(names)  # Randomize the names

    while True:
        # Try generating a pairing list
        pairings = names[:]
        shuffle(pairings)

        # Check if any name is paired with itself
        if all(name != pairing for name, pairing in zip(names, pairings)):
            break  # Exit the loop if pairings are valid

    # Assign pairings back to participants
    for i, participant in enumerate(participants):
        participant["paired_to"] = pairings[i]

# Use the function in the pairing step
if st.button("Generate Pairings", key="generate_pairings"):
    generate_pairings(st.session_state.participants)
    st.success("Pairings have been generated!")
    st.write("Here are the pairings (for debugging purposes):")
    for participant in st.session_state.participants:
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
