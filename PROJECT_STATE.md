# Project State

## Overview

This project is a Vue 3 + Vite frontend for a cacao drying monitoring system with two protected experiences:

- `Admin Mode` for user, device, session, alert, and settings management
- `User Mode` for monitoring sensor readings, device status, history, analytics, and alerts

The app currently uses local browser storage for authentication/session state and for several temporary admin and test datasets, while ThingSpeak provides the live sensor feed and historical readings.

## Current Stack

- Vue 3
- Vite
- TypeScript in Vue single-file components
- Browser `fetch` for ThingSpeak API requests
- Local storage for auth, fallback data, and temporary admin datasets

## Current Access Model

### Public Area

Unauthenticated visitors can only access:

- Login
- Register

Protected dashboards stay hidden until login succeeds.

### Role-Based Protected Area

After login, the app checks the stored user role:

- `Admin` users are routed to the admin dashboard
- `Viewer` and `Manager` users are routed to the user dashboard

This logic is handled in [src/App.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/App.vue).

### Default Admin Account

The app seeds a default local admin account if no admin exists in `localStorage.users`:

- Email: `admin@cacaomonitor.local`
- Password: `admin123`
- Role: `Admin`

Newly registered accounts default to:

- Role: `Viewer`
- Status: `Active`

## App Shells

### Shared Root Shell

- [src/App.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/App.vue)
  - handles auth gating
  - stores active session in `authUser`
  - seeds a default admin account if needed
  - switches between public auth UI, admin UI, and user UI

### Admin Workspace

- [src/views/AdminDashboard.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/AdminDashboard.vue)
  - sidebar-based admin layout
  - navigation sections:
    - Users
    - Devices
    - Drying Sessions
    - Alerts
    - Settings

### User Workspace

- [src/views/UserDashboard.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/UserDashboard.vue)
  - sidebar-based user layout
  - navigation sections:
    - Dashboard
    - History
    - Analytics
    - Device Info
    - Alerts

## ThingSpeak Integration

ThingSpeak configuration lives in:

- [.env](/c:/Users/238fr/OneDrive/Desktop/PROJECT/.env)
- [src/services/thingspeak.ts](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/services/thingspeak.ts)

Current environment values:

- `VITE_THINGSPEAK_READ_API_KEY`
- `VITE_THINGSPEAK_CHANNEL_ID=2770965`

### Current Field Mapping

Based on the live channel response:

- `field1` -> `temperature`
- `field4` -> `moisture`
- `field2` and `field3` -> averaged into `ambientTemp`

### Available Service Functions

The frontend service currently exposes:

- `fetchLatestSensorSnapshot()`
- `fetchHistoricalSensorReadings(limit)`
- `fetchAllHistoricalSensorReadings(daysBack = 365)`
- `toChartSeries(readings)`

## User-Facing Views

### Auth

- [src/views/Login.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/Login.vue)
  - responsive login form
  - validates against locally stored users
  - emits `fullName`, `email`, and `role` on success

- [src/views/Register.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/Register.vue)
  - registration form with validation
  - saves new users to local storage
  - assigns new users `Viewer` role and `Active` status by default

### User Monitoring Views

- [src/views/DashboardModern.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/DashboardModern.vue)
  - displays latest ThingSpeak reading
  - shows temperature, moisture, and ambient temperature
  - falls back to `localStorage.sensorData`

- [src/views/History.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/History.vue)
  - shows full ThingSpeak history sorted newest first
  - includes date-range filter
  - includes CSV export
  - falls back to `localStorage.sensorHistory`

- [src/views/Analytics.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/Analytics.vue)
  - converts ThingSpeak history into chart-ready series
  - displays placeholder visual trend charts
  - reserves space for future Chart.js or ApexCharts integration

- [src/views/DeviceInfo.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/DeviceInfo.vue)
  - shows device ID, status, and last seen
  - reads from `localStorage.deviceInfo`

- [src/views/Alerts.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/Alerts.vue)
  - color-coded user alert cards
  - reads from `localStorage.alerts`

