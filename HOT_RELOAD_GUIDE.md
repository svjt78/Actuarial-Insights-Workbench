# Hot Reload Development Guide

## 🔥 Hot Reload is Now Enabled!

Your development environment is configured for **instant hot reload**. Code changes will automatically reflect without rebuilding containers!

---

## ✅ What Was Configured

### Backend (FastAPI + Uvicorn)
- ✅ Source code mounted as volume (`./backend:/app`)
- ✅ `--reload` flag enabled
- ✅ `--reload-delay 2` for stability
- ✅ `PYTHONUNBUFFERED=1` for immediate logs
- ✅ Auto-restart on `.py` file changes

### Frontend (Streamlit)
- ✅ Source code mounted as volume (`./frontend:/app`)
- ✅ `--server.fileWatcherType=poll` for cross-platform compatibility
- ✅ `--server.runOnSave=true` for automatic reruns
- ✅ Auto-reload on `.py` file changes

### Additional Mounts
- ✅ `./scripts:/scripts` - Easy access to training scripts
- ✅ `./data:/app/data` - Shared data folder
- ✅ `./backend/models:/app/models` - Shared models

---

## 🚀 How to Use

### First Time Setup

```bash
# 1. Build containers (only needed once)
docker-compose up --build

# Wait for both services to start
# Backend: http://localhost:8003
# Frontend: http://localhost:8502
```

### Daily Development Workflow

```bash
# Just start the containers (no rebuild needed!)
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

### Making Code Changes

**Backend Changes:**
1. Edit any `.py` file in `backend/` folder
2. Save the file
3. Watch terminal - you'll see:
   ```
   INFO:     Detected changes in 'main.py'
   INFO:     Reloading...
   INFO:     Application startup complete
   ```
4. API immediately reflects changes (typically <2 seconds)

**Frontend Changes:**
1. Edit any `.py` file in `frontend/` folder
2. Save the file
3. Streamlit automatically detects changes
4. Browser shows "Source file changed" banner
5. Click "Rerun" or wait for auto-rerun
6. UI updates instantly

---

## 📝 Examples

### Example 1: Update API Endpoint

```python
# Edit: backend/main.py
@app.get("/test")
async def test_endpoint():
    return {"message": "Hello from hot reload!"}  # <- Change this

# Save file
# Check http://localhost:8003/test immediately - no restart needed!
```

### Example 2: Update Frontend UI

```python
# Edit: frontend/app.py
st.title("My Updated Title")  # <- Change this

# Save file
# Browser shows "Source file changed"
# Click "Rerun" or wait for auto-rerun
```

### Example 3: Update Service Logic

```python
# Edit: backend/services/prediction.py
def predict_loss_ratio(self, input_data: Dict) -> Dict:
    # Add new logic here
    prediction = self.lr_model.predict(features_df)[0]
    # Changes apply immediately on next API call
```

---

## ⚡ Performance Tips

### Faster Reload Times

1. **Keep containers running** - Don't stop/start unnecessarily
2. **Edit one file at a time** - Reduces reload cycles
3. **Use backend API directly** - Test at http://localhost:8003/docs
4. **Monitor logs** - Watch reload status

### Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View only backend
docker-compose logs -f backend

# View only frontend
docker-compose logs -f frontend

# View last 50 lines
docker-compose logs --tail=50
```

---

## 🔧 Advanced Configuration

### Customize Reload Behavior

**Backend - Increase reload delay:**
```yaml
# docker-compose.yml
command: uvicorn main:app --host 0.0.0.0 --port 8003 --reload --reload-delay 5
```

**Frontend - Disable auto-rerun:**
```yaml
# docker-compose.yml
command: streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.fileWatcherType=poll
# Remove: --server.runOnSave=true
```

### Exclude Files from Reload

Create `.dockerignore` in backend/ or frontend/:
```
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.coverage
*.log
```

---

## 🐛 Troubleshooting

### Issue: Changes not reflecting

**Solution:**
```bash
# 1. Check if containers are running
docker ps

# 2. Verify volume mounts
docker inspect aiw-backend | grep Mounts -A 20

# 3. Restart containers
docker-compose restart

# 4. Check logs for errors
docker-compose logs -f backend
```

### Issue: "File watcher limit" error

**Solution (Linux/Mac):**
```bash
# Increase file watcher limit
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Issue: Slow reload times

**Solution:**
```bash
# 1. Reduce reload delay
# Edit docker-compose.yml: --reload-delay 1

# 2. Ensure no antivirus scanning Docker volumes

# 3. Use Docker Desktop with virtualization enabled
```

### Issue: Module not found after changes

**Solution:**
```bash
# Rebuild containers (dependencies may have changed)
docker-compose down
docker-compose up --build
```

---

## 📊 What Triggers Reload

### Backend (FastAPI)
- ✅ `.py` file changes in `backend/`
- ✅ `.py` file changes in `backend/services/`
- ❌ Data files (`.csv`, `.pkl`)
- ❌ Requirements changes (need rebuild)

### Frontend (Streamlit)
- ✅ `.py` file changes in `frontend/`
- ✅ `.py` file changes in `frontend/pages/`
- ✅ Config file changes (`.streamlit/config.toml`)
- ❌ Requirements changes (need rebuild)

---

## 🔄 When to Rebuild

You **don't need to rebuild** for code changes, but **do rebuild** when:

1. ❗ Adding new dependencies to `requirements.txt`
2. ❗ Changing Dockerfile
3. ❗ Changing system dependencies
4. ❗ Major Python package updates

```bash
# Rebuild command
docker-compose down
docker-compose up --build
```

---

## 💡 Pro Tips

### 1. Use API Docs for Backend Testing
- Visit http://localhost:8003/docs
- Test endpoints directly
- Faster than testing through frontend

### 2. Keep Terminal Open
- Watch reload messages
- Catch errors immediately
- See performance metrics

### 3. Use Multiple Terminals
```bash
# Terminal 1: Backend logs
docker-compose logs -f backend

# Terminal 2: Frontend logs
docker-compose logs -f frontend

# Terminal 3: Development work
# Your editor/IDE
```

### 4. Quick Restart
```bash
# If something seems stuck
docker-compose restart backend
docker-compose restart frontend
```

---

## 📈 Productivity Gains

**Before Hot Reload:**
- Edit code → Stop containers → Rebuild → Start → Test
- Time per change: ~2-5 minutes
- Iterations per hour: ~12-30

**After Hot Reload:**
- Edit code → Save → Auto-reload → Test
- Time per change: ~2-5 seconds
- Iterations per hour: ~720-1800

**Result: 60x faster development cycle!** 🚀

---

## ✅ Quick Reference

| Action | Command |
|--------|---------|
| Start dev environment | `docker-compose up` |
| Start in background | `docker-compose up -d` |
| View logs | `docker-compose logs -f` |
| Restart service | `docker-compose restart backend` |
| Stop all | `docker-compose down` |
| Rebuild | `docker-compose up --build` |
| Enter backend shell | `docker exec -it aiw-backend bash` |
| Enter frontend shell | `docker exec -it aiw-frontend bash` |

---

**Happy coding with instant feedback! 🎉**
