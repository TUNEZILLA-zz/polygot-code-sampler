# Slack Notifications Setup Guide

## 🔔 **Configure Slack Webhook for Regression Alerts**

### **Step 1: Create Slack App**

1. **Go to Slack API**: Visit https://api.slack.com/apps
2. **Create New App**: Click "Create New App"
3. **Choose Method**: Select "From scratch"
4. **App Name**: `PCS Performance Monitor` (or your preferred name)
5. **Workspace**: Select your Slack workspace
6. **Create App**: Click "Create App"

### **Step 2: Enable Incoming Webhooks**

1. **Features**: In your app settings, click "Incoming Webhooks"
2. **Toggle On**: Switch "Activate Incoming Webhooks" to ON
3. **Add Webhook**: Click "Add New Webhook to Workspace"
4. **Choose Channel**: Select the channel for performance alerts (e.g., `#performance-alerts`)
5. **Authorize**: Click "Allow"
6. **Copy URL**: Copy the webhook URL (starts with `https://hooks.slack.com/services/...`)

### **Step 3: Add GitHub Secret**

1. **Repository**: Go to your GitHub repository
2. **Settings**: Click "Settings" tab
3. **Secrets**: Go to "Secrets and variables" → "Actions"
4. **New Secret**: Click "New repository secret"
5. **Name**: `SLACK_WEBHOOK_URL`
6. **Value**: Paste your webhook URL
7. **Add Secret**: Click "Add secret"

### **Step 4: Test Notifications**

#### **Option A: Safe Test (Recommended)**
```bash
# Trigger workflow with emergency override (safe)
gh workflow run publish-dashboard.yml -f ALLOW_REGRESSION=true
```

#### **Option B: Trigger Real Regression (Advanced)**
```bash
# Temporarily lower threshold to trigger regression
# Edit .github/workflows/publish-dashboard.yml
# Change: --per-backend-thresholds "+1%:rust"
# Commit and push to trigger workflow
```

### **Step 5: Verify Integration**

1. **Check Slack**: Look for notification in your chosen channel
2. **Check GitHub**: Verify workflow completed successfully
3. **Check Dashboard**: Ensure data is still fresh and healthy

## 📱 **Notification Format**

When a regression is detected, you'll receive a Slack message like:

```
🚨 PCS Performance Regression Alert
Commit: abc1234
Run: 123456789
Dashboard: https://tunezilla-zz.github.io/polyglot-code-sampler/
```

## 🔧 **Troubleshooting**

### **No Notifications Received**
- **Check Secret**: Verify `SLACK_WEBHOOK_URL` is set correctly
- **Check Webhook**: Test webhook URL manually with curl
- **Check Workflow**: Ensure regression check step is running
- **Check Logs**: Review GitHub Actions logs for errors

### **Test Webhook Manually**
```bash
# Replace YOUR_WEBHOOK_URL with your actual webhook URL
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test notification from PCS Performance Monitor"}' \
  YOUR_WEBHOOK_URL
```

### **Disable Notifications**
```bash
# Remove the secret to disable notifications
# Go to GitHub → Settings → Secrets → Delete SLACK_WEBHOOK_URL
```

## 🎯 **Best Practices**

### **Channel Setup**
- **Dedicated Channel**: Use `#performance-alerts` or similar
- **Team Access**: Add relevant team members
- **Notification Settings**: Configure channel notifications appropriately

### **Message Formatting**
- **Emojis**: Use 🚨 for critical alerts, ⚠️ for warnings
- **Links**: Include direct links to dashboard and failing runs
- **Context**: Include commit SHA and run ID for easy debugging

### **Frequency Control**
- **Thresholds**: Adjust per-backend thresholds to control alert frequency
- **Grace Period**: 3-day grace period prevents false alarms on new tests
- **K-Anomaly**: Detects infrastructure issues vs. real regressions

## 📊 **Monitoring Dashboard**

The Slack notifications complement the live dashboard at:
**https://tunezilla-zz.github.io/polyglot-code-sampler/**

- **Real-time Status**: Data health indicators
- **Interactive Charts**: Performance trends and comparisons
- **About & Methods**: Detailed documentation of thresholds and methods
