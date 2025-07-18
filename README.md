# AI Poker Coach

An AI-powered MTT (Multi-Table Tournament) poker coaching application that generates realistic scenarios, evaluates decisions, and provides personalized feedback to help players improve their game.

## 🚀 Features

- **AI-Generated Scenarios**: Dynamic MTT scenarios tailored to player weaknesses
- **Decision Evaluation**: Comprehensive analysis of poker decisions with EV calculations
- **Personalized Coaching**: Adaptive learning system that tracks player progress
- **Weakness Detection**: Identifies specific leaks and patterns in play
- **Progress Tracking**: Detailed analytics and improvement metrics
- **Tournament Focus**: Specialized for MTT play with ICM considerations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AI POKER COACH                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Backend (FastAPI + Python)                        │
│  • AI Coach Service (OpenAI GPT-4)                 │
│  • Scenario Generator                               │
│  • Decision Evaluator                               │
│  • Player Context Management                       │
│  • SQLite Database (Local)                          │
│                                                     │
└─────────────────────────────────────────────────────┘
                           ↓
                    REST API (JSON)
                           ↓
┌─────────────────────────────────────────────────────┐
│                  FRONTEND (React)                   │
│  • Scenario Display                                 │
│  • Decision Input                                   │
│  • AI Feedback                                      │
│  • Progress Dashboard                               │
│  • Analytics & Reports                              │
└─────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** with FastAPI
- **OpenAI GPT-4** for AI coaching
- **SQLite** for local data persistence
- **Redis** for caching (optional)
- **SQLAlchemy** for ORM
- **Pydantic** for data validation

### Frontend
- **React 18** with TypeScript
- **React Query** for server state management
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Shadcn/ui** for UI components

### Mobile (Future)
- **React Native** with TypeScript
- **Async Storage** for local data
- **React Navigation** for navigation

## 📁 Project Structure

```
coach/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── api/
│   │   ├── games.py              # Game endpoints
│   │   ├── ai_coach.py           # AI coach endpoints
│   │   └── local_data.py         # Local data management
│   ├── models/
│   │   ├── scenario.py           # Scenario data models
│   │   ├── evaluation.py         # Evaluation models
│   │   └── player_context.py     # Player tracking
│   ├── services/
│   │   ├── ai_coach_service.py   # Core AI logic
│   │   ├── coaching_service.py   # High-level coaching
│   │   └── local_data_service.py # Local data management
│   ├── prompts/
│   │   ├── scenario_prompts.py   # AI scenario prompts
│   │   └── evaluation_prompts.py # AI evaluation prompts
│   ├── schemas/
│   │   ├── game.py               # Request/response schemas
│   │   └── analysis.py           # Analysis schemas
│   └── config/
│       ├── settings.py           # Configuration
│       └── database.py           # Database setup
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── game/             # Game components
│   │   │   │   └── ScenarioDisplay.tsx
│   │   │   └── ai-coach/         # AI coach components
│   │   │       ├── EvaluationFeedback.tsx
│   │   │       └── ProgressDashboard.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx     # Main dashboard
│   │   │   └── ScenarioTraining.tsx
│   │   ├── hooks/
│   │   │   └── useAICoach.ts     # AI coach hook
│   │   ├── services/
│   │   │   └── aiCoachAPI.ts     # API service
│   │   ├── types/
│   │   │   └── game.ts           # TypeScript types
│   │   └── config/
│   │       └── constants.ts      # Configuration
├── venv/                         # Python virtual environment
├── mobile/                       # React Native app (future)
├── .env                          # Environment variables
├── setup.py                      # Database initialization
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.9+ and pip
- **OpenAI API Key**
- **Redis** (optional, for caching)

### Backend Setup

1. **Environment Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup**
   ```bash
   # Initialize local SQLite database (creates ~/.coach directory)
   python setup.py
   ```

4. **Start Backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Frontend**
   ```bash
   npm start
   ```

### Alternative Setup (Using npm scripts)

```bash
# Complete setup (creates venv and installs packages)
npm run setup

# Initialize database
npm run db:init

