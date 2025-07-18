# AI-First Poker Coach - Personal MTT Training App

A personal AI-powered poker coaching application focused on MTT (Multi-Table Tournament) play, with the AI agent as the core intelligence generating scenarios, evaluating decisions, and tracking player weaknesses.

## 🧠 Core Concept

The AI agent is the brain of the application:
- **Generates** realistic MTT scenarios tailored to player weaknesses
- **Evaluates** every decision with detailed EV calculations
- **Tracks** specific leaks and weakness patterns
- **Coaches** with personalized improvement plans

The Android app is simply a presentation layer for interacting with the AI coach.

## 🎯 Project Philosophy

- **AI-First**: The AI generates all content dynamically - no hardcoded scenarios
- **Weakness-Focused**: AI identifies and targets specific player leaks
- **MTT-Specific**: Scenarios consider tournament dynamics (ICM, stack depths, stages)
- **Personal Use**: Designed for individual improvement tracking

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   AI POKER COACH                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Scenario Generator                              │
│     └─> Creates realistic MTT situations           │
│                                                     │
│  2. Decision Evaluator                              │
│     └─> Analyzes player actions & calculates EV    │
│                                                     │
│  3. Weakness Tracker                                │
│     └─> Identifies patterns & leaks                 │
│                                                     │
│  4. Progress Manager                                │
│     └─> Maintains player context & improvement     │
│                                                     │
└─────────────────────────────────────────────────────┘
                           ↓
                    API CALLS (JSON)
                           ↓
┌─────────────────────────────────────────────────────┐
│                  ANDROID APP                        │
│  • Displays scenarios                               │
│  • Captures decisions                               │
│  • Shows AI feedback                                │
│  • Tracks local progress                            │
└─────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend (AI Service)
- **Python 3.9+** with FastAPI
- **LLM Integration**: OpenAI GPT-4, Claude, or other foundation models
- **In-Memory Context**: Player weakness tracking
- **Optional**: Redis for persistent context storage

### Mobile App
- **React Native** with TypeScript
- **Async Storage** for local progress tracking
- **Axios** for API communication
- **Minimal UI libraries** for fast development

## 📁 Project Structure

```
poker-coach-ai/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── services/
│   │   └── ai_coach_service.py    # Core AI logic
│   ├── models/
│   │   ├── scenario.py            # Scenario data models
│   │   ├── evaluation.py          # Evaluation models
│   │   └── player_context.py      # Player tracking
│   ├── prompts/
│   │   ├── scenario_prompts.py    # LLM prompt templates
│   │   └── evaluation_prompts.py  # Evaluation prompts
│   └── api/
│       └── routes.py              # API endpoints
│
├── mobile/
│   ├── src/
│   │   ├── api/
│   │   │   └── AICoachAPI.ts     # API service
│   │   ├── screens/
│   │   │   ├── SetupScreen.tsx   # Game configuration
│   │   │   ├── ScenarioScreen.tsx # Play scenarios
│   │   │   └── FeedbackScreen.tsx # AI evaluation
│   │   ├── storage/
│   │   │   └── PlayerContext.ts  # Local storage
│   │   └── types/
│   │       └── poker.types.ts    # TypeScript types
│   └── android/                  # Android-specific files
│
└── docs/
    └── api.md                    # API documentation
```

## 🚀 Implementation Plan

### Phase 1: AI Core Development (Week 1)

#### 1.1 LLM Integration
```python
# backend/services/ai_coach_service.py

class AIPokerCoach:
    def __init__(self):
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.player_contexts = {}  # In-memory storage
    
    async def generate_scenario(self, params: ScenarioRequest):
        """Generate MTT-specific scenario based on player level"""
        prompt = self._build_scenario_prompt(
            game_type="MTT",
            stage=params.tournament_stage,
            stack_depth=params.stack_depth,
            player_weakness=params.focus_area,
            difficulty=params.skill_level
        )
        
        response = await self.llm.complete(prompt)
        return self._parse_scenario(response)
```

