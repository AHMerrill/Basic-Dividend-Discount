# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying the Dividend Discount Model Calculator to various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- Python 3.8+ installed
- Git installed
- All files committed to a Git repository

## 🌐 Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy Streamlit apps with zero configuration.

### Steps:
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Dividend Discount Model Calculator"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Click "Deploy"

3. **Your app will be live** at `https://your-app-name.streamlit.app`

## 🐳 Docker Deployment

### Local Docker
```bash
# Build the image
docker build -t ddm-calculator .

# Run the container
docker run -p 8501:8501 ddm-calculator
```

### Docker Hub
```bash
# Tag your image
docker tag ddm-calculator your-username/ddm-calculator

# Push to Docker Hub
docker push your-username/ddm-calculator
```

### Docker Compose
Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  ddm-calculator:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## ☁️ Heroku Deployment

### Method 1: Heroku CLI
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# Open the app
heroku open
```

### Method 2: GitHub Integration
1. Connect your GitHub repository to Heroku
2. Enable automatic deploys
3. Deploy from the main branch

## 🐙 GitHub Pages (Static Alternative)

For a static version, you can create a simple HTML interface:

1. Create a `static` folder with HTML/CSS/JS
2. Use GitHub Pages to serve static files
3. Note: This won't have the interactive Streamlit features

## 🔧 Environment Variables

Set these environment variables if needed:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

## 📊 Monitoring & Analytics

### Streamlit Cloud
- Built-in analytics dashboard
- Usage statistics
- Performance monitoring

### Custom Monitoring
Add to your app:
```python
import streamlit as st

# Add analytics
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

## 🔒 Security Considerations

1. **API Rate Limits**: Yahoo Finance has rate limits
2. **Input Validation**: All user inputs are validated
3. **Error Handling**: Graceful fallbacks for API failures
4. **HTTPS**: Use HTTPS in production

## 🚨 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **API Failures**
   - Check internet connection
   - Verify ticker symbols
   - Check Yahoo Finance API status

4. **Memory Issues**
   - Reduce data fetch periods
   - Optimize calculations
   - Use caching

### Debug Mode
```bash
streamlit run app.py --logger.level debug
```

## 📈 Performance Optimization

1. **Caching**: Use `@st.cache_data` for expensive operations
2. **Lazy Loading**: Load data only when needed
3. **Error Boundaries**: Handle failures gracefully
4. **Resource Limits**: Monitor memory and CPU usage

## 🔄 Continuous Deployment

### GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Streamlit Cloud
      run: |
        # Your deployment commands here
```

## 📞 Support

For deployment issues:
1. Check the [Streamlit documentation](https://docs.streamlit.io)
2. Review platform-specific guides
3. Open an issue on GitHub
4. Contact the maintainers

---

**Note**: The easiest deployment option is Streamlit Cloud, which requires minimal setup and provides excellent performance and monitoring capabilities. 