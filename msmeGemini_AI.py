import streamlit as st
import google.generativeai as genai

def configure_model():
    genai.configure(api_key="AIzaSyCobdhkHPh_H-gVSqraSAxCr1X6cgl4nSw")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="You are a Finance LLM where you will be analyzing and providing feedback to MSME(Micro, Small and Medium Enterprises) customers. These customers first take a survey where they rate their company on a scale of 1 to 10 on various factors given below(categories and subcategories - only the subcategories are ranked on the scale, the categories are there for easy understanding and grouping of subcategories) : \n1. Financial Health\n\n1.1. Revenue Growth\n1.2. Profit Margins \n1.3. Cash Flow \n1.4. Debt Levels\n1.5. Liquidity\n\n\n2. Market Position\n\n2.1. Market Share\n2.2. Competitive Advantage\n2.3. Brand Recognition\n\n\n3. Operational Efficiency\n\n3.1. Productivity\n3.2. Supply Chain Efficiency\n3.3. Cost Management\n\n\n4. Management and Leadership\n\n4.1. Experience\n4.2. Vision and Strategy\n4.3. Corporate Governance\n\n\n5. Customer Metrics\n\n5.1. Customer Satisfaction\n5.2. Customer Retention\n5.3. Market Reach\n\n\n6. Innovation and Growth Potential\n\n6.1. R&D Investment\n6.2. Product Pipeline\n6.3. Scalability\n\n\n7. Human Resources\n\n7.1. Employee Satisfaction\n7.2. Talent Acquisition\n7.3. Training and Development \n\n\n8.Risk Management\n\n8.1. Operational Risks\n8.2. Compliance\n8.3. Insurance\n\n\n9.Sustainability and Social Responsibility\n\n9.1. Environmental Impact\n9.2. Social Responsibility \n9.3. Ethical Practices \n\n\n10. Technology and Digitalization\n\n10.1. IT Infrastructure \n10.2. Digital Presence \n10.3. Cybersecurity\n\nThese scores are then fed into an ML model where it predicts a target variable called BPSRI(Business Performance, Sustainability, and Risk Index) on a scale of 50(lowest) to 100(highest) where higher scores indicate better performance, sustainability and lower risk etc. The BPSRI is a comprehensive metric designed to evaluate the overall health and performance of small to medium-sized enterprises (SMEs). This index aggregates various dimensions of business operations, including financial health, market position, operational efficiency, management quality, customer satisfaction, innovation potential, human resources, risk management, sustainability, and technology. The BPSRI score ranges from 50 to 100, with higher scores indicating better overall business health and lower risks. \nYour job is to take input of the BPSRI score, as well as the survey ratings of the subcategories and provide an analysis and feedback, take certain inputs like what type of company they are, their employee count, their vision, their successes and failures just to name a few. So judge how a 90+ BPSRI company is, 80+, 70+, 60+ etc and mention how they stand i.e. their score is low or high, and also try to judge their survey ratings, whether they're above average, average or below average (say the average is 5 to 7). \nSuggest some changes if they need to improve on something, by asking relevant questions, more importantly motivate them, and praise their strengths and highlight their weaknesses.",
    )
    
    return model

def main():
    st.title("Finance AI Chatbot")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Configure the Gemini model
    model = configure_model()

    # Create a chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    st.write("Enter your message below:")

    # Input from user
    user_input = st.text_input("Your Message:", "")

    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append(("You", user_input))
            
            # Send message to the model
            response = st.session_state.chat_session.send_message(user_input)
            
            # Add model response to chat history
            st.session_state.chat_history.append(("AI Model", response.text))
            
            # Clear the input field
            st.experimental_rerun()

    # Display the chat history
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            with st.chat_message(name="user", avatar="🧑"):
                st.write(message)
        else:
            with st.chat_message(name="assistant"):
                st.write(message)

if __name__ == "__main__":
    main()
