# JamfTerraform Frontend

Modern React + TypeScript frontend for the JamfTerraform application. Features a premium dark theme with tabbed navigation and real-time chat interface for HCL generation.

## Features

### ✨ Implemented

- **🎨 Premium Dark Theme**: Modern design system with custom color palette and smooth animations
- **📑 Tabbed Navigation**: Switch between Chat, Local Execution, and Cloud Execution
- **💬 Chat Interface**: Real-time conversation with AI for HCL generation
- **🔌 Backend Integration**: Centralized ExecutionService for API calls
- **📊 Health Monitoring**: Real-time backend connection status
- **⚡ Smooth Animations**: Message slide-ins, loading indicators, and transitions

### 🚧 Coming Soon

- **🖥️ Local Execution**: Execute Terraform via Tauri agent
- **☁️ Cloud Execution**: Managed cloud execution environment

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **CSS Custom Properties** - Design system
- **Google Fonts** - Inter (UI) & JetBrains Mono (code)

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── TabBar.tsx       # Tab navigation
│   │   ├── Chat.tsx         # Chat interface
│   │   ├── LocalExecution.tsx
│   │   └── CloudExecution.tsx
│   ├── services/
│   │   └── ExecutionService.ts  # API integration
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   ├── App.tsx              # Main app component
│   └── index.css            # Design system
├── package.json
└── vite.config.ts
```

## Getting Started

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Start dev server**:

   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## Design System

### Color Palette

- **Background**: Deep dark blues (#0a0a0f, #13131a)
- **Surface**: Elevated surfaces (#252535, #2d2d40)
- **Accent**: Vibrant purple gradient (#6366f1 → #7c3aed)
- **Text**: High contrast whites with opacity variants

### Typography

- **UI Font**: Inter (300-700 weights)
- **Code Font**: JetBrains Mono (400-600 weights)

### Spacing Scale

- XS: 0.25rem
- SM: 0.5rem
- MD: 1rem
- LG: 1.5rem
- XL: 2rem
- 2XL: 3rem

## Components

### TabBar

Horizontal tab navigation with active state indicators and smooth transitions.

### Chat

Full-featured chat interface with:

- Message history display
- User/assistant avatars
- Timestamp formatting
- Loading indicators
- Auto-scroll to latest message
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

### ExecutionService

Centralized service for all backend API calls:

- `generateHCL(request)` - Generate Terraform HCL
- `healthCheck()` - Check backend status

## API Integration

The frontend connects to the backend at `http://localhost:8000`:

- `POST /generate` - Generate HCL from prompt
- `GET /healthz` - Backend health check

## Development

### Hot Module Replacement

Vite provides instant HMR for rapid development.

### Type Safety

Full TypeScript coverage with strict mode enabled.

### Code Style

- ESLint configured for React best practices
- Functional components with hooks
- CSS modules for component styling

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Performance

- Lazy loading for optimal bundle size
- CSS animations using GPU acceleration
- Optimized re-renders with React hooks
