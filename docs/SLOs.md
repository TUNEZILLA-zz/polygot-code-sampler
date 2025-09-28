# Service Level Objectives (SLOs)
==================================

Pin what "good" looks like for the Code Live v0.5 Touring Rig system.

## 🎯 **Performance SLOs**

### **Frame Performance**
- **Frame p95 ≤ 10ms** (guard kicks at 12ms)
- **Frame p99 ≤ 15ms** (guard kicks at 18ms)
- **Frame p50 ≤ 8ms** (target: 6ms)
- **Frame budget**: 16.67ms (60 FPS)
- **Guard threshold**: 12ms (72% of budget)

### **Strobe Safety**
- **Strobe ≤ 8Hz** (hard limit)
- **On-time ≥ 120ms** (minimum safe duration)
- **Duty-cycle ≤ 35%** over 10s window
- **Auto-cap**: Strobe > 8Hz → auto-reduce to 8Hz
- **Safety margin**: 7.5Hz for production

### **A11y Compliance**
- **A11y fades 490±20ms** (target: 490ms, tolerance: ±20ms)
- **Motion-reduced mode**: Instant mono fallback
- **Strobe-capped ≤ 8Hz** in A11y mode
- **Hard mode**: Intensity cap 0.65, chromatic offset ≤ 0.15

### **Error Handling**
- **Error rate ≤ 1%** (target: 0.1%)
- **Metrics link easing**: in ≥ 300ms / out ≥ 200ms
- **Recovery time**: ≤ 2s for auto-recovery
- **Graceful degradation**: Mono fallback on error

## 🎛️ **Operator SLOs**

### **Response Time**
- **Hotkey response**: ≤ 100ms
- **Parameter changes**: ≤ 200ms
- **Scene transitions**: ≤ 500ms
- **Emergency stop**: ≤ 50ms

### **Reliability**
- **Uptime**: 99.9% (8.76 hours downtime/year)
- **Show continuity**: 99.99% (52 minutes downtime/year)
- **Data integrity**: 100% (no data loss)
- **Backup recovery**: ≤ 30s

### **Usability**
- **Learning curve**: ≤ 15 minutes for basic operation
- **Error recovery**: ≤ 30s for operator recovery
- **Documentation**: 100% coverage of critical functions
- **Training time**: ≤ 2 hours for full proficiency

## 🛡️ **Safety SLOs**

### **Motion Safety**
- **Motion watchdog**: ≤ 500ms response time
- **Reduced-motion compliance**: 100% (instant fallback)
- **Strobe safety**: 100% (auto-cap enforcement)
- **A11y compliance**: 100% (hard mode available)

### **System Safety**
- **Frame budget protection**: 100% (auto-reduce on breach)
- **Parameter slew limiting**: 100% (prevent overshoot)
- **Emergency stop**: ≤ 50ms (instant blackout)
- **Rollback capability**: ≤ 10s (instant rollback)

### **Venue Compliance**
- **Arena profile**: Strobe ≤ 6Hz, intensity ≤ 0.9, A11y hard mode
- **Club profile**: Strobe ≤ 7.5Hz, intensity ≤ 1.0, standard A11y
- **Theater profile**: Strobe ≤ 8Hz, intensity ≤ 0.8, A11y hard mode
- **Custom profiles**: 100% configurable per venue

## 📊 **Monitoring SLOs**

### **Observability**
- **Metrics collection**: 100% (all critical metrics)
- **Alerting**: ≤ 5s for critical alerts
- **Dashboard refresh**: ≤ 1s
- **Log retention**: 30 days minimum

### **Performance Monitoring**
- **Frame time tracking**: 100% (every frame)
- **Error rate tracking**: 100% (every request)
- **Resource usage**: 100% (CPU, memory, disk)
- **Network latency**: 100% (every API call)

### **Health Checks**
- **Liveness probe**: ≤ 1s response
- **Readiness probe**: ≤ 2s response
- **Health endpoint**: ≤ 500ms response
- **Status endpoint**: ≤ 200ms response

## 🎭 **Show SLOs**

### **Show Performance**
- **Show start time**: ≤ 5s
- **Scene transition**: ≤ 500ms
- **Parameter update**: ≤ 200ms
- **Show stop time**: ≤ 2s

### **Show Quality**
- **Visual quality**: 100% (no visual artifacts)
- **Audio sync**: ≤ 50ms (if applicable)
- **Smooth transitions**: 100% (no stuttering)
- **Consistent performance**: 100% (no frame drops)

### **Show Reliability**
- **Show continuity**: 99.99% (no unexpected stops)
- **Scene accuracy**: 100% (no scene drift)
- **Parameter accuracy**: 100% (no parameter drift)
- **Timing accuracy**: ≤ 10ms (precise timing)

## 🔧 **Operational SLOs**

