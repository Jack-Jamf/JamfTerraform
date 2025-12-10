# Bug Reproduction Steps

## Reported Issue

User reported that `localhost:5174` was not loading and is still not loading.

## Steps to Reproduce

1. Navigate to the frontend directory: `/Users/Shared/Tools/JamfTerraform/frontend`
2. Run the development server: `npm run dev`
3. Observe the output shows: `Local: http://localhost:5173/`
4. Attempt to access `localhost:5174` in browser
5. **Result**: Page does not load (connection refused or cannot connect)

## Expected Behavior

The application should be accessible at the URL displayed by the Vite dev server.

## Actual Behavior

- The dev server runs on port **5173** (default Vite port)
- User is attempting to access port **5174**
- No process is listening on port 5174, causing the connection failure

## Environment

- **Tool**: Vite v7.2.6
- **Framework**: React
- **Port**: 5173 (default)
- **Configuration**: `vite.config.ts` has no custom port specified
