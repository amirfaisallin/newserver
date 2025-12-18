"""
Example client script showing how to validate licenses from user applications
"""
import requests
import uuid
import platform

# Server URL
SERVER_URL = 'http://localhost:5000'

def get_device_id():
    """Generate a unique device ID based on system information"""
    # In production, you might want to use MAC address or other hardware identifiers
    machine_id = platform.node()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, machine_id))

def validate_license(license_key, device_name=None):
    """
    Validate license and register/update device
    
    Args:
        license_key: The license key to validate
        device_name: Optional device name
    
    Returns:
        dict: Validation result with 'valid' boolean and other info
    """
    if device_name is None:
        device_name = f"{platform.system()} - {platform.machine()}"
    
    device_id = get_device_id()
    
    try:
        response = requests.post(
            f'{SERVER_URL}/api/user/validate',
            json={
                'license_key': license_key,
                'device_id': device_id,
                'device_name': device_name
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        return {
            'valid': False,
            'message': f'Connection error: {str(e)}'
        }

def check_license(license_key):
    """
    Quick check if license is valid (without updating device info)
    
    Args:
        license_key: The license key to check
    
    Returns:
        dict: Check result with 'valid' boolean
    """
    try:
        response = requests.post(
            f'{SERVER_URL}/api/user/check',
            json={'license_key': license_key},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        return {
            'valid': False,
            'message': f'Connection error: {str(e)}'
        }

# Example usage
if __name__ == '__main__':
    print("License Validation Example\n")
    
    # Example license key (replace with actual license key)
    license_key = input("Enter license key: ").strip()
    
    if not license_key:
        print("License key is required!")
        exit(1)
    
    # Validate license
    print("\nValidating license...")
    result = validate_license(license_key)
    
    if result.get('valid'):
        print("✅ License is VALID!")
        print(f"   Username: {result.get('username')}")
        print(f"   Amount: {result.get('amount')}")
        print(f"   Message: {result.get('message')}")
    else:
        print("❌ License is INVALID or BLOCKED")
        print(f"   Reason: {result.get('message', 'Unknown error')}")
    
    # Quick check example
    print("\n" + "="*50)
    print("Quick check (without device update)...")
    check_result = check_license(license_key)
    
    if check_result.get('valid'):
        print("✅ License is still valid")
    else:
        print("❌ License is invalid or blocked")

