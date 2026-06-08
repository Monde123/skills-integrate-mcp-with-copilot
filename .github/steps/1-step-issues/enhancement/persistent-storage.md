# Persistent storage

The app currently stores all activities and signups in memory. As soon as the server restarts, everything is lost.

## Recommended Solution

- Move activity and signup data into a persistent store.
- Start with a JSON file such as `activities.json` and `students.json`.
- Later this can be upgraded to a real database if needed.

## Context

This will make the app usable beyond a single restart and let teachers change activity settings without modifying the Python source.
