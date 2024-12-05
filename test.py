import streamlit as st
import time
import uuid
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env file

GROQ_API_KEY = os.getenv('API_KEY')

if GROQ_API_KEY is None:
    print("API Key not found in the environment variables.")
else:
    print("API Key loaded successfully.")

# Configuration
MODEL = "llama-3.1-70b-versatile"

class DebateAgent:
    def __init__(self, name: str, perspective: str, emoji: str, llm: ChatGroq):
        self.name = name
        self.perspective = perspective
        self.emoji = emoji
        self.llm = llm
        self.memory: List[Dict] = []

    def generate_statement(self, topic: str, words_limit: int,debate_context: str = "") -> Dict:
        prompt = f"""You are {self.name}, arguing the {self.perspective} perspective on the topic: {topic}.
        Debate Context: {debate_context}
        Your response should be concise and limited to approximately {words_limit:.0f} words.
	Generate a focused, evidence-based statement within this limit.
        
        1. Builds on previous arguments
        2. Presents a clear, logical point
        3. Uses relevant examples
        4. Is concise yet compelling
        5. Maintains a professional and engaging tone"""

        response = self.llm.invoke([
            HumanMessage(content=prompt)
        ])
        
        return {
            "name": self.name,
            "perspective": self.perspective,
            "text": response.content,
            "timestamp": str(uuid.uuid4())
        }

class FactChecker:
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    def verify_claim(self, claim: str) -> Dict:
        try:
            wiki_search = self.wikipedia_tool.run(claim)
            
            verification_prompt = f"""Fact-Check Analysis:
            Claim: {claim}
            Wikipedia Search Results: {wiki_search}

            Evaluate the claim's accuracy:
            1. Is the claim supported by available evidence?
            2. Provide a credibility rating (0-100%)
            3. Offer context or correction if necessary
            4. Be concise and objective"""

            response = self.llm.invoke([
                HumanMessage(content=verification_prompt)
            ])

            return {
                "original_claim": claim,
                "verification": response.content,
                "timestamp": str(uuid.uuid4())
            }
        except Exception as e:
            return {
                "original_claim": claim,
                "verification": f"Verification error: {str(e)}",
                "timestamp": str(uuid.uuid4())
            }

class Moderator:
    def __init__(self, llm: ChatGroq):
        self.llm = llm

    def introduce_debate(self, topic: str, debater1: str, debater2: str) -> str:
        prompt = f"""As a professional debate moderator, create an engaging introduction for a debate:
        Topic: {topic}
        Debaters: {debater1} and {debater2} names are Nexia and Orion

        Provide a:
        1. Concise context of the debate topic
        2. Brief introduction of the debaters
        3. Clear explanation of debate rules
        4. Enthusiastic and professional tone
        5. Motivate the audience to pay attention"""

        response = self.llm.invoke([
            HumanMessage(content=prompt)
        ])
        return response.content

    def generate_transition(self, current_speaker: str, next_speaker: str, topic: str) -> str:
        prompt = f"""As a debate moderator, create a smooth transition:
        Current Speaker: {current_speaker}
        Next Speaker: {next_speaker}
        Topic: {topic}

        Provide a transition that:
        1. Acknowledges the previous speaker's key points
        2. Introduces the next speaker
        3. Maintains debate momentum
        4. Keeps the audience engaged"""

        response = self.llm.invoke([
            HumanMessage(content=prompt)
        ])
        return response.content

def run_timed_debate(topic: str, debate_duration: int, speaking_time: int):
    # Initialize LLM
    llm = ChatGroq(
        temperature=0.3,
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL
    )
    words_limit = speaking_time * 2.5

    # Initialize Agents with Emojis
    debater1 = DebateAgent("Nexia", "supportive", "🟢", llm)
    debater2 = DebateAgent("Orion", "opposing", "🔴", llm)
    fact_checker = FactChecker(llm)
    moderator = Moderator(llm)

    # Debate Timer and Control
    timer_placeholder = st.empty()

    # Debate Introduction
    st.header(f"⚖️ Moderator Introduces Debate")
    intro = moderator.introduce_debate(topic, debater1.name, debater2.name)
    st.write(intro)

    # Debate Timer Setup
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=debate_duration)

    # Debate Flow Containers: Initialize list of containers for the debate laps
    lap_containers = []

    # Debate Flow
    current_speaker = debater1
    other_speaker = debater2
    statements = []

    lap_counter = 0  # to keep track of rounds/laps of debate

    while datetime.now() < end_time:
        # Create a new lap container for each round of speaking
        with st.container():
            lap_counter += 1
            lap_containers.append(lap_counter)

            # Update Timer
            remaining_time = end_time - datetime.now()
            timer_placeholder.metric("Debate Time Left", 
                                     f"{remaining_time.seconds // 60}:{remaining_time.seconds % 60:02d}")

            # Step 1: Generate Statement for Current Speaker (Pro or Con)
            statement = current_speaker.generate_statement(
                topic,
                words_limit, 
                debate_context="\n".join([s['text'] for s in statements[-3:]])
            )
            statements.append(statement)

            # Step 2: Display Statement for the Current Speaker (Pro or Con)
            st.subheader(f"{current_speaker.emoji} {current_speaker.name}")
            st.write(statement['text'])

            # Step 3: Fact Check for Current Speaker's Statement
            st.subheader("🕵️ Fact Check")
            fact_check = fact_checker.verify_claim(statement['text'])
            with st.expander(f"Verification for {current_speaker.name}"):
                st.write(fact_check['verification'])

            # Step 4: Generate Moderator's Transition (for smooth flow)
            if current_speaker.name == "Nexia":
                st.subheader("⚖️ Moderator's Guidance")
                transition = moderator.generate_transition(
                    current_speaker.name, 
                    other_speaker.name, 
                    topic
                )
                st.write(transition)

            # Step 5: Pause for speaking time (for each speaker)
            time.sleep(10)

            # Step 6: Switch Speakers (after one round of speaking)
            current_speaker, other_speaker = other_speaker, current_speaker

    st.success("Debate has concluded!")


def main():
    st.set_page_config(layout="wide")
    st.title("🤖 Adversarial AI Debate System")
    
    # Sidebar for Debate Configuration
    st.sidebar.header("Debate Configuration")
    topic = st.sidebar.text_input("Debate Topic", 
                                  placeholder="E.g., 'Who is the Greatest: Messi or Ronaldo?'")
    
    debate_duration = st.sidebar.slider(
        "Total Debate Duration (minutes)", 
        min_value=5, max_value=60, value=15
    )
    
    speaking_time = st.sidebar.slider(
        "Speaking Time per Turn (seconds)", 
        min_value=10, max_value=1200, value=160
    )
    if st.sidebar.button("Start Debate"):
        if topic:
            run_timed_debate(topic, debate_duration, speaking_time)
        else:
            st.sidebar.error("Please enter a debate topic")

if __name__ == "__main__":
    main()