# Start development server
npm run dev
```

## 🎯 API Endpoints

### AI Coach Endpoints

- `POST /api/ai/scenario` - Generate new scenario
- `POST /api/ai/evaluate` - Evaluate player decision
- `GET /api/ai/progress/{player_id}` - Get progress report
- `GET /api/ai/coaching-plan/{player_id}` - Get coaching plan
- `POST /api/ai/coaching-session/start` - Start session
- `GET /api/ai/weakness-analysis/{player_id}` - Get weakness analysis

### Game Endpoints

- `POST /api/games/scenario/generate` - Generate scenario
- `POST /api/games/scenario/evaluate` - Evaluate decision
- `GET /api/games/player/{player_id}/stats` - Get player stats
- `POST /api/games/session/start` - Start session

## 🔧 Configuration

### Environment Variables

```bash
# Backend (.env)
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite:///~/.coach/player_data.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000/api
```

### Key Settings

- **OpenAI Model**: GPT-4 (configurable)
- **Temperature**: 0.7 (balance creativity/consistency)
- **Max Tokens**: 2000 (scenario/evaluation length)
- **Database**: SQLite local file storage
- **Caching**: Redis for scenario caching (optional)

## 📊 Key Features

### AI Scenario Generation

- **Dynamic Content**: Every scenario is unique
- **Weakness Targeting**: Scenarios focus on player leaks
- **Tournament Context**: ICM pressure, stack depths, stages
- **Realistic Situations**: Based on actual MTT dynamics

### Decision Evaluation

- **EV Calculations**: Expected value analysis
- **Leak Detection**: Pattern recognition in mistakes
- **Coaching Feedback**: Personalized improvement tips
- **Concept Reinforcement**: Key poker concepts highlighted

### Progress Tracking

- **Accuracy Trends**: Track improvement over time
- **Weakness Profiles**: Detailed leak analysis
- **Skill Assessment**: Overall skill level evaluation
- **Adaptive Learning**: Difficulty adjusts to performance

## 🎮 Usage

### Starting a Session

1. **Dashboard** - View progress and start training
2. **Scenario Training** - Practice with AI-generated scenarios
3. **Decision Making** - Choose actions (fold, call, raise)
4. **AI Feedback** - Receive detailed analysis
5. **Progress Tracking** - Monitor improvement

### Scenario Types

- **Preflop** - Opening ranges, 3-betting, blind defense
- **Postflop** - Bet sizing, bluffing, value betting
- **Tournament** - ICM spots, bubble play, final table
- **Specific Situations** - All-in decisions, river spots

## 🧠 AI Features

### Weakness Detection

The AI identifies patterns in player mistakes:

- **Preflop Leaks**: Range issues, position awareness
- **Postflop Leaks**: Bet sizing, bluff frequency
- **Tournament Leaks**: ICM ignorance, risk assessment
- **Mental Game**: Tilt indicators, consistency issues

### Adaptive Difficulty

- **Performance Tracking**: Monitors accuracy rates
- **Dynamic Adjustment**: Increases/decreases difficulty
- **Skill-Based Scenarios**: Matches player level
- **Challenge Progression**: Gradual skill building

## 📈 Analytics

### Player Metrics

- **Overall Accuracy**: Decision correctness rate
- **Improvement Rate**: Skill development velocity
- **Concept Mastery**: Understanding of key concepts
- **Weakness Severity**: Leak impact assessment

### Progress Reports

- **Session Summaries**: Performance per session
- **Trend Analysis**: Long-term improvement patterns
- **Benchmarking**: Comparison to skill level norms
- **Coaching Recommendations**: Personalized study plan

## 💾 Local Data Management

### Data Storage

All player data is stored locally in your home directory:

```
~/.coach/
├── player_data.db          # SQLite database (all game data)
├── backups/                # Automatic database backups
│   ├── backup_20240115.db
│   └── backup_20240116.db
├── exports/                # Player data exports (JSON)
│   └── player_export.json
└── logs/                   # Session logs
    └── sessions.log
```

### Data Management Features

- **Automatic Backups**: Daily database backups
- **Export/Import**: JSON export of all player data
- **Privacy**: All data stays on your local machine
- **Portability**: Easy to backup and transfer
- **No Server Required**: No database server setup needed

### API Endpoints for Data Management

- `GET /api/local/info` - Get local data storage info
- `POST /api/local/backup` - Create database backup
- `GET /api/local/backups` - List available backups
- `POST /api/local/export/{player_id}` - Export player data
- `GET /api/local/stats` - Get database statistics

## 🔮 Future Enhancements

### Phase 2: Advanced Features
- **Hand Range Visualization**: GTO range displays
- **Session Review**: AI analysis of full sessions
- **Opponent Modeling**: Adjust to different player types
- **Multi-way Scenarios**: Complex multi-player situations

### Phase 3: Mobile App
- **React Native App**: Native mobile experience
- **Offline Capability**: Practice without internet
- **Push Notifications**: Study reminders
- **Touch Interface**: Mobile-optimized UI

### Phase 4: PLO Support
- **PLO Scenarios**: Pot Limit Omaha training
- **4-Card Analysis**: PLO-specific evaluation
- **PLO Leaks**: Different leak categories
- **Range Complexity**: PLO range visualization

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
npm run format
```

### Database Initialization

```bash
# Initialize local SQLite database
python setup.py
```

## ❓ Troubleshooting

### Common Issues

1. **OpenAI API Key**: Ensure key is set in environment variables
2. **Database Initialization**: Run `python setup.py` to initialize local database
3. **Port Conflicts**: Make sure ports 8000 and 3000 are free
4. **Dependencies**: Run `pip install -r requirements.txt` and `npm install`
5. **Permissions**: Ensure write access to home directory (~/.coach/)

### Performance Optimization

- Use Redis for caching scenarios (optional)
- Local SQLite database provides fast performance
- Implement request queuing for AI calls
- Regular database cleanup and maintenance

## 📞 Support

For support, please:
1. Check the [troubleshooting guide](#-troubleshooting)
2. Search existing [issues](https://github.com/yairmassury/coach/issues)
3. Create a new issue with detailed description

---

**Status**: 🚀 Ready for Development
**Focus**: MTT No-Limit Hold'em
**Platform**: Web (React) + API (FastAPI)
**AI Provider**: OpenAI GPT-4