- [src/views/AddDevice.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/views/AddDevice.vue)
  - still exists as a standalone device registration screen
  - currently not exposed in the user sidebar after the role split

## Admin Components

### Users Management

- [src/components/AdminUsersManagement.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/components/AdminUsersManagement.vue)
  - table and mobile cards
  - columns:
    - Name
    - Email
    - Phone
    - Role
    - Status
    - Actions
  - supports search, role filter, and status filter
  - supports inline edit and delete

### Devices Management

- [src/components/AdminDevicesManagement.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/components/AdminDevicesManagement.vue)
  - table and mobile cards
  - columns:
    - Device Name
    - Serial
    - Owner
    - Status
    - Last Seen
    - Actions
  - supports search, filter, and sort
  - includes actions:
    - Reboot
    - Claim
    - Edit
    - Remove

### Drying Sessions Overview

- [src/components/AdminDryingSessionsOverview.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/components/AdminDryingSessionsOverview.vue)
  - shows drying session summary cards
  - supports filters:
    - All
    - Active
    - Completed
    - Alerts
  - columns:
    - Batch Name
    - Device
    - User
    - Start Date
    - End Date
    - Current Moisture
    - Status
  - includes moisture progress bars
  - uses `localStorage.dryingSessions`

### Alerts Panel

- [src/components/AdminAlertsPanel.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/components/AdminAlertsPanel.vue)
  - table and mobile cards
  - columns:
    - Device
    - Type
    - Severity
    - Message
    - Timestamp
    - Resolved
    - Actions
  - supports severity filtering
  - supports checkbox toggle and `Mark Resolved` action
  - uses `localStorage.alerts`

### Settings Panel

- [src/components/AdminSettingsPanel.vue](/c:/Users/238fr/OneDrive/Desktop/PROJECT/src/components/AdminSettingsPanel.vue)
  - grouped settings form with local persistence
  - sections:
    - System Settings
    - Device Config Defaults
    - User Roles
  - includes text fields, dropdowns, toggles, and save action
  - uses `localStorage.adminSettings`

## Local Storage Keys In Use

- `authUser`
- `users`
- `sensorData`
- `sensorHistory`
- `analyticsData`
- `deviceInfo`
- `devices`
- `alerts`
- `dryingSessions`
- `adminSettings`

## Current Behavior Notes

- Login and registration are local-only; there is no backend authentication yet
- The admin and user dashboards share the same app URL; role determines the destination after login
- ThingSpeak powers the live dashboard, history, and analytics data paths
- Admin datasets such as users, devices, sessions, alerts, and settings are still local-storage-based for testing
- Some legacy standalone views still exist even when not currently linked from the latest dashboard navigation

## Verification Status

The current project state has been validated through:

- successful `npm run build`
- successful live ThingSpeak requests for channel `2770965`
- recent verification of the role-based split between admin and user workspaces
- cleanup of previous icon/config/encoding issues in active screens

## Known Limitations

- No automated test suite exists yet
- Browser interaction and responsive checks are still manual
- Auth is not backend-backed and is not secure for production use
- Role enforcement is frontend-only
- Analytics still uses placeholder visual charts instead of a chart library
- Admin data is still temporary local test data
- Some text encoding artifacts like `Â°C` still remain in a few view files and should be cleaned up

## Recommended Next Steps

1. Add a dedicated admin login flow or clearer role-targeted auth UI.
2. Replace placeholder analytics visuals with Chart.js or ApexCharts.
3. Add loading and error states to ThingSpeak-powered screens.
4. Move auth and role enforcement to a real backend if production use is planned.
5. Add automated tests for auth routing, ThingSpeak data formatting, and admin component behavior.
6. Clean remaining `Â°C` encoding artifacts from active views.
7. Consider moving repeated design tokens into shared CSS variables or a global stylesheet.

## Run Commands

- Development: `npm run dev`
- Production build: `npm run build`
- Preview build: `npm run preview`
