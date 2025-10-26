# Railway Deployment Guide

This guide will help you deploy the Agentic Data Analysis application to Railway.

## Prerequisites

1. A [Railway](https://railway.app/) account (sign up for free)
2. An OpenAI API key ([get one here](https://platform.openai.com/api-keys))
3. Git installed on your local machine

## Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   - If you haven't already, create a new repository on GitHub
   - Push this code to your repository:
     ```bash
     git add .
     git commit -m "Prepare for Railway deployment"
     git push origin main
     ```

2. **Create a new project on Railway**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select the `AgenticDataAnalysis` repository

3. **Configure Environment Variables**
   - Once the project is created, click on your service
   - Go to the "Variables" tab
   - Add the following environment variable:
     - `OPENAI_API_KEY`: Your OpenAI API key

4. **Deploy**
   - Railway will automatically detect the configuration and deploy your app
   - Wait for the deployment to complete (usually 2-5 minutes)
   - Once deployed, Railway will provide a public URL

### Option 2: Deploy from CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Railway project**
   ```bash
   cd AgenticDataAnalysis
   railway init
   ```

4. **Add environment variables**
   ```bash
   railway variables set OPENAI_API_KEY=your-api-key-here
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Generate domain**
   ```bash
   railway domain
   ```

## Configuration Files

The following files have been created for Railway deployment:

- **Procfile**: Defines the command to start the application
- **railway.toml**: Railway-specific configuration
- **.env.example**: Template for required environment variables
- **requirements.txt**: Python dependencies (already exists)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | Your OpenAI API key for AI functionality | Yes |

## Post-Deployment

After deployment, you can:

1. **Access your application**: Use the Railway-provided URL
2. **View logs**: Check the "Deployments" tab in Railway dashboard
3. **Monitor usage**: Track resource usage in Railway dashboard
4. **Update deployment**: Push changes to GitHub (auto-deploys) or run `railway up`

## Troubleshooting

### Build Fails
- Check that `requirements.txt` includes all dependencies
- Verify Python version compatibility (Railway uses Python 3.10+ by default)

### Application Won't Start
- Ensure `OPENAI_API_KEY` is set in Railway environment variables
- Check deployment logs in Railway dashboard for error messages

### Upload Size Issues
- The app is configured to handle files up to 2000 MB
- Railway's free tier has deployment size limits - check your plan

## Cost Considerations

- Railway offers a free tier with limited resources
- The application uses:
  - OpenAI API (charged separately by OpenAI)
  - Railway hosting (free tier available)
  - Bandwidth and storage (check Railway pricing)

## Support

- Railway Documentation: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- OpenAI API Documentation: https://platform.openai.com/docs

## Security Notes

- Never commit your `.env` file or API keys to Git
- The `.gitignore` file should include `.env`
- Always use environment variables for sensitive data
- Rotate your OpenAI API key if it's ever exposed
