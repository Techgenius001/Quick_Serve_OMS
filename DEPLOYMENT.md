# Deployment Guide for Render

## Prerequisites

- GitHub account with your code pushed
- Render account (sign up at https://render.com)
- Gmail account for sending emails (optional but recommended)

## Step 1: Prepare Email Settings (Optional)

If you want email notifications to work:

1. Go to your Gmail account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → 2-Step Verification → App passwords
   - Create a new app password for "Mail"
   - Save this password for later

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. Go to https://render.com/dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to create all services

### Option B: Manual Setup

1. **Create PostgreSQL Database:**

   - Click "New +" → "PostgreSQL"
   - Name: `smartkibandaski-db`
   - Choose free tier
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create Web Service:**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `smartkibandaski`
     - Environment: `Python 3`
     - Build Command: `./build.sh`
     - Start Command: `gunicorn smartkibadaski.wsgi:application`
     - Instance Type: Free

3. **Add Environment Variables:**

   - `RENDER` = `true`
   - `SECRET_KEY` = (click "Generate" for a secure key)
   - `DATABASE_URL` = (paste the Internal Database URL from step 1)
   - `ADMIN_EMAIL` = `samuelnjhihia333@gmail.com`
   - `EMAIL_HOST_USER` = `hotel@smartkibandaski.com` (or your Gmail)
   - `EMAIL_HOST_PASSWORD` = (your Gmail app password from Step 1)

4. Click "Create Web Service"

## Step 3: Post-Deployment

1. **Create Superuser:**

   - Go to your Render dashboard
   - Click on your web service
   - Go to "Shell" tab
   - Run: `python manage.py createsuperuser`
   - Follow the prompts

2. **Add Menu Categories and Items:**
   - Visit your site URL
   - Go to `/admin`
   - Login with superuser credentials
   - Add menu categories (Breakfast, Lunch, etc.)
   - Add menu items with images

## Step 4: Configure Custom Domain (Optional)

1. In Render dashboard, go to your web service
2. Click "Settings" → "Custom Domain"
3. Add your domain
4. Update your DNS records as instructed

## Important Notes

- **Free Tier Limitations:**

  - Service spins down after 15 minutes of inactivity
  - First request after spin-down takes 30-60 seconds
  - Database has 90-day expiration on free tier

- **Media Files:**

  - For production, consider using AWS S3 or Cloudinary for media storage
  - Current setup stores media files locally (will be lost on redeploy)

- **Email Settings:**
  - If you don't configure email, inquiries will still be saved to database
  - You can view them in the admin dashboard

## Troubleshooting

### Build Fails

- Check that `build.sh` has execute permissions
- Verify all dependencies in `requirements.txt` are correct

### Database Connection Issues

- Ensure `DATABASE_URL` environment variable is set correctly
- Check that database is in the same region as web service

### Static Files Not Loading

- Run `python manage.py collectstatic` manually in Shell
- Check that `STATIC_ROOT` is configured correctly

### Email Not Sending

- Verify Gmail app password is correct
- Check that 2FA is enabled on Gmail account
- Ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set

## Support

For issues, check:

- Render logs in dashboard
- Django error messages
- Contact: samuelnjhihia333@gmail.com
