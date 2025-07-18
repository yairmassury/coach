# Coach - Poker Coaching Application

A comprehensive poker coaching application that tracks player progress, analyzes strengths and weaknesses, and provides AI-powered personalized coaching recommendations.

## 🎯 Project Overview

Coach is designed to help poker players improve their game through:
- **Game Session Tracking**: Record and analyze poker sessions
- **AI-Powered Analysis**: Get intelligent insights on your play style
- **Progress Monitoring**: Track improvement over time
- **Personalized Coaching**: Receive tailored recommendations
- **Performance Metrics**: Detailed statistics and analytics

## 🚀 Features

### Core Features
- **User Management**: Registration, authentication, and profile management
- **Session Tracking**: Log poker sessions with buy-ins, cash-outs, and duration
- **Hand History Analysis**: Upload and analyze played hands
- **Performance Metrics**: Win/loss rates, ROI, hourly rates
- **AI Coaching**: Personalized recommendations based on play style

### Advanced Features
- **Weakness Detection**: Identify common mistakes and leaks
- **Strength Analysis**: Highlight areas of strong play
- **Progress Tracking**: Visual charts showing improvement over time
- **Bankroll Management**: Track and analyze bankroll changes
- **Position Analysis**: Analyze play by table position
- **Opponent Analysis**: Track tendencies of regular opponents

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** with FastAPI
- **PostgreSQL** database with SQLAlchemy ORM
- **OpenAI GPT-4** for AI analysis
- **JWT** for authentication
- **Docker** for containerization

### Frontend
- **React 18** with TypeScript
- **Modern UI framework** (to be determined)
- **Responsive design** for mobile and desktop

### Development Tools
- **pytest** for backend testing
- **Jest** for frontend testing
- **Docker Compose** for local development
- **GitHub Actions** for CI/CD

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Docker and Docker Compose
- OpenAI API key

## 🏗️ Project Structure

```
coach/
├── backend/                 # Python FastAPI backend
│   ├── api/                # API endpoints
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── config/             # Configuration
│   └── tests/              # Backend tests
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── hooks/          # Custom hooks
│   └── public/             # Static assets
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── docker-compose.yml      # Docker configuration
```

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yairmassury/coach.git
cd coach
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Add your OpenAI API key and database credentials
```

### 3. Docker Development (Recommended)
```bash
# Start all services
docker-compose up -d

# The application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### 4. Manual Development Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python scripts/init_db.py

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 📊 Database Setup

### Using Docker (Recommended)
Database is automatically set up with Docker Compose.

### Manual Setup
```bash
# Create PostgreSQL database
createdb coach_db

# Run initialization script
python scripts/init_db.py

# (Optional) Seed with sample data
python scripts/seed_data.py
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## 🏛️ Architecture

### Backend Architecture
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Database ORM for Python
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication

### Frontend Architecture
- **React**: Component-based UI library
- **TypeScript**: Type-safe JavaScript
- **Custom Hooks**: Reusable logic components
- **Context API**: State management

### Database Schema
- **Users**: User accounts and profiles
- **GameSessions**: Poker session records
- **HandHistory**: Individual hand data
- **AnalysisResults**: AI analysis results

## 🔐 Security

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Data Protection**: Encryption at rest and in transit
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: API rate limiting for protection

## 🚀 Deployment

### Development
```bash
docker-compose up -d
```

### Production
Detailed deployment instructions available in `docs/deployment.md`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 Development Workflow

1. **Planning**: Check `PROJECT_PLAN.md` for development phases
2. **Issues**: Use GitHub Issues for tracking tasks
3. **Branches**: Create feature branches for new development
4. **Testing**: Ensure tests pass before submitting PRs
5. **Code Review**: All changes require code review

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **API Key Issues**
   - Verify OpenAI API key is set in `.env`
   - Check API key permissions and rate limits

3. **Docker Issues**
   - Ensure Docker is running
   - Check port availability (3000, 8000, 5432)
   - Run `docker-compose down` and `docker-compose up -d`

### Getting Help
- Check the [documentation](docs/)
- Review [GitHub Issues](https://github.com/yairmassury/coach/issues)
- Create a new issue if needed

## 📚 Documentation

- **Project Plan**: `PROJECT_PLAN.md` - Detailed development plan
- **API Documentation**: `docs/api.md` - API endpoints and usage
- **Setup Guide**: `docs/setup.md` - Detailed setup instructions
- **Architecture**: `docs/architecture.md` - Technical architecture

## 🛣️ Roadmap

### Phase 1 - Foundation (Weeks 1-2)
- ✅ Project setup and structure
- ✅ Development environment
- Basic API and database setup
- Authentication system

### Phase 2 - Core Features (Weeks 3-5)
- Game session tracking
- Hand history storage
- Basic analysis features
- User dashboard

### Phase 3 - AI Integration (Weeks 6-8)
- OpenAI integration
- Hand analysis algorithms
- Coaching recommendations
- Performance metrics

### Phase 4 - Frontend (Weeks 9-11)
- React application
- User interface
- Data visualization
- Mobile responsiveness

### Phase 5 - Advanced Features (Weeks 12-14)
- Advanced analytics
- Progress tracking
- Social features
- Export capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Yair Massury** - Project Creator and Lead Developer

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI and React communities
- PostgreSQL team
- All contributors and testers

---

**Status**: 🚧 In Development  
**Version**: 0.1.0  
**Last Updated**: July 2025

For detailed development information, see [PROJECT_PLAN.md](PROJECT_PLAN.md).