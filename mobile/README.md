# Mobile App - AI Agency OS

React Native app for AI Agency OS - manage agency on the go.

## Structure

```
mobile/
├── src/
│   ├── screens/
│   │   ├── DashboardScreen.tsx - Analytics, tasks, cost
│   │   ├── ChatScreen.tsx - Chat with agents
│   │   ├── AgentsScreen.tsx - 68 agents list, run
│   │   ├── ProjectsScreen.tsx - Projects, clients, tasks
│   │   ├── ClientPortalScreen.tsx - Client view
│   │   └── SettingsScreen.tsx - Auth, billing, team
│   ├── components/
│   │   ├── AgentCard.tsx
│   │   ├── TaskCard.tsx
│   │   ├── RealtimeListener.tsx - WebSocket
│   │   └── CostChart.tsx
│   ├── lib/
│   │   ├── api.ts - Same as web SDK
│   │   └── websocket.ts - Realtime
│   └── App.tsx
├── package.json
└── README.md
```

## Setup

```bash
npx react-native init AIAgencyOS --template react-native-template-typescript
cd AIAgencyOS
npm install axios @react-navigation/native @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context

# Copy src from this folder
```

## Features

- Dashboard with cost, revenue, tasks (Recharts native)
- Chat with 68 agents
- Run agent from mobile
- Projects + tasks + client portal
- Realtime via WebSocket - push notifications for task completed
- Offline cache for projects
- Biometric auth (Face ID)

## PWA Alternative (Current)

We already have PWA - installable on mobile via browser:

- `manifest.json` + `sw.js` in `frontend/public/`
- Works offline partially
- Push notifications for task updates
- Add to home screen - looks like native app

To test PWA:
1. Open https://5173-...e2b.app on mobile
2. Add to Home Screen
3. Open as app - standalone display

## Future: Full React Native

Full RN app would use same backend APIs:

```ts
// Same SDK as web
import { AIAgencyClient } from '../sdk/typescript'
const client = new AIAgencyClient({ baseUrl: 'https://api.ai-agency.os' })

// In DashboardScreen
const [stats, setStats] = useState(null)
useEffect(() => {
  client.listProjects().then(setStats)
}, [])

// Realtime
useEffect(() => {
  const ws = client.connectRealtime('general', userId, (data) => {
    if (data.type === 'task_update') {
      // Show push notification
      PushNotification.localNotification({ title: 'Task updated', message: data.task_id })
    }
  })
  return () => ws.close()
}, [])
```

## Cost

- PWA: $0 - already done
- React Native: ~1 week to build MVP with 6 screens
- Expo: easier, OTA updates

## Monetization

- Mobile app as Pro feature: $199 plan includes mobile
- White-label mobile: $499 - your branding, your App Store listing
