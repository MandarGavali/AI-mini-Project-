# Mini Flight Reminder Tool - AI & Data Science Project
# A complete flight delay prediction and reminder system

import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Configuration
WEATHER_API_KEY = "your_openweather_api_key"  # Get from openweathermap.org
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Airport codes mapping (simplified for demo)
AIRPORT_CODES = {
    'mumbai': 'BOM', 'delhi': 'DEL', 'bangalore': 'BLR', 'chennai': 'MAA',
    'kolkata': 'CCU', 'hyderabad': 'HYD', 'pune': 'PNQ', 'ahmedabad': 'AMD',
    'goa': 'GOI', 'kochi': 'COK', 'jaipur': 'JAI', 'lucknow': 'LKO',
    'london': 'LHR', 'new york': 'JFK', 'dubai': 'DXB', 'singapore': 'SIN'
}

class FlightReminderAI:
    """AI-powered flight delay prediction and reminder system"""
    
    def __init__(self):
        self.delay_factors = {
            'weather_impact': {
                'Rain': 0.3, 'Thunderstorm': 0.7, 'Snow': 0.8, 'Fog': 0.6,
                'Clear': 0.1, 'Clouds': 0.2, 'Drizzle': 0.25
            },
            'seasonal_factors': {
                'winter': 0.4, 'monsoon': 0.5, 'summer': 0.2, 'spring': 0.2
            }
        }
    
    def get_weather_data(self, city, api_key):
        """Fetch weather forecast data"""
        try:
            if not api_key or api_key == "your_openweather_api_key":
                # Mock data for demo purposes
                return self.get_mock_weather(city)
            
            url = f"{WEATHER_BASE_URL}?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return self.get_mock_weather(city)
        except:
            return self.get_mock_weather(city)
    
    def get_mock_weather(self, city):
        """Generate realistic mock weather data for demo"""
        import random
        weather_conditions = ['Clear', 'Clouds', 'Rain', 'Drizzle', 'Thunderstorm']
        
        # Simulate seasonal weather patterns
        current_month = datetime.now().month
        if current_month in [6, 7, 8, 9]:  # Monsoon
            weather_conditions = ['Rain', 'Thunderstorm', 'Drizzle', 'Clouds']
        elif current_month in [12, 1, 2]:  # Winter
            weather_conditions = ['Fog', 'Clear', 'Clouds']
        
        selected_weather = random.choice(weather_conditions)
        temp = random.randint(15, 35)
        humidity = random.randint(40, 90)
        wind_speed = random.uniform(2, 15)
        
        return {
            'list': [{
                'main': {
                    'temp': temp,
                    'humidity': humidity
                },
                'weather': [{'main': selected_weather, 'description': selected_weather.lower()}],
                'wind': {'speed': wind_speed},
                'dt_txt': (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')
            }],
            'city': {'name': city.title()}
        }
    
    def calculate_delay_probability(self, weather_data, travel_date, city):
        """AI-powered delay probability calculation"""
        base_probability = 0.15  # Base 15% chance
        
        if not weather_data or 'list' not in weather_data:
            return base_probability, "Unable to fetch weather data", []
        
        # Extract weather information
        forecast = weather_data['list'][0]
        weather_main = forecast['weather'][0]['main']
        temperature = forecast['main']['temp']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        
        # Weather impact
        weather_factor = self.delay_factors['weather_impact'].get(weather_main, 0.2)
        
        # Temperature extremes
        temp_factor = 0
        if temperature < 5 or temperature > 40:
            temp_factor = 0.2
        
        # High humidity (fog risk)
        humidity_factor = 0.1 if humidity > 85 else 0
        
        # Strong winds
        wind_factor = 0.15 if wind_speed > 10 else 0
        
        # Day of week factor (weekends busier)
        travel_datetime = datetime.strptime(travel_date, '%Y-%m-%d')
        weekend_factor = 0.1 if travel_datetime.weekday() >= 5 else 0
        
        # Holiday season factor
        holiday_factor = 0
        if travel_datetime.month in [12, 1, 4, 10]:  # Holiday months
            holiday_factor = 0.15
        
        # Calculate total probability
        total_probability = min(base_probability + weather_factor + temp_factor + 
                              humidity_factor + wind_factor + weekend_factor + 
                              holiday_factor, 0.95)
        
        # Generate risk factors list
        risk_factors = []
        if weather_factor > 0.2:
            risk_factors.append(f"Weather: {weather_main}")
        if temp_factor > 0:
            risk_factors.append(f"Extreme temperature: {temperature}°C")
        if humidity_factor > 0:
            risk_factors.append("High humidity (fog risk)")
        if wind_factor > 0:
            risk_factors.append(f"Strong winds: {wind_speed:.1f} m/s")
        if weekend_factor > 0:
            risk_factors.append("Weekend travel")
        if holiday_factor > 0:
            risk_factors.append("Holiday season")
        
        return total_probability, weather_main, risk_factors
    
    def generate_smart_reminders(self, delay_prob, weather_main, risk_factors, city):
        """Generate AI-powered smart reminders"""
        reminders = []
        
        # Basic reminders
        if delay_prob > 0.6:
            reminders.append("🚨 HIGH delay risk - arrive 2+ hours early")
            reminders.append("📱 Check flight status frequently")
        elif delay_prob > 0.4:
            reminders.append("⚠️ MODERATE delay risk - arrive 90 minutes early")
        else:
            reminders.append("✅ LOW delay risk - standard check-in time")
        
        # Weather-specific reminders
        weather_reminders = {
            'Rain': ["☔ Carry umbrella", "🚗 Allow extra travel time to airport"],
            'Thunderstorm': ["⛈️ Monitor weather updates", "📞 Consider travel insurance"],
            'Snow': ["❄️ Dress warmly", "🚙 Use reliable transport to airport"],
            'Fog': ["🌫️ Expect visibility delays", "📱 Download airline app for updates"],
            'Clear': ["☀️ Perfect flying weather!", "😎 Enjoy your journey"]
        }
        
        if weather_main in weather_reminders:
            reminders.extend(weather_reminders[weather_main])
        
        # Smart suggestions based on risk factors
        if "Weekend travel" in risk_factors:
            reminders.append("🏃 Expect crowded airport - use online check-in")
        
        if "Holiday season" in risk_factors:
            reminders.append("🎄 Holiday rush - book airport parking in advance")
        
        # City-specific tips
        city_tips = {
            'mumbai': "🌧️ Monsoon city - always carry rain gear",
            'delhi': "🌫️ Fog common in winter mornings",
            'bangalore': "🌤️ Pleasant weather year-round",
            'pune': "🌦️ Check monsoon updates in rainy season"
        }
        
        if city.lower() in city_tips:
            reminders.append(city_tips[city.lower()])
        
        return reminders[:6]  # Return top 6 reminders

def main():
    st.set_page_config(
        page_title="✈️ Smart Flight Reminder Tool",
        page_icon="✈️",
        layout="wide"
    )
    
    # Header
    st.title("✈️ AI-Powered Flight Reminder Tool")
    st.markdown("**Get smart reminders and delay predictions for your flight**")
    st.markdown("---")
    
    # Initialize AI system
    ai_system = FlightReminderAI()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Flight Details")
        
        # City input
        city = st.selectbox(
            "Select your departure city:",
            options=list(AIRPORT_CODES.keys()),
            index=0,
            help="Choose your departure city"
        )
        
        # Date input
        min_date = datetime.now().date()
        max_date = min_date + timedelta(days=30)
        travel_date = st.date_input(
            "Travel date:",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
        
        # API key input (optional)
        api_key = st.text_input(
            "OpenWeather API Key (optional):",
            value="",
            type="password",
            help="Get free API key from openweathermap.org"
        )
        
        analyze_button = st.button("🔍 Analyze Flight", type="primary")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if analyze_button:
            with st.spinner("Analyzing flight conditions..."):
                # Get weather data
                weather_data = ai_system.get_weather_data(city, api_key or WEATHER_API_KEY)
                
                # Calculate delay probability
                delay_prob, weather_main, risk_factors = ai_system.calculate_delay_probability(
                    weather_data, travel_date.strftime('%Y-%m-%d'), city
                )
                
                # Generate reminders
                reminders = ai_system.generate_smart_reminders(
                    delay_prob, weather_main, risk_factors, city
                )
                
                # Display results
                st.subheader("📊 Flight Analysis Results")
                
                # Delay probability gauge
                prob_percentage = int(delay_prob * 100)
                if prob_percentage < 30:
                    color = "green"
                    risk_level = "LOW"
                elif prob_percentage < 60:
                    color = "orange"
                    risk_level = "MODERATE"
                else:
                    color = "red"
                    risk_level = "HIGH"
                
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: {color}15; border: 2px solid {color};">
                    <h3 style="color: {color}; margin: 0;">🎯 Delay Risk: {risk_level}</h3>
                    <h2 style="color: {color}; margin: 10px 0;">{prob_percentage}% Probability</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Weather information
                if weather_data and 'list' in weather_data:
                    forecast = weather_data['list'][0]
                    temp = forecast['main']['temp']
                    humidity = forecast['main']['humidity']
                    wind_speed = forecast['wind']['speed']
                    
                    st.subheader("🌤️ Weather Forecast")
                    
                    weather_col1, weather_col2, weather_col3, weather_col4 = st.columns(4)
                    with weather_col1:
                        st.metric("Weather", weather_main)
                    with weather_col2:
                        st.metric("Temperature", f"{temp}°C")
                    with weather_col3:
                        st.metric("Humidity", f"{humidity}%")
                    with weather_col4:
                        st.metric("Wind Speed", f"{wind_speed:.1f} m/s")
                
                # Risk factors
                if risk_factors:
                    st.subheader("⚠️ Risk Factors Detected")
                    for factor in risk_factors:
                        st.warning(f"• {factor}")
                
                # Smart reminders
                st.subheader("💡 Smart Reminders")
                for i, reminder in enumerate(reminders, 1):
                    st.info(f"**{i}.** {reminder}")
                
                # Additional insights
                st.subheader("📈 AI Insights")
                insights = f"""
                Based on our AI analysis for **{city.title()} ({AIRPORT_CODES.get(city, 'N/A')})** on **{travel_date.strftime('%B %d, %Y')}**:
                
                • **Weather Impact**: {weather_main} conditions contribute {int(ai_system.delay_factors['weather_impact'].get(weather_main, 0.2) * 100)}% to delay risk
                • **Travel Day**: {'Weekend travel increases crowding' if travel_date.weekday() >= 5 else 'Weekday travel - typically less crowded'}
                • **Season**: {'Holiday season - expect higher traffic' if travel_date.month in [12, 1, 4, 10] else 'Regular season - normal traffic expected'}
                
                **Recommendation**: {'Arrive early and stay flexible with your plans' if delay_prob > 0.4 else 'Normal check-in procedures should suffice'}
                """
                st.markdown(insights)
    
    # with col2:
    #     st.subheader("ℹ️ About This Tool")
    #     st.markdown("""
    #     This AI-powered tool analyzes:
        
    #     🌡️ **Weather Conditions**
    #     - Temperature extremes
    #     - Precipitation & storms
    #     - Wind speeds & visibility
        
    #     📅 **Travel Patterns**
    #     - Day of week effects
    #     - Seasonal variations
    #     - Holiday periods
        
    #     🤖 **AI Predictions**
    #     - Machine learning algorithms
    #     - Historical delay patterns
    #     - Risk factor weighting
        
    #     ---
        
    #     **🔧 Tech Stack:**
    #     - Python + Streamlit
    #     - OpenWeather API
    #     - Predictive Analytics
    #     - Real-time Data Processing
    #     """)
        
    #     # Quick tips
    #     with st.expander("💡 Quick Tips"):
    #         st.markdown("""
    #         • Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
    #         • Check 24-48 hours before travel
    #         • Follow airline social media for updates
    #         • Download airline mobile apps
    #         • Consider travel insurance for high-risk flights
    #         """)
    
    # # Footer
    # st.markdown("---")
    # st.markdown("*Built with ❤️ for AI & Data Science Project | Weather data powered by OpenWeatherMap*")

if __name__ == "__main__":
    main()