#### 1.2 Scenario Generation Prompts
```python
def _build_scenario_prompt(self, **params):
    return f"""
    Generate a realistic MTT poker scenario with these parameters:
    
    Tournament Stage: {params['stage']}
    Stack Depth: {params['stack_depth']} BB
    Focus Area: {params['player_weakness']}
    
    Create a scenario that specifically tests: {params['player_weakness']}
    
    Return in this EXACT JSON format:
    {{
        "hero_position": "BTN|CO|MP|EP|SB|BB",
        "hero_stack": 1500,
        "villain_position": "position",
        "villain_stack": 2000,
        "blinds": {{"small": 50, "big": 100}},
        "ante": 10,
        "hero_cards": ["As", "Kh"],
        "action_history": ["UTG folds", "MP raises to 250", "CO folds"],
        "current_street": "preflop|flop|turn|river",
        "board": ["Qd", "Js", "3c"],
        "pot_size": 425,
        "to_call": 250,
        "optimal_action": {{
            "action": "fold|call|raise",
            "amount": 0,
            "reasoning": "detailed explanation"
        }},
        "gto_frequencies": {{
            "fold": 0.3,
            "call": 0.5,
            "raise": 0.2
        }}
    }}
    """
```

#### 1.3 Decision Evaluation
```python
async def evaluate_decision(self, 
                          scenario_id: str, 
                          player_action: str,
                          player_id: str):
    """AI evaluates the decision and updates weakness profile"""
    
    evaluation_prompt = f"""
    Evaluate this poker decision:
    
    Scenario: {scenario_details}
    Player Action: {player_action}
    Player History: {player_weaknesses}
    
    Provide evaluation in JSON:
    {{
        "correct": boolean,
        "ev_difference": -2.5,
        "leak_type": "category.specific_leak",
        "severity": 1-10,
        "explanation": "why this was good/bad",
        "coaching_tip": "specific advice",
        "concepts": ["pot odds", "position", "ranges"]
    }}
    """
    
    result = await self.llm.complete(evaluation_prompt)
    self._update_player_weaknesses(player_id, result)
    return result
```

### Phase 2: Simple Android App (Week 2)

#### 2.1 Minimal Setup
```bash
# Create React Native app
npx react-native init PokerCoachAI --template react-native-template-typescript
cd PokerCoachAI

# Install minimal dependencies
npm install axios @react-native-async-storage/async-storage
npm install @react-navigation/native @react-navigation/stack
```

#### 2.2 API Service
```typescript
// mobile/src/api/AICoachAPI.ts
class AICoachAPI {
  private baseURL = 'http://your-server:8000/api';
  
  async generateScenario(params: ScenarioParams): Promise<Scenario> {
    const context = await PlayerContext.get();
    const response = await axios.post(`${this.baseURL}/ai/scenario`, {
      ...params,
      player_id: context.id,
      focus_area: context.topWeakness
    });
    return response.data;
  }
  
  async evaluateDecision(
    scenarioId: string, 
    action: PlayerAction
  ): Promise<Evaluation> {
    const response = await axios.post(`${this.baseURL}/ai/evaluate`, {
      scenario_id: scenarioId,
      action: action,
      player_id: await PlayerContext.getId()
    });
    
    // Update local weakness tracking
    await PlayerContext.updateWeaknesses(response.data);
    
    return response.data;
  }
}
```

#### 2.3 Core Screens
```typescript
// mobile/src/screens/ScenarioScreen.tsx
const ScenarioScreen = () => {
  const [scenario, setScenario] = useState<Scenario | null>(null);
  
  useEffect(() => {
    loadNewScenario();
  }, []);
  
  const loadNewScenario = async () => {
    const scenario = await api.generateScenario({
      gameType: 'MTT',
      tournamentStage: 'middle',
      stackDepth: 40
    });
    setScenario(scenario);
  };
  
  const handleAction = async (action: string) => {
    const evaluation = await api.evaluateDecision(
      scenario.id,
      action
    );
    
    navigation.navigate('Feedback', { 
      evaluation, 
      scenario 
    });
  };
  
  return (
    <View>
      <PokerTable scenario={scenario} />
      <ActionButtons onAction={handleAction} />
    </View>
  );
};
```