### **Deployment**
- **Deployment time**: ≤ 5 minutes
- **Rollback time**: ≤ 2 minutes
- **Configuration time**: ≤ 1 minute
- **Testing time**: ≤ 10 minutes

### **Maintenance**
- **Update time**: ≤ 15 minutes
- **Backup time**: ≤ 5 minutes
- **Recovery time**: ≤ 10 minutes
- **Cleanup time**: ≤ 2 minutes

### **Support**
- **Response time**: ≤ 1 hour (business hours)
- **Resolution time**: ≤ 4 hours (critical issues)
- **Documentation**: 100% up-to-date
- **Training**: 100% operator coverage

## 📈 **Business SLOs**

### **Availability**
- **System uptime**: 99.9% (8.76 hours downtime/year)
- **Show uptime**: 99.99% (52 minutes downtime/year)
- **Planned maintenance**: ≤ 4 hours/month
- **Emergency maintenance**: ≤ 1 hour/incident

### **Performance**
- **Show quality**: 100% (no quality issues)
- **Operator satisfaction**: ≥ 95%
- **Venue compliance**: 100%
- **Safety compliance**: 100%

### **Cost**
- **Resource efficiency**: ≥ 90% (optimal resource usage)
- **Maintenance cost**: ≤ $100/month
- **Support cost**: ≤ $50/month
- **Total cost of ownership**: ≤ $200/month

## 🎯 **SLO Targets Summary**

| Category | Metric | Target | Guard | Critical |
|----------|--------|--------|-------|----------|
| **Performance** | Frame p95 | ≤ 10ms | ≤ 12ms | ≤ 15ms |
| **Performance** | Strobe Hz | ≤ 8Hz | ≤ 7.5Hz | ≤ 6Hz |
| **Performance** | A11y fades | 490±20ms | 490±10ms | 490±5ms |
| **Performance** | Error rate | ≤ 1% | ≤ 0.5% | ≤ 0.1% |
| **Operator** | Hotkey response | ≤ 100ms | ≤ 50ms | ≤ 25ms |
| **Operator** | Scene transition | ≤ 500ms | ≤ 300ms | ≤ 200ms |
| **Safety** | Motion watchdog | ≤ 500ms | ≤ 300ms | ≤ 100ms |
| **Safety** | Emergency stop | ≤ 50ms | ≤ 25ms | ≤ 10ms |
| **Show** | Show start | ≤ 5s | ≤ 3s | ≤ 2s |
| **Show** | Scene transition | ≤ 500ms | ≤ 300ms | ≤ 200ms |
| **Operational** | Deployment | ≤ 5min | ≤ 3min | ≤ 2min |
| **Operational** | Rollback | ≤ 2min | ≤ 1min | ≤ 30s |
| **Business** | Uptime | 99.9% | 99.95% | 99.99% |
| **Business** | Show uptime | 99.99% | 99.995% | 99.999% |

## 🚨 **Alerting Thresholds**

### **Critical Alerts**
- Frame p95 > 15ms
- Strobe > 8Hz
- A11y fade > 510ms
- Error rate > 1%
- Emergency stop > 50ms

### **Warning Alerts**
- Frame p95 > 12ms
- Strobe > 7.5Hz
- A11y fade > 500ms
- Error rate > 0.5%
- Hotkey response > 100ms

### **Info Alerts**
- Frame p95 > 10ms
- Strobe > 7Hz
- A11y fade > 490ms
- Error rate > 0.1%
- Scene transition > 500ms

## 📊 **SLO Monitoring**

### **Metrics Collection**
- **Frame time**: Every frame (60 FPS)
- **Strobe rate**: Every strobe event
- **A11y fades**: Every fade event
- **Error rate**: Every request
- **Response time**: Every operation

### **Dashboard Metrics**
- **Real-time**: Frame time, strobe rate, error rate
- **Historical**: Trends, patterns, anomalies
- **Alerts**: Critical, warning, info
- **Status**: System health, show status

### **Reporting**
- **Daily**: Performance summary
- **Weekly**: Trend analysis
- **Monthly**: SLO compliance report
- **Quarterly**: Business impact analysis

## 🎯 **SLO Compliance**

### **Measurement**
- **Continuous monitoring**: 24/7/365
- **Automated alerts**: Real-time
- **Manual checks**: Daily
- **Audit trails**: Complete

### **Reporting**
- **SLO compliance**: Monthly
- **Performance trends**: Weekly
- **Incident reports**: As needed
- **Business impact**: Quarterly

### **Improvement**
- **SLO review**: Quarterly
- **Target adjustment**: As needed
- **Process improvement**: Continuous
- **Technology updates**: As available

---

**🎭 Code Live v0.5 — Touring Rig SLOs**  
**Ready for Stage!** ✨