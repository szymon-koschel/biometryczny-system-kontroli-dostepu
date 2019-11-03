# zsw
web intercom

## how to spawn?
uasge: `zsw.py [-h] [--lockfile LOCKFILE] index`

### what's the index?
index is a csv file with authorized users names and their faces, e.g.:
```
Kamil Janiec,./images/janiec.jpg
John Doe,./image/doe.jpg
```

## how does it work?
An app opens a door when some authorized user is recognized in the webcam.

### internals
1. App is looking via webcam.
2. App is creating `lockfile` if someone is recognized.
3. App blocks its execution while `lockfile` exist.
4. App resumes its execution when `lockfile` is removed.

As a conclusion:
- `lockfile` exists == door is open.
- `lockfile` doesn't exist == door is locked.