### Phase 3: Player Context & Progress Tracking

#### 3.1 Local Context Management
```typescript
// mobile/src/storage/PlayerContext.ts
interface PlayerContext {
  id: string;
  skillLevel: 'beginner' | 'intermediate' | 'advanced';
  
  weaknesses: {
    preflop: {
      threeBetTooTight: number;      // 0-100 severity
      overlimpingStrong: number;
      notStealingEnough: number;
      defendingBBPoorly: number;
    };
    postflop: {
      cBetTooMuch: number;
      overfolding: number;
      missedValueBets: number;
      bluffingIncorrectly: number;
    };
    tournament: {
      bubbleFactorIgnored: number;
      ladderingTooMuch: number;
      notAdjustingToStacks: number;
    };
  };
  
  stats: {
    scenariosPlayed: number;
    correctDecisions: number;
    evGained: number;
    sessionsCount: number;
    lastPlayed: Date;
  };
  
  focusAreas: string[];  // AI-determined priorities
}

class PlayerContextManager {
  static async updateWeaknesses(evaluation: Evaluation) {
    const context = await this.get();
    
    // Decay all weaknesses slightly
    Object.keys(context.weaknesses).forEach(category => {
      Object.keys(context.weaknesses[category]).forEach(leak => {
        context.weaknesses[category][leak] *= 0.98;
      });
    });
    
    // Reinforce identified leak
    if (evaluation.leak_type) {
      const [category, leak] = evaluation.leak_type.split('.');
      context.weaknesses[category][leak] = Math.min(
        100,
        context.weaknesses[category][leak] + evaluation.severity * 2
      );
    }
    
    await this.save(context);
  }
}
```

## 🔌 API Specification

### Endpoints

#### 1. Generate Scenario
```http
POST /api/ai/scenario
Content-Type: application/json

{
  "game_type": "MTT",
  "tournament_stage": "early|middle|bubble|itm|final_table",
  "stack_depth": 25,
  "player_id": "user123",
  "difficulty": "beginner|intermediate|advanced"
}

Response:
{
  "id": "scenario_abc123",
  "hero_position": "BTN",
  "hero_cards": ["As", "Kh"],
  "board": ["Qd", "Js", "3c"],
  "pot_size": 450,
  "action_required": true,
  "valid_actions": ["fold", "call:250", "raise:600-2500"]
}
```

#### 2. Evaluate Decision
```http
POST /api/ai/evaluate
Content-Type: application/json

{
  "scenario_id": "scenario_abc123",
  "action": "raise:750",
  "player_id": "user123",
  "time_taken": 15.3
}

Response:
{
  "correct": false,
  "optimal_action": "call",
  "ev_difference": -2.45,
  "leak_identified": "preflop.threeBetTooTight",
  "explanation": "Calling is better here because...",
  "coaching_tip": "Consider villain's 3bet range...",
  "improvement_areas": ["3bet defense", "pot odds calculation"]
}
```

#### 3. Get Progress Report
```http
GET /api/ai/progress/{player_id}

Response:
{
  "overall_skill": 65,
  "improvement_rate": 2.3,
  "biggest_leaks": [
    {"type": "preflop.threeBetTooTight", "severity": 78},
    {"type": "postflop.overfolding", "severity": 65}
  ],
  "recommended_focus": "3bet defense ranges",
  "stats": {
    "total_hands": 534,
    "win_rate": 3.2,
    "accuracy_trend": [0.45, 0.48, 0.52, 0.58]
  }
}
```

#### 4. Get Coaching Plan
```http
GET /api/ai/coaching-plan/{player_id}

Response:
{
  "current_focus": "3bet defense from BB",
  "exercises": [
    {
      "type": "scenario_set",
      "description": "BB vs BTN 3bet spots",
      "target_hands": 20
    }
  ],
  "concepts_to_study": [
    "Linear vs polarized 3bet ranges",
    "Stack depth adjustments"
  ],
  "estimated_sessions": 5
}
```

## 🚦 Quick Start Guide

