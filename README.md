# License Management System

একটি প্রফেশনাল License Management System যেখানে আপনি লাইসেন্স তৈরি, ম্যানেজ এবং ট্র্যাক করতে পারবেন।

## Features

- ✅ **লাইসেন্স তৈরি**: Username, Amount এবং License Key দিয়ে নতুন লাইসেন্স তৈরি করুন
- ✅ **লাইসেন্স তালিকা**: সব লাইসেন্স দেখুন এবং সার্চ করুন
- ✅ **Block/Unblock**: লাইসেন্স ব্লক করলে ইউজারের অ্যাক্সেস বন্ধ হয়ে যাবে, আনব্লক করলে আবার কাজ করবে
- ✅ **Active Devices**: প্রতিটি লাইসেন্সের জন্য কতগুলো ডিভাইস অ্যাক্টিভ আছে তা দেখুন
- ✅ **Delete License**: লাইসেন্স ডিলিট করলে ইউজারের অ্যাক্সেস বন্ধ হয়ে যাবে
- ✅ **User API**: ক্লায়েন্ট অ্যাপ্লিকেশন থেকে লাইসেন্স ভ্যালিডেট করার API

## Installation

1. Python 3.7+ ইনস্টল করুন

2. Dependencies ইনস্টল করুন:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

সার্ভার `http://localhost:5000` এ চালু হবে।

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

## API Endpoints

### Admin Endpoints (Authentication Required)

- `POST /api/license/generate` - নতুন লাইসেন্স কী জেনারেট করুন
- `POST /api/license/create` - নতুন লাইসেন্স তৈরি করুন
- `GET /api/license/list?search=...` - লাইসেন্স তালিকা পান
- `POST /api/license/<id>/block` - লাইসেন্স ব্লক করুন
- `POST /api/license/<id>/unblock` - লাইসেন্স আনব্লক করুন
- `DELETE /api/license/<id>/delete` - লাইসেন্স ডিলিট করুন
- `GET /api/license/<id>/devices` - লাইসেন্সের অ্যাক্টিভ ডিভাইস দেখুন

### User Endpoints (For Client Applications)

- `POST /api/user/validate` - লাইসেন্স ভ্যালিডেট করুন এবং ডিভাইস রেজিস্টার করুন
- `POST /api/user/check` - লাইসেন্স চেক করুন (ডিভাইস আপডেট ছাড়া)

### User API Example

```python
import requests

# Validate license and register device
response = requests.post('http://localhost:5000/api/user/validate', json={
    'license_key': 'YOUR_LICENSE_KEY',
    'device_id': 'unique-device-id',
    'device_name': 'My Device'
})

data = response.json()
if data.get('valid'):
    print('License is valid!')
else:
    print('License is invalid or blocked')
```

## Database

SQLite database (`license_management.db`) স্বয়ংক্রিয়ভাবে তৈরি হবে। এতে তিনটি টেবিল আছে:

1. **admins** - Admin ইউজার তথ্য
2. **licenses** - লাইসেন্স তথ্য
3. **active_devices** - অ্যাক্টিভ ডিভাইস তথ্য

## Security Notes

- Production environment এ default admin password পরিবর্তন করুন
- Secret key পরিবর্তন করুন
- HTTPS ব্যবহার করুন
- Database backup নিন

## License

MIT License

