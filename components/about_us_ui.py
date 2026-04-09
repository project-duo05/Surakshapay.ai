def get_about_us_html():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Warm, Human-centric About Us Styles */
        body {
            margin: 0;
            padding: 0;
            background: transparent;
        }
        .about-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #334155;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            margin: 20px auto;
            max-width: 900px;
        }

        /* 1. HERO SECTION */
        .story-hero {
            background: linear-gradient(135deg, #0f52ba 0%, #1e3a8a 100%);
            padding: 80px 40px;
            text-align: center;
            color: white;
        }
        .story-hero h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.2;
            color: white !important;
        }
        .story-hero p {
            font-size: 1.25rem;
            max-width: 600px;
            margin: 0 auto 30px;
            opacity: 0.95;
            color: white !important;
            font-weight: 400;
        }
        .heart-icon {
            font-size: 50px;
            animation: pulse 2s infinite;
            display: inline-block;
            margin-bottom: 10px;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        /* 2. THE STORY INTERVIEW / LETTER */
        .our-story {
            padding: 60px 40px;
            background: #ffffff;
            line-height: 1.8;
            font-size: 1.15rem;
        }
        .our-story h2 {
            color: #0f52ba !important;
            font-size: 2.2rem;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 800;
        }
        .story-text {
            max-width: 700px;
            margin: 0 auto;
        }
        .story-text p {
            margin-bottom: 25px;
            color: #475569 !important;
            font-weight: 400;
        }
        
        .quote-block {
            background: #f8fafc;
            border-left: 5px solid #0f52ba;
            padding: 25px 35px;
            margin: 40px 0;
            border-radius: 0 12px 12px 0;
            font-style: italic;
            font-size: 1.25rem;
            color: #1e293b;
        }

        /* 3. MEET THE TEAM / MISSION */
        .mission-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            padding: 20px 40px 60px;
            background: #ffffff;
            max-width: 800px;
            margin: 0 auto;
        }
        .mission-card {
            background: #f8fafc;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            text-align: left;
        }
        .mission-card-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        .mission-card h3 {
            font-size: 1.3rem;
            color: #0f52ba !important;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .mission-card p {
            font-size: 1.05rem;
            color: #475569 !important;
            line-height: 1.6;
            margin: 0;
        }

        /* 4. A HUMAN PROMISE */
        .promise-footer {
            text-align: center;
            padding: 60px 40px;
            background: #0f52ba;
            color: white;
            border-radius: 0 0 12px 12px;
        }
        .promise-footer h2 {
            font-size: 2.2rem;
            color: white !important;
            margin-bottom: 20px;
        }
        .promise-footer p {
            font-size: 1.2rem;
            color: #e2e8f0 !important;
            max-width: 600px;
            margin: 0 auto;
        }
        .signature {
            margin-top: 30px;
            font-family: 'Brush Script MT', cursive, sans-serif;
            font-size: 2.5rem;
            color: #60a5fa;
        }
    </style>
</head>
<body>
    <div class="about-container">
        
        <!-- HERO -->
        <div class="story-hero">
            <span class="heart-icon">❤️</span>
            <h1>Built by People, for People.</h1>
            <p>We didn't just build an algorithm. We built a shield to protect everyday people from the stress of digital fraud.</p>
        </div>

        <!-- THE STORY -->
        <div class="our-story">
            <h2>Our Story</h2>
            <div class="story-text">
                <p>Hello! We're the team behind <strong>Suraksha Pay AI</strong>. Our journey didn't start in a boardroom or an IT lab; it started with a real-life problem.</p>
                
                <p>A few years ago, someone close to us had their bank account compromised. We watched them spend weeks stressed, making phone calls, and fighting to get their hard-earned money back. It was exhausting, scary, and felt completely unfair.</p>

                <div class="quote-block">
                    "Technology shouldn't just be smart. It should have your back when things go wrong."
                </div>

                <p>We realized that traditional banking systems were too slow to catch these anomalies. They reacted <em>after</em> the damage was done. So, we asked ourselves: <strong>What if we could teach machines to spot trouble before it happens?</strong></p>
                
                <p>That's how Suraksha Pay AI was born. We took advanced machine learning architectures—like Hybrid Risk Engines—and gave them a single, human purpose: to act as a digital bodyguard for your transactions.</p>
            </div>
        </div>

        <!-- THE MISSION -->
        <div class="mission-grid">
            <div class="mission-card">
                <div class="mission-card-icon">🤝</div>
                <h3>Empathy First</h3>
                <p>We design our alerts to be clear and helpful, not confusing or robotic. We want you to feel informed, not overwhelmed.</p>
            </div>
            <div class="mission-card">
                <div class="mission-card-icon">🛡️</div>
                <h3>Fierce Protection</h3>
                <p>Behind our friendly interface is a military-grade AI model that never sleeps, tirelessly weeding out anomalies 24/7.</p>
            </div>
        </div>

        <!-- PROMISE -->
        <div class="promise-footer">
            <h2>Our Promise to You</h2>
            <p>We know that behind every transaction is a real person trying to live their life. We promise to keep building tools that put your peace of mind first.</p>
            <div class="signature">Made by Shivang Gupta & Aavya Chandra</div>
        </div>

    </div>
</body>
</html>
"""
