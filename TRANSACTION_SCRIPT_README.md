# Transaction Panel Script with License Management

## 📋 Overview

এই script আপনার transaction panel এর সাথে license management system connect করেছে। Script শুধুমাত্র license active থাকলে কাজ করবে, blocked থাকলে disable হয়ে যাবে।

## 🔑 License Information

- **License Key**: `YQ8EJR4LTBSM`
- **Server URL**: `http://localhost:5000`
- **Current Status**: Active ✅

## 🚀 Installation & Usage

### 1. Script ব্যবহার করুন

`transaction_panel_with_license.js` ফাইলটি আপনার browser console এ paste করুন অথবা userscript হিসেবে ব্যবহার করুন।

### 2. License Check

- Script load হওয়ার সময় automatically license validate করবে
- প্রতি 30 সেকেন্ডে license check করবে
- License blocked হলে script automatically disable হবে
- License active হলে script enable হবে

## 🎯 Features

### License Management
- ✅ Automatic license validation on script load
- ✅ Periodic license checking (every 30 seconds)
- ✅ Real-time license status notification
- ✅ Script auto-disable if license blocked
- ✅ Script auto-enable if license active

### Transaction Panel (Original Features)
- ✅ Add demo transactions
- ✅ Pending transactions shown at top
- ✅ Transaction list with header
- ✅ Keyboard shortcut: `Ctrl+S` to open panel
- ✅ Triple click to open panel

## 📱 How It Works

1. **Script Start**: Script load হওয়ার সময় license validate করবে
2. **License Valid**: Script কাজ করবে, notification দেখাবে "License Active"
3. **License Blocked**: Script disable হবে, notification দেখাবে "License Blocked"
4. **Periodic Check**: প্রতি 30 সেকেন্ডে license check করবে
5. **Auto Enable/Disable**: License status change হলে automatically enable/disable হবে

## 🔧 Configuration

Script এর শুরুতে এই variables পরিবর্তন করতে পারেন:

```javascript
let licenseKey = "YQ8EJR4LTBSM";  // আপনার license key
let serverUrl = "http://localhost:5000";  // Server URL
```

## 📊 License Status Notifications

Script screen এর top-right corner এ notification দেখাবে:

- **Green**: License Active - Script Enabled ✅
- **Red**: License Blocked/Invalid - Script Disabled ❌
- **Yellow**: License Check Failed - Script Disabled ⚠️

## 🛠️ Admin Panel থেকে License Manage করুন

1. `http://localhost:5000` এ যান
2. Admin login করুন (admin / admin123)
3. License List এ `YQ8EJR4LTBSM` খুঁজুন
4. Block/Unblock করুন
5. Script automatically update হবে

## ⚠️ Important Notes

- License blocked করলে script immediately disable হবে
- License unblock করলে script automatically enable হবে
- Server offline থাকলে script disable হবে
- Device ID automatically generate হবে এবং localStorage এ save হবে

## 🐛 Troubleshooting

### Script কাজ করছে না?
1. Browser console check করুন (F12)
2. License key সঠিক আছে কিনা check করুন
3. Server running আছে কিনা check করুন (`http://localhost:5000`)
4. License blocked আছে কিনা admin panel এ check করুন

### License Check Failed?
- Server URL সঠিক আছে কিনা check করুন
- Server running আছে কিনা verify করুন
- Network connection check করুন

## 📝 Example Usage

1. Script load করুন
2. License validate হবে automatically
3. Green notification দেখবেন "License Active"
4. `Ctrl+S` press করুন panel open করতে
5. Transaction add করুন
6. Admin panel থেকে license block করুন
7. Script automatically disable হবে
8. Red notification দেখবেন "License Blocked"

---

**Made with ❤️ for License Management System**