### Backend Setup
```bash
# Clone and setup
git clone <repo>
cd poker-coach-ai/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn openai python-dotenv

# Set environment variables
echo "OPENAI_API_KEY=your-key-here" > .env

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Mobile App Setup
```bash
# Setup React Native app
cd mobile
npm install

# For Android development
npx react-native run-android

# For development with hot reload
npx react-native start
```

### Test the AI Coach
```bash
# Test scenario generation
curl -X POST http://localhost:8000/api/ai/scenario \
  -H "Content-Type: application/json" \
  -d '{
    "game_type": "MTT",
    "tournament_stage": "middle",
    "stack_depth": 30,
    "player_id": "test_user"
  }'
```

## 📊 Tournament-Specific Features

### MTT Stages
```typescript
enum TournamentStage {
  EARLY = "early",        // Deep stacks, low pressure
  MIDDLE = "middle",      // Antes kick in, stealing important  
  BUBBLE = "bubble",      // Maximum ICM pressure
  ITM = "itm",           // In the money, ladder considerations
  FINAL_TABLE = "ft"     // Final table dynamics
}
```

### Stack Depth Considerations
```typescript
interface StackDepthParams {
  deep: ">50BB",         // Complex postflop play
  medium: "20-50BB",     // Standard tournament play
  short: "10-20BB",      // Push/fold considerations
  micro: "<10BB"         // Pure push/fold
}
```

### ICM Awareness
The AI considers ICM (Independent Chip Model) pressure in bubble and final table situations, adjusting optimal play accordingly.

## 🎯 Weakness Tracking System

### Categories of Leaks

**Preflop Leaks:**
- Opening too wide/tight
- 3betting incorrectly  
- Poor blind defense
- Limping strong hands
- Not stealing enough

**Postflop Leaks:**
- C-betting too frequently
- Missing value bets
- Overfolding to aggression
- Poor bet sizing
- Bluffing wrong spots

**Tournament Specific:**
- Ignoring ICM pressure
- Not adjusting to stack depths
- Poor push/fold decisions
- Laddering too much
- Bubble play errors

## 🔄 Development Workflow

1. **Start with API**: Get the AI generating good scenarios via Postman
2. **Basic App Shell**: Create minimal 3-screen app
3. **Iterate on Prompts**: Refine AI responses based on testing
4. **Add Progress Tracking**: Implement weakness detection
5. **Polish UI**: Improve user experience

## 🚀 Future Enhancements

### Phase 2: Advanced Features
- **Hand Range Visualization**: Show optimal ranges
- **Session Review**: AI analyzes full sessions
- **Opponent Modeling**: Adjust to different player types
- **Multi-way Scenarios**: 3+ player situations

### Phase 3: PLO Support
- Modified prompt templates for PLO
- 4-card hand evaluation
- PLO-specific leaks (not folding trash, overvaluing weak draws)
- Different position dynamics

### Phase 4: Advanced AI Features
- **Voice Coaching**: Real-time audio feedback
- **Live Session Mode**: AI coaches during real play
- **Peer Comparison**: Compare progress with similar players
- **Custom Scenarios**: User-requested situations

## 📈 Success Metrics

Track improvement through:
- EV gained per session
- Leak severity reduction over time
- Decision speed improvement
- Accuracy in different spots
- Overall win rate correlation

## 🤝 Contributing

This is a personal project, but contributions are welcome:
1. Improve prompt engineering
2. Add new leak categories
3. Enhance UI/UX
4. Add more tournament formats

## 📝 License

MIT License - See LICENSE file for details

## 🛠️ Troubleshooting

### Common Issues

**LLM Response Quality**
- Adjust temperature settings
- Improve prompt specificity
- Add more examples to prompts

**Performance**
- Cache common scenarios
- Implement request queuing
- Use faster LLM models for simple evaluations

**Android Development**
- Enable developer mode on device
- Check ADB connection
- Verify Metro bundler is running

---

**Status**: 🚧 In Development  
**Focus**: MTT No-Limit Hold'em (PLO coming later)  
**Platform**: Android (via React Native) 